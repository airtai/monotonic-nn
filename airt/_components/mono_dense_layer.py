# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/MonoDenseLayer.ipynb.

# %% auto 0
__all__ = ['T', 'get_saturated_activation', 'get_activation_functions', 'apply_activations', 'get_monotonicity_indicator',
           'apply_monotonicity_indicator_to_kernel', 'replace_kernel_using_monotonicity_indicator', 'MonoDense',
           'CDFHead']

# %% ../../nbs/MonoDenseLayer.ipynb 3
from contextlib import contextmanager
from datetime import datetime
from functools import lru_cache
from typing import *

import numpy as np
import tensorflow as tf
from numpy.typing import ArrayLike, NDArray
from tensorflow.keras.layers import Concatenate, Dense, Dropout
from tensorflow.types.experimental import TensorLike

from .helpers import export

# %% ../../nbs/MonoDenseLayer.ipynb 9
def get_saturated_activation(
    convex_activation: Callable[[TensorLike], TensorLike],
    concave_activation: Callable[[TensorLike], TensorLike],
    a: float = 1.0,
    c: float = 1.0,
) -> Callable[[TensorLike], TensorLike]:
    @tf.function
    def saturated_activation(
        x: TensorLike,
        convex_activation: Callable[[TensorLike], TensorLike] = convex_activation,
        concave_activation: Callable[[TensorLike], TensorLike] = concave_activation,
        a: float = a,
        c: float = c,
    ) -> TensorLike:
        cc = convex_activation(tf.ones_like(x) * c)
        ccc = concave_activation(-tf.ones_like(x) * c)
        return a * tf.where(
            x <= 0,
            convex_activation(x + c) - cc,
            concave_activation(x - c) + cc,
        )

    return saturated_activation  # type: ignore


@lru_cache
def get_activation_functions(
    activation: Optional[Union[str, Callable[[TensorLike], TensorLike]]] = None,
) -> Tuple[
    Callable[[TensorLike], TensorLike],
    Callable[[TensorLike], TensorLike],
    Callable[[TensorLike], TensorLike],
]:
    convex_activation = tf.keras.activations.get(
        activation.lower() if isinstance(activation, str) else activation
    )

    @tf.function
    def concave_activation(x: TensorLike) -> TensorLike:
        return -convex_activation(-x)

    saturated_activation = get_saturated_activation(
        convex_activation, concave_activation
    )
    return convex_activation, concave_activation, saturated_activation

# %% ../../nbs/MonoDenseLayer.ipynb 13
@tf.function
def apply_activations(
    x: TensorLike,
    *,
    units: int,
    convex_activation: Callable[[TensorLike], TensorLike],
    concave_activation: Callable[[TensorLike], TensorLike],
    saturated_activation: Callable[[TensorLike], TensorLike],
    is_convex: bool = False,
    is_concave: bool = False,
    activation_weights: Tuple[float, float, float] = (7.0, 7.0, 2.0),
) -> TensorLike:
    if convex_activation is None:
        return x

    elif is_convex:
        normalized_activation_weights = np.array([1.0, 0.0, 0.0])
    elif is_concave:
        normalized_activation_weights = np.array([0.0, 1.0, 0.0])
    else:
        if len(activation_weights) != 3:
            raise ValueError(f"activation_weights={activation_weights}")
        if (np.array(activation_weights) < 0).any():
            raise ValueError(f"activation_weights={activation_weights}")
        normalized_activation_weights = np.array(activation_weights) / sum(
            activation_weights
        )

    s_convex = round(normalized_activation_weights[0] * units)
    s_concave = round(normalized_activation_weights[1] * units)
    s_saturated = units - s_convex - s_concave

    x_convex, x_concave, x_saturated = tf.split(
        x, (s_convex, s_concave, s_saturated), axis=-1
    )

    y_convex = convex_activation(x_convex)
    y_concave = concave_activation(x_concave)
    y_saturated = saturated_activation(x_saturated)

    y = tf.concat([y_convex, y_concave, y_saturated], axis=-1)

    return y

