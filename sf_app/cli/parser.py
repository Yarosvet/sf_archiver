import argparse


def configure_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='Shannon Fano archiver',
        description='Compress and decompress files using SF Archiver'
    )
    subparsers = parser.add_subparsers(dest='mode', help='Mode of operation')

    # Sub-parser for compress mode
    compress_parser = subparsers.add_parser('compress', help='Compress files')
    compress_parser.add_argument('-i', '--input', help='Input file', required=True, type=str)
    compress_parser.add_argument('-o', '--output', help='Output file or directory', required=True)
    compress_parser.add_argument(
        '-A', '--algorithm',
        help='Compression algorithm (0 - Shannon-Fano (default), 1 - Huffman)',
        choices=[0, 1],
        default=0,
        type=int
    )
    compress_parser.add_argument(
        '-v', '--verify',
        help='Store CRC32 checksum of the original file in the compressed file',
        action='store_true'
    )

    # Sub-parser for decompress mode
    decompress_parser = subparsers.add_parser('decompress', help='Decompress files')
    decompress_parser.add_argument('-i', '--input', help='Input file', required=True, type=str)
    decompress_parser.add_argument(
        '-o', '--output',
        help='Output file or directory (default ./)',
        required=False,
        default='./'
    )
    decompress_parser.add_argument(
        '-v', '--verify',
        help='Verify CRC32 checksum stored in compressed file',
        action='store_true'
    )
    # Sub-parser for gui mode
    gui_parser = subparsers.add_parser('gui', help='Run GUI')  # noqa: F841

    return parser
