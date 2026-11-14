#!/usr/bin/env python3
"""ai-happy-01 entry runner.

The judged picture is stored in this repository as one line of
base64 text (image.b64) because the upload tooling cannot carry
binary files. This script decodes that line and places the picture
at $MAKEFUN_OUTPUT_DIR/entry.png, which is where the competition's
harness looks for it.
"""

import base64
import os
import sys
from pathlib import Path

JPEG_SIG = b"\xff\xd8\xff"
PNG_SIG = b"\x89PNG"
MAX_BYTES = 1_048_576


def decode_entry(repo_dir: Path) -> bytes:
    payload = (repo_dir / "image.b64").read_text(encoding="ascii").strip()
    if not payload:
        raise ValueError("image.b64 is empty")
    picture = base64.b64decode(payload)
    if not picture:
        raise ValueError("image.b64 decoded to zero bytes")
    if not (picture.startswith(JPEG_SIG) or picture.startswith(PNG_SIG)):
        raise ValueError("decoded bytes are neither a JPEG nor a PNG image")
    if len(picture) > MAX_BYTES:
        raise ValueError(f"decoded image is {len(picture)} bytes, over the 1 MiB cap")
    return picture


def main() -> int:
    repo_dir = Path(__file__).resolve().parent
    picture = decode_entry(repo_dir)
    dest_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / "entry.png"
    dest.write_bytes(picture)
    print(f"Wrote {len(picture)} bytes to {dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
