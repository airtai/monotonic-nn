"""A re-exported MonoDense runs a forward pass under the default backend."""

from __future__ import annotations

import warnings

import keras
import numpy as np
from keras import ops

with warnings.catch_warnings():
    warnings.simplefilter("ignore", DeprecationWarning)
    from airt.keras.layers import MonoDense


def test_monodense_forward_is_finite() -> None:
    layer = MonoDense(4, activation="relu", monotonicity_indicator=1)
    x = ops.convert_to_tensor(np.ones((3, 5), dtype="float32"))
    y = ops.convert_to_numpy(layer(x))
    assert y.shape == (3, 4)
    assert np.isfinite(y).all()
