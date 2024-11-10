"""Module for encoding and decoding files using the protocol."""
from dataclasses import dataclass
from typing import BinaryIO
from zlib import crc32

FORMAT_HEADER = b"SF"
FORMAT_VERSION = 1


@dataclass
class DecodeReport:
    """Metadata and content length of the decoded file."""

    meta: bytes
    content_length: int


CHECKSUM_BUFFER_SIZE = 512
ENCODING_BUFFER_SIZE = 8
MAX_METADATA_SIZE = 300


def encode(
        if_stream: BinaryIO,
        of_stream: BinaryIO,
        table: dict[bytes, str],
        meta: bytes = None,
        *,
        enable_checksum: bool = True
) -> None:
    """Encode the input stream using the table and write the result to the output stream."""
    if meta is None:
        meta = b""
    if len(meta) > MAX_METADATA_SIZE:
        raise ValueError(f"Metadata is too long ({MAX_METADATA_SIZE} bytes max)")
    # Construct header
    header = (FORMAT_HEADER +
              FORMAT_VERSION.to_bytes(1, "big") +
              b"\x00\x00\x00\x00\x00\x00\x00\x00" +  # (8b) There will be content length (will be filled later)
              b"\x00\x00\x00\x00" +  # Here will be CRC32 (4b) (will be filled later)
              (len(table) - 1).to_bytes(1, 'big') +  # Table length - 1 (in symbols)
              meta.rjust(MAX_METADATA_SIZE, b"\x00"))  # Metadata (300b)
    content_length_pos = 3
    checksum_pos = 11
    of_stream.write(header)
    # Write table
    table_buffer = b""
    for b, code in table.items():
        table_buffer += (b +
                         (len(code) - 1).to_bytes() +
                         int(code, 2).to_bytes((len(code) + (8 - len(code) % 8)) // 8, 'big'))
    of_stream.write(table_buffer)
    # Write content
    buffer = ""
    c = 0
    checksum_buffer = b""
    checksum = crc32(checksum_buffer)
    while sym := if_stream.read(1):
        c += 1
        buffer += table[sym]
        while len(buffer) >= ENCODING_BUFFER_SIZE:
            of_stream.write(int(buffer[:ENCODING_BUFFER_SIZE], 2).to_bytes(1, 'big'))
            buffer = buffer[ENCODING_BUFFER_SIZE:]
        # For checksum
        if enable_checksum:
            checksum_buffer += sym
            if len(checksum_buffer) >= CHECKSUM_BUFFER_SIZE:
                checksum = crc32(checksum_buffer, checksum)
                checksum_buffer = b""
    if buffer:  # It's certainly less than 8
        # Write the rest of the buffer
        of_stream.write(int(buffer.ljust(8, '0'), 2).to_bytes(1, 'big'))
    del buffer
    # Checksum for the rest of the buffer
    if enable_checksum and checksum_buffer:
        checksum = crc32(checksum_buffer, checksum)
    # Update content length in header
    if c > 2 ** 64 - 1:
        raise ValueError("Content is too long")
    of_stream.seek(content_length_pos)
    of_stream.write(c.to_bytes(8, 'big'))
    # Write checksum
    if enable_checksum:
        of_stream.seek(checksum_pos)
        of_stream.write(checksum.to_bytes(4, 'big'))
    # Return to the end of stream
    of_stream.seek(0, 2)


def decode(
        if_stream: BinaryIO,
        of_stream: BinaryIO,
        *,
        enable_checksum: bool = True
) -> DecodeReport:
    """Decode the input stream and write the result to the output stream."""
    # Read header (312b)
    header = if_stream.read(316)
    # Check protocol code
    if header[:2] != FORMAT_HEADER:
        raise ValueError("Invalid protocol header")
    # Check version
    if header[2] != FORMAT_VERSION:
        raise ValueError("Invalid protocol version")
    # Read length of file and table
    content_length = int().from_bytes(header[3: 11], 'big')  # 8 bytes read
    checksum_orig = int().from_bytes(header[11: 15], 'big')  # 4 bytes read
    table_length = int(header[15]) + 1
    # Read metadata
    _meta = header[16:]
    # Read table
    table: dict[str, bytes] = {}
    for _i in range(table_length):
        b = if_stream.read(1)
        code_length = int().from_bytes(if_stream.read(1), 'big') + 1
        code = (bin(int.from_bytes(if_stream.read((code_length + (8 - code_length % 8)) // 8), 'big'))[2:]
                .zfill(code_length))
        table[code] = b
    # Read content and write to output stream
    binary_buffer = ""
    symbols_decoded = 0
    checksum_buffer = b""
    checksum = crc32(checksum_buffer)
    while sym := if_stream.read(1):
        binary_buffer += bin(int().from_bytes(sym))[2:].zfill(8)
        found = True
        while found and binary_buffer and symbols_decoded < content_length:
            found = False
            for k in table.keys():
                if binary_buffer.startswith(k):
                    of_stream.write(table[k])
                    binary_buffer = binary_buffer[len(k):]
                    symbols_decoded += 1
                    found = True
                    # For checksum
                    if enable_checksum and checksum_orig != 0:  # If checksum was 0, we just didn't write it in the file
                        checksum_buffer += table[k]
                        if len(checksum_buffer) >= CHECKSUM_BUFFER_SIZE:
                            checksum = crc32(checksum_buffer, checksum)
                            checksum_buffer = b""
                    break
    if symbols_decoded < content_length:
        raise ValueError("Invalid content length")
    # Checksum for the rest of the buffer
    if enable_checksum and checksum_orig != 0 and checksum_buffer:
        checksum = crc32(checksum_buffer, checksum)
    # Check checksum
    if enable_checksum and checksum_orig not in (0, checksum):
        raise ValueError("Checksum mismatch")
    return DecodeReport(
        meta=_meta,
        content_length=content_length
    )
