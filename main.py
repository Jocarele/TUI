from os import system
from MySQLdb_tui import MySQLdb_tui
from PostgreSQL import PostgreSQL
from SQLite import SQLite
from ConnectionTUI import ConnectionTUI
from node import Node
from tabulate import tabulate

#
# Variaveis globais
#
# TODO: [low] listar todas as variaveis globais aqui
gConDataSQLite = ConnectionTUI(None, None, None, None, "tui.db", None)
g_SQLite = None

g_connectionsTUI = []

g_erro = ""

#
# menu inicial -> exibe 'Conexoes'
#
def menu1():
  global g_erro
  global g_connectionsTUI

  system("clear")
  print("====================================")

  if len(g_erro) > 0:
    print(f"\n\tERRO: {g_erro}\n")

  print("Conexoes: ")
  print(" 0 - Criar nova conexao")
  
  for i in range(0, len(g_connectionsTUI)):
    print(f" {i+1} - {g_connectionsTUI[i]}")

  print("-1 - Sair")
  print("\nSelecione uma das opcoes: ")

#
# menu 'funcionalidades'
#
def menu2():
  global g_erro
  
  system("clear")
  print("====================================")

  if len(g_erro) > 0:
    print(f"\n\tERRO: {g_erro}\n")

  print(" 0 - Voltar")
  print(" 1 - listar estrutura da base")
  print(" 2 - buscar dados de uma tabela/view")
  print(" 3 - executar query")
  print(" 4 - Configuracoes")
  print(" 5 - Exportar dados em CSV")
  print("-1 - Sair ")
  print("\nSelecione uma das opcoes: ")

#
# submenu ~ lista tabelas
#
def menu3():
  global g_erro
  global g_no
  system("clear")
  print("====================================")

  if len(g_erro) > 0:
    print(f"\n\tERRO: {g_erro}\n")

  l_tam = len(g_no.children)
  print(" 0 - Voltar")
  for i in range(0,l_tam):
    print(f"{str(i+1):>2} - {g_no.children[i].value}")
  
  print("-1 - Sair ")
  print("\nSelecione uma das opcoes: ")
  
#
#
#
def readConnectionsTUI():
  global g_SQLite
  l_rowsDict = g_SQLite.executeQuery("SELECT * FROM conexao;")

  listaObjs = []    

  for row in l_rowsDict:
    listaObjs.append(
      ConnectionTUI(
        row["ID"],
        row["host"],
        row["username"],
        row["password"],
        row["database"],
        row["dbms"],
      )
    )

  return listaObjs

#
#
#
def addConnectionTUI():
  global g_erro
  system("clear")
  print("============ Nova Conexao ============")

  try:
    print("Digite o DBMS (1 - MySQL; 2 - PostgreSQL): ")
    l_dbms = int(input())

    print("Digite o Host: ")
    l_host = input()

    print("Digite o usuario: ")
    l_username = input()

    print("Digite a senha: ")
    l_password = input()

    print("Digite o nome da base: ")

    l_database = input()

    # TODO: [low] verificar se é uma conexao valida

    l_query = f"INSERT INTO conexao (host, username, password, database, dbms) VALUES ('{l_host}', '{l_username}', '{l_password}', '{l_database}', {l_dbms})"

    l_result = g_SQLite.executeQuery(l_query)
    
    if (l_result == None):
      g_erro = "Nao foi possivel cadastrar!"
    else:
      g_erro = "Nova conexao cadastrada com sucesso!"

  except:
    g_erro = "Falha ao cadastrar nova conexao."

#
#
#
def crateTree():
  global g_db
  global g_no
  

 

  if(g_db.getConData().getDBMS()==1):
    l_lista = g_db.executeQuery("SELECT t.table_name AS tabela, group_concat(concat(c.column_name,' - ',c.data_type)) AS campos FROM information_schema.tables t JOIN information_schema.columns c ON (t.table_name = c.table_name) WHERE t.table_schema = 'university' GROUP BY t.table_name;") 
  else:
    l_lista = g_db.executeQuery("SELECT t.table_name AS tabela, string_agg(c.column_name||' - '||c.data_type, ',') AS campos FROM information_schema.tables t JOIN information_schema.columns c ON (t.table_name = c.table_name) WHERE t.table_catalog = 'university' AND t.table_schema NOT IN ('pg_catalog', 'information_schema') GROUP BY t.table_name;") 

  g_no = Node(g_db.getConData().getDatabase())
  j=0
  for l_dict in l_lista:
    l_key = list(l_dict.keys())
    l_listaValue = l_dict[l_key[1]]
    valueSplit = l_listaValue.split(",")
    g_no.makeChildren(Node(l_dict[l_key[0]]))
    for value in valueSplit:
      g_no.children[j].makeChildren(Node(value))
    j +=1

#  
#  
#  
def tabelizar(l_query):
  if(l_query == None):
    pass
  l_tableDict = {}
  l_listaChaves = list(l_query[0].keys())

  for i in l_listaChaves:
    l_tableDict[i] = []
  
  for dict in l_query:
    for key in dict:
      l_tableDict[key].append(dict[key]) 
  print(tabulate(l_tableDict, headers="keys",tablefmt="presto"))  

