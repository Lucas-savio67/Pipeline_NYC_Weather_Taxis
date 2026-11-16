from dataclasses import dataclass 

@dataclass(frozen=True)
class IngestionInfo: 
    ingested_data:dict[str,bool]
    errors:dict[str,dict[str]]