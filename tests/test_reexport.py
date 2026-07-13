"""monotonic-nn re-exports must resolve to the same mononet.legacy objects."""

from __future__ import annotations


def test_layers_monodense_is_mononet_legacy() -> None:
    import mononet.legacy as legacy
    from airt.keras.layers import MonoDense

    assert MonoDense is legacy.MonoDense


def test_component_module_reexports_full_surface() -> None:
    import mononet.legacy as legacy
    from airt._components import mono_dense_layer as m

    for name in (
        "MonoDense",
        "create_type_1",
        "create_type_2",
        "get_saturated_activation",
        "get_activation_functions",
        "apply_activations",
        "get_monotonicity_indicator",
        "apply_monotonicity_indicator_to_kernel",
        "replace_kernel_using_monotonicity_indicator",
    ):
        assert getattr(m, name) is getattr(legacy, name), name


def test_version_is_040a1() -> None:
    import airt

    assert airt.__version__ == "0.4.0a1"