# %% ../../nbs/MonoDenseLayer.ipynb 17
def get_monotonicity_indicator(
    monotonicity_indicator: ArrayLike,
    *,
    input_shape: Tuple[int, ...],
    units: int,
) -> TensorLike:
    # convert to tensor if needed and make it broadcastable to the kernel
    monotonicity_indicator = np.array(monotonicity_indicator)
    if len(monotonicity_indicator.shape) < 2:
        monotonicity_indicator = np.reshape(monotonicity_indicator, (-1, 1))
    elif len(monotonicity_indicator.shape) > 2:
        raise ValueError(
            f"monotonicity_indicator has rank greater than 2: {monotonicity_indicator.shape}"
        )

    monotonicity_indicator_broadcasted = np.broadcast_to(
        monotonicity_indicator, shape=(input_shape[-1], units)
    )

    if not np.all(
        (monotonicity_indicator == -1)
        | (monotonicity_indicator == 0)
        | (monotonicity_indicator == 1)
    ):
        raise ValueError(
            f"Each element of monotonicity_indicator must be one of -1, 0, 1, but it is: '{monotonicity_indicator}'"
        )
    return monotonicity_indicator

# %% ../../nbs/MonoDenseLayer.ipynb 21
def apply_monotonicity_indicator_to_kernel(
    kernel: tf.Variable,
    monotonicity_indicator: ArrayLike,
) -> TensorLike:
    # convert to tensor if needed and make it broadcastable to the kernel
    monotonicity_indicator = tf.convert_to_tensor(monotonicity_indicator)

    # absolute value of the kernel
    abs_kernel = tf.abs(kernel)

    # replace original kernel values for positive or negative ones where needed
    xs = tf.where(
        monotonicity_indicator == 1,
        abs_kernel,
        kernel,
    )
    xs = tf.where(monotonicity_indicator == -1, -abs_kernel, xs)

    return xs


@contextmanager
def replace_kernel_using_monotonicity_indicator(
    layer: tf.keras.layers.Dense,
    monotonicity_indicator: TensorLike,
) -> Generator[None, None, None]:
    old_kernel = layer.kernel

    layer.kernel = apply_monotonicity_indicator_to_kernel(
        layer.kernel, monotonicity_indicator
    )
    try:
        yield
    finally:
        layer.kernel = old_kernel

