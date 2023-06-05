Constrained Monotonic Neural Networks
================

<!-- WARNING: THIS FILE WAS AUTOGENERATED! DO NOT EDIT! -->

This Python library implements Monotonic Dense Layer as described in
Davor Runje, Sharath M. Shankaranarayana, “Constrained Monotonic Neural
Networks” \[[PDF](https://arxiv.org/pdf/2205.11775.pdf)\].

If you use this library, please cite:

``` title="bibtex"
@inproceedings{runje2023,
  title={Constrained Monotonic Neural Networks},
  author={Davor Runje and Sharath M. Shankaranarayana},
  booktitle={Proceedings of the 40th {International Conference on Machine Learning}},
  year={2023}
}
```

This package contains an implementation of our Monotonic Dense Layer
[`MonoDense`](https://monotonic.airt.ai/latest/api/airt/keras/layers/MonoDense/#airt.keras.layers.MonoDense)
(Constrained Monotonic Fully Connected Layer). Below is the figure from
the paper for reference.

In the code, the variable `monotonicity_indicator` corresponds to **t**
in the figure and parameters `is_convex`, `is_concave` and
`activation_weights` are used to calculate the activation selector **s**
as follows:

- if `is_convex` or `is_concave` is **True**, then the activation
  selector **s** will be (`units`, 0, 0) and (0, `units`, 0),
  respecively.

- if both `is_convex` or `is_concave` is **False**, then the
  `activation_weights` represent ratios between $\breve{s}$, $\hat{s}$
  and $\tilde{s}$, respecively. E.g. if `activation_weights = (2, 2, 1)`
  and `units = 10`, then

$$
(\breve{s}, \hat{s}, \tilde{s}) = (4, 4, 2)
$$

![mono-dense-layer-diagram](https://github.com/airtai/monotonic-nn/raw/main/nbs/images/mono-dense-layer-diagram.png)

## Running in Google Colab

You can start this interactive tutorial in Google Colab by clicking the
button below:

<a href="https://colab.research.google.com/github/airtai/monotonic-nn/blob/main/nbs/index.ipynb" target=”_blank”>
<img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open in Colab" />
</a>

## Install

``` sh
pip install monotonic-nn
```

## How to use

In this example, we’ll assume we have a simple dataset with three inputs
values $x_1$, $x_2$ and $x_3$ sampled from the normal distribution,
while the output value $y$ is calculated according to the following
formula before adding Gaussian noise to it:

$y = x_1^3 + \sin\left(\frac{x_2}{2 \pi}\right) + e^{-x_3}$

<table id="T_37b51">
  <thead>
    <tr>
      <th id="T_37b51_level0_col0" class="col_heading level0 col0" >x0</th>
      <th id="T_37b51_level0_col1" class="col_heading level0 col1" >x1</th>
      <th id="T_37b51_level0_col2" class="col_heading level0 col2" >x2</th>
      <th id="T_37b51_level0_col3" class="col_heading level0 col3" >y</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td id="T_37b51_row0_col0" class="data row0 col0" >0.304717</td>
      <td id="T_37b51_row0_col1" class="data row0 col1" >-1.039984</td>
      <td id="T_37b51_row0_col2" class="data row0 col2" >0.750451</td>
      <td id="T_37b51_row0_col3" class="data row0 col3" >0.234541</td>
    </tr>
    <tr>
      <td id="T_37b51_row1_col0" class="data row1 col0" >0.940565</td>
      <td id="T_37b51_row1_col1" class="data row1 col1" >-1.951035</td>
      <td id="T_37b51_row1_col2" class="data row1 col2" >-1.302180</td>
      <td id="T_37b51_row1_col3" class="data row1 col3" >4.199094</td>
    </tr>
    <tr>
      <td id="T_37b51_row2_col0" class="data row2 col0" >0.127840</td>
      <td id="T_37b51_row2_col1" class="data row2 col1" >-0.316243</td>
      <td id="T_37b51_row2_col2" class="data row2 col2" >-0.016801</td>
      <td id="T_37b51_row2_col3" class="data row2 col3" >0.834086</td>
    </tr>
    <tr>
      <td id="T_37b51_row3_col0" class="data row3 col0" >-0.853044</td>
      <td id="T_37b51_row3_col1" class="data row3 col1" >0.879398</td>
      <td id="T_37b51_row3_col2" class="data row3 col2" >0.777792</td>
      <td id="T_37b51_row3_col3" class="data row3 col3" >-0.093359</td>
    </tr>
    <tr>
      <td id="T_37b51_row4_col0" class="data row4 col0" >0.066031</td>
      <td id="T_37b51_row4_col1" class="data row4 col1" >1.127241</td>
      <td id="T_37b51_row4_col2" class="data row4 col2" >0.467509</td>
      <td id="T_37b51_row4_col3" class="data row4 col3" >0.780875</td>
    </tr>
  </tbody>
</table>

Now, we’ll use the
[`MonoDense`](https://monotonic.airt.ai/latest/api/airt/keras/layers/MonoDense/#airt.keras.layers.MonoDense)
layer instead of `Dense` layer to build a simple monotonic network. By
default, the
[`MonoDense`](https://monotonic.airt.ai/latest/api/airt/keras/layers/MonoDense/#airt.keras.layers.MonoDense)
layer assumes the output of the layer is monotonically increasing with
all inputs. This assumtion is always true for all layers except possibly
the first one. For the first layer, we use `monotonicity_indicator` to
specify which input parameters are monotonic and to specify are they
increasingly or decreasingly monotonic:

- set 1 for increasingly monotonic parameter,

- set -1 for decreasingly monotonic parameter, and

- set 0 otherwise.

In our case, the `monotonicity_indicator` is `[1, 0, -1]` because $y$
is: 

- monotonically increasing w.r.t. $x_1$
$\left(\frac{\partial y}{x_1} = 3 {x_1}^2 \geq 0\right)$, and

- monotonically decreasing w.r.t. $x_3$
  $\left(\frac{\partial y}{x_3} = - e^{-x_2} \leq 0\right)$.

``` python
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Input

from airt.keras.layers import MonoDense

model = Sequential()

model.add(Input(shape=(3,)))
monotonicity_indicator = [1, 0, -1]
model.add(
    MonoDense(128, activation="elu", monotonicity_indicator=monotonicity_indicator)
)
model.add(MonoDense(128, activation="elu"))
model.add(MonoDense(1))

model.summary()
```

    Model: "sequential"
    _________________________________________________________________
     Layer (type)                Output Shape              Param #   
    =================================================================
     mono_dense (MonoDense)      (None, 128)               512       
                                                                     
     mono_dense_1 (MonoDense)    (None, 128)               16512     
                                                                     
     mono_dense_2 (MonoDense)    (None, 1)                 129       
                                                                     
    =================================================================
    Total params: 17,153
    Trainable params: 17,153
    Non-trainable params: 0
    _________________________________________________________________

Now we can train the model as usual using `Model.fit`:

``` python
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.optimizers.schedules import ExponentialDecay

lr_schedule = ExponentialDecay(
    initial_learning_rate=0.01,
    decay_steps=10_000 // 32,
    decay_rate=0.9,
)
optimizer = Adam(learning_rate=lr_schedule)
model.compile(optimizer=optimizer, loss="mse")

model.fit(
    x=x_train, y=y_train, batch_size=32, validation_data=(x_val, y_val), epochs=10
)
```

    Epoch 1/10
    313/313 [==============================] - 3s 5ms/step - loss: 9.4221 - val_loss: 6.1277
    Epoch 2/10
    313/313 [==============================] - 1s 4ms/step - loss: 4.6001 - val_loss: 2.7813
    Epoch 3/10
    313/313 [==============================] - 1s 4ms/step - loss: 1.6221 - val_loss: 2.1111
    Epoch 4/10
    313/313 [==============================] - 1s 4ms/step - loss: 0.9479 - val_loss: 0.2976
    Epoch 5/10
    313/313 [==============================] - 1s 4ms/step - loss: 0.9008 - val_loss: 0.3240
    Epoch 6/10
    313/313 [==============================] - 1s 4ms/step - loss: 0.5027 - val_loss: 0.1455
    Epoch 7/10
    313/313 [==============================] - 1s 4ms/step - loss: 0.4360 - val_loss: 0.1144
    Epoch 8/10
    313/313 [==============================] - 1s 4ms/step - loss: 0.4993 - val_loss: 0.1211
    Epoch 9/10
    313/313 [==============================] - 1s 4ms/step - loss: 0.3162 - val_loss: 1.0021
    Epoch 10/10
    313/313 [==============================] - 1s 4ms/step - loss: 0.2640 - val_loss: 0.2522

    <keras.callbacks.History>

## License

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons Licence" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br />This
work is licensed under a
<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative
Commons Attribution-NonCommercial-ShareAlike 4.0 International
License</a>.

You are free to: - Share — copy and redistribute the material in any
medium or format

- Adapt — remix, transform, and build upon the material

The licensor cannot revoke these freedoms as long as you follow the
license terms.

Under the following terms: - Attribution — You must give appropriate
credit, provide a link to the license, and indicate if changes were
made. You may do so in any reasonable manner, but not in any way that
suggests the licensor endorses you or your use.

- NonCommercial — You may not use the material for commercial purposes.

- ShareAlike — If you remix, transform, or build upon the material, you
  must distribute your contributions under the same license as the
  original.

- No additional restrictions — You may not apply legal terms or
  technological measures that legally restrict others from doing
  anything the license permits.
