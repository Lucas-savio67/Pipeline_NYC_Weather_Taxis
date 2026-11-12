from dataclasses import dataclass
from src.data_extraction.interfaces.extraction_interface import ExtractionInterface 
@dataclass(frozen=True)
class ExtractionModel: 
    implementation:ExtractionInterface
    bucket_name:str 
    layer:str 