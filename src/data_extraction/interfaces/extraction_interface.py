from abc import ABC, abstractmethod 
from typing import Any
from config.return_contracts.extraction_contract import ExtractionInfo

class ExtractionInterface(ABC): 
    @abstractmethod 
    def extract(self, bucket_name: str, layer: str) -> ExtractionInfo:
        pass