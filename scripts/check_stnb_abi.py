#!/usr/bin/env python3
"""Read-only, eight-byte STNB format inspection. No imports or execution of weight data.

This tool is intended only for a file the user has already acquired lawfully
and authorized for local inspection; it never fetches anything over a network.
A PASS is only header-version compatibility, never inference compatibility.
Python >=3.10, standard library only.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

MAGIC = b"STNB"
HEADER_PREFIX_BYTES = 8
DEFAULT_LOADER_VERSION = 1


def inspect_header(prefix: bytes, loader_version: int = DEFAULT_LOADER_VERSION) -> dict:
    """Interpret only the 4-byte magic and 4-byte LE version."""
    if not isinstance(loader_version, int) or isinstance(loader_version, bool) or loader_version <= 0:
        raise ValueError("loader_version must be a positive integer")
    if len(prefix) < HEADER_PREFIX_BYTES:
        return {"verdict": "UNCERTAIN_TRUNCATED", "actual_version": None,
                "loader_version": loader_version, "bytes_read": len(prefix),
                "meaning": "Not enough bytes to identify the model format"}
    if prefix[:4] != MAGIC:
        return {"verdict": "FAIL_MAGIC", "actual_version": None,
                "loader_version": loader_version, "bytes_read": HEADER_PREFIX_BYTES,
                "meaning": "The file does not start with STNB"}
    version = int.from_bytes(prefix[4:8], byteorder="little", signed=False)
    match = version == loader_version
    return {"verdict": "PASS_HEADER_VERSION_ONLY" if match else "FAIL_VERSION_MISMATCH",
            "actual_version": version, "loader_version": loader_version,
            "bytes_read": HEADER_PREFIX_BYTES,
            "meaning": "Version matches; full model, codec, size, license and inference are UNTESTED" if match
                       else "This loader is specified to reject a model with this version"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path, help="Already authorized local nano.bin; no download")
    parser.add_argument("--loader-version", type=int, default=DEFAULT_LOADER_VERSION,
                        help="Pinned C loader NANO_BIN_VERSION, default 1")
    args = parser.parse_args(argv)
    if args.loader_version <= 0:
        parser.error("--loader-version must be positive")
    try:
        with args.file.open("rb") as stream:
            prefix = stream.read(HEADER_PREFIX_BYTES)
    except OSError as exc:
        print(json.dumps({"verdict": "UNCERTAIN_FILE_ACCESS", "error": str(exc),
                          "no_model_code_executed": True}))
        return 2
    result = inspect_header(prefix, args.loader_version)
    result.update(file=str(args.file), no_model_code_executed=True,
                  no_payload_download=True, entire_file_hash_verified=False)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["verdict"] == "PASS_HEADER_VERSION_ONLY" else 2 if result["verdict"].startswith("UNCERTAIN") else 1


if __name__ == "__main__":
    raise SystemExit(main())
