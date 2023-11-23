import mysql.connector

conexao = mysql.connector.connect(
    host='localhost',
    database='mega',
    user='root',
    password=''
)

cursor = conexao.cursor()
cursor.execute('select database();')
linha = cursor.fetchone()
print('Banco conectado...')