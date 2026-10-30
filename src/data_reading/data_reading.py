from src.data_reading.interfaces.reading_interface import ReadingInterface
from typing import Any
import logging 
logger = logging.getLogger(__name__)
class DataReadingErrors(Exception): 
    pass
class DataReading: 
    def __init__(self, data_reading:ReadingInterface) -> None: 
        self.data_reading = data_reading 
    def read_general_data(self) -> dict[str, Any]: 
        logger.info("Iniciando a leitura dos dados! ")
        try:
            leitura  = self.data_reading.read_data()
            logger.info("FLuxo de leitura dos dados finalizado! ")
            return leitura 
        except Exception as e: 
            logger.warning(f"Erro crítico: {str(e)}! ")
    
        