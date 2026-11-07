from src.data_transforming.interfaces.transformation_interface import TransformingInterface
import pandas as pd 
import logging 
logger = logging.getLogger(__name__)
from typing import Any
class GenericTransformingErrors(Exception): 
    pass
class GenericTransforming(TransformingInterface[dict[str, pd.DataFrame]]): 
    def __init__(self, generic_rules:dict[str,Any]) -> None: 
        self.rules= generic_rules
    def transform(self, data:dict[str, pd.DataFrame]) -> tuple[dict[str,pd.DataFrame], dict[str,dict]]:
        all_errors = {}
        all_info = {}
        transformed_data = {}
        if not data: 
            logger.error("Erro, nenhum DF foi encontrado! ")
            raise GenericTransformingErrors('Erro, nenhum DF foi encontrado! ')
        logger.info(f"Iniciando o fluxo de transformações genéricas! ")
        for nome , df in data.items(): 
            logger.info(f"Iniciando as transformações genéricas de {nome}! ")
            df_rules = self.rules.get(nome)
            df,rp_info, rp_errors = self.remove_duplicates(df, nome, df_rules)
            df,fn_info, fn_errors = self.fill_null_values(df, nome, df_rules)
            df,rc_info,rc_errors = self.rename_columns(df, nome, df_rules)
            logger.info(f"Finalizando o fluxo de trtansformações genéricas de {nome}! ")
            all_errors[nome] = {'errors': [rp_errors, fn_errors, rc_errors]}
            logger.info(f"Erros de {nome}: {all_errors}")
            all_info[nome] = {'info': [rp_info, fn_info, rc_info]}
            logger.info(f"Informações de transformações referentes a {nome}: {all_info}! ")
            transformed_data[nome] = {'data': df, 'errors': all_errors, 'info': all_info} 
        return transformed_data
    def fill_null_values(self,df :pd.DataFrame, nome:str, rules:Any) -> tuple[pd.DataFrame, dict[str,Any], dict[str,dict]]: 
        fill_null_columns = rules.get('fill_null_columns', [])
        null_info = {}
        null_errors = {}
        if not fill_null_columns: 
            null_info['qtd_nulos'] = {'nulos': df.isna().sum().sum()}
            logger.warning(f"Preenchimento de nulos não existe para {nome}, pulando...")
            return df, null_info, null_errors
        logger.info(f"Iniciando o fluxo de preenchimento de nulos de {nome}! ")
        antes = df.isna().sum().sum()
        for column, value in fill_null_columns.items(): 
            try: 
                df[column] = df[column].fillna(value) 
                nulos_coluna = df[column].isna().sum()
                logger.info(f'A coluna {column} teve seus valores nulos preenchidos, {nulos_coluna} valores nulos! ')
            except KeyError as e: 
                logger.warning(f"Erro, a coluna {column} não está no DF! ") 
                null_errors['error'] = {'column_name': str(e)}
            except TypeError as e: 
                logger.warning(f'Erro, o valor {value} é incompatível com a coluna {column}: {str(e)}!  ')
                null_errors['error'] = {'value_type': type(value)}
        logger.info(f'Finalizando o fluxo de preenchimento de nulos de {nome}! ')
        null_info['qtd_nulos'] = {'nulos_antes': antes, 'depois': df.isna().sum()}
        return df, null_info, null_errors 
    def rename_columns(self,df :pd.DataFrame, nome:str, rules:Any) -> tuple[pd.DataFrame, dict[str,Any], dict[str,dict]]: 
        columns_to_rename = rules.get('columns_to_rename', {}) 
        rename_columns_info = {}
        rename_columns_errors = {}
        if not columns_to_rename: 
            logger.warning(f"Renomeação de colunas não existe para {nome}, pulando...")
            rename_columns_info['renomeação_colunas'] = {'nomes': df.columns.to_list()}
            return df, rename_columns_info, rename_columns_errors
        logger.info(f"Iniciando o fluxo de renomemação de colunas de {df}! ")
        antes = df.columns.to_list()
        for nome_antigo, nome_novo in columns_to_rename.items(): 
            if nome_antigo not in antes: 
                logger.warning(f"Erro, a coluna {nome_antigo} não existe em {nome}! ")
                rename_columns_errors['error'] = {'wrong_name': nome_antigo}
            else: 
                df = df.rename(columns={nome_antigo:nome_novo}, errors='raise')
                logger.info(f'A coluna {nome_antigo} foi renomeada com sucesso! ')
        logger.info(f'Finalizando o fluxo de renoemação de colunas de {nome}! ')
        rename_columns_info['renomeação_colunas'] = {'antes': antes, 'depois': df.columns.to_list()}
        return df, rename_columns_info, rename_columns_errors
    def remove_duplicates(self,df :pd.DataFrame, nome:str, rules) -> tuple[pd.DataFrame, dict[str,Any], dict[str,dict]]: 
        drop_duplicates = rules.get('drop_duplicates', {}) 
        duplicates_info = {}
        duplicates_errors = {}
        if not drop_duplicates: 
            logger.warning(f"Exclusão de duplicatas não existe para {nome}, pulando...")
            duplicates_info['qtd_duplicatas'] = {'duplicatas': df.duplicated().sum()}
            return df, duplicates_info, duplicates_errors 
        antes = df.duplicated().sum()
        logger.info(f"Iniciando o fluxo de remoção de duplicatas de {nome}! ")
        try :
            for subset in drop_duplicates.values(): 
                if not subset:
                    df = df.drop_duplicates() 
                    logger.info(f"Removendo duplicatas de {nome} sem subset! ")
                else: 
                    df = df.drop_duplicates(subset=subset)
                    logger.info(f"Removendo duplicatas de {nome} com subset! ")
        except KeyError as e: 
            logger.warning(f"Erro, alguma coluna do subset não existe, veirifique: {str(e)}! ")
            duplicates_errors['error'] = {'wrong_column': str(e)}
        duplicates_info['qtd_duplicatas'] = {'antes': antes, 'depois': df.duplicated().sum()}
        logger.info("Finalizando o fluxo de remoção de duplicatas! ")
        return df, duplicates_info, duplicates_errors
