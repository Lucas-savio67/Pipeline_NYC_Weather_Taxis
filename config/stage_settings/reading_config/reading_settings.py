from src.data_reading.data_reading import DataReading
from typing import Any
import logging
logger= logging.getLogger(__name__)
class ReadingOrchestration(): 
    def __init__(self, data_reading:DataReading) -> None: 
        self.reading = data_reading
    def orchestrate_reading(self, implementations:dict[str,Any]) -> dict: 
        read_data = {}
        try :
            for nome, implementation in implementations.items(): 
                read = self.reading(implementation).read_general_data() 
                read_data[nome] = read
            return read_data  
        except Exception as e:
            logger.warning(f"Erro: {str(e)} ao fazer a leitura de dados! ")

