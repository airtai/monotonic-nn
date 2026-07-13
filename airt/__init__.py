"""monotonic-nn — a deprecated compatibility shim over ``mononet``.

The monotonic-network construction from Runje & Shankaranarayana (ICML 2023)
is now maintained in `mononet <https://github.com/davorrunje/mononet>`_ with
PyTorch, JAX, and Keras 3 backends. This package re-exports
``mononet.legacy`` so existing ``airt.*`` imports keep working. New code should
use ``mononet`` directly.
"""

from pkgutil import extend_path

__version__ = "0.4.0"
__path__ = extend_path(__path__, __name__)
__all__: list[str] = []
