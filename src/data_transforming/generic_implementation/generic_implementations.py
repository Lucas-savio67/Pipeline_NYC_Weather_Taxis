from src.data_transforming.interfaces.transformation_interface import TransformingInterface
import pandas as pd 
import logging 
logger = logging.getLogger(__name__)
from typing import Any
class GenericTransforming(TransformingInterface[dict[str, pd.DataFrame]]): 
    def __init__(self, generic_rules:dict[str,Any]) -> None: 
        self.rules= generic_rules
        self.errors:dict[str,dict] = {}
        self.info:dict[str,Any] = {}
    def transform(self, data:dict[str, pd.DataFrame]) -> tuple[dict[str,pd.DataFrame], dict[str,dict]]:
        pass 
    def fill_null_values(self,df :pd.DataFrame, nome:str) -> tuple[pd.DataFrame, dict[str,Any], dict[str,dict]]: 
        fill_null_columns = self.rules.get('fill_null_columns', [])
        null_info = {}
        null_errors = {}
        for column, value in fill_null_columns.items(): 
            try: 
                df[column] = df[column].fillna(value) 
                logger.info(f'A coluna {column} teve seus valores nulos preenchidos! ')
            except KeyError as e: 
                logger.warning(f"Erro, a coluna {column} não está no DF! ") 
                null_errors[column] = {'error': str(e)}
        logger.info(f"O DF {nome} teve seus valores nulos preenchidos com sucesso! ")
        null_info['qtd_nulos'] = df.isna().sum().sum()
        return df, null_info, null_errors 
    
