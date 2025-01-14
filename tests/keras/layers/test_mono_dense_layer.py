import numpy as np
import tensorflow as tf

from airt.keras.layers._mono_dense import get_activation_functions, apply_activations


def test_activation_functions() -> None:
    a_convex, a_concave = get_activation_functions("relu")
    assert a_convex(0) == 0
    assert a_concave(0) == 0
    assert a_convex(1) == 1
    assert a_concave(1) == 0
    assert a_convex(-1) == 0
    assert a_concave(-1) == -1

    x = tf.constant(np.arange(-10, 10.001, 0.1))
    y_convex = a_convex(x)
    y_concave = a_concave(x)
    np.testing.assert_almost_equal(y_convex.numpy(), -y_concave.numpy()[::-1])

def test_apply_activations() -> None:
    a_convex, a_concave = get_activation_functions("relu")
    rng = np.random.default_rng(42)
    x = tf.constant(rng.normal(size=255))
    units = x.shape[0]
    assert units % 2 == 1

    y = apply_activations(x, units=units, convex_activation=a_convex, concave_activation=a_concave)
    assert (y.numpy()[:units // 2 + 1] >= 0).all()
    assert (y.numpy()[units // 2 + 1:] <= 0).all()
