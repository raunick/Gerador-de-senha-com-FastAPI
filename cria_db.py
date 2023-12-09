import sqlite3
from datetime import datetime

# Conectar ao banco de dados (ou criar se não existir)
conn = sqlite3.connect('senhas.db')

# Criar um cursor para executar comandos SQL
cursor = conn.cursor()

# Criar tabela para armazenar senhas
cursor.execute('''
    CREATE TABLE IF NOT EXISTS senhas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        senha TEXT NOT NULL,
        tipo TEXT CHECK(tipo IN ('urgente', 'preferencial', 'normal')) NOT NULL,
        criada_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        chamada_em TIMESTAMP
    )
''')

# Commit para salvar as alterações
conn.commit()

# Fechar a conexão
conn.close()
