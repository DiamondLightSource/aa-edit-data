import argparse
import subprocess
from collections.abc import Iterator
from datetime import datetime
from itertools import islice
from pathlib import Path
from typing import Any

from aa_remove_data.pb_utils import PBUtils


def get_nano_diff(sample1: Any, sample2: Any) -> int:
    """Get the difference in nano seconds between two samples.

    Args:
        sample1 (Any): An Archiver Appliance sample.
        sample2 (Any): Another Archiver Appliance sample.

    Returns:
        int: Difference in nanoseconds.
    """
    diff = (sample2.secondsintoyear - sample1.secondsintoyear) * 10**9 + (
        sample2.nano - sample1.nano
    )
    if not diff > 0:
        raise ValueError(
            f"diff ({diff}) is non-positive - ensure sample2 comes after sample1."
        )
    return diff


def get_seconds_diff(sample1: Any, sample2: Any) -> int:
    """Get the difference in whole seconds between two samples.

    Args:
        sample1 (Any): An Archiver Appliance sample.
        sample2 (Any): Another Archiver Appliance sample.

    Returns:
        int: Difference in seconds
    """
    diff = sample2.secondsintoyear - sample1.secondsintoyear
    if not diff >= 0:
        raise ValueError(
            f"diff ({diff}) is negative - ensure sample2 comes after sample1."
        )
    return diff


def filter_samples_to_period(pb: Any, period: float) -> Iterator:
    """Reduce the frequency of a list of samples. Specify the desired minimum period.

    Args:
        samples (list): List of samples.
        period (float): Desired minimum period between adjacent samples.
        initial_sample (Any, optional): An initial sample to find an initial diff.

    Returns:
        list: Reduced list of samples
    """
    seconds_delta = period
    nano_delta = (seconds_delta * 10**9) // 1
    if not nano_delta >= 1:
        raise ValueError(f"Period ({period}) must be at least 1 nanosecond.")

    if seconds_delta >= 5:  # Save time for long periods by ignoring nano
        delta = seconds_delta
        get_diff = get_seconds_diff
    else:
        delta = nano_delta  # For short periods still count nano
        get_diff = get_nano_diff

    first_sample = next(pb.get_samples())
    yield first_sample
    last_yielded_sample = first_sample
    for sample in islice(pb.get_samples(), 1, None):
        if get_diff(last_yielded_sample, sample) >= delta:
            last_yielded_sample = sample
            yield sample


def apply_min_period(pb, period):
    return (sample for sample in filter_samples_to_period(pb, period))


def is_before(sample, seconds, nano):
    if sample.secondsintoyear < seconds or (
        sample.secondsintoyear == seconds and sample.nano < nano
    ):
        return True
    else:
        return False


def is_after(sample, seconds, nano):
    if sample.secondsintoyear > seconds or (
        sample.secondsintoyear == seconds and sample.nano > nano
    ):
        return True
    else:
        return False


def remove_before_ts(pb: Any, seconds: int, nano: int = 0) -> Iterator:
    """Remove all samples before a certain timestamp.

    Args:
        samples (list): List of samples.
        seconds (int): Seconds portion of timestamp.
        nano (int, optional): Nanoseconds portion of timestamp. Defaults to 0.

    Returns:
        list: Reduced list of samples.
    """
    return (
        sample for sample in pb.get_samples() if not is_before(sample, seconds, nano)
    )


def remove_after_ts(pb: Any, seconds: int, nano: int = 0) -> Iterator:
    """Remove all samples after a certain timestamp.

    Args:
        samples (list): List of samples.
        seconds (int): Seconds portion of timestamp.
        nano (int, optional): Nanoseconds portion of timestamp. Defaults to 0.

    Returns:
        list: Reduced list of samples.
    """
    return (
        sample for sample in pb.get_samples() if not is_after(sample, seconds, nano)
    )


