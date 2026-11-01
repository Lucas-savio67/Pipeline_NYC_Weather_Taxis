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
            logger.info("Fluxo de leitura dos dados finalizado! ")
            if leitura[1]:
                logger.warning(f'APIs com erro: {leitura[1]}')
            logger.info(f"APIs extraídas com sucesso: {leitura[0].keys()}")
            return leitura[0] 
        except Exception as e: 
            logger.warning(f"Erro crítico: {str(e)}! ")
    
        