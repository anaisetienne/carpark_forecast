import pandas as pd

from neuralforecast.core import NeuralForecast
from sklearn.preprocessing import RobustScaler

from ml_utils import config


def get_n_beats_predictions():
    df = pd.read_csv(config.raw_data_path_processed, parse_dates=['date'])
    df = df.rename(columns={'date': 'ds', 'nb_cars':'y'})

    robust_scaler = RobustScaler()

    df['y'] = robust_scaler.fit_transform(df['y'].values.reshape(-1, 1))
    df['unique_id'] = 1

    n_beats = NeuralForecast.load(path=config.n_beats_25_absolute_path)

    Y_hat_df_n_beats = n_beats.predict(df=df, test_size=150).reset_index()

    predictions_scaled = Y_hat_df_n_beats['NBEATS'].values.reshape(-1, 1)

    # Inversez la mise à l'échelle
    predictions = robust_scaler.inverse_transform(predictions_scaled)

    return predictions


def get_n_hits_predictions():
    df = pd.read_csv(config.raw_data_path_processed, parse_dates=['date'])
    df = df.rename(columns={'date': 'ds', 'nb_cars':'y'})

    robust_scaler = RobustScaler()

    df['y'] = robust_scaler.fit_transform(df['y'].values.reshape(-1, 1))
    df['unique_id'] = 1

    n_hits = NeuralForecast.load(path=config.n_hits_25_absolute_path)

    Y_hat_df_n_hits = n_hits.predict(df=df, test_size=150).reset_index()

    predictions_scaled = Y_hat_df_n_hits['NHITS'].values.reshape(-1, 1)

    # Inversez la mise à l'échelle
    predictions = robust_scaler.inverse_transform(predictions_scaled)

    return predictions
