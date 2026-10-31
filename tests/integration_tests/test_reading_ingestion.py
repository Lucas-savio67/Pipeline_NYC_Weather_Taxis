from src.data_ingestion.implementations.api_s3_ingestion import APIS3Ingestion 
from src.data_reading.implementations.api_reading import APIReading 
from src.data_reading.data_reading import DataReading 
from src.data_ingestion.data_ingestion import DataIngestion 
from unittest.mock import patch, Mock, MagicMock 
from moto import mock_aws
import boto3
import json
@mock_aws
@patch('src.data_reading.implementations.api_reading.requests.get')
def test_success_integration(mock_get): 
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'data_1': [1,2,3], 'data_2': [4,5,6]}
    mock_get.return_value = mock_response
    reading = APIReading({'NasaPower': { 
        'url': 'fake_url'
    }})
    
    general_reading = DataReading(reading)
    read = general_reading.read_general_data()
    s3_client = boto3.client( 
        's3', region_name='us-east-1'
    )
    s3_client.create_bucket(Bucket='bucket_falso')
    ingestion = APIS3Ingestion(s3_client)
    general_ingestion = DataIngestion(ingestion)
    general_ingestion.ingest_general_data('bronze', read , 'bucket_falso') 
    response = s3_client.get_object(Bucket='bucket_falso', 
                                    Key='bronze/JSONs/NasaPower/NasaPower.json')
    injected_data = response["Body"].read()
    injected_data = json.loads(injected_data)
    assert injected_data == read['NasaPower']