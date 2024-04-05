"""Airt neural network library."""

from .__about__ import __version__

__all__ = ["__version__"]

# extend path if needed
from pkgutil import extend_path

if "__path__" in globals():
    __path__ = extend_path(__path__, __name__)
