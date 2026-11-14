#!/usr/bin/env python3
"""ai-happy-01 entry: write the happy image to $MAKEFUN_OUTPUT_DIR/entry.png.

The image ships in the repo as image.b64 (base64, one line) because the
GitHub connector cannot push binary files. This program decodes it at
runtime and writes the bytes to the output directory. The image is a
JPEG, 1024x1024, 253,186 bytes: a handwritten letter from a six-year-old
to the judge, who sits alone all day — so the child drew the judge a
friend, a dog named Biscuit who does not judge.
"""

import base64
import os
import sys
from pathlib import Path


def main() -> int:
    here = Path(__file__).resolve().parent
    b64_path = here / "image.b64"

    with open(b64_path, "r", encoding="ascii") as f:
        data = base64.b64decode(f.read().strip())

    if not data:
        raise ValueError("image.b64 decoded to no bytes")

    # JPEG files start with FF D8 FF; PNG files with the 8-byte PNG signature.
    if not (data.startswith(b"\xff\xd8\xff") or data.startswith(b"\x89PNG")):
        raise ValueError("image.b64 does not decode to a JPEG or PNG image")

    if len(data) > 1_048_576:
        raise ValueError(f"decoded image is {len(data)} bytes, over the 1 MiB limit")

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)

    out_path = out_dir / "entry.png"
    with open(out_path, "wb") as f:
        f.write(data)

    print(f"Wrote {len(data)} bytes to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