# %% ../../nbs/MonoDenseLayer.ipynb 28
@export
class MonoDense(Dense):
    """Monotonic counterpart of the regular Dense Layer of tf.keras

    This is an implementation of our Monotonic Dense Unit or Constrained Monotone Fully Connected Layer. The below is the figure from the paper for reference.

    - the parameter `monotonicity_indicator` corresponds to **t** in the figure below, and

    - parameters `is_convex`, `is_concave` and `activation_weights` are used to calculate the activation selector **s** as follows:

        - if `is_convex` or `is_concave` is **True**, then the activation selector **s** will be (`units`, 0, 0) and (0, `units`, 0), respecively.

        - if both  `is_convex` or `is_concave` is **False**, then the `activation_weights` represent ratios between $\\breve{s}$, $\\hat{s}$ and $\\tilde{s}$,
          respecively. E.g. if `activation_weights = (2, 2, 1)` and `units = 10`, then

    $$
    (\\breve{s}, \\hat{s}, \\tilde{s}) = (4, 4, 2)
    $$

    ![mono-dense-layer-diagram.png](../../../../../images/nbs/images/mono-dense-layer-diagram.png)

    """

    def __init__(
        self,
        units: int,
        *,
        activation: Optional[Union[str, Callable[[TensorLike], TensorLike]]] = None,
        monotonicity_indicator: ArrayLike = 1,
        is_convex: bool = False,
        is_concave: bool = False,
        activation_weights: Tuple[float, float, float] = (7.0, 7.0, 2.0),
        **kwargs: Any,
    ):
        """Constructs a new MonoDense instance.

        Params:
            units: Positive integer, dimensionality of the output space.
            activation: Activation function to use, it is assumed to be convex monotonically
                increasing function such as "relu" or "elu"
            monotonicity_indicator: Vector to indicate which of the inputs are monotonically increasing or
                monotonically decreasing or non-monotonic. Has value 1 for monotonically increasing,
                -1 for monotonically decreasing and 0 for non-monotonic.
            is_convex: convex if set to True
            is_concave: concave if set to True
            activation_weights: relative weights for each type of activation, the default is (1.0, 1.0, 1.0).
                Ignored if is_convex or is_concave is set to True
            **kwargs: passed as kwargs to the constructor of `Dense`

        Raise:
            ValueError:
                - if both **is_concave** and **is_convex** are set to **True**, or
                - if any component of activation_weights is negative or there is not exactly three components
        """
        if is_convex and is_concave:
            raise ValueError(
                "The model cannot be set to be both convex and concave (only linear functions are both)."
            )

        if len(activation_weights) != 3:
            raise ValueError(
                f"There must be exactly three components of activation_weights, but we have this instead: {activation_weights}."
            )

        if (np.array(activation_weights) < 0).any():
            raise ValueError(
                f"Values of activation_weights must be non-negative, but we have this instead: {activation_weights}."
            )

        super(MonoDense, self).__init__(units=units, activation=None, **kwargs)

        self.units = units
        self.org_activation = activation
        self.monotonicity_indicator = monotonicity_indicator
        self.is_convex = is_convex
        self.is_concave = is_concave
        self.activation_weights = activation_weights

        (
            self.convex_activation,
            self.concave_activation,
            self.saturated_activation,
        ) = get_activation_functions(self.org_activation)

    def get_config(self) -> Dict[str, Any]:
        """Get config is used for saving the model"""
        return dict(
            units=self.units,
            activation=self.org_activation,
            monotonicity_indicator=self.monotonicity_indicator,
            is_convex=self.is_convex,
            is_concave=self.is_concave,
            activation_weights=self.activation_weights,
        )

    def build(self, input_shape: Tuple, *args: List[Any], **kwargs: Any) -> None:
        """Build

        Args:
            input_shape: input tensor
            args: positional arguments passed to Dense.build()
            kwargs: keyword arguments passed to Dense.build()
        """
        super(MonoDense, self).build(input_shape, *args, **kwargs)
        self.monotonicity_indicator = get_monotonicity_indicator(
            monotonicity_indicator=self.monotonicity_indicator,
            input_shape=input_shape,
            units=self.units,
        )

    def call(self, inputs: TensorLike) -> TensorLike:
        """Call

        Args:
            inputs: input tensor of shape (batch_size, ..., x_length)

        Returns:
            N-D tensor with shape: `(batch_size, ..., units)`.

        """
        # calculate W'*x+y after we replace the kernal according to monotonicity vector
        with replace_kernel_using_monotonicity_indicator(
            self, monotonicity_indicator=self.monotonicity_indicator
        ):
            h = super(MonoDense, self).call(inputs)

        y = apply_activations(
            h,
            units=self.units,
            convex_activation=self.convex_activation,
            concave_activation=self.concave_activation,
            saturated_activation=self.saturated_activation,
            is_convex=self.is_convex,
            is_concave=self.is_concave,
            activation_weights=self.activation_weights,
        )

        return y

    @classmethod
    def create_type_1(
        cls,
        inputs: Union[TensorLike, Dict[str, TensorLike], List[TensorLike]],
        *,
        units: int,
        final_units: int,
        activation: Union[str, Callable[[TensorLike], TensorLike]],
        n_layers: int,
        final_activation: Optional[
            Union[str, Callable[[TensorLike], TensorLike]]
        ] = None,
        monotonicity_indicator: Union[int, Dict[str, int], List[int]] = 1,
        is_convex: Union[bool, Dict[str, bool], List[bool]] = False,
        is_concave: Union[bool, Dict[str, bool], List[bool]] = False,
        dropout: Optional[float] = None,
    ) -> TensorLike:
        """Builds Type-1 monotonic network

        Type-1 architecture corresponds to the standard MLP type of neural network architecture used in general, where each
        of the input features is concatenated to form one single input feature vector $\mathbf{x}$ and fed into the network,
        with the only difference being that instead of standard fully connected or dense layers, we employ monotonic dense units
        throughout. For the first (or input layer) layer, the indicator vector $\mathbf{t}$, is used to identify the monotonicity
        property of the input feature with respect to the output. Specifically, $\mathbf{t}$ is set to $1$ for those components
        in the input feature vector that are monotonically increasing and is set to $-1$ for those components that are monotonically
        decreasing and set to $0$ if the feature is non-monotonic. For the subsequent hidden layers, monotonic dense units with the
        indicator vector $\mathbf{t}$ always being set to $1$ are used in order to preserve monotonicity. Finally, depending on
        whether the problem at hand is a regression problem or a classification problem (or even a multi-task problem), an appropriate
        activation function (such as linear activation or sigmoid or softmax) to obtain the final output.

        ![mono-dense-layer-diagram.png](../../../images/nbs/images/type-1.png)

        Args:
            inputs: input tensor or a dictionary of tensors
            units: number of units in hidden layers
            final_units: number of units in the output layer
            activation: the base activation function
            n_layers: total number of layers (hidden layers plus the output layer)
            final_activation: the activation function of the final layer (typicall softmax, sigmoid or linear).
                If set to None (default value), then the linear activation is used.
            monotonicity_indicator: if an instance of dictionary, then maps names of input feature to their monotonicity
                indicator (-1 for monotonically decreasing, 1 for monotonically increasing and 0 otherwise). If int,
                then all input features are set to the same monotinicity indicator.
            is_convex: set to True if a particular input feature is convex
            is_concave: set to True if a particular inputs feature is concave
            dropout: dropout rate. If set to float greater than 0, Dropout layers are inserted after hidden layers.

        Returns:
            Output tensor

        """
        return _create_type_1(
            inputs,
            units=units,
            final_units=final_units,
            activation=activation,
            n_layers=n_layers,
            final_activation=final_activation,
            monotonicity_indicator=monotonicity_indicator,
            is_convex=is_convex,
            is_concave=is_concave,
            dropout=dropout,
        )

    @classmethod
    def create_type_2(
        cls,
        inputs: Union[TensorLike, Dict[str, TensorLike], List[TensorLike]],
        *,
        input_units: Optional[int] = None,
        units: int,
        final_units: int,
        activation: Union[str, Callable[[TensorLike], TensorLike]],
        n_layers: int,
        final_activation: Optional[
            Union[str, Callable[[TensorLike], TensorLike]]
        ] = None,
        monotonicity_indicator: Union[int, Dict[str, int], List[int]] = 1,
        is_convex: Union[bool, Dict[str, bool], List[bool]] = False,
        is_concave: Union[bool, Dict[str, bool], List[bool]] = False,
        dropout: Optional[float] = None,
    ) -> TensorLike:
        """Builds Type-2 monotonic network

        Type-2 architecture is another example of a neural network architecture that can be built employing proposed
        monotonic dense blocks. The difference when compared to the architecture described above lies in the way input
        features are fed into the hidden layers of neural network architecture. Instead of concatenating the features
        directly, this architecture provides flexibility to employ any form of complex feature extractors for the
        non-monotonic features and use the extracted feature vectors as inputs. Another difference is that each monotonic
        input is passed through separate monotonic dense units. This provides an advantage since depending on whether the
        input is completely concave or convex or both, we can adjust the activation selection vector $\mathbf{s}$ appropriately
        along with an appropriate value for the indicator vector $\mathbf{t}$. Thus, each of the monotonic input features has
        a separate monotonic dense layer associated with it. Thus as the major difference to the above-mentioned architecture,
        we concatenate the feature vectors instead of concatenating the inputs directly. The subsequent parts of the network are
        similar to the architecture described above wherein for the rest of the hidden monotonic dense units, the indicator vector
        $\mathbf{t}$ is always set to $1$ to preserve monotonicity.

        ![mono-dense-layer-diagram.png](../../../images/nbs/images/type-2.png)

        Args:
            inputs: input tensor or a dictionary of tensors
            input_units: used to preprocess features before entering the common mono block
            units: number of units in hidden layers
            final_units: number of units in the output layer
            activation: the base activation function
            n_layers: total number of layers (hidden layers plus the output layer)
            final_activation: the activation function of the final layer (typicall softmax, sigmoid or linear).
                If set to None (default value), then the linear activation is used.
            monotonicity_indicator: if an instance of dictionary, then maps names of input feature to their monotonicity
                indicator (-1 for monotonically decreasing, 1 for monotonically increasing and 0 otherwise). If int,
                then all input features are set to the same monotinicity indicator.
            is_convex: set to True if a particular input feature is convex
            is_concave: set to True if a particular inputs feature is concave
            dropout: dropout rate. If set to float greater than 0, Dropout layers are inserted after hidden layers.

        Returns:
            Output tensor

        """
        return _create_type_2(
            inputs,
            input_units=input_units,
            units=units,
            final_units=final_units,
            activation=activation,
            n_layers=n_layers,
            final_activation=final_activation,
            monotonicity_indicator=monotonicity_indicator,
            is_convex=is_convex,
            is_concave=is_concave,
            dropout=dropout,
        )

