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
        self.sample_type = ""
        if filepath:
            self.read_pb(filepath)

    def _escape_data(self, data: bytes) -> bytes:
        """Replace escape characters with alternatives, to avoid conflitcs.
        Should exactly mirror _unescape_data().

        Args:
            data (bytes): A serialised protobuf sample.

        Returns:
            bytes: The serialised sample with escape characters replaced.
        """
        data = data.replace(b"\x1b", b"\x1b\x01")  # Escape escape character
        data = data.replace(b"\x0a", b"\x1b\x02")  # Escape newline
        data = data.replace(b"\x0d", b"\x1b\x03")  # Escape carriage return
        return data

    def _unescape_data(self, data: bytes) -> bytes:
        """Replace escape character alternatives with the escape characters.
        Should exactly mirror _escape_data().

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

    def _convert_to_class_name(self, sample_type: str) -> str:
        """Convert the name of a sample type to CamelCase to correspond to
        that sample type's class name.

        Args:
            sample_type (str): Name of sample type.

        Returns:
            str: Name of sample class, e.g VectorDouble.
        """
        # Split the enum name by underscores and capitalize each part
        parts = sample_type.split("_")
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

    def get_sample_type(self) -> str:
        """Get the name of a pb file's sample type using information in its
        header.

        Returns:
            str: Name of sample type, e.g VECTOR_DOUBLE.
        """
        type_descriptor = self.header.DESCRIPTOR.fields_by_name["type"]
        enum_descriptor = type_descriptor.enum_type
        return enum_descriptor.values_by_number[self.header.type].name

    def get_sample_class(self) -> type:
        """Get the EPICSEvent_pb2 class corresponding to samples in a pb file.
        Instances of this class can interpret pb samples of a matching type.

        Returns:
            type: pb sample class.
        """
        # Ensure self.sample_type is set first.
        if not self.sample_type:
            self.sample_type = self.get_sample_type()
        sample_type_camel = self._convert_to_class_name(self.sample_type)
        sample_class = getattr(EPICSEvent_pb2, sample_type_camel)
        return sample_class

    def generate_test_samples(self, sample_type=6, lines=100, year=2024,
                              seconds_gap=1, nano_gap=0):
        self.header.pvname = 'test'
        self.header.year = year
        self.header.type = sample_type
        sample_class = self.get_sample_class()
        self.samples = [sample_class() for n in range(lines)]
        time_gap = seconds_gap * 10**9 + nano_gap
        time = 0
        for i, sample in enumerate(self.samples):
            sample.secondsintoyear = time // 10**9
            sample.nano = time % 10 ** 9
            sample.val = i
            time += time_gap

    def write_to_txt(self, filepath: PathLike):
        """Write a text file from a PBUtils object.

        Args:
            filepath (PathLike): Filepath for file to be written.
        """
        pvname = self.header.pvname
        year = self.header.year
        sample_type = self.get_sample_type()
        data_strs = [self.get_datastr(sample, year) for sample in self.samples]
        with open(filepath, "w") as f:
            f.write(f"{pvname}, {sample_type}, {year}\n")
            f.write(f"DATE{' ' * 19}SECONDS{' ' * 5}NANO{' ' * 9}VAL\n")
            f.writelines(data_strs)

    def read_pb(self, filepath: PathLike):
        """Read a pb file that is structured in the Archiver Appliance format.
        Gathers the header and samples from this file and assigns them to
        self.header self.samples.

        Args:
            filepath (PathLike): Path to pb file.
        """
        with open(filepath, "rb") as f:
            first_line = self._unescape_data(f.readline().strip())
            self.header.ParseFromString(first_line)
            sample_class = self.get_sample_class()
            lines = f.readlines()
            self.samples = [sample_class() for n in range(len(lines))]
            for i, sample in enumerate(self.samples):
                line = self._unescape_data(lines[i].strip())
                sample.ParseFromString(line)

    def write_pb(self, filepath: PathLike):
        """Write a pb file that is structured in the Archiver Appliance format.
        Must have a valid header and list of samples to write.

        Args:
            filepath (PathLike): Path to file to be written.
        """
        header_b = self._escape_data(self.header.SerializeToString()) + b"\n"
        samples_b = [
            self._escape_data(sample.SerializeToString()) + b"\n"
            for sample in self.samples
        ]
        with open(filepath, "wb") as f:
            f.writelines([header_b] + samples_b)
