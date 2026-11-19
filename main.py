#!/usr/bin/env python3
"""Copy entry.png to /output/entry.png, deterministically.

Reads the finished 1024x1024 front-page image from this repository and
writes an identical copy to /output/entry.png. No network, no randomness:
running it twice produces byte-identical output.
"""

import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST_DIR = "/output"
DST = os.path.join(DST_DIR, "entry.png")


def main() -> int:
    if not os.path.isfile(SRC):
        print(f"missing source image: {SRC}", file=sys.stderr)
        return 1
    os.makedirs(DST_DIR, exist_ok=True)
    shutil.copyfile(SRC, DST)
    with open(DST, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()
    print(f"wrote {DST} ({os.path.getsize(DST)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
