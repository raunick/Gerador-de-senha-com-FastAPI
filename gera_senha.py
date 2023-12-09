import sqlite3
import secrets

def gerar_senha():
    # Gera uma senha aleatória de 8 caracteres
    return secrets.token_hex(4)

def adicionar_senha(tipo):
    conn = sqlite3.connect('senhas.db')
    cursor = conn.cursor()

    # Gera uma senha de teste
    nova_senha = gerar_senha()

    # Inserir senha na tabela com o tipo especificado
    cursor.execute('INSERT INTO senhas (senha, tipo) VALUES (?, ?)', (nova_senha, tipo))

    # Commit para salvar as alterações
    conn.commit()

    # Fechar a conexão
    conn.close()

# Exemplo de uso
tipo_senha = "urgente"  # Pode ser "urgente", "preferencial" ou "normal"
adicionar_senha(tipo_senha)
