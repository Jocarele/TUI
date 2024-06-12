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
        self.cursor = self.db.cursor(cursor_factory=DictCursor)
        
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
            data =self.cursor.fetchall()
            total_fields = self.cursor.description  
            for reg in data:
                stiring = ""    
                for i in total_fields:
                    stiring += " " + str(i[0]) + " = " + str(reg[i[0]])
                print(stiring)
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
        self.db = psycopg.connect(host =self.host,user = self.username, password = self.password, database = self.database)

       
    


