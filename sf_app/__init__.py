"""SF Archiver (Shannon-Fano Archiver)."""
from sf_app.controllers import AppController


def run():
    """Run the application using controller."""
    c = AppController()
    c.run()
