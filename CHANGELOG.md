# Release notes

<!-- do not remove -->

## 0.4.0

- **Reimplemented as a thin compatibility shim over
  [mononet](https://github.com/davorrunje/mononet).** `MonoDense`, the
  `create_type_1`/`create_type_2` builders, and the module-level helpers now
  re-export `mononet.legacy` (numerically identical to the previous
  implementation).
- **Breaking:** now requires **Keras 3** (via `tensorflow>=2.16`) and **Python
  3.11+** (was tf.keras / Python 3.9–3.11).
- Deprecated: importing `airt.keras.layers` emits a `DeprecationWarning`. New
  code should use `mononet` directly.
- Build modernized from nbdev to a plain `pyproject.toml`.
- `experiments.py` is kept as-is; the maintained benchmarks now live in the
  mononet docs.

## 0.3.4

- fix bug: old version in __init__.py


## 0.3.3

- removed support for saving Keras model since it was unstable



## 0.3.2

- add support for saving Keras model



## 0.3.1

- add support for import different subpackages with the same root packge name and different locations



## 0.3.0

Initial version as published at ICML 2023


