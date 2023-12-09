import streamlit as st
import requests
import secrets
import string


# Definindo a URL da API FastAPI
API_URL = "http://127.0.0.1:8000"  # Atualize com o endereço da sua API

# Título do aplicativo Streamlit
st.title("Interagindo com a API FastAPI")



# Função para criar uma nova senha
def criar_senha():
    st.subheader("Criar Nova Senha")

    opcoes_tipo = ["normal", "preferencial", "urgente"]
    tipo = st.selectbox("Tipo", opcoes_tipo)

    if st.button("Criar Senha"):
        senha_input = gerar_senha_aleatoria()
        st.text("Enviando dados para a API...")  # Adicione esta linha para depuração
        st.text(f"Senha Input: {senha_input}")  # Adicione esta linha para depuração
        st.text(f"Tipo: {tipo}")  # Adicione esta linha para depuração
        dados_senha = {"senha": senha_input, "tipo": tipo}
        response = requests.post(f"{API_URL}/senhas/", json=dados_senha)

        # Verificar se a resposta é válida antes de acessar os elementos JSON
        if response.ok:
            try:
                mensagem = response.json()["mensagem"]
                st.success(mensagem)
            except ValueError as e:
                st.error(f"Erro ao decodificar JSON: {e}")
        else:
            st.error(f"Erro na requisição: {response.status_code} - {response.text}")

# Função para gerar uma senha aleatória
def gerar_senha_aleatoria():
    caracteres = string.ascii_letters + string.digits + string.punctuation
    senha = ''.join(secrets.choice(caracteres) for _ in range(12))  # 12 caracteres, ajuste conforme necessário
    return senha
    
# Função para chamar uma senha em tempo real
def chamar_senha():
    st.subheader("Chamar Senha")
    opcoes_tipo = ["normal", "preferencial", "urgente"]
    tipo = st.selectbox("Tipo", opcoes_tipo)
    if st.button("Chamar Senha"):
        response = requests.post(f"{API_URL}/chamar_senha/?tipo={tipo}")
        if response.status_code == 200:
            st.success(f"Senha chamada: {response.json()['senha_chamada']}")
            print(response.json()["senha_chamada"])
        else:
            st.error(response.json()["detail"])


# Função para obter todas as senhas
def obter_senhas():
    st.subheader("Obter Todas as Senhas")
    response = requests.get(f"{API_URL}/senhas/")
    senhas = response.json()["senhas"]
    st.write(senhas)

# Função para obter senhas chamadas
def obter_senhas_chamadas():
    st.subheader("Senhas Chamadas")
    response = requests.get(f"{API_URL}/senhas_chamadas/")
    senhas_chamadas = response.json()["senhas_chamadas"]
    st.write(senhas_chamadas)

# Sidebar com opções
opcao = st.sidebar.selectbox("Selecione uma opção", ["Criar Senha", "Chamar Senha", "Obter Senhas", "Senhas Chamadas"])

# Executando a função correspondente à opção escolhida
if opcao == "Criar Senha":
    criar_senha()
elif opcao == "Chamar Senha":
    chamar_senha()
elif opcao == "Obter Senhas":
    obter_senhas()
elif opcao == "Senhas Chamadas":
    obter_senhas_chamadas()
