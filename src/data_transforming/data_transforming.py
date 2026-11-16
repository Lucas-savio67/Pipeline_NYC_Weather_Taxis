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
            transforming = self.interface.transform(data)
            logger.info(f'Informações de Transformação: \nErros: {transforming.errors} \nDados transformados: {transforming.transformed_data} \n Info dos dados: {transforming.info}')
            return transforming.real_transformed_data
        except Exception as e: 
            logger.error(f"Erro crítico {e} impossibilitou {nome} de realizar transformações!  ")


