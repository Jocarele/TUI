import sqlite3
import pymysql as MySQLdb
import pymysql.cursors
import psycopg


    
    
    



def main():
    print("-----------------------------\n")
    #CONECTA AO BANCO DE DADOS SQLITE
    db_lite = sqlite3.connect('cnf_salvados.db')
    cursor_lite = db_lite.cursor()

    #ESCOLHE O BANCO DE DADOS A SER CONECTADO
    banco_de_dados = 0
    while (not(banco_de_dados == 1 or banco_de_dados == 2)):
        banco_de_dados=int(input("1-MYSQL \n2-Postgre? \n"))

    #MOSTRA AS OPÇÕES DE CONEXÕES
    print("Deseja utilizar uma conecção existente ou criar uma nova?\n")
    print("Conexões existentes: ")

    cursor_lite.execute("SELECT * from configuracoes;")
    data = cursor_lite.fetchall()

    i=0
    ID = []
    host = []
    username = []
    senha = []
    database = []

    for registro in data:
        ID.append(str(registro[0]))
        host.append(registro[1])
        username.append(registro[2])
        senha.append(registro[3])
        database.append(registro[4])
        print("ID = "+ID[i]+", Host = "+host[i]+", Username = "+username[i]+", Senha = "+senha[i]+", Database = "+database[i]+ "\n")
        i+=1
    ## ID começa em 1, mas indeces começam em 0
    opcao = int(input("Digite o ID se deseja utilizar um existente. Caso contrario digite 0\n"))
    opcao -=1

    if (opcao == -1):
        ID_new = i+1
        host_new = input("Digite o host: ")
        username_new = input("Digite o username: ")
        senha_new = input("DIgite sua senha: ")
        database_new = input("Digite seu banco de dados: ")
        
        #conecta a um banco de dados com nova configuração
        if(banco_de_dados == 1):
            db = MySQLdb.connect(host = host_new,user = username_new, password= senha_new, database =database_new)
            cursor_banco = db.cursor()
        elif (banco_de_dados == 2):
            db = psycopg.connect(host = host_new,database= database_new,user = username_new, password = senha_new)
            cursor_banco = db.cursor()

        #salva nova conexão no SQLite    
        salvar=input("Deseja salvar a conexão?\n 1 para sim,\n 2 para não.")
        if (salvar == "1"):
            try:
                cursor_lite.execute("INSERT INTO configuracoes VALUES('"+str(ID_new)+"','"+host_new+"','"+username_new+"','"+senha_new+"','"+database_new+"');")
                db_lite.commit()
            except:
                db_lite.rollback()

    #Conecta a um banco de dados com a configuração salva
    else:
        if(opcao >= 0 and opcao <= i):
            if(banco_de_dados == 1):
                db = MySQLdb.connect(host =host[opcao],user = username[opcao], password = senha[opcao], database = database[opcao])
                #cursor_banco = db.cursor()
                cursor_banco = db.cursor(pymysql.cursors.DictCursor)
                
                    
            elif(banco_de_dados == 2):
                db = psycopg.connect(host = host[opcao],database= database[opcao],user = username[opcao], password = senha[opcao])
                cursor_banco = db.cursor()    
            
    
    sql = input("Digite o comando que deseja em sql :")

    while (sql[-1]!=";"):
        sql2 = input()
        sql = sql + sql2

    sql_split = sql.split()
    print (sql_split[0])
    #VERIFICA A OPERAÇÃO A SER REALIZADA
    if(sql_split[0].lower() == "select"):
        try:

            cursor_banco.execute(sql)
            data =cursor_banco.fetchall()
            total_fields = cursor_banco.description  
           
            for reg in data:
               stiring = ""    
               for i in total_fields:
                    stiring += " " + str(i[0]) + " = " + str(reg[i[0]])
                
               print(stiring)    
            


            #for registro in data:
            #  print(registro)
        
        except:
            print("Algo foi digitado errado.")
        
    elif (sql_split[0].lower() == "delete"):
        print("delete")
    elif (sql_split[0].lower() == "insert"):
        print("insert")
    




if __name__ == "__main__":
    main()