import sqlite3
from Banco import Banco
from ConnectionTUI import ConnectionTUI

class SQLite(Banco):
  def __init__(self, _con):
    Banco.__init__(self, _con)
    self.setDBCon()
    self.setCursor()

  def setDBCon(self):
    self.DBCon = sqlite3.connect(self.getConData().getDatabase())
