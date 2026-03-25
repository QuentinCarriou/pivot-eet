import pandas as pd
import streamlit as st
from io import BytesIO
from pathlib import Path

st.title("WeeFin")
st.subheader("Outil de transformation des templates de collecte EET")

uploaded_file = st.file_uploader("Uploadez votre template de collecte EET WeeFin", type="xlsx")

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    result = pd.concat([df[["Datapoint Name"]], df.iloc[:, 10:]], axis=1).set_index("Datapoint Name").T
    output_name = Path(uploaded_file.name).stem + "_pivoted.xlsx"
    
    # Convert to Excel in memory
    output = BytesIO()
    result.to_excel(output, index=False)
    output.seek(0)
    
    st.success("Le fichier a été traité avec succès")
    st.download_button(
        label="Télécharger le fichier au format EET",
        data=output,
        file_name=output_name,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )