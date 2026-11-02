from src.data_extraction.interfaces.extraction_interface import ExtractionInterface
import logging 
logger = logging.getLogger(__name__)
import io 
import pandas as pd
from mypy_boto3_s3 import S3Client
from botocore.exceptions import ClientError
class ParquetExtractorErrors(Exception): 
    pass
class ParquetExtractor(ExtractionInterface): 
    def __init__(self, s3_client:S3Client) -> None: 
        self.client = s3_client 
    def extract(self, bucket_name, layer) -> tuple[dict[str,pd.DataFrame], dict[str,dict]]:
        extracted_parquets = {}
        errors = {}
        try : 
            logger.info("Iniciando o fluxo de extração de parquets...")
            paginator = self.client.get_paginator('list_objects_v2')
            pages = paginator.paginate(Bucket = bucket_name, Prefix=f'{layer}/parquets/')
            for page in pages: 
                if 'Contents' in page: 
                    for object in page['Contents']: 
                        try :
                            caminho_s3 = object['Key']
                            response = self.client.get_object(Bucket=bucket_name, Key=caminho_s3)
                            bytes_content = response['Body'].read()
                            df = pd.read_parquet(io.BytesIO(bytes_content), engine='pyarrow')
                            extracted_parquets[caminho_s3] = df 
                            logger.info(f"O parquet {caminho_s3} foi extraído e transformado em DataFrame com sucesso! ")
                        except ClientError as e: 
                            logger.warning(f'Erro ao obter o objeto {caminho_s3}: {str(e)} ')
                            errors[caminho_s3] = {'error': str(e)} 
                        except KeyError as e: 
                            logger.warning(f'Erro: {str(e)}')
                            errors['No_Key'] = {'error': 'No_Key'}
                        except (TypeError, OSError, AttributeError) as e: 
                            logger.warning(f'O corpo de {caminho_s3} não pôde ser lido: {str(e)}')
                            errors[caminho_s3] = {'error': str(e)}
                            
                        
        except ClientError as e: 
            logger.warning(f"Erro ao listar os objetos: {str(e)}")
            raise ParquetExtractorErrors(f'Erro ao listar os objetos: {str(e)}') 
        logger.info("Finalizando o fluxo de extração de arquivos Parquet...")
        return extracted_parquets, errors