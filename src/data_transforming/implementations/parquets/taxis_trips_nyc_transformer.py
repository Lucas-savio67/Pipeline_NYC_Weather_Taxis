from src.data_transforming.interfaces.transformation_interface import TransformingInterface
from config.return_contracts.transforming_contract import TransformingInfo
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
    def transform(self, data: dict[str, pd.DataFrame]) -> TransformingInfo:
        all_errors = {}
        if not data: 
            logger.error("Erro, nenhum parquet referente a taxis_trips_nyc! ")
            raise TaxisTripsErrors("Erro, nenhum parquet referente a taxis_trips_nyc! ")
        if not self.rules: 
            logger.error('Erro, nenhuma regra de transformação de taxis_trips_nyc! ')
            raise TaxisTripsErrors('Erro, nenhuma regra de transformação de taxis_trips_nyc! ')
        taxis_trips_info =TransformingInfo()
        transformed = False
        try :
            logger.info("Iniciando o fluxo de transformação do parquet taxis_trips! ")
            df, errors = self.concatenate_dfs(data)
            if not errors: 
                transformed = True
            df, column_errors = self.create_new_columns(df, self.rules)
            all_errors = {'concatenation': errors, 'columns': column_errors}
            taxis_trips_info.real_transformed_data['yellow_taxis_trips'] = df 
            taxis_trips_info.errors['yellow_taxis_trips'] = all_errors
            taxis_trips_info.transformed_data['yellow_taxis_trips'] = {'specific': transformed}
            taxis_trips_info.info['yellow_taxis_trips'] = {'info': {'tamanho': len(df) , 'tipos_colunas': df.dtypes.astype(str).to_list()}}
            return taxis_trips_info
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
    def create_new_columns(self, data:pd.DataFrame, rules:dict[str, dict]) -> pd.DataFrame: 
        new_columns = rules.get('new_columns', {})
        errors = {}
        if not new_columns: 
            logger.warning("Erro, as colunas novas não foram passadas! ")
            raise TaxisTripsErrors("Erro, as colunas novas não foram passadas! ")
        logger.info("Iniciando o fluxo de criação de colunas para taxis_trips...")
        for nome_coluna, regra_coluna in new_columns.items(): 
            coluna = regra_coluna['column']
            new_column_data= regra_coluna['column_data']
            if not coluna or not new_column_data: 
                logger.warning(f"Verifique se a coluna a mapear ou informações da coluna {nome_coluna} foram passadas! ")
                errors[nome_coluna] = {'error': 'no_info'}
            else:
                data[nome_coluna] = data[coluna].astype(str).map(new_column_data)
                logger.info(f'A coluna {nome_coluna} foi criada, valores: {data[nome_coluna].unique()}')
        return data, errors
        
        