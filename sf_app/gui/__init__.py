import signal

from PyQt6.QtWidgets import QApplication

from .mechanics import MainWindow


class GUI:
    def __init__(self):
        self._app = QApplication([])
        self.main_window = MainWindow()
        self.compress_callback = self.main_window.compress_callback
        self.decompress_callback = self.main_window.decompress_callback

    def run(self):
        # Restore default signal handler for SIGINT to make app close on Ctrl+C
        signal.signal(signal.SIGINT, signal.SIG_DFL)

        self.main_window.show()
        self._app.exec()
