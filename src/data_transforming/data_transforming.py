from src.data_transforming.interfaces.transformation_interface import TransformingInterface 
from typing import Any 
import logging 
import pandas as pd
logger = logging.getLogger(__name__)
class DataTransforming: 
    def __init__(self, interface:TransformingInterface[Any]) -> None: 
        self.interface = interface 
    def transform_general_data(self, data:Any, nome:str) -> Any:
        try :
            transformed_data, errors = self.interface.transform(data)
            if errors: 
                logger.warning(f"Erros de transformação de {nome}: {errors}! ")
            logger.info(f"Dados transformados com sucesso: {transformed_data.keys()}")
            return transformed_data
        except Exception as e: 
            logger.error(f"Erro crítico {e} impossibilitou {nome} de realizar transformações específicas! ")


