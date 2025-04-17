from dataclasses import dataclass
from typing import Callable, Literal

import numpy as np

from ..helpers import export
from ..import_utils import optional_import_block, require_optional_import
from .common import MonotonicDataset, MonotonicityVector, generate_cubic_data

with optional_import_block():
    import torch
    from torch.utils.data import DataLoader, Dataset, TensorDataset

__all__ = [
    "MonotonicTorchDataset",
    "create_torch_datasets",
]


@dataclass
@export("monotonic.data")
class MonotonicTorchDataset:
    """A class to hold the PyTorch dataset and the corresponding data."""

    name: str
    monotonicity_vector: MonotonicityVector
    train_data: MonotonicDataset
    test_data: MonotonicDataset

    train_dataset: "Dataset"
    test_dataset: "Dataset"

    train_loader: "DataLoader"
    test_loader: "DataLoader"

    def plot(self, dataset: Literal["train", "test"] = "train") -> None:
        """Plot the dataset.

        Args:
            dataset (Literal["train", "test"]): The dataset to plot.
                Options are "train" or "test". Default is "train".
        """
        data = self.train_data if dataset == "train" else self.test_data
        data.plot()


def _numpy_to_torch_dataset(data: MonotonicDataset) -> TensorDataset:
    """Convert numpy arrays to a PyTorch TensorDataset.

    Args:
        x (NDArray): The input features.
        y (NDArray): The target variable.

    Returns:
        TensorDataset: The converted PyTorch dataset.
    """
    x_tensor = torch.from_numpy(data.x).float()
    y_tensor = torch.from_numpy(data.y).float()
    return TensorDataset(x_tensor, y_tensor)


@require_optional_import("torch", "torch")
def _monotonic_to_torch_dataset(
    train_data: MonotonicDataset,
    test_data: MonotonicDataset,
    *,
    batch_size: int = 32,
) -> MonotonicTorchDataset:
    """Convert a MonotonicDataset to a MonotonicTorchDataset dataset.

    Args:
        train_md (MonotonicDataset): The training dataset.
        test_md (MonotonicDataset): The testing dataset.

    Returns:
        MonotonicTorchDataset: The converted dataset.
    """
    error_message = train_data.is_compatible(test_data.monotonicity_vector)
    if error_message:
        raise ValueError(error_message)

    train_dataset = _numpy_to_torch_dataset(train_data)
    test_dataset = _numpy_to_torch_dataset(test_data)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    return MonotonicTorchDataset(
        name=train_data.name,
        monotonicity_vector=train_data.monotonicity_vector,
        train_data=train_data,
        test_data=test_data,
        train_dataset=train_dataset,
        test_dataset=test_dataset,
        train_loader=train_loader,
        test_loader=test_loader,
    )


@require_optional_import("torch", "torch")
@export("monotonic.data")
def create_torch_datasets(
    data_f: Callable[[int, float, float, float], MonotonicDataset],
    *,
    n_samples: int = 1000,
    train_split: float = 0.8,
    noise: float = 0.1,
    x_mean: float = 0.0,
    x_std: float = 1.0,
    batch_size: int = 32,
) -> MonotonicTorchDataset:
    """Create a PyTorch dataset of synthetic cubic data.

    Args:
        n_samples: total number of points to generate.
        train_split: proportion of data to use for training.
        noise:     standard deviation of Gaussian noise to add to y.
        x_mean:    mean of the Gaussian to sample x from.
        x_std:     stddev of the Gaussian to sample x from.
        batch_size: batch size for the DataLoader.

    Returns:
        MonotonicTorchDataset: The created dataset.
    """
    train_size = int(np.round(n_samples * train_split))
    test_size = n_samples - train_size

    train_data, test_data = [
        generate_cubic_data(
            n_samples=n_samples, noise=noise, x_mean=x_mean, x_std=x_std
        )
        for n_samples in [train_size, test_size]
    ]

    return _monotonic_to_torch_dataset(
        train_data=train_data,
        test_data=test_data,
        batch_size=batch_size,
    )
