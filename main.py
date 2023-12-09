from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# Configuração do CORS
origins = ["*"]  # Permite todas as origens, ajuste conforme necessário
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos, ajuste conforme necessário
    allow_headers=["*"],  # Permite todos os cabeçalhos, ajuste conforme necessário
)

# Modelo Pydantic para definir a estrutura dos dados da senha
class Senha(BaseModel):
    senha: str
    tipo: str

# Conectar ao banco de dados
conn = sqlite3.connect('senhas.db')
cursor = conn.cursor()

# Rota para criar uma nova senha
@app.post("/senhas/")
async def criar_senha(senha: Senha):
    # Inserir senha na tabela
    cursor.execute('INSERT INTO senhas (senha, tipo) VALUES (?, ?)', (senha.senha, senha.tipo))
    
    # Commit para salvar as alterações
    conn.commit()
    
    return {"mensagem": "Senha criada com sucesso!"}

# Rota para obter todas as senhas
@app.get("/senhas/")
async def obter_senhas():
    cursor.execute('SELECT * FROM senhas')
    senhas = cursor.fetchall()
    return {"senhas": senhas}

# Rota para obter uma senha específica pelo ID
@app.get("/senhas/{senha_id}")
async def obter_senha(senha_id: int):
    cursor.execute('SELECT * FROM senhas WHERE id = ?', (senha_id,))
    senha = cursor.fetchone()
    if senha:
        return {"senha": senha}
    raise HTTPException(status_code=404, detail="Senha não encontrada")

# Rota para chamar uma senha em tempo real
@app.post("/chamar_senha/")
async def chamar_senha(tipo: str):
    cursor.execute('SELECT * FROM senhas WHERE tipo = ? AND chamada_em IS NULL ORDER BY criada_em LIMIT 1', (tipo,))
    senha = cursor.fetchone()

    if senha:
        # Atualiza a coluna chamada_em com a data e hora atuais
        cursor.execute('UPDATE senhas SET chamada_em = ? WHERE id = ?', (datetime.now(), senha[0]))
        conn.commit()
        return {"senha_chamada": {"id": senha[0], "tipo": senha[2], "chamada_em": datetime.now().isoformat()}}
    else:
        raise HTTPException(status_code=404, detail="Nenhuma senha disponível do tipo especificado")

# Rota para obter todas as senhas chamadas
@app.get("/senhas_chamadas/")
async def obter_senhas_chamadas():
    cursor.execute('SELECT * FROM senhas WHERE chamada_em IS NOT NULL')
    senhas_chamadas = cursor.fetchall()
    return {"senhas_chamadas": senhas_chamadas}


# Rota para obter a última senha chamada
@app.get("/ultima_senha_chamada/")
async def obter_ultima_senha_chamada():
    cursor.execute('SELECT senha, tipo, chamada_em FROM senhas WHERE chamada_em IS NOT NULL ORDER BY chamada_em DESC LIMIT 1')
    ultima_senha_chamada = cursor.fetchone()

    if ultima_senha_chamada:
        senha, tipo, chamada_em = ultima_senha_chamada
        return {"ultima_senha_chamada": {"senha": senha,"tipo": tipo, "chamada_em": chamada_em}}
    else:
        return {"ultima_senha_chamada": None}
   
# Rota para obter as últimas senhas chamadas
@app.get("/ultimas_chamadas/")
async def obter_ultimas_chamadas():
    cursor.execute('SELECT tipo, chamada_em FROM senhas WHERE chamada_em IS NOT NULL ORDER BY chamada_em DESC LIMIT 3')
    ultimas_chamadas = cursor.fetchall()

    if ultimas_chamadas:
        ultimas_chamadas_formatadas = [{"tipo": chamada[0], "chamada_em": chamada[1]} for chamada in ultimas_chamadas]
        return {"ultimas_chamadas": ultimas_chamadas_formatadas}
    else:
        return {"ultimas_chamadas": []}