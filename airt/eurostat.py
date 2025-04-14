from pathlib import Path
from typing import Optional
import eurostat
import pandas as pd
import tensorflow as tf


class EurostatDataset():
    def __init__(self, download_path: Path):
        """Initialize the EurostatDataset class

        Args:
            download_path (Path): Path to the folder where the data will be downloaded
        """
        self.download_path = download_path
        pass

    @property
    def toc(self) -> pd.DataFrame:
        return eurostat.get_toc_df()
    
    def get_data(self, code: str, flags: bool = False) -> pd.DataFrame:
        """Get data from Eurostat
        
        If the doata is downloaded locally, it will be loaded from the local file.
        If the data is not downloaded, it will be downloaded from Eurostat.

        Args:
            code (str): Eurostat code
            flags (bool, optional): Flags. Defaults to False.
        """
        ...

    def download_data(self, *, code: Optional[str] = None, flags: bool = False) -> None:
        """Download data from Eurostat and save it to a folder

        Args:
            code (Optional[str], optional): Eurostat code. If None, download all data. Defaults to None.
            flags (bool, optional): Flags. Defaults to False.
        """
        ...

    def preprocess_data(self) -> None:
        """Preprocess the downloaded data
        """
        ...

    def to_dataset(self) -> tf.data.Dataset:
        """Convert the downloaded data to a dataset

        Returns:
            tf.data.Dataset: Dataset
        """
        ...

class EurostatEmbeddingTrainer():
    def __init__(self, output_dim: int, dataset: tf.data.Dataset):
        """Initialize the EurostatEmbeddingTrainer class

        Create a model that embeds Eurostat data into a lower-dimensional space

        Args:
            output_dim (int): Output dimension
            dataset (tf.data.Dataset): Eurostat dataset
        """
        ...

    @property
    def model(self) -> tf.keras.Model:
        """The trained model

        Raises:
            ValueError: If the model is not trained
        """
        ...

    def build(self) -> None:
        """Build the model
        """
        ...

    def train(self) -> None:
        """Train the model
        """
        ...

