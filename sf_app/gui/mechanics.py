"""Mechanics of the GUI."""
from PyQt6.QtCore import QThread, pyqtSlot
from PyQt6.QtWidgets import QFileDialog, QMainWindow, QMessageBox

from sf_app.misc import QtEventBridge, SimpleCallback

from .main_window import Ui_MainWindow


class QThreadedSafeTask(QThread):
    """A task that runs in a separate thread and can safely call a callback in the main thread."""

    def __init__(self, action, *args, **kwargs):
        super().__init__()
        self.action = action
        self.args = args
        self.kwargs = kwargs
        self.error_callback = SimpleCallback()
        self._error_bridge = QtEventBridge(self.error_callback)

    def run(self):
        try:
            self.action(*self.args, **self.kwargs)
        except Exception as e:
            self._error_bridge(f"{type(e).__name__}: {str(e)}")


class MainWindow(QMainWindow):
    """Main window of the GUI."""

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.compress_callback = SimpleCallback()
        self.decompress_callback = SimpleCallback()

        self.ui.compress_button.clicked.connect(self._compress_clicked)
        self.ui.decompress_button.clicked.connect(self._decompress_clicked)

        self._running_tasks = []

    def show_error(self, message: str):
        m = QMessageBox(parent=self)
        m.setIcon(QMessageBox.Icon.Critical)
        m.setInformativeText(message)
        m.setWindowTitle('Error')
        m.exec()

    @pyqtSlot()
    def _compress_clicked(self):
        input_path, _ = QFileDialog.getOpenFileName(
            self,
            'Open file to compress',
            '',
            'All files (*)'
        )
        if input_path:
            output_path, _ = QFileDialog.getSaveFileName(
                self,
                'Save compressed file',
                '',
                'SF files (*.sf);;Binary files (*.bin);;All files (*)'
            )
            alg = 0 if self.ui.fano_radio.isChecked() else 1
            if output_path:
                # Place callback in a separate thread to avoid blocking the UI
                a = QThreadedSafeTask(
                    self.compress_callback,
                    input_path,
                    output_path,
                    self.ui.verify_checkbox.isChecked(),
                    alg
                )
                a.error_callback.set_callable(self.show_error)
                a.start()
                self._running_tasks.append(a)
                self.lock_ui()
                self.ui.statusbar.showMessage('Compressing...')

                @pyqtSlot()
                def _():
                    self.unlock_ui()
                    self._running_tasks.remove(a)
                    self.ui.statusbar.showMessage('Compression finished', 3000)

                a.finished.connect(_)

    @pyqtSlot()
    def _decompress_clicked(self):
        input_path, _ = QFileDialog.getOpenFileName(
            self,
            'Open file to decompress',
            '',
            'SF files (*.sf);;Binary files (*.bin);;All files (*)'
        )
        if input_path:
            output_dir = QFileDialog.getExistingDirectory(
                self,
                'Select output directory',
                ''
            )
            if output_dir:
                # Place callback in a separate thread to avoid blocking the UI
                a = QThreadedSafeTask(
                    self.decompress_callback,
                    input_path,
                    output_dir,
                    self.ui.verify_checkbox.isChecked()
                )
                a.error_callback.set_callable(self.show_error)
                a.start()
                self._running_tasks.append(a)
                self.lock_ui()
                self.ui.statusbar.showMessage('Decompressing...')

                @pyqtSlot()
                def _():
                    self.unlock_ui()
                    self._running_tasks.remove(a)
                    self.ui.statusbar.showMessage('Decompression finished', 3000)

                a.finished.connect(_)

    def lock_ui(self):
        self.ui.compress_button.setEnabled(False)
        self.ui.decompress_button.setEnabled(False)

    def unlock_ui(self):
        self.ui.compress_button.setEnabled(True)
        self.ui.decompress_button.setEnabled(True)
