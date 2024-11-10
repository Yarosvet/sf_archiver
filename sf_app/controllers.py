"""Module contains controllers for the application."""
import pathlib

from sf_app.cli import CommandLineInterface
from sf_app.gui import GUI
from sf_app.logic import compress_huffman, compress_shannon_fano, decompress


class AppController:
    """Main controller of the application."""

    def __init__(self):
        self._cli = CommandLineInterface()
        self._cli.compress_callback.set_callable(self._compress)
        self._cli.decompress_callback.set_callable(self._decompress)
        self._cli.gui_callback.set_callable(self._run_gui)

        self._gui = GUI()
        self._gui.compress_callback.set_callable(self._compress)
        self._gui.decompress_callback.set_callable(self._decompress)

    @staticmethod
    def _compress(input_path: str, output_path: str, verify: bool, algorithm: int):  # noqa: FBT001
        filename = pathlib.Path(input_path).name
        with open(input_path, 'rb') as fi, open(output_path, 'wb') as fo:
            if algorithm == 1:
                compress_huffman(fi, fo, filename, enable_checksum=verify)
            else:
                compress_shannon_fano(fi, fo, filename, enable_checksum=verify)

    @staticmethod
    def _decompress(input_path, output_path, verify: bool):  # noqa: FBT001
        use_orig_filename = False
        if pathlib.Path(output_path).is_dir():
            output_path = pathlib.Path(output_path) / "temp.bin"
            use_orig_filename = True
        with open(input_path, 'rb') as fi, open(output_path, 'wb') as fo:
            filename = decompress(fi, fo, enable_checksum=verify)
        if use_orig_filename:
            new_path = pathlib.Path(output_path).with_name(filename)
            pathlib.Path(output_path).replace(new_path)

    def _run_gui(self):
        self._gui.run()

    def run(self):
        self._cli.run()
