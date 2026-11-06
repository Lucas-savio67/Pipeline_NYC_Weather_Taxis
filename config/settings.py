from src.data_reading.implementations.api_reading import APIReading 
from src.data_ingestion.implementations.api_s3_ingestion import APIS3Ingestion 
from src.data_ingestion.implementations.parquet_ingestion import ParquetIngestionS3
from src.data_extraction.implementations.parquet_extractor import ParquetExtractor 
from src.data_extraction.implementations.json_extractor import JsonExtractor
from src.data_transforming.implementations.jsons.nasa_power_transformation import NasaPowerTransformation 
from src.data_transforming.implementations.parquets.taxis_trips_nyc_transformer import TaxisTripsTransformer
from config.transformations_rules.nasa_power_rules import nasa_power_rules 
from config.transformations_rules.taxis_trips_rules import taxis_trips_rules
from utils.schema_validator import validate_schema
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
        'JSON': [JsonExtractor(client) , bucket_name],
        'Parquets': [ParquetExtractor(client), bucket_name]
    }
    return implementations
def specific_transforming_settings(): 
    implementations = { 
        'bronze/JSONs/NasaPower/NasaPower.json': NasaPowerTransformation(nasa_power_rules) , 
        'yellow_taxis_trips':  TaxisTripsTransformer(validate_schema, taxis_trips_rules)
    }
    return implementations