from src.data_reading.implementations.api_reading import APIReading 
from src.data_ingestion.implementations.api_s3_ingestion import APIS3Ingestion 
from src.data_ingestion.implementations.parquet_ingestion import ParquetIngestionS3
from src.data_extraction.implementations.parquet_extractor import ParquetExtractor 
from src.data_extraction.implementations.json_extractor import JsonExtractor

from pathlib import Path
import boto3
from dotenv import load_dotenv
import os
from data.apis.apis_config import apis
from utils.discover_parquets import discover_parquets
load_dotenv()

def reading_settings() -> dict[str]: 
    implementations = {
        'APIs': APIReading(apis),
        
    }
    return implementations
def ingestion_settings(client, bucket_name) -> dict[str]: 
    
    parquets = discover_parquets({'yellow_taxis_trips': Path('yellow_taxis_trips_NYC')})
    implementations = {
        'APIs': [APIS3Ingestion(client), bucket_name], 
        'Parquets': [ParquetIngestionS3(client), bucket_name, parquets]
    }
    return implementations
def extraction_settings(client, bucket_name) -> dict[str]: 
    
    implementations = { 
        'APIs': [JsonExtractor(client) , bucket_name],
        'Parquets': [ParquetExtractor(client), bucket_name]
    }
    return implementations