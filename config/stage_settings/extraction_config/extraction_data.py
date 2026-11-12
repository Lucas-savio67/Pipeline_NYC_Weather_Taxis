from config.stage_settings.extraction_config.extraction_model import ExtractionModel
from src.data_extraction.implementations.json_extractor import JsonExtractor 
from src.data_extraction.implementations.parquet_extractor import ParquetExtractor
from mypy_boto3_s3 import S3Client
def return_extraction_data(s3_client:S3Client, bucket_name:str, layer:str) -> dict[str, ExtractionModel]: 
    implementations = { 
        'JSON': ExtractionModel(JsonExtractor(s3_client), bucket_name, layer ) , 
        'Parquets': ExtractionModel(ParquetExtractor(s3_client), bucket_name, layer )
    }
    return implementations