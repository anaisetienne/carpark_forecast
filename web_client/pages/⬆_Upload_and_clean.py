import os

import streamlit as st
import pandas as pd

# CONFIG
from ml_utils import config
# CLEANING
from ml_utils import data_cleaning as dc


df = None
cleaned_df = pd.DataFrame()

file = st.file_uploader("Thanks to select a xlsx file")
if file:
    df = pd.read_excel( file,
                        dtype=dc.custom_dtype,
                        parse_dates=['creation_date_hour', 'beginning_date_hour', 'end_date_hour'])
    cleaned_df = dc.clean_df(df)

if not cleaned_df.empty:

    unique_ids_list = cleaned_df['pocket'].unique().tolist()
    pocket_id = st.selectbox('Choose your pocket id', unique_ids_list)
    button = st.button('Clean and process data for this pocket')
    if button:
        # Récupérer les lignes correspondantes à l'ID recherché
        selected_pocket_df = cleaned_df.loc[df['pocket'] == pocket_id]
        st.title('Cleaned Data')
        st.dataframe(selected_pocket_df)

        time_series_df = dc.create_time_series_df(selected_pocket_df)
        st.title('Data preprocessed for time serie model')
        st.dataframe(time_series_df)
        # Save CSV to use the df elsewhere
        print("AVANT")
        st.session_state["pocket_id"] = pocket_id
        print("APRES")
        selected_pocket_df.to_csv(config.raw_data_path)
        time_series_df.to_csv(config.raw_data_path_processed)


# FOOTER
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer:before {
                content: 'Le Wagon batch 1775 @ 2023';
                display: block;
                color: white;
                position: relative;
                padding: 5px;
                top: 3px;
                }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
