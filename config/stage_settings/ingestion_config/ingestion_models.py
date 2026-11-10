from dataclasses import dataclass 
from typing import Any 
from src.data_ingestion.interfaces.ingestion_interface import IngestionInterface
@dataclass(frozen=True) 
class IngestionModel: 
    implementation:IngestionInterface 
    bucket_name:str 
    layer:str 
    data:dict[str,Any]