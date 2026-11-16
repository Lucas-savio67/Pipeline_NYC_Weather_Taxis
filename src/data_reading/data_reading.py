from src.data_reading.interfaces.reading_interface import ReadingInterface
from src.data_reading.implementations.api_reading import APIReadingErrors
from typing import Any
import logging 
logger = logging.getLogger(__name__)

class DataReading: 
    def __init__(self, data_reading:ReadingInterface) -> None: 
        self.data_reading = data_reading 
    def read_general_data(self) -> dict[str, Any]: 
        logger.info("Iniciando a leitura dos dados! ")
        try:
            leitura  = self.data_reading.read_data()
            logger.info(f"Informações de leitura: \n'Dados lidos: {leitura.read_data} \nErros: {leitura.errors}")
            return leitura.real_read_data
        except APIReadingErrors as e: 
            logger.error(f"Erro crítico: {str(e)}! ")
            return None 
    
        