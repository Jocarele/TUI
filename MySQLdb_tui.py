from Banco import Banco
import pymysql as MySQLdb

class MySQLdb_tui(Banco):

  def __init__(self, _con):
    Banco.__init__(self, _con)
    self.setDBCon()
    self.setCursor()

  def setDBCon(self):
    self.DBCon = MySQLdb.connect(
      host     = self.getConData().getHost(),
      user     = self.getConData().getUsername(),
      password = self.getConData().getPassword(),
      database = self.getConData().getDatabase()
    )
