from src.data_extraction.implementations.json_extractor import JsonExtractor 
from src.data_extraction.data_extraction import DataExtraction 
from src.data_ingestion.implementations.api_s3_ingestion import APIS3Ingestion 
from src.data_ingestion.data_ingestion import DataIngestion
from moto import mock_aws
from unittest.mock import MagicMock
import logging
import boto3

@mock_aws
def test_success_ingestion_extraction(caplog): 
    
    key = 'bronze/JSONs/NasaPower/NasaPower.json'
    fake_data = {'NasaPower' : {'data': [1,2,3], 'status': 'success'}}
    s3_client = boto3.client( 
            's3', region_name='us-east-1'
    )
    s3_client.create_bucket(Bucket='bucket_falso')
    json_ingestion = APIS3Ingestion(s3_client)
    DataIngestion(json_ingestion).ingest_general_data('bronze', fake_data , 'bucket_falso')
    json_extractor = JsonExtractor(s3_client)
    with caplog.at_level(logging.INFO):
        extraction = DataExtraction(json_extractor).extract_general_data('bucket_falso', 'bronze')
    expected_outcome = {key: fake_data['NasaPower']}
    assert extraction == expected_outcome
    
    assert f"Arquivos extraídos com sucesso: {expected_outcome.keys()}"
