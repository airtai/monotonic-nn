"""The re-exported builders build runnable Keras models (upstream convention)."""

from __future__ import annotations

import warnings

import keras
import numpy as np

with warnings.catch_warnings():
    warnings.simplefilter("ignore", DeprecationWarning)
    from airt.keras.layers import MonoDense, create_type_1, create_type_2


def test_create_type_1_builds_runnable_model() -> None:
    inputs = [keras.Input(shape=(1,)) for _ in range(4)]
    out = create_type_1(
        inputs, units=8, final_units=1, activation="elu", n_layers=3,
        monotonicity_indicator=[1, 1, -1, 0],
    )
    model = keras.Model(inputs, out)
    xs = [np.zeros((2, 1), dtype="float32") for _ in range(4)]
    assert tuple(model(xs).shape) == (2, 1)


def test_create_type_2_builds_runnable_model() -> None:
    inputs = [keras.Input(shape=(1,)) for _ in range(4)]
    out = create_type_2(
        inputs, units=8, final_units=1, activation="elu", n_layers=2,
        monotonicity_indicator=[1, -1, 0, 1],
    )
    model = keras.Model(inputs, out)
    xs = [np.zeros((2, 1), dtype="float32") for _ in range(4)]
    assert tuple(model(xs).shape) == (2, 1)


def test_classmethods_reachable() -> None:
    assert callable(MonoDense.create_type_1)
    assert callable(MonoDense.create_type_2)
