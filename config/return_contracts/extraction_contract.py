from dataclasses import dataclass 
from typing import Any
@dataclass(frozen=True)
class ExtractionInfo: 
    real_extracted_data:dict[str, Any]
    extracted_data:dict[str,bool]
    errors:dict[str,dict[str]]