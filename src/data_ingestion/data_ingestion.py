from src.data_ingestion.interfaces.ingestion_interface import IngestionInterface
import logging 
from src.data_ingestion.implementations.api_s3_ingestion import APIIngestionErrors 
from src.data_ingestion.implementations.parquet_ingestion import ParquetIngestionErrors
logger = logging.getLogger(__name__)
from typing import Any
class DataIngestion: 
    def __init__(self, data_ingestion:IngestionInterface) -> None: 
        self.data_ingestion = data_ingestion 
    def ingest_general_data(self, layer:str, data:dict[str,Any], bucket_name:str) -> str: 
        logger.info("Iniciando fluxo de ingestão dos dados...")
        try : 
            ingestion = self.data_ingestion.save(layer, data, bucket_name)
            logger.info(f"Infomações de ingestão na camada {layer}: \nDados injetados: {ingestion.ingested_data} \nErros: {ingestion.errors}")
            return 'Ingestão dos dados no S3 finalizada!'
        except (ParquetIngestionErrors, APIIngestionErrors) as e: 
            logger.warning(f"Erro crítico: {str(e)}")