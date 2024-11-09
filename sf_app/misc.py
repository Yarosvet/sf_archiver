from typing import Callable


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
