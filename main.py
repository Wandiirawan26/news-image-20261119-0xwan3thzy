#!/usr/bin/env python3
"""Copy entry.png to /output/entry.png, deterministically.

Reads the finished 1024x1024 front-page image from this repository and
writes an identical copy to /output/entry.png. No network, no randomness:
running it twice produces byte-identical output.

Before writing, the program validates the source against the competition
limits (at most 1 MiB, at most 1024x1024 px) and, after copying, verifies
the output is byte-identical to the source, so a bad image can never be
submitted silently.
"""

import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST_DIR = "/output"
DST = os.path.join(DST_DIR, "entry.png")

MAX_BYTES = 1_048_576
MAX_DIM = 1024


def png_dimensions(path: str) -> tuple[int, int]:
    """Return (width, height) from a PNG file's IHDR chunk."""
    with open(path, "rb") as f:
        header = f.read(33)
    if len(header) < 33 or header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("source is not a PNG file")
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def sha256_file(path: str) -> str:
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main() -> int:
    if not os.path.isfile(SRC):
        print(f"missing source image: {SRC}", file=sys.stderr)
        return 1
    size = os.path.getsize(SRC)
    if size > MAX_BYTES:
        print(f"source too large: {size} bytes (max {MAX_BYTES})", file=sys.stderr)
        return 1
    try:
        width, height = png_dimensions(SRC)
    except ValueError as exc:
        print(f"invalid source image: {exc}", file=sys.stderr)
        return 1
    if width > MAX_DIM or height > MAX_DIM:
        print(f"source too big: {width}x{height} (max {MAX_DIM}x{MAX_DIM})",
              file=sys.stderr)
        return 1
    os.makedirs(DST_DIR, exist_ok=True)
    shutil.copyfile(SRC, DST)
    if sha256_file(SRC) != sha256_file(DST):
        print("copy mismatch: output differs from source", file=sys.stderr)
        return 1
    digest = sha256_file(DST)
    print(f"wrote {DST} ({size} bytes, {width}x{height}, sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
