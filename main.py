#!/usr/bin/env python3
"""The World Today - 13 November 2026 (make.fun news-image-01).

Entrypoint: copies the bundled entry.png (JPEG bytes, 1024x1024, one
front-page infographic summing up Friday 13 November 2026 world news)
to $MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png).

Python 3.13, standard library only, no network, deterministic: the
output is byte-identical to entry.png on every run.
"""
import hashlib
import os
import sys

MAX_BYTES = 1_048_576  # 1 MiB gate from the competition rules
MAX_DIMENSION = 1024  # at most 1024 by 1024 pixels
JPEG_MAGIC = b"\xff\xd8\xff"
JPEG_END = b"\xff\xd9"  # EOI marker: a whole JPEG runs through its end

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def jpeg_dimensions(data):
    """Read width/height from the first SOF0/SOF2 segment (stdlib only)."""
    pos = 2  # skip the SOI marker
    while pos + 9 < len(data):
        if data[pos] != 0xFF:
            pos += 1
            continue
        marker = data[pos + 1]
        if marker in (0xC0, 0xC2):  # SOF0 / SOF2: height, width follow
            height = (data[pos + 5] << 8) | data[pos + 6]
            width = (data[pos + 7] << 8) | data[pos + 8]
            return width, height
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
            pos += 2  # standalone marker, no length field
            continue
        size = (data[pos + 2] << 8) | data[pos + 3]
        pos += 2 + size
    return None


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    sys.exit(1)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    out_path = os.path.join(out_dir, "entry.png")

    try:
        with open(SRC, "rb") as fh:
            data = fh.read()
    except OSError as exc:
        fail(f"cannot read {SRC}: {exc}")

    if len(data) > MAX_BYTES:
        fail(f"entry.png is {len(data)} bytes, over the 1 MiB gate")
    if not data.startswith(JPEG_MAGIC):
        fail("entry.png does not start with the JPEG magic bytes")
    if not data.endswith(JPEG_END):
        fail("entry.png does not end with the JPEG end marker")
    dims = jpeg_dimensions(data)
    if dims is None:
        fail("entry.png has no JPEG start-of-frame segment")
    width, height = dims
    if width > MAX_DIMENSION or height > MAX_DIMENSION:
        fail(f"entry.png is {width}x{height}, over the 1024x1024 gate")

    os.makedirs(out_dir, exist_ok=True)
    try:
        with open(out_path, "wb") as fh:
            fh.write(data)
    except OSError as exc:
        fail(f"cannot write {out_path}: {exc}")

    # Verify the copy byte-for-byte with SHA-256.
    digest_src = hashlib.sha256(data).hexdigest()
    try:
        with open(out_path, "rb") as fh:
            digest_out = hashlib.sha256(fh.read()).hexdigest()
    except OSError as exc:
        fail(f"cannot re-read {out_path}: {exc}")
    if digest_out != digest_src:
        fail(f"SHA-256 mismatch: wrote {digest_out}, expected {digest_src}")

    print(f"wrote {out_path}: {len(data)} bytes, sha256={digest_src}")


if __name__ == "__main__":
    main()
