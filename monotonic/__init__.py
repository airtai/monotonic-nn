"""Constrained Monotonic Neural Networks."""

from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)  # Extend the path for namespace packages
from .__about__ import __version__

__all__ = ["__path__", "__version__", "meaning_of_life"]


def meaning_of_life() -> int:
    """Return the meaning of life."""
    return 42
