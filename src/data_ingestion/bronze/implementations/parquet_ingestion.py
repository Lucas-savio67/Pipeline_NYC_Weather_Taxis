from src.data_ingestion.interfaces.ingestion_interface import IngestionInterface 
from config.return_contracts.ingestion_contract import IngestionInfo
from mypy_boto3_s3 import S3Client
from botocore.exceptions import ClientError, BotoCoreError
import logging 
logger = logging.getLogger(__name__)
class ParquetIngestionErrors(Exception): 
    pass
class ParquetIngestionS3(IngestionInterface): 
    def __init__(self, s3_client:S3Client) -> None: 
        self.client = s3_client 
    def save(self, layer, data, bucket_name) -> IngestionInfo:
        errors = {}
        ingested_data = {}
        if not data: 
            logger.error("Erro, nenhum parquet existente! ")
            raise ParquetIngestionErrors('Erro, nenhum parquet existente! ')
        logger.info("Iniciando o fluxo de ingestão de Parquets no S3! ")
        try :
            for nome, files in data.items(): 
                ingested = False 
                if not files: 
                    logger.warning(f"Erro, nenhuma parquet referente a {nome} existe! ")
                    errors[nome] = {'error': 'no_files'}
                logger.info(f"Injetando parquets referentes a {nome}... ")
                try :
                    for file in files: 
                        file_name = f'{layer}/parquets/{nome}/{file}'
                        
                        self.client.upload_file(file, bucket_name, file_name)
                        ingested = True 
                except OSError as e: 
                    logger.warning(f"Erro ao injetar o parquet {file} no S3: {str(e)}")
                    errors[nome] = {'error': str(e)}
                ingested_data[nome] = ingested 
        except ClientError as e: 
            logger.warning(f"Erro de cliente ao injetar os parquets no S3: {str(e)}! ")
            raise ParquetIngestionErrors
        except BotoCoreError as e: 
            logger.warning(f'Erro botocore ao injetar os parquets no S3: {str(e)}! ')
            raise ParquetIngestionErrors(f'Erro botocore ao injetar os parquets no S3: {str(e)}! ')
        IngestionInfo.errors = errors 
        IngestionInfo.ingested_data = ingested_data
        logger.info("Finalizando o fluxo de ingestão de parquets...")
        return IngestionInfo
