from sf_app.cli import CommandLineInterface


class AppController:
    def __init__(self):
        self._cli = CommandLineInterface()
        self._cli.compress_callback.set_callable(self._compress)
        self._cli.decompress_callback.set_callable(self._decompress)
        self._cli.gui_callback.set_callable(self._run_gui)

    def _compress(self, input_path, output_path):
        ...

    def _decompress(self, input_path, output_path):
        ...

    def _run_gui(self):
        ...

    def run(self):
        self._cli.run()
