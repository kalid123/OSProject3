import os

BLOCK_SIZE = 512
MAGIC = b'4348PRJ3'


def to_be8(n: int) -> bytes:
    return n.to_bytes(8, 'big', signed=False)


def from_be8(b: bytes) -> int:
    return int.from_bytes(b, 'big', signed=False)


def validate_index_file(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Index file '{path}' does not exist")
    with open(path, 'rb') as f:
        magic = f.read(8)
        if magic != MAGIC:
            raise ValueError("Not a valid index file: magic mismatch")
        f.seek(0, os.SEEK_END)
        if f.tell() % BLOCK_SIZE != 0:
            raise ValueError("Corrupted file size: not a multiple of block size")