# %% ../../nbs/MonoDenseLayer.ipynb 33
def _create_mono_block(
    *,
    units: List[int],
    activation: Union[str, Callable[[TensorLike], TensorLike]],
    monotonicity_indicator: TensorLike = 1,
    is_convex: bool = False,
    is_concave: bool = False,
    dropout: Optional[float] = None,
) -> Callable[[TensorLike], TensorLike]:
    def create_mono_block_inner(
        x: TensorLike,
        *,
        units: List[int] = units,
        activation: Union[str, Callable[[TensorLike], TensorLike]] = activation,
        monotonicity_indicator: TensorLike = monotonicity_indicator,
        is_convex: bool = is_convex,
        is_concave: bool = is_concave,
    ) -> TensorLike:
        if len(units) == 0:
            return x

        y = x
        for i in range(len(units)):
            y = MonoDense(
                units=units[i],
                activation=activation if i < len(units) - 1 else None,
                monotonicity_indicator=monotonicity_indicator if i == 0 else 1,
                is_convex=is_convex,
                is_concave=is_concave,
                name=f"mono_dense_{i}"
                + ("_increasing" if i != 0 else "")
                + ("_convex" if is_convex else "")
                + ("_concave" if is_concave else ""),
            )(y)
            if (i < len(units) - 1) and dropout:
                y = Dropout(dropout)(y)

        return y

    return create_mono_block_inner

