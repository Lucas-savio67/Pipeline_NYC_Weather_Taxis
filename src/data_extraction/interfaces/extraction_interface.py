from abc import ABC, abstractmethod 
class ExtractionInterface(ABC): 
    @abstractmethod 
    def extract(self, bucket_name:str, layer:str) -> dict: 
        pass