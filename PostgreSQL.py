import psycopg
from Banco import Banco

class PostgreSQL(Banco):

  def __init__(self, _con):
    Banco.__init__(self, _con)
    self.setDBCon()
    self.setCursor()

  
  def setDBCon(self):
    stiring = "postgresql://"+self.getConData().getUsername()+":"+self.getConData().getPassword()
    stiring += "@" + self.getConData().getHost() +"/"+ self.getConData().getDatabase()

    self.DBCon = psycopg.connect(stiring)
