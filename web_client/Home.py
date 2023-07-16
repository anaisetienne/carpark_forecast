import os
import streamlit as st


import os
os.environ['PYTORCH_ENABLE_MPS_FALLBACK'] = '1'


# chemin absolu du répertoire racine
root_dir = os.path.dirname(os.path.abspath(__file__))



# nom du dossier du modèle
# model_folder = config.tgv_model_path
model_folder = 'img/home.jpg'

# chemin complet du dossier du modèle
model_path = os.path.join(root_dir, model_folder)

if 'pocket_id' not in st.session_state:
    st.session_state["pocket_id"] = "0"

st.title("Forecast application ")
col1, col2 = st.columns(2)

col1.image(model_path)
col2.text("The procedure is as follows:")
col2.text("1 - Click on Upload and clean in the sidebar")
col2.text("2 - Select an xlsx file to upload")
col2.text("3 - Click on button to process cleaning")
col2.text("4 - Click on Forecast in the sidebar")
col2.text("5 - Click on button to predict")
col2.text("6 - Enjoy the predictions 🎊")


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
