from os import system
from MySQLdb_tui import MySQLdb_tui
from PostgreSQL import PostgreSQL
from SQLite import SQLite
from ConnectionTUI import ConnectionTUI

#
# Variaveis globais
#
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

  print(" 1 - listar estrutura da base")
  print(" 2 - buscar dados de uma tabela/view")
  print(" 3 - executar query")
  print(" 4 - Configuracoes")
  print("-1 - Sair")
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

    # TODO: impedir SQL Injection
    '''
      Boas pessoas não precisam de leis para obrigá-las a agir responsavelmente,
      enquanto as pessoas ruins encontrarão um modo de contornar as leis.
                                                                        - Platao
    '''
    l_query = f"INSERT INTO conexao (host, username, password, database, dbms) VALUES ('{l_host}', '{l_username}', '{l_password}', '{l_database}', {l_dbms})"

    g_SQLite.executeQuery(l_query)
    # TODO: verificar se inseriu
  except:
    g_erro = "Falha ao cadastrar nova conexao."

#
#
#
def main():
  global g_connectionsTUI
  global g_SQLite
  global g_erro

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
          l_db = None
          sel = l_op_selecionada1 - 1

          if(g_connectionsTUI[sel].getDBMS()== 1):
            l_db = MySQLdb_tui(g_connectionsTUI[sel])
          else:
            l_db = PostgreSQL(g_connectionsTUI[sel])

          l_op_selecionada2 = -9

          while l_op_selecionada2 != -1:
            menu2()
            
            try : 
              l_op_selecionada2 = int(input())
            except:
              g_erro = "Opção invalida"
              continue
            match l_op_selecionada2:
              case -1: # sair
                l_db.closeConn()
                l_db = None
                pass
              case 3:
                students = l_db.executeQuery("select * from student limit 10;")

                for s in students:
                  print(s)
                
                print("Pressione ENTER para retornar ao menu.")
                input()

            g_erro = ""
        else:
          g_erro ="Opção invalida"

if __name__ == "__main__":
  main()

'''
#
# Anotacoes
#
TODO: ... funcionalidades
  TODO: printar estrutura em arvore
      # nao sei

  TODO: ver dados de uma certa tabela
      # listar tabelas/views da base e pedir para o usuario selecionar

  TODO: executar SQL (consultas apenas)
      # 50% feito, falta formatar saída e tratar erros

  TODO: configurar limite de print

  TODO: exportar dados em CSV
      # postgresql -> usar COPY
      # mysql -> SELECT * FROM data.employees INTO OUTFILE 'employees.csv';
'''