#
# exporta um arquivo CSV
#
def exportCSV(p_rows, p_file):
  global g_no
  global g_db

  # busca os dados da tabela
  # rows = g_db.executeQuery(p_query)

  if (len(p_rows) > 0):
    # escreve no arq
    with open(p_file, 'w') as writer:
      # printa nome das colunas
      for col in list(p_rows[0].keys()):
        writer.write(f"{col};")
      writer.write("\n")
      
      # printa os dados
      for r in p_rows:
        for v in list(r.values()):
          writer.write(f"{str(v)};")
        writer.write("\n")
      system("clear")
      print(f"Arquivo {p_file} criado!")

#
# funcao principal
#
def main():
  global g_connectionsTUI
  global g_SQLite
  global g_erro
  global g_limit
  global g_no
  global g_db
  global g_counter

  g_counter = 1

  g_limit = 1000
  g_SQLite = SQLite(gConDataSQLite)

  l_op_selecionada1 = -9

  while l_op_selecionada1 != -1:
    g_connectionsTUI = readConnectionsTUI()
    menu1()

    try:
      l_op_selecionada1 = int(input())
    except:
      g_erro = "Opcao invalida!"
      continue

    g_erro = ""

    match l_op_selecionada1:
      case 0: # cadastrar nova conexao
        addConnectionTUI()
        pass
      case -1: # sair
        pass
      case _: # selecionou algum dos bancos
        if (l_op_selecionada1 >= 1 and l_op_selecionada1 <= len(g_connectionsTUI)):
          # TODO: [low] colocar em uma funcao separada
          g_db = None
          sel = l_op_selecionada1 - 1

          try:
            if(g_connectionsTUI[sel].getDBMS()== 1):
              g_db = MySQLdb_tui(g_connectionsTUI[sel])
            else:
              g_db = PostgreSQL(g_connectionsTUI[sel])
          except:
            g_erro = f"FALHA AO CONECTAR - {g_connectionsTUI[sel]}"
            l_op_selecionada1 = -9
            continue

          crateTree()

          l_op_selecionada2 = -9

          while l_op_selecionada2 != -1 and l_op_selecionada2 != 0:
            menu2()
            
            try : 
              l_op_selecionada2 = int(input())
            except:
              g_erro = "Opção invalida"
              continue

            match l_op_selecionada2:
              case 0: # voltar
                g_db.closeConn()
                g_db = None

              case 1: # mostra estrutura em arvore
                system("clear")
                print(g_no)
                print ("\nPressione ENTER para voltar ao menu...")
                input()

              case 2: # listar dados de uma tabela
                l_op_selecionada3 = -9
                while(l_op_selecionada3 != -1 and l_op_selecionada3 != 0):
                  menu3()
                  try:
                    l_op_selecionada3 =int(input())
                  except:
                    g_erro = "Opção invalida"
                  
                  match l_op_selecionada3:
                    case 0:
                      pass
                    case -1:
                      exit()
                    case _:
                      tam = len(g_no.children)+1
                      if (l_op_selecionada3 >= 1 and l_op_selecionada3 <= tam):
                        lista3 = g_db.executeQuery("select * from "+ g_no.children[l_op_selecionada3-1].value + " limit " +str(g_limit)+";")
                        tabelizar(lista3)
                        print("Pressione ENTER para voltar ao menu...")
                        input()
                      else:
                        g_erro = "Opção selecionada é invalida"
                        continue
              case 3: # executar SQL
                l_sql = ""
                l_ponto_virgula = l_sql.find(";")
                
                print("Digite a query: ")
                
                while(l_ponto_virgula == -1):
                  l_sql += input() + " "
                  l_ponto_virgula = l_sql.find(";")

                l_sql = l_sql[0:l_ponto_virgula]
                l_sql += " limit " + str(g_limit) + ";"
                query = g_db.executeQuery(l_sql)

                if(query != None):
                  tabelizar(query)

                  print("Deseja salvar em CSV: ")
                  salvar =input("s para sim ")
                  if(salvar == "s"):
                    exportCSV(query, f"query-{g_counter}.csv")
                    g_counter += 1

                print("Pressione ENTER para retornar ao menu.")
                input()

              case 4: # config LIMIT
                g_limit = -1
                while (g_limit < 1):
                  try:
                    g_limit =int(input("Digite o novo valor para limitar o print: "))
                  except:
                    print ("Valor digitado invalido.")

              case 5: # exportar CSV
                l_op_selecionada3 = -9
                while(l_op_selecionada3 != -1 and l_op_selecionada3 != 0):
                  menu3()

                  try:
                    l_op_selecionada3 = int(input())
                  except:
                    g_erro = "Opção invalida"
                    continue

                  g_erro = ""
                  
                  match l_op_selecionada3:
                    case 0:
                      pass
                    case _:
                      if (l_op_selecionada3 >= 1 and l_op_selecionada3 <= len(g_no.children)):
                        l_table = g_no.children[l_op_selecionada3 - 1].value

                        l_sql = f"select * from {l_table} limit {g_limit};"

                        l_query = g_db.executeQuery(l_sql)
                        exportCSV(l_query, f"{l_table}.csv")

                        
                        print("Pressione ENTER para voltar ao menu...")
                        input()
                      else:
                        g_erro = "Opcao invalida!"

              case -1: #sair
                exit()

            g_erro = ""
        else:
          g_erro ="Opção invalida"

if __name__ == "__main__":
  main()

'''
#
# Anotacoes
#
TODO: printar estrutura em arvore (95%)
    # falta: mostrar PKs e tamanho da coluna
'''
