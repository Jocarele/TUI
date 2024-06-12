import sqlite3
from bancos import banco

class SQLite_class(banco):

     def __init__(self,host,username,password,database):
        self.username = username
        self.host = host
        self.password = password
        self.database = database 
        self.set_db()
        self.set_cursor()

    def get_cursor(self):
        return self.cursor

    def set_cursor(self):
        self.cursor = self.db.cursor()
        
    def get_db(self):
        return self.db

    def get_database(self):
        return self.database 
    
    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def get_host(self):
        return self.host

    def get_connection_info(self):
        list[3] = [self.get_host(),self.get_username(),self.get_password(),self.get_database]   
        return list
    
    #def set_database(self):
    #    pass

     def queries(self,sql):
          try:
               self.cursor.execute(sql)
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
                   
        except:
            print("VERIFIQUE O SQL NOVAMENTE")

    def att(self,sql):
        try:
            tuplas_afetadas = self.cursor.execute(sql)
            print("foram afetadas " + tuplas_afetadas + " tuplas")
            self.db.commit()
        except:
            self.db.rollback()
            print("VERIFIQUE O SQL NOVAMENTE")


    
    def set_db(self):
        self.db = sqlite3.connect(host =self.host,user = self.username, password = self.password, database = self.database)


    def instruction (self,sql):
        sql_split = sql.split()
        if(sql_split[0].lower() == "select"):
            self.queries(self,sql)
        else:
            self.att(self,sql)

       
    
    
