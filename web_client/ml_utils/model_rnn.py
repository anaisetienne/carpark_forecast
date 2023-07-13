import os

import numpy as np
import pandas as pd

from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA

from ml_utils import config

from tensorflow import keras

# chemin absolu du répertoire racine
root_dir = os.path.dirname(os.path.abspath(__file__))

# chemin absolu du répertoire parent
parent_dir = os.path.dirname(root_dir)

# nom du dossier du modèle
# model_folder = config.tgv_model_path
model_folder = 'models/tgv_model_1'


model_folder_25 = 'models/df_25_model_3_bis'
# chemin complet du dossier du modèle
model_path = os.path.join(parent_dir, model_folder_25)


predictions_25_model = keras.models.load_model(model_path)


def tgv_prediction(model):
    '''
    Returns a prediction of number of cars for 14 days from pocket number
    '''

    df = pd.read_csv(config.raw_data_path_processed, parse_dates=[0], index_col=[0])
    df_last_56 = df.tail(56)
    df_last_56['truc'] = 0

    #Scaling
    scaler = MinMaxScaler()
    y_scaler = MinMaxScaler()
    # TARGET
    y_scaler.fit(np.log(df_last_56[['nb_cars']]).values.reshape(-1, 1))

    scaled_df = scaler.fit_transform(df_last_56)

    #PCA
    pca = PCA(n_components=25).fit(scaled_df)
    proj = pd.DataFrame(pca.transform(scaled_df))
    proj.index = df_last_56.index

    pred = model.predict(np.array(proj).reshape(1,56,25))
    pred = y_scaler.inverse_transform(pred)
    pred = np.exp(pred).tolist()

    return pred
