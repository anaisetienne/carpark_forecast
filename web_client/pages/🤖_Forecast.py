import streamlit as st

from graph_predict import *

from config import raw_data_path_processed
from model_rnn import predictions


# st.write(st.session_state["pocket_id"])
pocket_id = st.session_state["pocket_id"]

st.title("Forecasting number of cars in specific carpark.")

title_text = """
  #### Actual pocket id : <span style="color:teal">{temp1}</span>
""".format(temp1=pocket_id)

st.markdown(title_text, unsafe_allow_html=True)

# pocket_id = st.selectbox("Pocket ID",
#         ("25",
#         "34",
#         "36",
#         "52",
#         "95",
#         "180",
#         "206",
#         "272",
#         "287",
#         "368",
#         "781",
#         "875",
#         "1435",
#         "5435",
#         "6287"))

button = st.button('Predict')

if button:
    df = pd.read_csv(raw_data_path_processed, parse_dates=['date'])

    date_reference = pd.to_datetime('2023-06-05')
    date_reference_past = get_past_year_weekday(date_reference)
    data_to_plot = get_data_past_two_weeks(date_reference, 15, df)
    data_to_plot_forecast = prepare_forecast_data_for_plotting(date_reference, 15, predictions)
    data_past = get_data_from_last_year(date_reference_past, df, period=30)

    fig = plot_graph_plotly(data_to_plot, data_to_plot_forecast, data_past, date_reference)
    st.plotly_chart(fig, use_container_width=True)



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
