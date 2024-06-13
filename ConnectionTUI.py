class ConnectionTUI():
  def __init__(self, _id, _host, _username, _password, _database, _dbms):
    self.id       = _id
    self.host     = _host
    self.username = _username
    self.password = _password
    self.database = _database
    self.dbms     = _dbms

  def getId(self):
    return self.id

  def getHost(self):
    return self.host

  def getUsername(self):
    return self.username

  def getPassword(self):
    return self.password

  def getDatabase(self):
    return self.database

  def getDBMS(self):
    return self.dbms

  def __str__(self):
    return f"{self.username}@{self.host} [{self.database}]"
