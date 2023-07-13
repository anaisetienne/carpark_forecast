import os

raw_data_path = "./sourcedata.csv"
raw_data_path_processed = "./sourcedataproc.csv"
tgv_model_path = 'models/tgv_model_1'
rnn_predictions_25 = 'models/df_25_model_3'
n_beats_25_path = 'models/n_beats_25'
n_hits_25_path = 'models/n_hits_25'


# Obtenir le chemin absolu du répertoire racine
root_dir = os.path.dirname(os.path.abspath(__file__))

# Obtenir le chemin absolu du répertoire parent
parent_dir = os.path.dirname(root_dir)


# Charger le modèle à partir du répertoire parent
n_beats_25_absolute_path = os.path.join(parent_dir, n_beats_25_path)

# Charger le modèle à partir du répertoire parent
n_hits_25_absolute_path = os.path.join(parent_dir, n_hits_25_path)

rnn_predictions_25_path = os.path.join(parent_dir, rnn_predictions_25)