# %% ../../nbs/MonoDenseLayer.ipynb 35
T = TypeVar("T")


def _prepare_mono_input_n_param(
    inputs: Union[TensorLike, Dict[str, TensorLike], List[TensorLike]],
    param: Union[T, Dict[str, T], List[T]],
) -> Tuple[List[TensorLike], List[T], List[str]]:
    if isinstance(inputs, list):
        if isinstance(param, int):
            param = [param] * len(inputs)  # type: ignore
        elif isinstance(param, list):
            if len(inputs) != len(param):
                raise ValueError(f"{len(inputs)} != {len(param)}")
        else:
            raise ValueError(f"Uncompatible types: {type(inputs)=}, {type(param)=}")
        sorted_feature_names = [f"{i}" for i in range(len(inputs))]

    elif isinstance(inputs, dict):
        sorted_feature_names = sorted(inputs.keys())

        if isinstance(param, int):
            param = [param] * len(inputs)  # type: ignore
        elif isinstance(param, dict):
            if set(param.keys()) != set(sorted_feature_names):
                raise ValueError(f"{set(param.keys())} != {set(sorted_feature_names)}")
            else:
                param = [param[k] for k in sorted_feature_names]
        else:
            raise ValueError(f"Uncompatible types: {type(inputs)=}, {type(param)=}")

        inputs = [inputs[k] for k in sorted_feature_names]

    else:
        if not isinstance(param, int):
            raise ValueError(f"Uncompatible types: {type(inputs)=}, {type(param)=}")
        inputs = [inputs]
        param = [param]  # type: ignore
        sorted_feature_names = ["inputs"]

    return inputs, param, sorted_feature_names

# %% ../../nbs/MonoDenseLayer.ipynb 43
def _check_convexity_params(
    monotonicity_indicator: List[int],
    is_convex: List[bool],
    is_concave: List[bool],
    names: List[str],
) -> Tuple[bool, bool]:
    ix = [
        i for i in range(len(monotonicity_indicator)) if is_convex[i] and is_concave[i]
    ]

    if len(ix) > 0:
        raise ValueError(
            f"Parameters both convex and concave: {[names[i] for i in ix]}"
        )

    has_convex = any(is_convex)
    has_concave = any(is_concave)
    if has_convex and has_concave:
        print("WARNING: we have both convex and concave parameters")

    return has_convex, has_concave

