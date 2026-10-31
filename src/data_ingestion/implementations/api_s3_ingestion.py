from src.data_ingestion.interfaces.ingestion_interface import IngestionInterface
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
    def save(self, layer, data, bucket_name) -> str:
        if not data: 
            logger.error("Erro, nenhuma API foi lida! ")
            raise  APIIngestionErrors("Erro, nenhuma API foi lida! ")
        logger.info("Começando o fluxo de ingestão de APIs no bucket S3...")
        try :
            for nome, conteudo in data.items(): 
                file= f'{layer}/{nome}.json'
                self.client.put_object(
                    Bucket=bucket_name , 
                    Key=file ,
                    Body=json.dumps(conteudo, ensure_ascii=False, indent=2)
                )
        except (ClientError, BotoCoreError) as e: 
            logger.warning(f"Erro ao injetar as APIs para o bucket: {str(e)}")
        except (TypeError, ValueError, UnicodeEncodeError) as e: 
            logger.warning(f"Erro ao serializar os arquivos JSONs: {str(e)}") 
        logger.info("Fluxo d eingestão de APIs (JSONs) terminando...")
        return 'Dados injetados com sucesso! '