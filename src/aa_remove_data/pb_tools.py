from itertools import islice
from pathlib import Path

import typer

from aa_remove_data.archiver_data import ArchiverData
from aa_remove_data.remove_data import validate_pb_file

app = typer.Typer()


@app.command()
def pb_2_txt(filename: Path, txt_filename: Path | None = None):
    """Convert a .pb file to a human-readable .txt file."""
    txt_file = txt_filename if txt_filename else filename.with_suffix(".txt")
    print(f"Writing {txt_file}")
    # Validation
    validate_pb_file(filename, should_exist=True)
    ad = ArchiverData(filename)
    ad.write_txt(txt_file)
    print("Write completed!")


@app.command()
def print_header(filename: Path, lines: int = 0, start: int = 0):
    """Print the header and first few lines of a .pb file."""
    # Validation
    validate_pb_file(filename, should_exist=True)
    ad = ArchiverData(filename)
    print(f"Name: {ad.header.pvname}, Type: {ad.pv_type}, Year: {ad.header.year}")
    if lines:
        print(f"DATE{' ' * 19}SECONDS{' ' * 5}NANO{' ' * 9}VAL")
        for sample in islice(ad.get_samples(), start, start + lines):
            print(ad.format_datastr(sample, ad.header.year).strip())
