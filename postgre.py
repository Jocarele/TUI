import psycopg
from bancos import banco

class postgre_class(banco):

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

    def queries(self):
        pass

    def att(self):
        pass

    
    def set_db(self):
        self.db = psycopg.connect(host =self.host,user = self.username, password = self.password, database = self.database)

       
    


