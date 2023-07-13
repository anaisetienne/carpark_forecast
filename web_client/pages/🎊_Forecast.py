# THIRD PARTY
import streamlit as st
import pandas as pd

# OWN
from ml_utils import model_mlp as mlp
from ml_utils import model_rnn as rnn
from ml_utils import config
from ml_utils import graph_predict as gp


pocket_id = st.session_state["pocket_id"]

st.title("Forecasting number of cars in specific carpark.")

title_text = """
  #### Actual pocket id : <span style="color:teal">{temp1}</span>
""".format(temp1=pocket_id)

st.markdown(title_text, unsafe_allow_html=True)

model_id = st.selectbox("Model type",
        ("RNN",
        "NBEATS",
        "NHITS"))

button = st.button('Predict')

if button:
    df = pd.read_csv(config.raw_data_path_processed, parse_dates=['date'])
    if model_id == 'RNN':
        model = rnn.predictions_25_model
        predictions_tgv = rnn.tgv_prediction(model)
        result = [[num] for num in predictions_tgv[0]]
    elif model_id == 'NBEATS':
        result = mlp.get_n_beats_predictions()

    elif model_id == 'NHITS':
        result = mlp.get_n_hits_predictions()


    date_reference = pd.to_datetime('2023-06-05')
    date_reference_past = gp.get_past_year_weekday(date_reference)
    data_to_plot = gp.get_data_past_two_weeks(date_reference, 15, df)
    data_to_plot_forecast = gp.prepare_forecast_data_for_plotting(date_reference, 15, result)
    data_past = gp.get_data_from_last_year(date_reference_past, df, period=30)

    fig = gp.plot_graph_plotly(data_to_plot, data_to_plot_forecast, data_past, date_reference)
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
