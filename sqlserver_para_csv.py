import sys
import pandas as pd
# Biblioteca que permite acesso ao Sql Server.
import pyodbc

# Obter informações de autenticação
server = "" # Nome do servidor de banco de dados
database = "" # Nome do banco de dados
username = '' # Usuário
password = '' # Senha
if len(sys.argv) < 4:
    print('Processo interrompido! Informe os parâmetros corretamente, por favor.')
    sys.exit()
else:    
    server = sys.argv[1]
    database = sys.argv[2]
    username = sys.argv[3]
    password = sys.argv[4]

# Definir a string de conexão com o banco de dados usando usuário e senha.
conn_string = f"DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}" 

# Conectar-se ao banco de dados.
conn = pyodbc.connect(conn_string) 

# Definir consulta sql.
query = "select top 10 clie_cd_codigo, clie_tx_nome, clie_tx_enderecos from tb_clientes " 

# Obter a lista de clientes através de um cursor.
cursor = conn.cursor() 
cursor.execute(query)

# Obter nomes dos campos.
column_names = [i[0] for i in cursor.description]

data = []

# Adicionar nomes dos campos a um array.
data.append(column_names)

# Adicionar cada registro do cursor no array.
x = 1
for row in cursor: 
    data.append([row[0], row[1], str(row[2])])
    x += 1

# Adicionar conteúdo do array a um dataframe pandas.
df = pd.DataFrame(data)

# Exportar conteúdo do dataframe para um arquivo no formato CSV.
df.to_csv(r'lista_clientes1.csv', index=False, header=False)

# Método alternativo: Inserir o conteúdo da consulta direto no dataframe Pandas, sem precisar do cursor.
df2 = pd.read_sql(query, conn) 
# Exportar para CSV.
df2.to_csv(r'lista_clientes2.csv', index=False, header=False)

# Fecha a conexão do banco.
conn.close()
