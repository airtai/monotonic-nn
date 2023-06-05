Loan
================

<!-- WARNING: THIS FILE WAS AUTOGENERATED! DO NOT EDIT! -->

Lending club loan *data* contains complete loan data for all loans
issued through 2007-2015 of several banks. Each data point is a
28-dimensional feature including the current loan status, latest payment
information, and other additional features. The task is to predict loan
defaulters given the feature vector. The possibility of loan default
should be nondecreasing w.r.t. number of public record bankruptcies,
Debt-to-Income ratio, and non-increasing w.r.t. credit score, length of
employment, annual income. Thus the `monotonicity_indicator`
corrsponding to these features are set to 1.

References:

1.  https://www.kaggle.com/wendykan/lending-club-loan-data (Note:
    Currently, the dataset seems to be withdrawn from kaggle)

``` python
monotonicity_indicator = {
    f"feature_{i}": mi for i, mi in enumerate([-1, 1, -1, -1, 1] + [0] * 23)
}
```

## Running in Google Colab

<a href="https://colab.research.google.com/github/airtai/monotonic-nn/blob/main/nbs/experiments/Loan.ipynb" target=”_blank”>
<img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open in Colab" />
</a>

These are a few examples of the dataset:

<style type="text/css">
</style>
<table id="T_5f5bc">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_5f5bc_level0_col0" class="col_heading level0 col0" >0</th>
      <th id="T_5f5bc_level0_col1" class="col_heading level0 col1" >1</th>
      <th id="T_5f5bc_level0_col2" class="col_heading level0 col2" >2</th>
      <th id="T_5f5bc_level0_col3" class="col_heading level0 col3" >3</th>
      <th id="T_5f5bc_level0_col4" class="col_heading level0 col4" >4</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_5f5bc_level0_row0" class="row_heading level0 row0" >feature_0</th>
      <td id="T_5f5bc_row0_col0" class="data row0 col0" >0.833333</td>
      <td id="T_5f5bc_row0_col1" class="data row0 col1" >1.000000</td>
      <td id="T_5f5bc_row0_col2" class="data row0 col2" >0.666667</td>
      <td id="T_5f5bc_row0_col3" class="data row0 col3" >0.333333</td>
      <td id="T_5f5bc_row0_col4" class="data row0 col4" >0.666667</td>
    </tr>
    <tr>
      <th id="T_5f5bc_level0_row1" class="row_heading level0 row1" >feature_1</th>
      <td id="T_5f5bc_row1_col0" class="data row1 col0" >0.000000</td>
      <td id="T_5f5bc_row1_col1" class="data row1 col1" >0.000000</td>
      <td id="T_5f5bc_row1_col2" class="data row1 col2" >0.000000</td>
      <td id="T_5f5bc_row1_col3" class="data row1 col3" >0.000000</td>
      <td id="T_5f5bc_row1_col4" class="data row1 col4" >0.000000</td>
    </tr>
    <tr>
      <th id="T_5f5bc_level0_row2" class="row_heading level0 row2" >feature_2</th>
      <td id="T_5f5bc_row2_col0" class="data row2 col0" >0.400000</td>
      <td id="T_5f5bc_row2_col1" class="data row2 col1" >1.000000</td>
      <td id="T_5f5bc_row2_col2" class="data row2 col2" >0.800000</td>
      <td id="T_5f5bc_row2_col3" class="data row2 col3" >0.500000</td>
      <td id="T_5f5bc_row2_col4" class="data row2 col4" >0.700000</td>
    </tr>
    <tr>
      <th id="T_5f5bc_level0_row3" class="row_heading level0 row3" >feature_3</th>
      <td id="T_5f5bc_row3_col0" class="data row3 col0" >0.005263</td>
      <td id="T_5f5bc_row3_col1" class="data row3 col1" >0.003474</td>
      <td id="T_5f5bc_row3_col2" class="data row3 col2" >0.005263</td>
      <td id="T_5f5bc_row3_col3" class="data row3 col3" >0.007158</td>
      <td id="T_5f5bc_row3_col4" class="data row3 col4" >0.006842</td>
    </tr>
    <tr>
      <th id="T_5f5bc_level0_row4" class="row_heading level0 row4" >feature_4</th>
      <td id="T_5f5bc_row4_col0" class="data row4 col0" >0.005185</td>
      <td id="T_5f5bc_row4_col1" class="data row4 col1" >0.023804</td>
      <td id="T_5f5bc_row4_col2" class="data row4 col2" >0.029700</td>
      <td id="T_5f5bc_row4_col3" class="data row4 col3" >0.024434</td>
      <td id="T_5f5bc_row4_col4" class="data row4 col4" >0.021962</td>
    </tr>
    <tr>
      <th id="T_5f5bc_level0_row5" class="row_heading level0 row5" >feature_5</th>
      <td id="T_5f5bc_row5_col0" class="data row5 col0" >0.185751</td>
      <td id="T_5f5bc_row5_col1" class="data row5 col1" >0.134860</td>
      <td id="T_5f5bc_row5_col2" class="data row5 col2" >0.236641</td>
      <td id="T_5f5bc_row5_col3" class="data row5 col3" >0.745547</td>
      <td id="T_5f5bc_row5_col4" class="data row5 col4" >0.440204</td>
    </tr>
    <tr>
      <th id="T_5f5bc_level0_row6" class="row_heading level0 row6" >feature_6</th>
      <td id="T_5f5bc_row6_col0" class="data row6 col0" >0.240654</td>
      <td id="T_5f5bc_row6_col1" class="data row6 col1" >0.036215</td>
      <td id="T_5f5bc_row6_col2" class="data row6 col2" >0.271807</td>
      <td id="T_5f5bc_row6_col3" class="data row6 col3" >0.778037</td>
      <td id="T_5f5bc_row6_col4" class="data row6 col4" >0.260125</td>
    </tr>
    <tr>
      <th id="T_5f5bc_level0_row7" class="row_heading level0 row7" >feature_7</th>
      <td id="T_5f5bc_row7_col0" class="data row7 col0" >0.000000</td>
      <td id="T_5f5bc_row7_col1" class="data row7 col1" >0.000000</td>
      <td id="T_5f5bc_row7_col2" class="data row7 col2" >0.000000</td>
      <td id="T_5f5bc_row7_col3" class="data row7 col3" >1.000000</td>
      <td id="T_5f5bc_row7_col4" class="data row7 col4" >0.000000</td>
    </tr>
    <tr>
      <th id="T_5f5bc_level0_row8" class="row_heading level0 row8" >feature_8</th>
      <td id="T_5f5bc_row8_col0" class="data row8 col0" >0.000000</td>
      <td id="T_5f5bc_row8_col1" class="data row8 col1" >0.000000</td>
      <td id="T_5f5bc_row8_col2" class="data row8 col2" >0.000000</td>
      <td id="T_5f5bc_row8_col3" class="data row8 col3" >0.000000</td>
      <td id="T_5f5bc_row8_col4" class="data row8 col4" >0.000000</td>
    </tr>
    <tr>
      <th id="T_5f5bc_level0_row9" class="row_heading level0 row9" >feature_9</th>
      <td id="T_5f5bc_row9_col0" class="data row9 col0" >0.000000</td>
      <td id="T_5f5bc_row9_col1" class="data row9 col1" >0.000000</td>
      <td id="T_5f5bc_row9_col2" class="data row9 col2" >1.000000</td>
      <td id="T_5f5bc_row9_col3" class="data row9 col3" >0.000000</td>
      <td id="T_5f5bc_row9_col4" class="data row9 col4" >1.000000</td>
    </tr>
    <tr>
      <th id="T_5f5bc_level0_row10" class="row_heading level0 row10" >feature_10</th>
      <td id="T_5f5bc_row10_col0" class="data row10 col0" >0.000000</td>
      <td id="T_5f5bc_row10_col1" class="data row10 col1" >0.000000</td>
      <td id="T_5f5bc_row10_col2" class="data row10 col2" >0.000000</td>
      <td id="T_5f5bc_row10_col3" class="data row10 col3" >0.000000</td>
      <td id="T_5f5bc_row10_col4" class="data row10 col4" >0.000000</td>
    </tr>
    <tr>
      <th id="T_5f5bc_level0_row11" class="row_heading level0 row11" >feature_11</th>
      <td id="T_5f5bc_row11_col0" class="data row11 col0" >0.000000</td>
      <td id="T_5f5bc_row11_col1" class="data row11 col1" >0.000000</td>
      <td id="T_5f5bc_row11_col2" class="data row11 col2" >0.000000</td>
      <td id="T_5f5bc_row11_col3" class="data row11 col3" >0.000000</td>
      <td id="T_5f5bc_row11_col4" class="data row11 col4" >0.000000</td>
    </tr>
    <tr>
      <th id="T_5f5bc_level0_row12" class="row_heading level0 row12" >feature_12</th>
      <td id="T_5f5bc_row12_col0" class="data row12 col0" >0.000000</td>
      <td id="T_5f5bc_row12_col1" class="data row12 col1" >1.000000</td>
      <td id="T_5f5bc_row12_col2" class="data row12 col2" >0.000000</td>
      <td id="T_5f5bc_row12_col3" class="data row12 col3" >0.000000</td>
      <td id="T_5f5bc_row12_col4" class="data row12 col4" >0.000000</td>
    </tr>
    <tr>
      <th id="T_5f5bc_level0_row13" class="row_heading level0 row13" >feature_13</th>
      <td id="T_5f5bc_row13_col0" class="data row13 col0" >1.000000</td>
      <td id="T_5f5bc_row13_col1" class="data row13 col1" >0.000000</td>
      <td id="T_5f5bc_row13_col2" class="data row13 col2" >0.000000</td>
      <td id="T_5f5bc_row13_col3" class="data row13 col3" >1.000000</td>
      <td id="T_5f5bc_row13_col4" class="data row13 col4" >0.000000</td>
    </tr>
    <tr>
      <th id="T_5f5bc_level0_row14" class="row_heading level0 row14" >feature_14</th>
      <td id="T_5f5bc_row14_col0" class="data row14 col0" >0.000000</td>
      <td id="T_5f5bc_row14_col1" class="data row14 col1" >0.000000</td>
      <td id="T_5f5bc_row14_col2" class="data row14 col2" >0.000000</td>
      <td id="T_5f5bc_row14_col3" class="data row14 col3" >0.000000</td>
      <td id="T_5f5bc_row14_col4" class="data row14 col4" >0.000000</td>
    </tr>
    <tr>
      <th id="T_5f5bc_level0_row15" class="row_heading level0 row15" >feature_15</th>
      <td id="T_5f5bc_row15_col0" class="data row15 col0" >1.000000</td>
      <td id="T_5f5bc_row15_col1" class="data row15 col1" >1.000000</td>
      <td id="T_5f5bc_row15_col2" class="data row15 col2" >1.000000</td>
      <td id="T_5f5bc_row15_col3" class="data row15 col3" >0.000000</td>
      <td id="T_5f5bc_row15_col4" class="data row15 col4" >1.000000</td>
    </tr>
    <tr>
      <th id="T_5f5bc_level0_row16" class="row_heading level0 row16" >feature_16</th>
      <td id="T_5f5bc_row16_col0" class="data row16 col0" >0.000000</td>
      <td id="T_5f5bc_row16_col1" class="data row16 col1" >0.000000</td>
      <td id="T_5f5bc_row16_col2" class="data row16 col2" >0.000000</td>
      <td id="T_5f5bc_row16_col3" class="data row16 col3" >1.000000</td>
      <td id="T_5f5bc_row16_col4" class="data row16 col4" >0.000000</td>
    </tr>
    <tr>
      <th id="T_5f5bc_level0_row17" class="row_heading level0 row17" >feature_17</th>
      <td id="T_5f5bc_row17_col0" class="data row17 col0" >0.000000</td>
      <td id="T_5f5bc_row17_col1" class="data row17 col1" >0.000000</td>
      <td id="T_5f5bc_row17_col2" class="data row17 col2" >0.000000</td>
      <td id="T_5f5bc_row17_col3" class="data row17 col3" >0.000000</td>
      <td id="T_5f5bc_row17_col4" class="data row17 col4" >0.000000</td>
    </tr>
    <tr>
      <th id="T_5f5bc_level0_row18" class="row_heading level0 row18" >feature_18</th>
      <td id="T_5f5bc_row18_col0" class="data row18 col0" >0.000000</td>
      <td id="T_5f5bc_row18_col1" class="data row18 col1" >0.000000</td>
      <td id="T_5f5bc_row18_col2" class="data row18 col2" >0.000000</td>
      <td id="T_5f5bc_row18_col3" class="data row18 col3" >0.000000</td>
      <td id="T_5f5bc_row18_col4" class="data row18 col4" >0.000000</td>
    </tr>
    <tr>
      <th id="T_5f5bc_level0_row19" class="row_heading level0 row19" >feature_19</th>
      <td id="T_5f5bc_row19_col0" class="data row19 col0" >0.000000</td>
      <td id="T_5f5bc_row19_col1" class="data row19 col1" >0.000000</td>
      <td id="T_5f5bc_row19_col2" class="data row19 col2" >0.000000</td>
      <td id="T_5f5bc_row19_col3" class="data row19 col3" >0.000000</td>
      <td id="T_5f5bc_row19_col4" class="data row19 col4" >0.000000</td>
    </tr>
    <tr>
      <th id="T_5f5bc_level0_row20" class="row_heading level0 row20" >feature_20</th>
      <td id="T_5f5bc_row20_col0" class="data row20 col0" >0.000000</td>
      <td id="T_5f5bc_row20_col1" class="data row20 col1" >0.000000</td>
      <td id="T_5f5bc_row20_col2" class="data row20 col2" >0.000000</td>
      <td id="T_5f5bc_row20_col3" class="data row20 col3" >0.000000</td>
      <td id="T_5f5bc_row20_col4" class="data row20 col4" >0.000000</td>
    </tr>
    <tr>
      <th id="T_5f5bc_level0_row21" class="row_heading level0 row21" >feature_21</th>
      <td id="T_5f5bc_row21_col0" class="data row21 col0" >0.000000</td>
      <td id="T_5f5bc_row21_col1" class="data row21 col1" >0.000000</td>
      <td id="T_5f5bc_row21_col2" class="data row21 col2" >0.000000</td>
      <td id="T_5f5bc_row21_col3" class="data row21 col3" >0.000000</td>
      <td id="T_5f5bc_row21_col4" class="data row21 col4" >0.000000</td>
    </tr>
    <tr>
      <th id="T_5f5bc_level0_row22" class="row_heading level0 row22" >feature_22</th>
      <td id="T_5f5bc_row22_col0" class="data row22 col0" >0.000000</td>
      <td id="T_5f5bc_row22_col1" class="data row22 col1" >0.000000</td>
      <td id="T_5f5bc_row22_col2" class="data row22 col2" >0.000000</td>
      <td id="T_5f5bc_row22_col3" class="data row22 col3" >0.000000</td>
      <td id="T_5f5bc_row22_col4" class="data row22 col4" >0.000000</td>
    </tr>
    <tr>
      <th id="T_5f5bc_level0_row23" class="row_heading level0 row23" >feature_23</th>
      <td id="T_5f5bc_row23_col0" class="data row23 col0" >0.000000</td>
      <td id="T_5f5bc_row23_col1" class="data row23 col1" >0.000000</td>
      <td id="T_5f5bc_row23_col2" class="data row23 col2" >0.000000</td>
      <td id="T_5f5bc_row23_col3" class="data row23 col3" >0.000000</td>
      <td id="T_5f5bc_row23_col4" class="data row23 col4" >0.000000</td>
    </tr>
    <tr>
      <th id="T_5f5bc_level0_row24" class="row_heading level0 row24" >feature_24</th>
      <td id="T_5f5bc_row24_col0" class="data row24 col0" >0.000000</td>
      <td id="T_5f5bc_row24_col1" class="data row24 col1" >0.000000</td>
      <td id="T_5f5bc_row24_col2" class="data row24 col2" >0.000000</td>
      <td id="T_5f5bc_row24_col3" class="data row24 col3" >0.000000</td>
      <td id="T_5f5bc_row24_col4" class="data row24 col4" >0.000000</td>
    </tr>
    <tr>
      <th id="T_5f5bc_level0_row25" class="row_heading level0 row25" >feature_25</th>
      <td id="T_5f5bc_row25_col0" class="data row25 col0" >0.000000</td>
      <td id="T_5f5bc_row25_col1" class="data row25 col1" >0.000000</td>
      <td id="T_5f5bc_row25_col2" class="data row25 col2" >0.000000</td>
      <td id="T_5f5bc_row25_col3" class="data row25 col3" >0.000000</td>
      <td id="T_5f5bc_row25_col4" class="data row25 col4" >0.000000</td>
    </tr>
    <tr>
      <th id="T_5f5bc_level0_row26" class="row_heading level0 row26" >feature_26</th>
      <td id="T_5f5bc_row26_col0" class="data row26 col0" >0.000000</td>
      <td id="T_5f5bc_row26_col1" class="data row26 col1" >0.000000</td>
      <td id="T_5f5bc_row26_col2" class="data row26 col2" >0.000000</td>
      <td id="T_5f5bc_row26_col3" class="data row26 col3" >0.000000</td>
      <td id="T_5f5bc_row26_col4" class="data row26 col4" >0.000000</td>
    </tr>
    <tr>
      <th id="T_5f5bc_level0_row27" class="row_heading level0 row27" >feature_27</th>
      <td id="T_5f5bc_row27_col0" class="data row27 col0" >0.000000</td>
      <td id="T_5f5bc_row27_col1" class="data row27 col1" >0.000000</td>
      <td id="T_5f5bc_row27_col2" class="data row27 col2" >0.000000</td>
      <td id="T_5f5bc_row27_col3" class="data row27 col3" >0.000000</td>
      <td id="T_5f5bc_row27_col4" class="data row27 col4" >0.000000</td>
    </tr>
    <tr>
      <th id="T_5f5bc_level0_row28" class="row_heading level0 row28" >ground_truth</th>
      <td id="T_5f5bc_row28_col0" class="data row28 col0" >0.000000</td>
      <td id="T_5f5bc_row28_col1" class="data row28 col1" >0.000000</td>
      <td id="T_5f5bc_row28_col2" class="data row28 col2" >0.000000</td>
      <td id="T_5f5bc_row28_col3" class="data row28 col3" >0.000000</td>
      <td id="T_5f5bc_row28_col4" class="data row28 col4" >0.000000</td>
    </tr>
  </tbody>
