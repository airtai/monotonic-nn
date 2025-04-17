from typing import Callable, TypeVar

__all__ = ["T", "export"]

T = TypeVar("T")


def export(module: str) -> Callable[[T], T]:
    """Decorator to export a function or class to a specific module.

    Args:
        module (str): The module to which the function or class should be exported.
    """

    def _decorator(o: T) -> T:
        """Decorator to export a function or class to a specific module."""
        if not hasattr(o, "__module__"):
            raise ValueError("The object must have a __module__ attribute.")
        o.__module__ = module

        return o
