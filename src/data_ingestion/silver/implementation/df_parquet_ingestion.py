from src.data_ingestion.interfaces.ingestion_interface import IngestionInterface
from config.return_contracts.ingestion_contract import IngestionInfo
from botocore.exceptions import ClientError, BotoCoreError, ParamValidationError
import pandas as pd
from io import BytesIO
from mypy_boto3_s3 import S3Client
import logging 
logger = logging.getLogger(__name__)
class DfParquetIngestionErrors(Exception): 
    pass
class DfParquetIngestion(IngestionInterface): 
    def __init__(self, s3_client:S3Client) -> None: 
        self.client = s3_client
    def save(self, layer:str, data:dict[str, pd.DataFrame], bucket_name:str) -> IngestionInfo:
        logger.info("Iniciando o fluxo de ingestão na camada silver do S3...")
        ingested_data = {}
        errors = {}
        try :
            for nome, df in data.items(): 
                ingested = False
                try :
                    
                    logger.info(f"Injentando o DataFrame {nome} no bucket S3! ")
                    buffer = BytesIO()
                    df.to_parquet(buffer)
                    buffer.seek(0)
                    logger.info(f'O DataFrame {nome} foi transformado em parquet com sucesso! ')
                    self.client.put_object(Bucket=bucket_name, Body=buffer.getvalue(), Key=f'{layer}/{nome}/{nome}.parquet')
                    logger.info(f'O Parquet {nome} foi enviado a camada silver so S3 com sucesso! ')
                    ingested = True
                except ParamValidationError as e: 
                    logger.warning(f"Erro, verifique se o objeto {nome} é um paruqte em Bytes! ")
                    errors[nome] = {'error': str(e)}
                ingested_data[nome] = ingested
        except ClientError as e: 
            logger.warning(f"Erro de cliente ao realizar o processo de ingestão: {str(e)}! ")
            raise DfParquetIngestionErrors(f"Erro de cliente ao realizar o processo de ingestão: {str(e)}!  ")
        except BotoCoreError as e: 
            logger.warning(f'Erro botocre ao relizar o processo de ingestão: {str(e)}! ')
            raise DfParquetIngestionErrors(f'Erro botocre ao relizar o processo de ingestão: {str(e)}! ')
        IngestionInfo.ingested_data = ingested_data 
        IngestionInfo.errors = errors 
        logger.info("Finalizando o floxuo de ingestão na camada silver! ")
        return IngestionInfo