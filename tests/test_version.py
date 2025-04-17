import monotonic


def test_version() -> None:
    assert monotonic.__version__ is not None