</table>

## Hyperparameter search

The choice of the batch size and the maximum number of epochs depends on
the dataset size. For this dataset, we use the following values:

``` python
batch_size = 256
max_epochs = 20
```

We use the Type-2 architecture built using
[`MonoDense`](api/airt/keras/layers/MonoDense/#airt.keras.layers.MonoDense)
layer with the following set of hyperparameters ranges:

``` python
def hp_params_f(hp):
    return dict(
        units=hp.Int("units", min_value=4, max_value=32, step=1),
        n_layers=hp.Int("n_layers", min_value=1, max_value=2),
        activation=hp.Choice("activation", values=["elu"]),
        learning_rate=hp.Float(
            "learning_rate", min_value=1e-4, max_value=1e-2, sampling="log"
        ),
        weight_decay=hp.Float(
            "weight_decay", min_value=3e-2, max_value=0.3, sampling="log"
        ),
        dropout=hp.Float("dropout", min_value=0.0, max_value=0.5, sampling="linear"),
        decay_rate=hp.Float(
            "decay_rate", min_value=0.8, max_value=1.0, sampling="reverse_log"
        ),
    )
```

The following fixed parameters are used to build the Type-2 architecture
for this dataset:

- `final_activation` is used to build the final layer for regression
  problem (set to `None`) or for the classification problem
  (`"sigmoid"`),

- `loss` is used for training regression (`"mse"`) or classification
  (`"binary_crossentropy"`) problem, and

- `metrics` denotes metrics used to compare with previosly published
  results: `"accuracy"` for classification and “`mse`” or “`rmse`” for
  regression.

Parameters `objective` and `direction` are used by the tuner such that
`objective=f"val_{metrics}"` and direction is either `"min` or `"max"`.

Parameters `max_trials` denotes the number of trial performed buy the
tuner, `patience` is the number of epochs allowed to perform worst than
the best one before stopping the current trial. The parameter
`execution_per_trial` denotes the number of runs before calculating the
results of a trial, it should be set to value greater than 1 for small
datasets that have high variance in results.

``` python
final_activation = None
loss = "binary_crossentropy"
metrics = "accuracy"
objective = "val_accuracy"
direction = "max"
max_trials = 50
executions_per_trial = 1
patience = 5
```

The following table describes the best models and their hyperparameters
found by the tuner:

## The optimal model

These are the best hyperparameters found by previous runs of the tuner:

``` python
def final_hp_params_f(hp):
    return dict(
        units=hp.Fixed("units", value=8),
        n_layers=hp.Fixed("n_layers", 2),
        activation=hp.Fixed("activation", value="elu"),
        learning_rate=hp.Fixed("learning_rate", value=0.008),
        weight_decay=hp.Fixed("weight_decay", value=0.0),
        dropout=hp.Fixed("dropout", value=0.0),
        decay_rate=hp.Fixed("decay_rate", value=1.0),
    )
```

The final evaluation of the optimal model:

<style type="text/css">
</style>
<table id="T_7149d">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_7149d_level0_col0" class="col_heading level0 col0" >0</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_7149d_level0_row0" class="row_heading level0 row0" >units</th>
      <td id="T_7149d_row0_col0" class="data row0 col0" >8</td>
    </tr>
    <tr>
      <th id="T_7149d_level0_row1" class="row_heading level0 row1" >n_layers</th>
      <td id="T_7149d_row1_col0" class="data row1 col0" >2</td>
    </tr>
    <tr>
      <th id="T_7149d_level0_row2" class="row_heading level0 row2" >activation</th>
      <td id="T_7149d_row2_col0" class="data row2 col0" >elu</td>
    </tr>
    <tr>
      <th id="T_7149d_level0_row3" class="row_heading level0 row3" >learning_rate</th>
      <td id="T_7149d_row3_col0" class="data row3 col0" >0.008000</td>
    </tr>
    <tr>
      <th id="T_7149d_level0_row4" class="row_heading level0 row4" >weight_decay</th>
      <td id="T_7149d_row4_col0" class="data row4 col0" >0.000000</td>
    </tr>
    <tr>
      <th id="T_7149d_level0_row5" class="row_heading level0 row5" >dropout</th>
      <td id="T_7149d_row5_col0" class="data row5 col0" >0.000000</td>
    </tr>
    <tr>
      <th id="T_7149d_level0_row6" class="row_heading level0 row6" >decay_rate</th>
      <td id="T_7149d_row6_col0" class="data row6 col0" >1.000000</td>
    </tr>
    <tr>
      <th id="T_7149d_level0_row7" class="row_heading level0 row7" >val_accuracy_mean</th>
      <td id="T_7149d_row7_col0" class="data row7 col0" >0.652917</td>
    </tr>
    <tr>
      <th id="T_7149d_level0_row8" class="row_heading level0 row8" >val_accuracy_std</th>
      <td id="T_7149d_row8_col0" class="data row8 col0" >0.000085</td>
    </tr>
    <tr>
      <th id="T_7149d_level0_row9" class="row_heading level0 row9" >val_accuracy_min</th>
      <td id="T_7149d_row9_col0" class="data row9 col0" >0.652851</td>
    </tr>
    <tr>
      <th id="T_7149d_level0_row10" class="row_heading level0 row10" >val_accuracy_max</th>
      <td id="T_7149d_row10_col0" class="data row10 col0" >0.653065</td>
    </tr>
    <tr>
      <th id="T_7149d_level0_row11" class="row_heading level0 row11" >params</th>
      <td id="T_7149d_row11_col0" class="data row11 col0" >577</td>
    </tr>
  </tbody>
</table>