import os

import streamlit as st
import pandas as pd
import pandas_profiling

# CONFIG
from config import raw_data_path

# CLEANING
from data_cleaning import *

# GRAPH
from graph_predict import *


# Profiling
from streamlit_pandas_profiling import st_profile_report

# ML
#from pycaret.classification import setup, compare_models, pull, save_model


st.session_state["pocket_id"] = "0"

# df = None
# cleaned_df = pd.DataFrame()

# with st.sidebar:
#     with st.columns(3)[1]:
#         st.image("./img/logo_devFool.png", width=75)
#     st.title("Carpark forecast project")
#     choices = st.radio("Navigation", ["Upload", "Profiling", "Forecast"])
#     st.info('The doors of the future are open to those who know how to push them. 🤖')


# Upload and cleaning
# if choices == "Upload":
#     file = st.file_uploader("Thanks to select a xlsx file")
#     if file:
#         df = pd.read_excel( file,
#                             dtype=custom_dtype,
#                             parse_dates=['creation_date_hour', 'beginning_date_hour', 'end_date_hour'])
#         cleaned_df = clean_df(df)

#     if not cleaned_df.empty:

#         unique_ids_list = cleaned_df['pocket'].unique().tolist()
#         pocket_id = st.selectbox('Choose your pocket id', unique_ids_list)
#         button = st.button('Clean and process data for this pocket')
#         if button:
#             # Récupérer les lignes correspondantes à l'ID recherché
#             selected_pocket_df = cleaned_df.loc[df['pocket'] == pocket_id]
#             st.title('Cleaned Data')
#             st.dataframe(selected_pocket_df)

#             time_series_df = create_time_series_df(selected_pocket_df)
#             st.title('Data preprocessed for time serie model')
#             st.dataframe(time_series_df)
#             # Save CSV to use the df elsewhere
#             selected_pocket_df.to_csv(raw_data_path)
#             st.session_state["pocket_id"] = pocket_id


# elif choices == "Profiling":
#     st.title("Exploratory Data Analysis")
#     profile_report = df.profile_report()
#     st_profile_report(profile_report)

# elif choices == "Forecast":
#     st.title("Forecasting number of cars in specific carpark")

#     st.write(st.session_state["pocket_id"])

#     pocket_id = st.selectbox("Pocket ID",
#             ("25",
#             "34",
#             "36",
#             "52",
#             "95",
#             "180",
#             "206",
#             "272",
#             "287",
#             "368",
#             "781",
#             "875",
#             "1435",
#             "5435",
#             "6287"))

#     button = st.button('Predict')

#     if button:
#         df = pd.read_csv('../prepared_data/01_06_2021_to_20_06_2023_prepared_df_875.csv', parse_dates=['date'])

#         date_reference = pd.to_datetime('2023-06-05')
#         date_reference_past = get_past_year_weekday(date_reference)
#         data_to_plot = get_data_past_two_weeks(date_reference, 15, df)
#         data_to_plot_forecast = prepare_forecast_data_for_plotting(date_reference, 15, future)
#         data_past = get_data_from_last_year(date_reference_past, df, period=30)

#         fig = plot_graph(data_to_plot, data_to_plot_forecast, data_past, date_reference)
#         st.pyplot()



# else:
#     pass



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
