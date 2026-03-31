from __future__ import annotations

import hashlib
from pathlib import Path

CHUNK_SIZE = 1024 * 1024


def compute_sha256(path: Path) -> str:
    sha256 = hashlib.sha256()

    with path.open("rb") as file_handle:
        while True:
            chunk = file_handle.read(CHUNK_SIZE)
            if not chunk:
                break
            sha256.update(chunk)

    return sha256.hexdigest()


def derive_short_hash(sha256_hex: str) -> str:
    return sha256_hex[:8]


def hash_file(path: Path) -> tuple[str, str]:
    sha256_hex = compute_sha256(path)
    short_hash = derive_short_hash(sha256_hex)
    return sha256_hex, short_hash