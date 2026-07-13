"""Importing airt.keras.layers must warn that monotonic-nn is deprecated."""

from __future__ import annotations

import importlib
import sys
import warnings


def test_import_emits_deprecation_warning() -> None:
    # Force a fresh import so the module-level warning re-fires.
    sys.modules.pop("airt.keras.layers", None)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        importlib.import_module("airt.keras.layers")
    assert any(
        issubclass(w.category, DeprecationWarning)
        and "mononet" in str(w.message)
        for w in caught
    )
