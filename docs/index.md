# monotonic-nn (deprecated)

!!! warning "This package is deprecated"
    `monotonic-nn` is now a thin compatibility shim over
    [**mononet**](https://github.com/davorrunje/mononet), the maintained
    multi-backend implementation (PyTorch, JAX, Keras 3). Existing `airt.*`
    imports keep working via `mononet.legacy`, but **new code should use
    `mononet` directly**.

    As of v0.4.0 this package requires **Keras 3** (`tensorflow>=2.16`) and
    **Python 3.11+**.

## Documentation & benchmarks

The current documentation and the maintained paper-reproduction benchmarks live
in the mononet docs:

- Docs: <https://davorrunje.github.io/mononet/>
- Benchmarks: <https://davorrunje.github.io/mononet/benchmarks/paper-reproduction/>

The experiment notebooks in this site are **archived** for historical reference.
