from datetime import datetime, timedelta
from os import PathLike

from aa_remove_data.generated import EPICSEvent_pb2


class PBUtils:
    def __init__(self, filepath: PathLike | None = None):
        """Initialise a PBUtils object. If filepath is set, read the protobuf
        file at this location to gether its header, samples and type.

        Args:
            filepath (Optional[PathLike], optional): Path to pb file to be
            read. Defaults to None.
        """
        self.header = EPICSEvent_pb2.PayloadInfo()  # type: ignore
        self.samples = []
        self.pv_type = ""
        if filepath:
            self.read_pb(filepath)

    def _remove_aa_escape_chars(self, data: bytes) -> bytes:
        """Replace Archiver Appliance escape characters with alternatives, to
        avoid conflitcs when serialising.

        Args:
            data (bytes): A serialised protobuf sample.

        Returns:
            bytes: The serialised sample with escape characters replaced.
        """
        data = data.replace(b"\x1b", b"\x1b\x01")  # Escape escape character
        data = data.replace(b"\x0a", b"\x1b\x02")  # Escape newline
        data = data.replace(b"\x0d", b"\x1b\x03")  # Escape carriage return
        return data

    def _add_aa_escape_chars(self, data: bytes) -> bytes:
        """Add in Archiver Appliance escape characters which have previosuly
        been removed. Should exactly mirror _remove_aa_escape_chars().

        Args:
            data (bytes): A serialised protobuf message with escape characters
            replaced.

        Returns:
            bytes: The serialised protobuf message containing escape
            characters.
        """
        data = data.replace(b"\x1b\x03", b"\x0d")  # Unescape carriage return
        data = data.replace(b"\x1b\x02", b"\x0a")  # Unescape newline
        data = data.replace(b"\x1b\x01", b"\x1b")  # Unescape escape character
        return data

    def _get_pv_class_name(self) -> str:
        """Convert the name of a pv type to CamelCase to correspond to that
        sample type's class name.

        Args:
            pv_type (str): Name of pv type.

        Returns:
            str: Name of pv class, e.g VectorDouble.
        """
        # Split the enum name by underscores and capitalize each part
        parts = self.pv_type.split("_")
        return "".join(part.capitalize() for part in parts)

    def convert_to_datetime(self, year: int, seconds: int) -> datetime:
        """Get the date and time from a year and the number of seconds passed.
        Args:
            year (int): A year
            seconds (int): The number of seconds into that year that have
            passed.
        Returns:
            datetime: A datetime object of the correct date and time.
        """
        return datetime(year, 1, 1) + timedelta(seconds=seconds)

    def get_datastr(self, sample: type, year: int) -> str:
        """Get a string contaiing information about a sample.
        Args:
            sample (type): A sample from a pb file.
            year (int): The year the sample was collected.
        Returns:
            str: A string containing the sample information.
        """
        date = self.convert_to_datetime(year, sample.secondsintoyear)
        return (
            f"{date}    {sample.secondsintoyear:8d}    {sample.nano:9d}"
            f"    {sample.val}\n"
        )

    def get_pv_type(self) -> str:
        """Get the name of a pb file's pv type using information in its
        header.

        Returns:
            str: Name of pv type, e.g VECTOR_DOUBLE.
        """
        type_descriptor = self.header.DESCRIPTOR.fields_by_name["type"]
        enum_descriptor = type_descriptor.enum_type
        return enum_descriptor.values_by_number[self.header.type].name

    def get_proto_class(self) -> type:
        """Get the EPICSEvent_pb2 class corresponding to the pv in a pb file.
        Instances of this class can interpret pb messages of a matching type.

        Returns:
            type: EPICSEvent_pb2 protocol buffer class.
        """
        # Ensure self.pv_type is set first.
        if not self.pv_type:
            self.pv_type = self.get_pv_type()
        pv_type_camel = self._get_pv_class_name()
        proto_class = getattr(EPICSEvent_pb2, pv_type_camel)
        return proto_class

    def write_to_txt(self, filepath: PathLike):
        """Write a text file from a PBUtils object.

        Args:
            filepath (PathLike): Filepath for file to be written.
        """
        pvname = self.header.pvname
        year = self.header.year
        pv_type = self.get_pv_type()
        data_strs = [self.get_datastr(sample, year) for sample in self.samples]
        with open(filepath, "w") as f:
            # Write header
            f.write(f"{pvname}, {pv_type}, {year}\n")
            # Write column titles
            f.write(f"DATE{' ' * 19}SECONDS{' ' * 5}NANO{' ' * 9}VAL\n")
            # Write body
            f.writelines(data_strs)

    def read_pb(self, filepath: PathLike):
        """Read a pb file that is structured in the Archiver Appliance format.
        Gathers the header and samples from this file and assigns them to
        self.header self.samples.

        Args:
            filepath (PathLike): Path to pb file.
        """
        with open(filepath, "rb") as f:
            first_line = self._add_aa_escape_chars(f.readline().strip())
            self.header.ParseFromString(first_line)
            lines = f.readlines()
        proto_class = self.get_proto_class()
        self.samples = [proto_class() for n in range(len(lines))]
        for i, sample in enumerate(self.samples):
            line = self._add_aa_escape_chars(lines[i].strip())
            sample.ParseFromString(line)

    def write_pb(self, filepath: PathLike):
        """Write a pb file that is structured in the Archiver Appliance format.
        Must have a valid header and list of samples to write.

        Args:
            filepath (PathLike): Path to file to be written.
        """
        header_b = self._remove_aa_escape_chars(self.header.SerializeToString()
                                                ) + b"\n"
        samples_b = [
            self._remove_aa_escape_chars(sample.SerializeToString()) + b"\n"
            for sample in self.samples
        ]
        with open(filepath, "wb") as f:
            f.writelines([header_b] + samples_b)
