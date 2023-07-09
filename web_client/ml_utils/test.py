import pandas as pd

df = pd.read_excel('../../../../Downloads/bookings_whithout_onepark.xlsx')

# Liste des ID à extraire
ids_to_extract = ['0000000025', '0000000036', '0000000272']

# Extraction des lignes correspondant aux ID spécifiés
extracted_data = df[df['pocket'].isin(ids_to_extract)]

# Chemin et nom de fichier Excel de destination
output_file = '../../../../Downloads/test.xlsx'

# Sauvegarde du DataFrame extrait dans un fichier Excel
extracted_data.to_excel(output_file, index=False)
