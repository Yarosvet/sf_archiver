meta:
  id: sf_archive
  file-extension: sf
  title: SF Archiver binary format
  application: SF Archiver
  license: MIT
  endian: be

seq:
  - id: header
    type: header
    size: 312
  - id: table
    type: assigned_code
    repeat: expr
    repeat-expr: header.table_length_decreased + 1
  - id: body
    size-eos: true

types:
  header:
    seq:
      - id: magic
        contents: "SF"
      - id: version
        type: u1
      - id: content_length
        type: u8
      - id: table_length_decreased
        type: u1
      - id: metadata
        type: str
        encoding: utf-8
        size: 300
  assigned_code:
    seq:
      - id: byte
        size: 1
      - id: code_length_decreased
        type: u1
      - id: binary_code
        size: ((code_length_decreased + 1) + (8 - (code_length_decreased + 1) % 8)) / 8
