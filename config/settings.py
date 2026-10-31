from src.data_reading.implementations.api_reading import APIReading 
from src.data_ingestion.implementations.api_s3_ingestion import APIS3Ingestion 
from src.data_ingestion.implementations.parquet_ingestion import ParquetIngestionS3
from pathlib import Path
import boto3
from dotenv import load_dotenv
import os
from data.apis.apis_config import apis
from utils.discover_parquets import discover_parquets
load_dotenv()
def reading_settings(): 
    implementations = {
        'APIs': APIReading(apis),
        
    }
    return implementations
def ingestion_settings(): 
    parquets = discover_parquets({'yellow_taxis_trips': Path('data/parquets/yellow_taxis_trips_NYC')})
    s3_client = boto3.client('s3' ,
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID") , 
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY") , 
    region_name=os.getenv("AWS_REGION"))
    
    implementations = {
        'APIs': [APIS3Ingestion(s3_client), os.getenv("AWS_BUCKET_NAME")], 
        'Parquets': [ParquetIngestionS3(s3_client), os.getenv("AWS_BUCKET_NAME"), parquets]
    }
    return implementations