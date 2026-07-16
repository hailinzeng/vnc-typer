#!/usr/bin/env python3
"""Create a simple PNG-backed ICO file."""

import struct
import sys
from pathlib import Path


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: make_ico.py input.png output.ico")

    png_path = Path(sys.argv[1])
    ico_path = Path(sys.argv[2])
    png = png_path.read_bytes()

    # ICONDIR + one ICONDIRENTRY. Width/height 64 match the source PNG.
    header = struct.pack("<HHH", 0, 1, 1)
    entry = struct.pack("<BBBBHHII", 64, 64, 0, 0, 1, 32, len(png), 22)
    ico_path.write_bytes(header + entry + png)


if __name__ == "__main__":
    main()
