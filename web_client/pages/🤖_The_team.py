import os
import streamlit as st



# chemin absolu du répertoire racine
root_dir = os.path.dirname(os.path.abspath(__file__))

# chemin absolu du répertoire parent
parent_dir = os.path.dirname(root_dir)

print(parent_dir)


st.title("The A-Team")

# Liste des noms des fichiers d'images
image_files = [os.path.join(parent_dir, 'img/anais.png'), os.path.join(parent_dir, 'img/annett.png'), os.path.join(parent_dir, 'img/zyad.jpeg'), os.path.join(parent_dir, 'img/remy.jpg'), os.path.join(parent_dir, 'img/reinis.jpg')]

# Pour chaque fichier image, affichez l'image
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)
col5 = st.columns(1)
with col1:
   st.subheader("The expert")
   st.image(image_files[0])
   st.text("Anaïs")

with col2:
   st.subheader("The exogenous 😉")
   st.image(image_files[1])
   st.text("Annett")

with col3:
    st.subheader("The architect")
    st.image(image_files[4])
    st.text("Reinis")

with col4:
    st.subheader("The swiss army knife")
    st.image(image_files[3])
    st.text("Rémy")


st.subheader("The invisble man")
st.image(image_files[2])
st.text("Zyad")



# with col3:
#    st.header("An owl")
#    st.image("https://static.streamlit.io/examples/owl.jpg")
