from src.data_ingestion.interfaces.ingestion_interface import IngestionInterface
import logging 
logger = logging.getLogger(__name__)
from typing import Any
class DataIngestion: 
    def __init__(self, data_ingestion:IngestionInterface) -> None: 
        self.data_ingestion = data_ingestion 
    def ingest_general_data(self, layer:str, data:dict[str,Any], bucket_name:str) -> str: 
        logger.info("Iniciando fluxo de ingestão dos dados...")
        try : 
            ingestion = self.data_ingestion.save(layer, data, bucket_name)
            if ingestion: 
                logger.warning(f'Dados com erro: {ingestion}')
            return 'Dados injetados no S3, verifique se algum deu erro! '
        except Exception as e: 
            logger.warning(f"Erro crítico: {str(e)}")
        logger.info("Finalizando fluxo de ingestão dos dados...")