# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/Helpers.ipynb.

# %% auto 0
__all__ = ['T', 'export']

# %% ../../nbs/Helpers.ipynb 1
from typing import Any, TypeVar

# %% ../../nbs/Helpers.ipynb 2
T = TypeVar("T")


def export(o: T, module: str = "airt.keras.layers") -> T:
    o.__module__ = module
    return o