def reduce_by_factor(pb, n) -> Iterator:
    """Reduce the size of a list of samples, keeping every nth sample and
    removing the rest.

    Args:
        samples (list): List of samples
        n (int): Every nth sample will be kept.
        initial (int, optional): End point of processing from a previous chunk.

    Returns:
        list: Reduced list of samples.
    """
    return (sample for i, sample in enumerate(pb.get_samples()) if i % n == 0)


def add_generic_args(parser):
    parser.add_argument(
        "filename", type=str, help="path/to/file.pb of PB file being processed"
    )
    parser.add_argument(
        "--new-filename",
        type=str,
        default=None,
        help="path/to/file.pb of new file to write to "
        + "(default: writes over original file)",
    )
    parser.add_argument(
        "--backup-filename",
        type=str,
        default=None,
        help="path/to/file.pb of a backup file, "
        + "(default: {original_filename}_backup.pb)",
    )
    parser.add_argument(
        "-t",
        "--write-txt",
        action="store_true",
        help="write result to a .txt file (default: False)",
    )
    return parser


def validate_pb_file(filepath, should_exist=False):
    filepath = Path(filepath)
    if filepath.suffix != ".pb":
        raise ValueError(
            f"Invalid file extension for {filepath}: '{filepath.suffix}'. "
            + "Expected '.pb'."
        )
    if should_exist:
        if not filepath.is_file():
            raise FileNotFoundError(f"{filepath} is not a filepath.")


def process_generic_args(args):
    validate_pb_file(args.filename, should_exist=True)

    if args.backup_filename is None and (args.new_filename in (None, args.filename)):
        args.backup_filename = args.filename.replace(".pb", "_backup.pb")
        args.new_filename = args.filename
    elif args.new_filename is None:
        args.new_filename = args.filename
    if args.backup_filename in (args.filename, args.new_filename):
        raise ValueError(
            f"Backup filename {args.backup_filename} cannot be the same as filename or"
            + " new-filename"
        )

    validate_pb_file(args.new_filename)
    if args.backup_filename is not None:
        validate_pb_file(args.backup_filename)
    return args


def process_timestamp(pb, timestamp):
    timestamp = [int(value) for value in timestamp.split(",")]
    if not len(timestamp) <= 6:
        raise ValueError(
            "Give timestamp in the form 'month,day,hour,minute,second,nanosecond'. "
            + "Month is required. All must be integers."
        )
    year = pb.header.year
    nano = timestamp.pop(5) if len(timestamp) == 6 else 0
    diff = datetime(*([year] + timestamp)) - datetime(year, 1, 1)
    seconds = int(diff.total_seconds())
    return seconds, nano


def aa_reduce_to_period():
    """Reduce the frequency of data in a PB file by setting a minimum period between
    data points."""
    parser = argparse.ArgumentParser()
    parser = add_generic_args(parser)
    parser.add_argument(
        "period", type=float, help="Minimum period between each data point"
    )
    args = parser.parse_args()
    args = process_generic_args(args)

    filename = Path(args.filename)
    new_pb = Path(args.new_filename)
    if args.backup_filename is not None:
        subprocess.run(["cp", filename, Path(args.backup_filename)], check=True)

    txt_filepath = new_pb.with_suffix(".txt")
    pb = PBUtils(filename)
    with open(new_pb, "wb") as f:
        f.write(pb.serialize(pb.header))
        f.writelines(
            pb.serialize(sample) for sample in apply_min_period(pb, args.period)
        )
    if args.write_txt:
        txt_filepath = new_pb.with_suffix(".txt")
        with open(txt_filepath, "w") as f:
            # Write header
            f.write(f"{pb.header.pvname}, {pb.pv_type}, {pb.header.year}\n")
            # Write column titles
            f.write(f"DATE{' ' * 19}SECONDS{' ' * 5}NANO{' ' * 9}VAL\n")
            f.writelines(
                pb.format_datastr(sample)
                for sample in apply_min_period(pb, args.period)
            )


