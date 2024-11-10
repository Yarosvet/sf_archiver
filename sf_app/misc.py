import json
from collections.abc import Callable

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot


class SimpleCallback:
    """Provides a simple callback mechanism"""

    def __init__(self):
        self._callback = None

    def __call__(self, *args, **kwargs):
        if self._callback is not None:
            self._callback(*args, **kwargs)

    def set_callable(self, func: Callable):
        """Set the callback function"""
        self._callback = func


class QtEventBridge(QObject):
    """Bridge between a callback (which may be from another thread) to qt signal and slot
    Warning! All arguments must be JSON-serializable
    """

    _signal = pyqtSignal(str, str)

    def __init__(self, safe_callable: Callable, parent: QObject | None = None) -> None:
        super().__init__(parent=parent)
        self._safe_callable = safe_callable

        @pyqtSlot(str, str)
        def _slot(json_args: str, json_kwargs: str):
            self._safe_callable(*json.loads(json_args), **json.loads(json_kwargs))

        self._slot = _slot
        self._signal.connect(self._slot)  # noqa

    def __call__(self, *args, **kwargs):
        """Emit the signal"""
        self._signal.emit(json.dumps(args), json.dumps(kwargs))  # noqa
