from abc import ABC, abstractmethod 
class IngestionInterface(ABC): 
    @abstractmethod
    def save(self, layer:str, data:dict, bucket_name:str) -> str: 
        pass 