import requests
import streamlit as st

# Definindo a URL da API FastAPI
API_URL = "http://127.0.0.1:8000"  # Atualize com o endereço da sua API

def obter_ultima_senha_chamada():
    response = requests.get(f"{API_URL}/ultima_senha_chamada/")
    ultima_senha_chamada = response.json()["ultima_senha_chamada"]

    st.header("Última Senha Chamada")

    if ultima_senha_chamada:
        st.success(f"Tipo: {ultima_senha_chamada['tipo']}")
        st.info(f"Chamada em: {ultima_senha_chamada['chamada_em']}")
    else:
        st.warning("Nenhuma senha foi chamada ainda.")

# Use as funções no seu app
if st.button("Atualizar"):
    obter_ultima_senha_chamada()
