from abc import ABC, abstractmethod 
class IngestionInterface(ABC): 
    @abstractmethod
    def save(self, path:str, data:dict) -> str: 
        pass 