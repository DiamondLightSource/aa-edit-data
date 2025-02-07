import argparse
import subprocess
from collections.abc import Callable
from datetime import datetime, timedelta
from itertools import islice
from os import PathLike
from pathlib import Path
from typing import Any

from aa_remove_data.generated import EPICSEvent_pb2


class ArchiverData:
    def __init__(self, filepath: PathLike):
        """Initialise a ArchiverData object. If filepath is set, read the protobuf
        file at this location to gather its header, samples and type.

        Args:
            filepath (Optional[PathLike], optional): Path to PB file to be
            read. Defaults to None.
            chunk_size (Optional[int], optional): Number of lines to read/write
            at one time.
        """
        self.filepath = Path(filepath)
        with open(filepath, "rb") as f:
            self.header = self.deserialize(f.readline(), EPICSEvent_pb2.PayloadInfo)  # type: ignore
        self.pv_type = self.get_pv_type()

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
                yield self.deserialize(line, proto_class)

    def get_samples_bytes(self):
        """Read a PB file that is structured in the Archiver Appliance format.
        Gathers the header and samples from this file and assigns them to
        self.header self.samples.

        Args:
            filepath (PathLike): Path to PB file.
        """
        with open(self.filepath, "rb") as f:
            yield from islice(f, 1, None)

    def process_and_write(
        self,
        filepath: PathLike,
        write_txt: bool,
        process_func: Callable,
        process_args: list | None = None,
        process_kwargs: dict | None = None,
        deserialize: bool = True,
    ):
        process_args = process_args or []
        process_kwargs = process_kwargs or {}
        filepath = Path(filepath)
        txt_filepath = filepath.with_suffix(".txt")
        mv_to = ""
        if filepath == self.filepath:
            mv_to = filepath
            filepath = self.get_temp_filename(filepath)
        with open(filepath, "wb") as f:
            f.write(self.serialize(self.header))
            if deserialize:
                f.writelines(
                    self.serialize(sample)
                    for sample in process_func(
                        self.get_samples(),
                        *process_args,
                        **process_kwargs,
                    )
                )
            else:
                f.writelines(
                    sample
                    for sample in process_func(
                        self.get_samples_bytes(),
                        *process_args,
                        **process_kwargs,
                    )
                )
        if mv_to:
            subprocess.run(["mv", filepath, mv_to], check=True)
        if write_txt:
            with open(txt_filepath, "w") as f:
                # Write header
                f.write(f"{self.header.pvname}, {self.pv_type}, {self.header.year}\n")
                # Write column titles
                f.write(f"DATE{' ' * 19}SECONDS{' ' * 5}NANO{' ' * 9}VAL\n")
                f.writelines(
                    self.format_datastr(sample, self.header.year)
                    for sample in process_func(
                        self.get_samples(),
                        *process_args,
                        **process_kwargs,
                    )
                )

    def write_pb(self, filepath: PathLike):
        filepath = Path(filepath)
        with open(filepath, "wb") as f:
            f.write(self.serialize(self.header))
            f.writelines(sample for sample in self.get_samples_bytes())

    def write_txt(self, filepath: PathLike):
        filepath = Path(filepath)
        txt_filepath = filepath.with_suffix(".txt")
        with open(txt_filepath, "w") as f:
            # Write header
            f.write(f"{self.header.pvname}, {self.pv_type}, {self.header.year}\n")
            # Write column titles
            f.write(f"DATE{' ' * 19}SECONDS{' ' * 5}NANO{' ' * 9}VAL\n")
            f.writelines(
                self.format_datastr(sample, self.header.year)
                for sample in self.get_samples()
            )

    @staticmethod
    def serialize(sample):
        return ArchiverData._replace_newline_chars(sample.SerializeToString()) + b"\n"

    @staticmethod
    def deserialize(line, proto_class):
        sample_bytes = ArchiverData._restore_newline_chars(line.rstrip(b"\n"))
        sample = proto_class()
        sample.ParseFromString(sample_bytes)
        return sample

    @staticmethod
    def _replace_newline_chars(data: bytes) -> bytes:
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

    @staticmethod
    def _restore_newline_chars(data: bytes) -> bytes:
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

    @staticmethod
    def convert_to_datetime(year: int, seconds: int) -> datetime:
        """Get the date and time from a year and the number of seconds passed.
        Args:
            year (int): A year
            seconds (int): The number of seconds into that year that have
            passed.
        Returns:
            datetime: A datetime object of the correct date and time.
        """
        ts = datetime(year, 1, 1) + timedelta(seconds=seconds)
        if ts.year != year:
            raise ValueError
        return ts

    @staticmethod
    def format_datastr(sample: Any, year: int) -> str:
        """Get a string containing information about a sample.
        Args:
            sample (type): A sample from a PB file.
        Returns:
            str: A string containing the sample information.
        """
        date = ArchiverData.convert_to_datetime(year, sample.secondsintoyear)
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

    @staticmethod
    def get_temp_filename(filename):
        filename = Path(filename)
        filename = filename.with_stem(f"{filename.stem}_tmp")
        if filename.exists():
            filename = ArchiverData.get_temp_filename(filename)
        return filename


def pb_2_txt():
    """Convert a .pb file to a human-readable .txt file."""
    parser = argparse.ArgumentParser()
    parser.add_argument("pb_filename", type=str)
    parser.add_argument("txt_filename", nargs="?", type=str, default="")
    args = parser.parse_args()
    pb_file = Path(args.pb_filename)
    txt_file = (
        Path(args.txt_filename) if args.txt_filename else pb_file.with_suffix(".txt")
    )
    print(f"Writing {txt_file}")
    # Validation
    if pb_file.suffix != ".pb":
        raise ValueError(f"Invalid file extension: '{pb_file.suffix}'. Expected '.pb'.")

    ad = ArchiverData(pb_file)
    ad.write_txt(txt_file)
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

    ad = ArchiverData(pb_file)
    print(f"Name: {ad.header.pvname}, Type: {ad.pv_type}, Year: {ad.header.year}")
    if lines:
        print(f"DATE{' ' * 19}SECONDS{' ' * 5}NANO{' ' * 9}VAL")
        for sample in islice(ad.get_samples(), args.start, args.start + lines):
            print(ad.format_datastr(sample, ad.header.year).strip())
