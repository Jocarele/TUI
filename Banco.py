from abc import ABC,abstractmethod
from ConnectionTUI import ConnectionTUI

class Banco(ABC):
  def __init__(self, _con):
    self.ConData = _con
    self.DBCon = None
    self.cursor = None

    match _con.getDBMS():
      case None:
        self.DBMSName = "SQLite"
      case 1:
        self.DBMSName = "MySQL"
      case 2:
        self.DBMSName = "PostgreSQL"

  def getConData(self):
    return self.ConData

  @abstractmethod
  def setDBCon(self):
    pass

  def executeQuery(self, query):
    querySplit = query.split()

    if(querySplit[0].lower() == "select"):
      try:
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        columns = self.cursor.description

        list = []

        for row in rows:
          obj = {}
          for i in range(0, len (columns)):
            obj[columns[i][0]] = row[i] # columns[i][0] -> indice 0 é o nome da coluna

          list.append(obj)

        return list
      except:
        print("Erro ao executar query. (1)(" + self.DBMSName + ")\nQuery: " + query)
        exit (1)
    else:
      try:
        self.cursor.execute(query)
        self.DBCon.commit()
      except:
        self.DBCon.rollback()
        print("Erro ao executar query. (2)(" + self.DBMSName + ")\nQuery: " + query)
        exit (1)

    return None

  def setCursor(self):
    self.cursor = self.DBCon.cursor()

  def closeConn(self):
    self.DBCon.close()