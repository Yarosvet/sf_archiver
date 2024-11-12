"""Graphical user interface for the application."""
import os
import signal

from PyQt6.QtGui import QFontDatabase, QIcon, QPixmap
from PyQt6.QtWidgets import QApplication

from .mechanics import MainWindow

FONTS = (
    "fonts/Roboto-Regular.ttf",
)


# FIXME: QFont::setPointSize: Point size <= 0 (-1), must be greater than 0

class GUI:
    """Graphical user interface."""

    def __init__(self):
        self._app = QApplication([])

        # Add fonts
        for _f in FONTS:
            QFontDatabase.addApplicationFont(os.path.join(os.path.dirname(__file__), _f))

        self.main_window = None
        self.compress_callback = None
        self.decompress_callback = None

    def build(self):
        self.main_window = MainWindow()
        self.compress_callback = self.main_window.compress_callback
        self.decompress_callback = self.main_window.decompress_callback

        # Load images  # TODO: make normal loading resources like all healthy people do
        self.main_window.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), "img/sf_icon.png")))
        self.main_window.ui.label.setPixmap(QPixmap(os.path.join(os.path.dirname(__file__), "img/sf_logo.png")))

    def run(self):
        # Restore default signal handler for SIGINT to make app close on Ctrl+C
        signal.signal(signal.SIGINT, signal.SIG_DFL)

        self.main_window.show()
        self._app.exec()
