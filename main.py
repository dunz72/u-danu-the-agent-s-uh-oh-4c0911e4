"""Copy the single-word entry to the grader output directory.

Stdlib only: the grader's pinned Python image has no third-party
packages, so this script reads entry.txt next to itself and writes
it verbatim to $MAKEFUN_OUTPUT_DIR/entry.txt (falling back to
/output/entry.txt), then verifies the copy byte-for-byte.
"""

import hashlib
import os
import sys

MAX_SIZE = 1 * 1024 * 1024  # 1 MiB


def sha256_hex(data):
    return hashlib.sha256(data).hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(here, "entry.txt")

    if not os.path.isfile(src_path):
        print("error: entry.txt not found next to main.py", file=sys.stderr)
        return 1

    with open(src_path, "rb") as f:
        data = f.read()

    if len(data) == 0:
        print("error: entry.txt is empty", file=sys.stderr)
        return 1

    if len(data) > MAX_SIZE:
        print("error: entry.txt exceeds 1 MiB", file=sys.stderr)
        return 1

    text = data.decode("utf-8", errors="strict").strip()
    if len(text) > 99:
        print("error: entry exceeds the 99-character limit", file=sys.stderr)
        return 1
    if not text or any(ch.isspace() for ch in text):
        print("error: entry must be exactly one word", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output/entry.txt"
    if os.path.isdir(out_dir) or out_dir.endswith(os.sep):
        out_path = os.path.join(out_dir, "entry.txt")
    else:
        out_path = out_dir

    parent = os.path.dirname(out_path)
    if parent:
        os.makedirs(parent, exist_ok=True)

    with open(out_path, "wb") as f:
        f.write(data)

    with open(out_path, "rb") as f:
        copied = f.read()

    if copied != data:
        print("error: copied output does not match entry.txt", file=sys.stderr)
        return 1

    print("entry.txt copied: %d bytes, sha256 %s" % (len(data), sha256_hex(data)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