# %% ../../nbs/MonoDenseLayer.ipynb 46
@export
def _create_type_1(
    inputs: Union[TensorLike, Dict[str, TensorLike], List[TensorLike]],
    *,
    units: int,
    final_units: int,
    activation: Union[str, Callable[[TensorLike], TensorLike]],
    n_layers: int,
    final_activation: Optional[Union[str, Callable[[TensorLike], TensorLike]]] = None,
    monotonicity_indicator: Union[int, Dict[str, int], List[int]] = 1,
    is_convex: Union[bool, Dict[str, bool], List[bool]] = False,
    is_concave: Union[bool, Dict[str, bool], List[bool]] = False,
    dropout: Optional[float] = None,
) -> TensorLike:
    """Builds Type-1 monotonic network

    Type-1 architecture corresponds to the standard MLP type of neural network architecture used in general, where each
    of the input features is concatenated to form one single input feature vector $\mathbf{x}$ and fed into the network,
    with the only difference being that instead of standard fully connected or dense layers, we employ monotonic dense units
    throughout. For the first (or input layer) layer, the indicator vector $\mathbf{t}$, is used to identify the monotonicity
    property of the input feature with respect to the output. Specifically, $\mathbf{t}$ is set to $1$ for those components
    in the input feature vector that are monotonically increasing and is set to $-1$ for those components that are monotonically
    decreasing and set to $0$ if the feature is non-monotonic. For the subsequent hidden layers, monotonic dense units with the
    indicator vector $\mathbf{t}$ always being set to $1$ are used in order to preserve monotonicity. Finally, depending on
    whether the problem at hand is a regression problem or a classification problem (or even a multi-task problem), an appropriate
    activation function (such as linear activation or sigmoid or softmax) to obtain the final output.

    ![mono-dense-layer-diagram.png](../../../images/nbs/images/type-1.png)

    Args:
        inputs: input tensor or a dictionary of tensors
        units: number of units in hidden layers
        final_units: number of units in the output layer
        activation: the base activation function
        n_layers: total number of layers (hidden layers plus the output layer)
        final_activation: the activation function of the final layer (typicall softmax, sigmoid or linear).
            If set to None (default value), then the linear activation is used.
        monotonicity_indicator: if an instance of dictionary, then maps names of input feature to their monotonicity
            indicator (-1 for monotonically decreasing, 1 for monotonically increasing and 0 otherwise). If int,
            then all input features are set to the same monotinicity indicator.
        is_convex: set to True if a particular input feature is convex
        is_concave: set to True if a particular inputs feature is concave
        dropout: dropout rate. If set to float greater than 0, Dropout layers are inserted after hidden layers.

    Returns:
        Output tensor

    """
    _, is_convex, _ = _prepare_mono_input_n_param(inputs, is_convex)
    _, is_concave, _ = _prepare_mono_input_n_param(inputs, is_concave)
    x, monotonicity_indicator, names = _prepare_mono_input_n_param(
        inputs, monotonicity_indicator
    )
    has_convex, has_concave = _check_convexity_params(
        monotonicity_indicator, is_convex, is_concave, names
    )

    y = tf.keras.layers.Concatenate()(x)

    y = _create_mono_block(
        units=[units] * (n_layers - 1) + [final_units],
        activation=activation,
        monotonicity_indicator=monotonicity_indicator,
        is_convex=has_convex,
        is_concave=has_concave and not has_convex,
        dropout=dropout,
    )(y)

    if final_activation is not None:
        y = tf.keras.activations.get(final_activation)(y)

    return y

