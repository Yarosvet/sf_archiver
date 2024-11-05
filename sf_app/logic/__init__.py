"""Main logic of the application."""
from typing import BinaryIO, Literal

from . import alg
from . import protocol


def compress_huffman(if_stream: BinaryIO, of_stream: BinaryIO, filename: str) -> None:
    """
    Compress the file using Huffman algorithm.
    As for now, it stores only filename in metadata.
    """
    __compress(if_stream, of_stream, filename, 'huffman')


def compress_shannon_fano(if_stream: BinaryIO, of_stream: BinaryIO, filename: str) -> None:
    """
    Compress the file using Shannon-Fano algorithm.
    As for now, it stores only filename in metadata.
    """
    __compress(if_stream, of_stream, filename, 'fano')


def __compress(if_stream: BinaryIO, of_stream: BinaryIO, filename: str, algorithm: Literal['fano', 'huffman']) -> None:
    distribution = alg.count_distribution(if_stream)
    table = alg.assign_shannon_fano(distribution) if algorithm == 'fano' else alg.assign_huffman(distribution)
    if_stream.seek(0)  # Guarantee that we are at the beginning of the file
    meta = filename.encode('utf-8') + b"\n"
    protocol.encode(if_stream, of_stream, table, meta)


def decompress(if_stream: BinaryIO, of_stream: BinaryIO) -> str:
    """
    Decompress the file.
    :return: Filename of the original file.
    """
    report = protocol.decode(if_stream, of_stream)
    return report.meta.lstrip(b"\x00").decode()