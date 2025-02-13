import argparse
from collections.abc import Callable
from datetime import datetime, timedelta
from itertools import islice
from os import PathLike
from pathlib import Path

from aa_remove_data.generated import EPICSEvent_pb2

DEFAULT_CHUNK_SIZE = 10000000


class PBUtils:
    def __init__(self, filepath: PathLike):
        """Initialise a PBUtils object. If filepath is set, read the protobuf
        file at this location to gether its header, samples and type.

        Args:
            filepath (Optional[PathLike], optional): Path to PB file to be
            read. Defaults to None.
            chunk_size (Optional[int], optional): Number of lines to read/write
            at one time.
        """
        self.filepath = filepath
        self.header = EPICSEvent_pb2.PayloadInfo()  # type: ignore
        self.read_header()
        self.pv_type = self.get_pv_type()
        self._write_started = []

    def _replace_newline_chars(self, data: bytes) -> bytes:
        """Replace newline characters with alternative to conform with the
        archiver PB format. See https://epicsarchiver.readthedocs.io/en/latest/developer/pb_pbraw.html.
        Args:
            data (bytes): A serialised protobuf sample.

        Returns:
            bytes: The serialised sample with escape characters replaced.
        """
        data = data.replace(b"\x1b", b"\x1b\x01")  # Escape escape character
        data = data.replace(b"\x0a", b"\x1b\x02")  # Escape newline
        data = data.replace(b"\x0d", b"\x1b\x03")  # Escape carriage return
        return data

    def _restore_newline_chars(self, data: bytes) -> bytes:
        """Restore newline characters that have been replaced by the archiver
        PB format. See https://epicsarchiver.readthedocs.io/en/latest/developer/pb_pbraw.html.
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

    def _get_proto_class_name(self) -> str:
        """Convert the name of a pv type to match the proto class name. This
        involves coverting to CamelCase and replacing 'WAVEFORM' with 'Vector'.
        The full mapping is described in
        epicsarchiverap/src/main/edu/stanford/slac/archiverappliance/PB/data/DBR2PBTypeMapping.java

        Returns:
            str: Name of proto class, e.g VectorDouble.
        """
        # Split the enum name by underscores and capitalize each part
        parts = self.pv_type.split("_")
        parts = [x.replace("WAVEFORM", "Vector") for x in parts]
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

    def format_datastr(self, sample: type) -> str:
        """Get a string containing information about a sample.
        Args:
            sample (type): A sample from a PB file.
        Returns:
            str: A string containing the sample information.
        """
        date = self.convert_to_datetime(self.header.year, sample.secondsintoyear)
        return (
            f"{date}    {sample.secondsintoyear:8d}    {sample.nano:9d}"
            f"    {sample.val}\n"
        )

    def get_pv_type(self) -> str:
        """Get the name of a PB file's pv type using information in its
        header.

        Returns:
            str: Name of pv type, e.g VECTOR_DOUBLE.
        """
        type_descriptor = self.header.DESCRIPTOR.fields_by_name["type"]
        enum_descriptor = type_descriptor.enum_type
        return enum_descriptor.values_by_number[self.header.type].name

    def get_proto_class(self) -> Callable:
        """Get the EPICSEvent_pb2 class corresponding to the pv in a PB file.
        Instances of this class can interpret PB messages of a matching type.

        Returns:
            Callable: EPICSEvent_pb2 protocol buffer class.
        """
        proto_class_name = self._get_proto_class_name()
        proto_class = getattr(EPICSEvent_pb2, proto_class_name)
        return proto_class

    def generate_test_value(self, val: int) -> str | bytes | int:
        """Generate an appropriate value for a sample based on it's pv type.

        Args:
            val (int): The original value.

        Returns:
            str | bytes | int: The value converted to an oppropriate type.
        """
        if self.pv_type.endswith("STRING"):
            return str(val)
        elif self.pv_type.endswith("BYTE") or self.pv_type.endswith("BYTES"):
            return val.to_bytes(2, byteorder="big")
        else:
            return val

    def generate_test_samples(
        self,
        pv_type: int = 6,
        samples: int = 100,
        year: int = 2024,
        start: int = 0,
        seconds_gap: int = 1,
        nano_gap: int = 0,
    ):
        """Generate test Archiver Appliance samples.

        Args:
            pv_type (int, optional): PV type enum. Defaults to 6 (SCALAR_DOUBLE).
            samples (int, optional): Number of samples to be generated.
            Defaults to 100.
            year (int, optional): Year associated with samples. Defaults to 2024.
            start: Initial number of seconds for first sample.
            seconds_gap (int, optional): Gap in seconds between samples.
            Defaults to 1.
            nano_gap (int, optional): Gap in nanoseconds between samples.
            Defaults to 0.
        """
        self.header.pvname = "generated_test_data"
        self.header.year = year
        self.header.type = pv_type

        self.pv_type = self.get_pv_type()
        sample_class = self.get_proto_class()
        self.samples = [sample_class() for _ in range(samples)]
        time_gap = seconds_gap * 10**9 + nano_gap
        time = start * 10**9
        for i, sample in enumerate(self.samples):
            sample.secondsintoyear = time // 10**9
            sample.nano = time % 10**9
            if self.pv_type.startswith("WAVEFORM"):
                sample.val.extend(
                    [self.generate_test_value(i * 5 + j) for j in range(5)]
                )
            else:
                sample.val = self.generate_test_value(i)
            time += time_gap

    def read_header(self):
        with open(self.filepath, "rb") as f:
            header_bytes = self._restore_newline_chars(f.readline().rstrip(b"\n"))
        self.header.ParseFromString(header_bytes)

    def get_samples(self):
        """Read a PB file that is structured in the Archiver Appliance format.
        Gathers the header and samples from this file and assigns them to
        self.header self.samples.

        Args:
            filepath (PathLike): Path to PB file.
        """
        proto_class = self.get_proto_class()
        with open(self.filepath, "rb") as f:
            for line in islice(f, 1, None):
                sample_bytes = self._restore_newline_chars(line.rstrip(b"\n"))
                sample = proto_class()
                sample.ParseFromString(sample_bytes)
                yield sample

    def serialize(self, sample):
        return self._replace_newline_chars(sample.SerializeToString()) + b"\n"


def pb_2_txt():
    """Convert a .pb file to a human-readable .txt file."""
    parser = argparse.ArgumentParser()
    parser.add_argument("pb_filename", type=str)
    parser.add_argument("txt_filename", type=str)
    args = parser.parse_args()
    pb_file = Path(args.pb_filename)
    txt_file = Path(args.txt_filename)
    # Validation
    if pb_file.suffix != ".pb":
        raise ValueError(f"Invalid file extension: '{pb_file.suffix}'. Expected '.pb'.")

    pb = PBUtils(pb_file)
    with open(txt_file, "w") as f:
        # Write header
        f.write(f"{pb.header.pvname}, {pb.pv_type}, {pb.header.year}\n")
        # Write column titles
        f.write(f"DATE{' ' * 19}SECONDS{' ' * 5}NANO{' ' * 9}VAL\n")
        for sample in pb.get_samples():
            f.write(pb.format_datastr(sample))
    print("Write completed!")


def print_header():
    """Print the header and first few lines of a .pb file."""
    parser = argparse.ArgumentParser()
    parser.add_argument("pb_filename", type=str)
    parser.add_argument("--lines", type=int, default=0)
    parser.add_argument("--start", type=int, default=0)
    args = parser.parse_args()
    pb_file = Path(args.pb_filename)
    lines = args.lines
    # Validation
    if pb_file.suffix != ".pb":
        raise ValueError(f"Invalid file extension: '{pb_file.suffix}'. Expected '.pb'.")

    pb = PBUtils(pb_file)
    print(f"Name: {pb.header.pvname}, Type: {pb.pv_type}, Year: {pb.header.year}")
    if lines:
        print(f"DATE{' ' * 19}SECONDS{' ' * 5}NANO{' ' * 9}VAL")
        for sample in islice(pb.get_samples(), args.start, args.start + lines):
            print(pb.format_datastr(sample).strip())
