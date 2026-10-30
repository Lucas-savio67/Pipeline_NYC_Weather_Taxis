from abc import ABC, abstractmethod 
class ReadingInterface(ABC): 
    @abstractmethod
    def read_data(self): 
        pass 
    