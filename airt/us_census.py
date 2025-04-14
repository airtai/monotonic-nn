from pathlib import Path
from typing import Optional
import census
import pandas as pd
import tensorflow as tf


class USCensusDataset():
    def __init__(self, download_path: Path, api_key: str):
        """Initialize the USCensusDataset class

        Args:
            download_path (Path): Path to the folder where the data will be downloaded
            api_key (str): API key for the US Census (see https://api.census.gov/data/key_signup.html)
        """
        self.download_path = download_path
        census_api = census.Census(api_key)
    
    def get_data(self, name: str, year: int) -> pd.DataFrame:
        """Get data from US Census
        
        If the doata is downloaded locally, it will be loaded from the local file.
        If the data is not downloaded, it will be downloaded from teh US Census.

        Args:
            name (str): Name of the dataset (e.g. "acs5")
            year (int): Year of the dataset
        """
        ...

    def download_data(self, *, name: Optional[str] = None, year: Optional[int] = None) -> None:
        """Download data from US Census and save it to a folder

        Args:
            name (Optional[str], optional): Name of the dataset (e.g. "acs5"). If None, download all data. Defaults to None.
            year (Optional[int], optional): Year of the dataset. If None, download all data. Defaults to None.
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

class USCensusEmbeddingTrainer():
    def __init__(self, output_dim: int, dataset: tf.data.Dataset):
        """Initialize the USCensusEmbeddingTrainer class

        Create a model that embeds US Census data into a lower-dimensional space

        Args:
            output_dim (int): Output dimension
            dataset (tf.data.Dataset): US Census dataset
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

