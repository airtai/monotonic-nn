> # ⚠️ Deprecated — now a compatibility shim over `mononet`
>
> As of **v0.4.0a1**, `monotonic-nn` is a thin, deprecated compatibility layer.
> The maintained, multi-backend implementation (PyTorch, JAX, Keras 3) lives in
> **[mononet](https://github.com/davorrunje/mononet)**. This package now
> re-exports `mononet.legacy` so existing `airt.*` imports keep working.
>
> **Breaking in 0.4.0a1:** requires **Keras 3** (via `tensorflow>=2.16`) and
> **Python 3.11+**. New code should use `mononet` directly. Docs:
> <https://davorrunje.github.io/mononet/>.

---

Constrained Monotonic Neural Networks
================

## Summary

This package implements the Constrained Monotonic Neural Network construction
described in:

Davor Runje, Sharath M. Shankaranarayana, “Constrained Monotonic Neural
Networks”, in Proceedings of the 40th International Conference on Machine
Learning, 2023. \[[PDF](https://arxiv.org/pdf/2205.11775.pdf)\].

#### Abstract

Wider adoption of neural networks in many critical domains such as finance and
healthcare is being hindered by the need to explain their predictions and to
impose additional constraints on them. Monotonicity constraint is one of the
most requested properties in real-world scenarios and is the focus of this
paper. One of the oldest ways to construct a monotonic fully connected neural
network is to constrain signs on its weights. Unfortunately, this construction
does not work with popular non-saturated activation functions as it can only
approximate convex functions. We show this shortcoming can be fixed by
constructing two additional activation functions from a typical unsaturated
monotonic activation function and employing each of them on the part of neurons.
Our experiments show this approach of building monotonic neural networks has
better accuracy when compared to other state-of-the-art methods, while being the
simplest one in the sense of having the least number of parameters, and not
requiring any modifications to the learning procedure or post-learning steps.
Finally, we prove it can approximate any continuous monotone function on a
compact subset of $\mathbb{R}^n$.

## Status: compatibility shim

Since **v0.4.0a1**, this package no longer contains its own implementation. Its
public API re-exports [`mononet.legacy`](https://github.com/davorrunje/mononet),
the maintained multi-backend (PyTorch / JAX / Keras 3) implementation of the same
construction. The re-exported objects are the very same ones from
`mononet.legacy`, and behaviour is numerically identical to the original
TensorFlow-Keras implementation (pinned by equivalence tests in `mononet`).

The following continue to import, now backed by `mononet` and emitting a
`DeprecationWarning`:

- `airt.keras.layers.MonoDense`
- `airt.keras.layers.MonoDense.create_type_1` / `create_type_2`
- the helpers in `airt._components.mono_dense_layer`

**New projects should depend on [`mononet`](https://github.com/davorrunje/mononet)
directly.**

## Requirements

- Python **3.11+**
- **Keras 3** — installed via `tensorflow>=2.16`

## Install

``` sh
pip install --pre monotonic-nn
```

`--pre` is required while `monotonic-nn` and `mononet` are in alpha.

## Usage (compatibility)

Existing code keeps working unchanged; the imports resolve to `mononet.legacy`.
The `monotonicity_indicator` uses the original three-value convention — `1` for
increasingly monotonic inputs, `-1` for decreasingly monotonic, `0` for
non-monotonic:

``` python
import keras
from keras import Sequential
from keras.layers import Input

from airt.keras.layers import MonoDense  # re-exported from mononet.legacy

model = Sequential(
    [
        Input(shape=(3,)),
        MonoDense(128, activation="elu", monotonicity_indicator=[1, 0, -1]),
        MonoDense(128, activation="elu"),
        MonoDense(1),
    ]
)
```

For the `create_type_1` / `create_type_2` builders, benchmarks, the strictly
multi-backend API, and current documentation, see the `mononet` docs:
<https://davorrunje.github.io/mononet/>.

## Citation

If you use this library, please cite:

``` title="bibtex"
@inproceedings{runje2023,
  title={Constrained Monotonic Neural Networks},
  author={Davor Runje and Sharath M. Shankaranarayana},
  booktitle={Proceedings of the 40th {International Conference on Machine Learning}},
  year={2023}
}
```

## License

This package is licensed under the **Creative Commons
Attribution-NonCommercial-ShareAlike 4.0 International License
(CC BY-NC-SA 4.0)** — see [LICENSE](LICENSE).

> The underlying implementation, [`mononet`](https://github.com/davorrunje/mononet),
> is available under the **Apache License 2.0**, which permits commercial use.
> If you need a permissive or commercial license, use `mononet` directly.
