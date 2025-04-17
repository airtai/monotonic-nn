from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal, Optional, TypeVar, Union

import numpy as np
from numpy.typing import NDArray

from ..import_utils import optional_import_block, require_optional_import

with optional_import_block():
    import matplotlib.pyplot as plt

__all__ = [
    "MonotonicDataset",
    "Monotonicity",
    "MonotonicityVector",
    "generate_cubic_data",
]

Monotonicity = TypeVar("Monotonicity", bound=Literal[-1, 0, 1])
MonotonicityVector = TypeVar(
    "MonotonicityVector", bound=Union[Monotonicity, Sequence[Monotonicity]]
)


@dataclass
class MonotonicDataset:
    """A class to hold the dataset and the corresponding data."""

    name: str
    monotonicity_vector: MonotonicityVector
    x: NDArray
    y: NDArray

    def __post_init__(self) -> None:
        if isinstance(self.monotonicity_vector, Sequence):
            if len(self.monotonicity_vector) != self.x.shape[1]:
                raise ValueError(
                    "Monotonicity vector length must match number of features."
                )
        else:
            self.monotonicity_vector = [self.monotonicity_vector] * self.x.shape[1]

    @require_optional_import("matplotlib", "plt")
    def plot(self) -> None:
        """Plot the dataset."""
        plt.scatter(self.x[:, 0], self.y)
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title(self.title)
        plt.show()

    def is_compatible(self, rhs: MonotonicityVector) -> Optional[str]:
        """Check if the dataset is compatible with the given monotonicity vector.

        Args:
            rhs (MonotonicityVector): The monotonicity vector to check against.

        Returns:
            Optional[str]: An error message if the vectors are not compatible,
                otherwise None.
        """
        if self.monotonicity_vector != rhs.monotonicity_vector:
            return (
                f"Monotonicity vector {self.monotonicity_vector} "
                f"does not match {rhs.monotonicity_vector}"
            )
        if self.name != rhs.name:
            return f"Dataset name {self.name} does not match {rhs.name}"
        if self.x.shape[1:] != rhs.x.shape[1:]:
            return f"Dataset shape {self.x.shape[1:]} does not match {rhs.x.shape[1:]}"
        return None


def generate_cubic_data(
    *,
    n_samples: int = 1000,
    noise: float = 0.1,
    x_mean: float = 0.0,
    x_std: float = 1.0,
    seed: int = 42,
) -> MonotonicDataset:
    """Generate synthetic data for y = x^3 + noise.

    Args:
        n_samples: total number of points to generate.
        noise:     standard deviation of Gaussian noise to add to y.
        x_mean:    mean of the Gaussian to sample x from.
        x_std:     stddev of the Gaussian to sample x from.

    Returns:
        MonotonicDataset: A dataset containing the generated data.
    """
    # 1) Sample x from N(x_mean, x_std^2)
    rnd = np.random.default_rng(seed=seed)
    x = rnd.normal(loc=x_mean, scale=x_std, size=(n_samples, 1))

    # 2) Compute y = x^3 + noise
    y = x[:, 0] ** 3 + rnd.normal(loc=0, scale=noise, size=n_samples)

    return MonotonicDataset(
        name="Cubic function",
        monotonicity_vector=[1],
        x=x,
        y=y,
    )
