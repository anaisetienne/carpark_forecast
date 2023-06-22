import os

import streamlit as st
import pandas as pd
import pandas_profiling

# Profiling
from streamlit_pandas_profiling import st_profile_report

# ML
from pycaret.classification import setup, compare_models, pull, save_model

with st.sidebar:
    with st.columns(3)[1]:
        st.image("./img/logo_devFool.png", width=75)
    st.title("Machine learning")
    choices = st.radio("Navigation", ["Upload", "Profiling", "TRUC"])
    st.info('Exploratory Data Analysis dans un fauteuil. 🤖')

if os.path.exists("../raw_data/sourcedata.csv"):
    df = pd.read_csv("../raw_data/sourcedata.csv", index_col=None)

if choices == "Upload":
    file = st.file_uploader("Merci de choisir un fichier csv")
    if file:
        df = pd.read_csv(file, index_col=None)
        df.to_csv("../raw_data/sourcedata.csv", index=None)
        st.dataframe(df)
elif choices == "Profiling":
    st.title("Exploratory Data Analysis")
    profile_report = df.profile_report()
    st_profile_report(profile_report)

elif choices == "TRUC":
    st.title("je suis dans TRUC")

elif choices == "ML":
    st.title("Machine Learning")
    chosen_target  = st.selectbox('Selectionner votre target', df.columns)
    object_columns = df.select_dtypes(include=['object']).columns
    # df['Transported'] = df['Transported'].astype(int)
    if st.button("Entrainer le modéle"):
        s = setup(df, target=chosen_target, session_id = 123, categorical_features=['PassengerId', 'HomePlanet', 'Cabin', 'Destination', 'Name'], normalize = True,transformation = True)
        st.write(s)

        # OOP API
        best = compare_models()
        st.write("coucou")
        st.write(best)
        print(best)

        # setup(df, target=chosen_target)
        # setup_df = pull()
        # st.dataframe(setup_df)
        # best_model = compare_models()
        # compare_df = pull()
        # st.dataframe(compare_df)
        # save_model(best_model, 'best_model')
else:
    pass
