import requests
import pprint #Usei esse módulo para melhor visualizaçao dos dados
import mysql.connector
from mysql.connector import Error


link_api = "http://api.weatherapi.com/v1/current.json"
key_api = "5a9cc2a1d94240e4851211054251012"

paramentros = {"key": key_api,
               "q":"Florianopolis"}

resposta = requests.get(link_api,params=paramentros)
if resposta.status_code == 200:
    dados_requisicao = resposta.json() #transformei os dados no formato json (dicionário)
    #pprint.pprint(dados_requisicao)
    temperatura = dados_requisicao["current"]["temp_c"]
    cidade = dados_requisicao["location"]["name"]
    estado = dados_requisicao["location"]["region"]
    data_atual = dados_requisicao["location"]["localtime"]
    #print(temperatura,cidade,estado,data_atual)
    
    registro = [(estado, cidade,temperatura,data_atual)]

#parâmetros de conexão
try:
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        #password="",
        database="tempo"
    )

    if conexao.is_connected():
        cursor = conexao.cursor()
#Acabei criando um banco de dados manualmente, mas poderia criar por código também; aqui criei somente a tabela e adicionei os dados
        criar_tabela = """
        CREATE TABLE IF NOT EXISTS Tempo(
            estado VARCHAR(100),
            cidade VARCHAR(100),
            temperatura VARCHAR(100),
            data_atual DATETIME
        );
        """

        cursor.execute(criar_tabela)
        print("Tabela criada com sucesso!")

        inserir = """
        INSERT INTO Tempo (estado, cidade, temperatura, data_atual)
        VALUES (%s, %s, %s,%s)
        """

        cursor.executemany(inserir,registro)
        conexao.commit()

        print("{cursor.rowcount} registro(s) inseridos com sucesso!")

except Error as e:
    print("Erro ao criar tabela:", e)
   

finally:
    if conexao.is_connected():
        cursor.close()
        conexao.close()
