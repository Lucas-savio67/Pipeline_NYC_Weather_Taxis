from config.stage_settings.ingestion_config.ingestion_models import IngestionModel 
from src.data_ingestion.bronze.implementations.api_s3_ingestion import APIS3Ingestion
from src.data_ingestion.bronze.implementations.parquet_ingestion import ParquetIngestionS3
from src.data_ingestion.silver.implementation.df_parquet_ingestion import DfParquetIngestion
from pathlib import Path
from utils.discover_parquets import discover_parquets
from typing import Any
from mypy_boto3_s3 import S3Client
def return_ingestion_data(s3_client:S3Client, bucket_name:str, layer:str, data:dict[str, Any]) -> dict[str, IngestionModel]: 
    parquets = discover_parquets({'yellow_taxis_trips': Path('data/parquets/yellow_taxis_trips_NYC')})
    apis = data['APIs']
    implementations = { 
        'APIs': IngestionModel(implementation=APIS3Ingestion(s3_client), bucket_name=bucket_name, layer=layer, data=apis) , 
        'Parquets': IngestionModel(implementation=ParquetIngestionS3(s3_client), bucket_name=bucket_name, layer=layer, data=parquets) , 
        'DFs': IngestionModel(implementation=DfParquetIngestion(s3_client), bucket_name=bucket_name, layer=layer, data=data)
    }
    return implementations
def return_silver_ingestion_data(s3_client:S3Client, bucket_name:str, layer:str, data:dict[str, Any]) -> dict[str, IngestionModel]: 
    implementations = {   'DFs': IngestionModel(implementation=DfParquetIngestion(s3_client), bucket_name=bucket_name, layer=layer, data=data) }
    return implementations