def aa_reduce_by_factor():
    """Reduce the number of data points in a PB file by a certain factor by removing all
    but every nth."""
    parser = argparse.ArgumentParser()
    parser = add_generic_args(parser)
    parser.add_argument("factor", type=int, help="factor to reduce the data by")
    args = parser.parse_args()
    args = process_generic_args(args)

    filename = Path(args.filename)
    new_pb = Path(args.new_filename)
    if args.backup_filename is not None:
        subprocess.run(["cp", filename, Path(args.backup_filename)], check=True)

    pb = PBUtils(filename)
    with open(new_pb, "wb") as f:
        f.write(pb.serialize(pb.header))
        f.writelines(
            pb.serialize(sample) for sample in reduce_by_factor(pb, args.factor)
        )
    if args.write_txt:
        txt_filepath = new_pb.with_suffix(".txt")
        with open(txt_filepath, "w") as f:
            # Write header
            f.write(f"{pb.header.pvname}, {pb.pv_type}, {pb.header.year}\n")
            # Write column titles
            f.write(f"DATE{' ' * 19}SECONDS{' ' * 5}NANO{' ' * 9}VAL\n")
            f.writelines(
                pb.format_datastr(sample)
                for sample in reduce_by_factor(pb, args.factor)
            )


def aa_remove_data_before():
    """Remove all data points before a certain timestamp in a PB file."""
    parser = argparse.ArgumentParser()
    parser = add_generic_args(parser)
    parser.add_argument(
        "timestamp",
        type=str,
        help="timestamp in the form 'month,day,hour,minute,second,nanosecond'"
        + "- month is required (default: {month},1,0,0,0,0)",
    )
    args = parser.parse_args()
    args = process_generic_args(args)

    filename = Path(args.filename)
    new_pb = Path(args.new_filename)
    if args.backup_filename is not None:
        subprocess.run(["cp", filename, Path(args.backup_filename)], check=True)

    pb = PBUtils(filename)
    seconds, nano = process_timestamp(pb, args.timestamp)

    with open(new_pb, "wb") as f:
        f.write(pb.serialize(pb.header))
        f.writelines(
            pb.serialize(sample) for sample in remove_before_ts(pb, seconds, nano)
        )
    if args.write_txt:
        txt_filepath = new_pb.with_suffix(".txt")
        with open(txt_filepath, "w") as f:
            # Write header
            f.write(f"{pb.header.pvname}, {pb.pv_type}, {pb.header.year}\n")
            # Write column titles
            f.write(f"DATE{' ' * 19}SECONDS{' ' * 5}NANO{' ' * 9}VAL\n")
            f.writelines(
                pb.format_datastr(sample)
                for sample in remove_before_ts(pb, seconds, nano)
            )


def aa_remove_data_after():
    """Remove all data points after a certain timestamp in a PB file."""
    parser = argparse.ArgumentParser()
    parser = add_generic_args(parser)
    parser.add_argument(
        "timestamp",
        type=str,
        help="timestamp in the form 'month,day,hour,minute,second,nanosecond'"
        + "- month is required (default: {month},1,0,0,0,0)",
    )
    args = parser.parse_args()
    args = process_generic_args(args)

    filename = Path(args.filename)
    new_pb = Path(args.new_filename)
    if args.backup_filename is not None:
        subprocess.run(["cp", filename, Path(args.backup_filename)], check=True)

    pb = PBUtils(filename)
    seconds, nano = process_timestamp(pb, args.timestamp)

    with open(new_pb, "wb") as f:
        f.write(pb.serialize(pb.header))
        f.writelines(
            pb.serialize(sample) for sample in remove_after_ts(pb, seconds, nano)
        )
    if args.write_txt:
        txt_filepath = new_pb.with_suffix(".txt")
        with open(txt_filepath, "w") as f:
            # Write header
            f.write(f"{pb.header.pvname}, {pb.pv_type}, {pb.header.year}\n")
            # Write column titles
            f.write(f"DATE{' ' * 19}SECONDS{' ' * 5}NANO{' ' * 9}VAL\n")
            f.writelines(
                pb.format_datastr(sample)
                for sample in remove_after_ts(pb, seconds, nano)
            )
