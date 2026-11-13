from src.data_ingestion.interfaces.ingestion_interface import IngestionInterface
from config.return_contracts.ingestion_contract import IngestionInfo
import json
from mypy_boto3_s3 import S3Client
from botocore.exceptions import ClientError, BotoCoreError
import logging
logger = logging.getLogger(__name__)
class APIIngestionErrors(Exception): 
    pass
class APIS3Ingestion(IngestionInterface): 
    def __init__(self, s3_client:S3Client) -> None: 
        self.client = s3_client
    def save(self, layer, data, bucket_name) -> IngestionInfo:
        errors = {}
        ingested_data = {}
        if not data: 
            logger.error("Erro, nenhuma API foi lida! ")
            raise  APIIngestionErrors("Erro, nenhuma API foi lida! ")
        logger.info("Começando o fluxo de ingestão de APIs no bucket S3...")
        try :
            for nome, conteudo in data.items(): 
                ingested = False
                try :
                    file= f'{layer}/JSONs/{nome}/{nome}.json'
                    self.client.put_object(
                        Bucket=bucket_name , 
                        Key=file ,
                        Body=json.dumps(conteudo, ensure_ascii=False, indent=2)
                    ) 
                    ingested = True 
                except (TypeError, ValueError, UnicodeEncodeError) as e: 
                    logger.warning(f"Erro ao serializar os arquivo JSON {nome}: {str(e)}")
                    errors[nome] = str(e)
                ingested_data[nome] = ingested
        except ClientError as e: 
            logger.warning(f"Erro de cliente ao injetar as APIs para o bucket: {str(e)}")
            raise APIIngestionErrors(f'Erro de cliente ao injetar as APIs para o bucket: {str(e)}')
        except BotoCoreError as e:
            logger.warning(f'Erro botocore ao injetar as APIs para o bucket: {str(e)}')
            raise APIIngestionErrors(f'Erro botocore ao injetar as APIs para o bucket: {str(e)}')
        IngestionInfo.errors = errors 
        IngestionInfo.ingested_data = ingested_data
        logger.info("Fluxo de ingestão de APIs (JSONs) terminando...")
        return IngestionInfo