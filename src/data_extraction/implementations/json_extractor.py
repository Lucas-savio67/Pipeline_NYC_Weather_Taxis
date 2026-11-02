from src.data_extraction.interfaces.extraction_interface import ExtractionInterface
import logging 
from mypy_boto3_s3 import S3Client
from botocore.exceptions import ClientError 

from typing import Any
import json
logger=  logging.getLogger(__name__)
class JSONExtractorErrors(Exception): 
    pass
class JsonExtractor(ExtractionInterface): 
    def __init__(self, s3_client:S3Client) -> None : 
        self.client = s3_client
    def extract(self, bucket_name, layer) -> tuple[dict[str, Any], dict[str,dict]]:
        extracted_json = {}
        errors = {}
        logger.info("Iniciando a extração de arquivos JSON do S3... ")
        try :
            paginator = self.client.get_paginator('list_objects_v2')
            pages = paginator.paginate(Bucket=bucket_name, Prefix=f'{layer}/JSONs/')
            for page in pages: 
                if 'Contents' in page:
                    for objeto in page['Contents']:
                        try :
                            caminho_s3 = objeto['Key']
                            response = self.client.get_object(Bucket=bucket_name ,Key= caminho_s3)
                            json_content = json.loads(response['Body'].read().decode('utf-8'))
                            extracted_json[caminho_s3] = json_content
                            logger.info(f"O JSON referente a {caminho_s3} foi extraído com sucesso! ")
                        except json.JSONDecodeError as e : 
                            logger.warning(f"Erro decodificar o JSON {caminho_s3}, {str(e)}")
                            errors[caminho_s3] = {'error': str(e)}
                        except (TypeError, AttributeError) as e : 
                            logger.warning(f"Erro, JSON {caminho_s3} com Body ausente ou incopatível com o método read(): {str(e)}! ")
                            errors[caminho_s3] = {'error': str(e)}
                        except UnicodeDecodeError as e: 
                            logger.warning(f"Erro de decodificação para o JSON {caminho_s3}! ")
                            errors[caminho_s3] = {'error': str(e)}
                        except ClientError as e : 
                            logger.warning(f'Erro ao obter o objeto {caminho_s3}: {str(e)} ')
                            errors[caminho_s3] = {'error': str(e)}
                else: 
                    logger.warning(f"Nenhum objeto foi encontrado na página: {page}! ")
                    errors['empty_page'] = {'error': 'No_object'}
        except ClientError as e: 
            logger.warning(f"Erro ao listar os objetos: {str(e)}")
            raise JSONExtractorErrors(f"Erro ao listar os objetos: {str(e)}")
        logger.info("Finalizando o fluxo de extração de JSONs...")
        return extracted_json, errors