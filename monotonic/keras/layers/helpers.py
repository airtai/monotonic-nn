from typing import TypeVar

__all__ = ["T", "export"]

T = TypeVar("T")


def export(o: T, module: str = "airt.keras.layers") -> T:
    o.__module__ = module
    return o
