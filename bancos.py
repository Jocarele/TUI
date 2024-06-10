from abc import ABC,abstractmethod

class banco(ABC):
    
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_cursor(self):
        pass
    
    @abstractmethod
    def set_cursor(self):
        pass
    @abstractmethod
    def get_db(self):
        pass

    @abstractmethod
    def get_database(self):
        pass 
    
    @abstractmethod
    def get_username(self):
        pass
    
    @abstractmethod
    def get_password(self):
        pass

    @abstractmethod
    def get_host(self):
        pass

    @abstractmethod
    def get_connection_info(self):
        pass
    
    
    #def set_database(self):
    #    pass

    @abstractmethod
    def queries(self):
        pass

    @abstractmethod
    def att(self):
        pass

    
    def set_db(self):
        pass
       
    


