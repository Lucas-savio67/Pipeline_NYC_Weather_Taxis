from src.data_extraction.interfaces.extraction_interface import ExtractionInterface 
from typing import Any
import logging 
logger = logging.getLogger(__name__)
class DataReadingErrors(Exception): 
    pass
class DataExtraction: 
    def __init__(self, extraction:ExtractionInterface) -> None: 
        self.extraction = extraction 
    def extract_general_data(self, bucket_name:str,layer:str ) -> dict[str,Any]: 
        logger.info("Iniciando o fluxo de extração dos dados...")
        try :
            extracted_data, errors = self.extraction.extract(bucket_name,layer)
            if errors: 
                logger.warning(f'Arquivos que deram erro na extração: {errors}')
            logger.info(f"Arquivos extraídos com sucesso: {extracted_data.keys()}")
            return extracted_data 
        except Exception as e: 
            logger.error(f"Erro crítico, impossível extrair os dados: {str(e)} ")
            return {}
        
            