# %% ../../nbs/MonoDenseLayer.ipynb 50
@export
def _create_type_2(
    inputs: Union[TensorLike, Dict[str, TensorLike], List[TensorLike]],
    *,
    input_units: Optional[int] = None,
    units: int,
    final_units: int,
    activation: Union[str, Callable[[TensorLike], TensorLike]],
    n_layers: int,
    final_activation: Optional[Union[str, Callable[[TensorLike], TensorLike]]] = None,
    monotonicity_indicator: Union[int, Dict[str, int], List[int]] = 1,
    is_convex: Union[bool, Dict[str, bool], List[bool]] = False,
    is_concave: Union[bool, Dict[str, bool], List[bool]] = False,
    dropout: Optional[float] = None,
) -> TensorLike:
    """Builds Type-2 monotonic network

    Type-2 architecture is another example of a neural network architecture that can be built employing proposed
    monotonic dense blocks. The difference when compared to the architecture described above lies in the way input
    features are fed into the hidden layers of neural network architecture. Instead of concatenating the features
    directly, this architecture provides flexibility to employ any form of complex feature extractors for the
    non-monotonic features and use the extracted feature vectors as inputs. Another difference is that each monotonic
    input is passed through separate monotonic dense units. This provides an advantage since depending on whether the
    input is completely concave or convex or both, we can adjust the activation selection vector $\mathbf{s}$ appropriately
    along with an appropriate value for the indicator vector $\mathbf{t}$. Thus, each of the monotonic input features has
    a separate monotonic dense layer associated with it. Thus as the major difference to the above-mentioned architecture,
    we concatenate the feature vectors instead of concatenating the inputs directly. The subsequent parts of the network are
    similar to the architecture described above wherein for the rest of the hidden monotonic dense units, the indicator vector
    $\mathbf{t}$ is always set to $1$ to preserve monotonicity.

    ![mono-dense-layer-diagram.png](../../../images/nbs/images/type-2.png)

    Args:
        inputs: input tensor or a dictionary of tensors
        input_units: used to preprocess features before entering the common mono block
        units: number of units in hidden layers
        final_units: number of units in the output layer
        activation: the base activation function
        n_layers: total number of layers (hidden layers plus the output layer)
        final_activation: the activation function of the final layer (typicall softmax, sigmoid or linear).
            If set to None (default value), then the linear activation is used.
        monotonicity_indicator: if an instance of dictionary, then maps names of input feature to their monotonicity
            indicator (-1 for monotonically decreasing, 1 for monotonically increasing and 0 otherwise). If int,
            then all input features are set to the same monotinicity indicator.
        is_convex: set to True if a particular input feature is convex
        is_concave: set to True if a particular inputs feature is concave
        dropout: dropout rate. If set to float greater than 0, Dropout layers are inserted after hidden layers.

    Returns:
        Output tensor

    """
    _, is_convex, _ = _prepare_mono_input_n_param(inputs, is_convex)
    _, is_concave, _ = _prepare_mono_input_n_param(inputs, is_concave)
    x, monotonicity_indicator, names = _prepare_mono_input_n_param(
        inputs, monotonicity_indicator
    )
    has_convex, has_concave = _check_convexity_params(
        monotonicity_indicator, is_convex, is_concave, names
    )

    if input_units is None:
        input_units = max(units // 4, 1)

    y = [
        (
            MonoDense(
                units=input_units,
                activation=activation,
                monotonicity_indicator=monotonicity_indicator[i],
                is_convex=is_convex[i],
                is_concave=is_concave[i],
                name=f"mono_dense_{names[i]}"
                + ("_increasing" if monotonicity_indicator[i] == 1 else "_decreasing")
                + ("_convex" if is_convex[i] else "")
                + ("_concave" if is_concave[i] else ""),
            )
            if monotonicity_indicator[i] != 0
            else (
                Dense(
                    units=input_units, activation=activation, name=f"dense_{names[i]}"
                )
            )
        )(x[i])
        for i in range(len(inputs))
    ]

    y = Concatenate(name="preprocessed_features")(y)
    monotonicity_indicator_block: List[int] = sum(
        [[abs(x)] * input_units for x in monotonicity_indicator], []
    )

    y = _create_mono_block(
        units=[units] * (n_layers - 1) + [final_units],
        activation=activation,
        monotonicity_indicator=monotonicity_indicator_block,
        is_convex=has_convex,
        is_concave=has_concave and not has_convex,
        dropout=dropout,
    )(y)

    if final_activation is not None:
        y = tf.keras.activations.get(final_activation)(y)

    return y

# %% ../../nbs/MonoDenseLayer.ipynb 52
from keras.layers import Layer

# Optimizacija CDFHead modula s novim izračunom gubitka mreže koristeći dinamički uzrokovane vremenske trenutke na razini grupe (batch) kao dinamičke granice diskretnih grupa. Ova metoda će dodatno ubrzati treniranje modela uz očuvanje točnosti modela kao i kod trenutne implementacije koja koristi gradijent CDF-a da bi izračunala PDF i vjerojatnosti danih događaja.


@export
class CDFHead(Layer):
    """Continuos Distribution Function (CDF) Head

    This is an implementation of the Continuos Distribution Function (CDF) Head. It uses dynamically sampled time points
    at batch level as dynamic boundaries of discrete groups. This method speeds up the training of the model while preserving
    the accuracy of the model as in the current implementation that uses the CDF gradient to compute the PDF and probabilities
    of given events.


    """

    def __init__(
        self,
        **kwargs: Any,
    ):
        """Constructs a new CDFHead instance.

        This is an implementation of the Continuos Distribution Function (CDF) Head. It uses dynamically sampled time points
        at batch level as dynamic boundaries of discrete groups. This method speeds up the training of the model while preserving
        the accuracy of the model as in the current implementation that uses the CDF gradient to compute the PDF and probabilities
        of given events.


        Args:
            **kwargs: passed as kwargs to the constructor of `Layer`

        """
        super(CDFHead, self).__init__(**kwargs)
