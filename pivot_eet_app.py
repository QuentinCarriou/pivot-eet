import pandas as pd
import streamlit as st
from io import BytesIO
from pathlib import Path

st.title("WeeFin")
st.subheader("Outil de transformation des templates de collecte EET")

uploaded_files = st.file_uploader("Uploadez vos templates de collecte EET WeeFin", type="xlsx", accept_multiple_files=True)

if uploaded_files:
    dfs = []
    for file in uploaded_files:
        df = pd.read_excel(file)
        result = pd.concat([df[["Datapoint Name"]], df.iloc[:, 10:]], axis=1).set_index("Datapoint Name").T
        dfs.append(result)
    
    combined = pd.concat(dfs, ignore_index=True)
    
    output = BytesIO()
    combined.to_excel(output, index=False)
    output.seek(0)
    
    st.success(f"{len(uploaded_files)} fichier(s) traité(s) avec succès")
    st.download_button(
        label="Télécharger le fichier au format EET",
        data=output,
        file_name="output_pivoted.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )