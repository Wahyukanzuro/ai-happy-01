import base64
import os
from pathlib import Path


def main():
    here = Path(__file__).resolve().parent
    data = base64.b64decode((here / "image.b64").read_text().strip())
    if not data[:3] == b"\xff\xd8\xff":
        raise ValueError("entry image is not a JPEG")
    if len(data) > 1024 * 1024:
        raise ValueError("entry image exceeds 1 MiB")
    out_dir = os.environ["MAKEFUN_OUTPUT_DIR"]
    out_path = Path(out_dir) / "entry.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(data)


if __name__ == "__main__":
    main()
