
from typing import Union
from .keras.layers import FraudEstimationModel, RiskEstimationModel

class DockerBuilder:
    """Docker builder class
    
    Creates a docker image from a Dockerfile and pushes it to a registry. It is based on TensorFlow's Serving docker image.

    """
    def __init__(self, *, base_image_name: str = "tensorflow/serving", tag="latest", registry="docker.io", model: Union[FraudEstimationModel, RiskEstimationModel], model_name: str, model_version: str) -> None:
        """Create a DockerBuilder object

        Args:
            base_image_name (str, optional): Name of the image. Defaults to "tensorflow/serving".
            tag (str, optional): Tag of the image. Defaults to "latest".
            registry (str, optional): Registry to push the image to. Defaults to "docker.io".
            model (Union[FraudEstimationModel, RiskEstimationModel]): Model to build the image from
            model_name (str): Name of the model
            model_version (str): Version of the model (uses semantic versioning)
        """
        pass

    def build(self) -> None:
        """Build a docker image from a model
        """
        pass

