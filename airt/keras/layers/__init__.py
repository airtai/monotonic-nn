"""Deprecated re-export of the monotonic dense layer, now backed by mononet."""

import warnings

from mononet.legacy import MonoDense, create_type_1, create_type_2

warnings.warn(
    "monotonic-nn is deprecated and is now a thin compatibility shim over "
    "mononet. Use mononet directly: https://github.com/davorrunje/mononet",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = ["MonoDense", "create_type_1", "create_type_2"]
