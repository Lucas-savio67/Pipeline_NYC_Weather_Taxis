from src.data_transforming.interfaces.transformation_interface import TransformingInterface
from utils.schema_validator import validate_schema
from typing import Any
import pandas as pd
import logging 
logger = logging.getLogger(__name__)
class TaxisTripsErrors(Exception): 
    pass 
class TaxisTripsTransformer(TransformingInterface[dict[str,pd.DataFrame]]): 
    def __init__(self, schema_validator:validate_schema, taxis_trips_rules:dict[str,Any]) -> None: 
        self.schema_validator = schema_validator
        self.rules = taxis_trips_rules
    def transform(self, data: dict[str, pd.DataFrame]) -> tuple[pd.DataFrame, dict[str, dict]]:
        extracted_data = {}
        if not data: 
            logger.error("Erro, nenhum parquet referente a taxis_trips_nyc! ")
            raise TaxisTripsErrors("Erro, nenhum parquet referente a taxis_trips_nyc! ")
        if not self.rules: 
            logger.error('Erro, nenhuma regra de transformação de taxis_trips_nyc! ')
            raise TaxisTripsErrors('Erro, nenhuma regra de transformação de taxis_trips_nyc! ')
        try :
            logger.info("Iniciando o fluxo de transformação do parquet taxis_trips! ")
            df, errors = self.concatenate_dfs(data)
            extracted_data['yellow_taxis_trips'] = df
            return extracted_data, errors 
        except TaxisTripsErrors as e: 
            logger.warning(f'Erro crítico {str(e)} impossibilitou a transformação do parquet taxis_trips_nyc! ')
            raise TaxisTripsErrors(f"Erro crítico {str(e)} impossibilitou a transformação do parquet taxis_trips_nyc! ")
    def concatenate_dfs(self, data: dict[str, pd.DataFrame]) -> tuple[pd.DataFrame, dict[str,dict]]:
        errors = {}
        valid_dfs = []
        logger.info("Inciando o fluxo de concatenação de DFs referentes a taxis_trips_nyc...")
        
        for nome, df in data.items(): 
                valid, difference = self.schema_validator(df, self.rules)
                if valid :
                    valid_dfs.append(df)
                else: 
                    logger.warning(f"O DF {nome} possui alguma difereça em relação aos requerimentos: {difference}")
                    errors[nome] = {'error': difference}
                    
        if not valid_dfs: 
            logger.error('Erro, nenhum DataFrame pode ser concatenado! ')
            raise TaxisTripsErrors("Erro, nenhum DataFrame pode ser concatenado! ")
        df = pd.concat(valid_dfs, ignore_index=True)
        return df, errors
        
        