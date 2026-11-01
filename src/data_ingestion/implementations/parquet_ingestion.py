from src.data_ingestion.interfaces.ingestion_interface import IngestionInterface 
from mypy_boto3_s3 import S3Client
from botocore.exceptions import ClientError, BotoCoreError
import logging 
logger = logging.getLogger(__name__)
class ParquetIngestionErrors(Exception): 
    pass
class ParquetIngestionS3(IngestionInterface): 
    def __init__(self, s3_client:S3Client) -> None: 
        self.client = s3_client 
    def save(self, layer, data, bucket_name) -> dict[str,dict]:
        errors = {}
        if not data: 
            logger.error("Erro, nenhum parquet existente! ")
            raise ParquetIngestionErrors('Erro, nenhum parquet existente! ')
        logger.info("Iniciando o fluxo de ingestão de Parquets no S3! ")
        for nome, files in data.items(): 
            if not files: 
                logger.warning(f"Erro, nenhuma parquet referente a {nome} existe! ")
            logger.info(f"Injetando parquets referentes a {nome}... ")
            try :
                for file in files: 
                    file_name = f'{layer}/parquets/{nome}/{file}'
                    
                    self.client.upload_file(file, bucket_name, file_name)
            except (OSError, ClientError, BotoCoreError) as e: 
                logger.warning(f"Erro ao injeta o parquet {file} no S3: {str(e)}")
                errors[nome] = {'error': str(e)}
        logger.info("Finalizando o fluxo de ingestão de parquets...")
        return errors
