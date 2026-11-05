from src.data_transforming.interfaces.transformation_interface import TransformingInterface 
from typing import Any
import logging 
logger = logging.getLogger(__name__)
import pandas as pd
class NasaPowerErrors(Exception): 
    pass
class NasaPowerTransformation(TransformingInterface): 
    def __init__(self, nasa_power_rules:dict[str,Any]) -> None: 
        self.rules = nasa_power_rules 
    def transform(self, data:Any, nome:str ) -> tuple[dict[str,pd.DataFrame], dict[str,dict]]:
        critical_error = {}
        normal_errors = {}
        if not data or data is None: 
            raise NasaPowerErrors(f"Erro, não há nenhuma dado referente a: {nome}! ")
        try :
            transformed_data = {}
            logger.info("Iniciando o fluxo de transformação do JSON NasaPower! ")
            
            df = self.structure_json(data, self.rules)
            df, errors = self.create_datetime_column(df, self.rules)
            transformed_data['NasaPower'] = df 
            logger.info("Fluxo de transformação do JSON NasaPower finalizado! ")

            return transformed_data, errors
        except NasaPowerTransformation: 
            critical_error['NasaPower'] = {'error': 'Não foi possível estruturar o JSON NasaPower! '}
            return critical_error 
            

        
    def structure_json(self, data:dict, rules:dict[str,Any]) -> tuple[pd.DataFrame, dict[str,dict]] : 
        logger.info('Estruturando o JSON NasaPower...')
        
        try :
            important_columns = rules.get('important_columns', [])
            if not important_columns: 
                raise NasaPowerErrors("Erro, parece que as colunas importantes para estruturação não foram passadas! ")
            df = pd.DataFrame(data[important_columns[0]][important_columns[1]])
            df.index.name = important_columns[2]
            df = df.reset_index()
            return df 
        except (KeyError,IndexError, ValueError, TypeError) as e: 
            logger.warning(f"Erro: {str(e)}! ")
            raise NasaPowerErrors(f'O erro {str(e)} impossibilitou a estrutuação de NasaPower! ')
            
        
        
    def create_datetime_column(self, df:pd.DataFrame, rules:dict[str,Any]) -> tuple[pd.DataFrame, dict[str,dict]]: 
        errors = {}  
        coluna_datas = rules.get('datetime_columns', {})
        logger.info("Tratando colunas de data de NasaPower! ")
        if not coluna_datas: 
            logger.warning("Erro, as colunas de data não foram passadas, verifique as regras de NasaPower! ")
            raise NasaPowerErrors('Erro, as colunas de data não foram passadas, verifique as regras de NasaPower! ')
        for nome, format in coluna_datas.items(): 
            try :
                df[nome] = pd.to_datetime(df[nome], format=format['format'])
                logger.info(f"A coluna {nome} foi transformada em datetime com seu respectivo formato! ")
            except KeyError as e : 
                logger.warning(f"Parece que a coluna {nome} não está no DF! ")
                errors[nome] = {'error': str(e)}
            except ValueError as e: 
                logger.warning(f"Erro, a coluna {nome} não é compatível com o formato fornecido! ")
                errors[nome] = {'error': str(e)}
        logger.info("Fluxo de tratameno de colunas datetime terminando! ")
        return df, errors
        


        