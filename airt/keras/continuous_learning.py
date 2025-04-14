from typing import Union

import tensorflow as tf

from airt._components.mono_dense_layer import FraudEstimationModel, RiskEstimationModel

__all__ = ["ContinuousLearning"]

class ContinuousLearning():
    def __init__(self, base_model: Union[FraudEstimationModel, RiskEstimationModel], model_name: str, model_version: str) -> None:
        """Create a ContinuosLearning object

        Args:
            model (Union[FraudEstimationModel, RiskEstimationModel]): Model to build the image from
            model_name (str): Name of the model
            model_version (str): Version of the model (uses semantic versioning)
        """
        self._base_model = base_model
        self._model_name = model_name
        self._model_version = model_version

    def retrain(self, dataset: tf.data.Dataset):
        """Retrain the model

        Args:
            dataset (tf.data.Dataset): Dataset to retrain the model
        """
        pass

    @property
    def model(self) -> Union[FraudEstimationModel, RiskEstimationModel]:
        """Return the retrained model"""
        return self._model