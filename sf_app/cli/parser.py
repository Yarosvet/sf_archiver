import argparse
import sys


def configure_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='Shannon Fano archiver',
        description='Compress and decompress files using SF Archiver'
    )
    parser.add_argument(
        'mode',
        choices=['compress', 'decompress', 'gui'],
        help='Mode of operation',
        default='gui',
        nargs='?'
    )
    parser.add_argument('-i', '--input', help='Input file', required='gui' not in sys.argv and len(sys.argv) > 1)
    parser.add_argument('-o', '--output', help='Output file or directory', default='.', required='compress' in sys.argv)
    return parser
