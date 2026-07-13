"""Deprecated re-export of the original public surface, now backed by mononet.

The implementation lives in ``mononet.legacy``; these names are kept so code
written against ``airt._components.mono_dense_layer`` continues to import.
"""

from mononet.legacy import (
    MonoDense,
    apply_activations,
    apply_monotonicity_indicator_to_kernel,
    create_type_1,
    create_type_2,
    get_activation_functions,
    get_monotonicity_indicator,
    get_saturated_activation,
    replace_kernel_using_monotonicity_indicator,
)

__all__ = [
    "MonoDense",
    "apply_activations",
    "apply_monotonicity_indicator_to_kernel",
    "create_type_1",
    "create_type_2",
    "get_activation_functions",
    "get_monotonicity_indicator",
    "get_saturated_activation",
    "replace_kernel_using_monotonicity_indicator",
]
