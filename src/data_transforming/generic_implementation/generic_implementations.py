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
        if not fill_null_columns: 
            null_info['qtd_nulos'] = df.isna().sum().sum()
            logger.warning(f"Preenchimento de nulos não existe para {nome}, pulando...")
            return df, null_info, null_errors
        logger.info(f"Iniciando o fluxo de preenchimento de nulos de {df}! ")
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
    def rename_columns(self,df :pd.DataFrame, nome:str) -> tuple[pd.DataFrame, dict[str,Any], dict[str,dict]]: 
        columns_to_rename = self.rules.get('columns_to_rename', {}) 
        rename_columns_info = {}
        rename_columns_errors = {}
        if not columns_to_rename: 
            logger.warning(f"Renomeação de colunas não existe para {nome}, pulando...")
            rename_columns_info['renomeação_colunas'] = {'nomes': df.columns.to_list()}
            return df, rename_columns_info, rename_columns_errors
        logger.info(f"Iniciando o fluxo de renoemação de colunas de {df}! ")
        antes = df.columns.to_list()
        for nome_antigo, nome_novo in columns_to_rename.items(): 
            if nome_antigo not in antes: 
                logger.warning(f"Erro, a coluna {nome_antigo} não existe em {nome}! ")
                rename_columns_errors[nome_antigo] = {'error': nome_antigo}
            else: 
                df = df.rename(columns={nome_antigo:nome_novo}, errors='raise')
        logger.info(f'Finalizando o fluxo de renoemação de colunas de {nome}! ')
        rename_columns_info['renomeação_colunas'] = {'antes': antes, 'depois': df.columns.to_list()}
        return df, rename_columns_info, rename_columns_errors
        
