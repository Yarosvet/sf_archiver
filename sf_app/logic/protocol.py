from dataclasses import dataclass
from typing import BinaryIO

FORMAT_HEADER = b"SF"
FORMAT_VERSION = 1


@dataclass
class DecodeReport:
    meta: bytes
    content_length: int


def encode(
        if_stream: BinaryIO,
        of_stream: BinaryIO,
        table: dict[bytes, str],
        meta: bytes = None
) -> None:
    if meta is None:
        meta = b""
    if len(meta) > 300:
        raise ValueError("Metadata is too long (300 bytes max)")
    # Construct header
    header = (FORMAT_HEADER +
              FORMAT_VERSION.to_bytes(1, "big") +
              b"\x00\x00\x00\x00\x00\x00\x00\x00" +  # (8b) There will be content length (will be filled later)
              (len(table) - 1).to_bytes(1, 'big') +  # Table length - 1 (in symbols)
              meta.rjust(300, b"\x00"))  # Metadata (300b)
    content_length_pos = 3
    of_stream.write(header)
    # Write table
    table_buffer = bytes()
    for b, code in table.items():
        table_buffer += (b +
                         (len(code) - 1).to_bytes() +
                         int(code, 2).to_bytes((len(code) + (8 - len(code) % 8)) // 8, 'big'))
    of_stream.write(table_buffer)
    # Write content
    buffer = ""
    c = 0
    while sym := if_stream.read(1):
        c += 1
        buffer += table[sym]
        while len(buffer) >= 8:
            of_stream.write(int(buffer[:8], 2).to_bytes(1, 'big'))
            buffer = buffer[8:]
    if buffer:  # It's certainly less than 8
        # Write the rest of the buffer
        of_stream.write(int(buffer.ljust(8, '0'), 2).to_bytes(1, 'big'))
    del buffer
    # Update content length in header
    if c > 2 ** 64 - 1:
        raise ValueError("Content is too long")
    of_stream.seek(content_length_pos)
    of_stream.write(c.to_bytes(8, 'big'))
    of_stream.seek(0, 2)


def decode(if_stream: BinaryIO, of_stream: BinaryIO) -> DecodeReport:
    # Read header (312b)
    header = if_stream.read(312)
    # Check protocol code
    if header[:2] != FORMAT_HEADER:
        raise ValueError("Invalid protocol header")
    # Check version
    if header[2] != FORMAT_VERSION:
        raise ValueError("Invalid protocol version")
    # Read length of file and table
    content_length = int().from_bytes(header[3: 11], 'big')  # 8 bytes read
    table_length = int(header[11]) + 1
    # Read metadata
    _meta = header[12:]
    # Read table
    table: dict[str, bytes] = {}
    for i in range(table_length):
        b = if_stream.read(1)
        code_length = int().from_bytes(if_stream.read(1), 'big') + 1
        code = (bin(int.from_bytes(if_stream.read((code_length + (8 - code_length % 8)) // 8), 'big'))[2:]
                .zfill(code_length))
        table[code] = b
    # Read content and write to output stream
    binary_buffer = ""
    symbols_decoded = 0
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
                    break
    if symbols_decoded < content_length:
        raise ValueError("Invalid content length")
    return DecodeReport(
        meta=_meta,
        content_length=content_length
    )
