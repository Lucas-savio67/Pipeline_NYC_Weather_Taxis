from src.data_ingestion.data_ingestion import DataIngestion
from typing import Any
import logging 
logger = logging.getLogger(__name__)
class IngestionOrchestration: 
    def __init__(self, data_ingestion:DataIngestion) -> None: 
        self.ingestion = data_ingestion 
    def orchestrate_ingestion(self, implementations:dict[str, Any]) -> str: 
        
        for model in implementations.values(): 
            self.ingestion(model.implementation).ingest_general_data(model.layer,model.data, model.bucket_name)
        return 'Orquestração de ingestão dos dados finalizada com sucesso! '
        
    