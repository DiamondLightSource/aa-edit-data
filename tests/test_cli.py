import subprocess
import sys

from aa_remove_data import __version__


def test_cli_version():
    cmd = [sys.executable, "-m", "aa_remove_data", "--version"]
    assert subprocess.check_output(cmd).decode().strip() == __version__
