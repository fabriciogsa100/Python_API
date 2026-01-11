from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel
from datetime import datetime
from mysql.connector import Error
import mysql.connector

from api_banco_dados import get_connection

app = FastAPI(title="API Tempo")

class Tempo(BaseModel):
    estado: str
    cidade: str
    temperatura: float
    data_atual: datetime

@app.get("/")
def home():
    return{"status": "API rodando com MySQL"}

#GET todos os registros
@app.get("/tempo",response_model=List[Tempo])
def listar_tempo():

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT estado, cidade, temperatura, data_atual
            FROM Tempo
            ORDER BY data_atual DESC    
        """)

        dados = cursor.fetchall()

        return dados
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()


# 🔹 GET por cidade
@app.get("/tempo/{cidade}", response_model=List[Tempo])
def listar_por_cidade(cidade: str):

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT estado, cidade, temperatura, data_atual
            FROM Tempo
            WHERE cidade = %s
            ORDER BY data_atual DESC
        """, (cidade,))

        dados = cursor.fetchall()

        if not dados:
            raise HTTPException(status_code=404, detail="Cidade não encontrada")

        return dados

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()