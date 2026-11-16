from abc import ABC, abstractmethod 
from config.return_contracts.ingestion_contract import IngestionInfo
class IngestionInterface(ABC): 
    @abstractmethod
    def save(self, layer:str, data:dict, bucket_name:str) -> IngestionInfo: 
        pass 