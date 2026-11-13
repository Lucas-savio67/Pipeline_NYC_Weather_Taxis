from src.data_extraction.interfaces.extraction_interface import ExtractionInterface 
from src.data_extraction.implementations.json_extractor import JSONExtractorErrors 
from src.data_extraction.implementations.parquet_extractor import ParquetExtractorErrors
from typing import Any
import logging 
logger = logging.getLogger(__name__)

class DataExtraction: 
    def __init__(self, extraction:ExtractionInterface) -> None: 
        self.extraction = extraction 
    def extract_general_data(self, bucket_name:str,layer:str ) -> dict[str,Any]: 
        logger.info("Iniciando o fluxo de extração dos dados...")
        try :
            extraction= self.extraction.extract(bucket_name,layer)
            logger.info(f"Informações de extração: \nDados extraídos: {extraction.extracted_data} \nErros: {extraction.errors}")
            return extraction.real_extracted_data
        except (JSONExtractorErrors, ParquetExtractorErrors) as e: 
            logger.error(f"Erro crítico, impossível extrair os dados: {str(e)} ")
            return None 

        
            
