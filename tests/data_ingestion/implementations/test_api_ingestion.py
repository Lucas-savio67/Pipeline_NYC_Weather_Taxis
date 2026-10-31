from unittest.mock import MagicMock, patch
from pathlib import Path
import json
from src.data_ingestion.implementations.api_s3_ingestion import APIS3Ingestion
from botocore.exceptions import ClientError
import logging 

def test_success_api_ingestion():


    s3_client = MagicMock()
    saver = APIS3Ingestion(s3_client)

    data = {'NasaPower' : {'data': [1,2,3], 'status': 'success'}}

    saver.save('bronze', data , 'bucket_falso')

    s3_client.put_object.assert_called_once()

    kwargs = s3_client.put_object.call_args.kwargs

    assert kwargs["Bucket"] == "bucket_falso"
    assert kwargs["Key"] == "bronze/JSONs/NasaPower/NasaPower.json"
    assert json.loads(kwargs["Body"]) == data['NasaPower']

def test_clienterror_ingestion(caplog): 
    s3_client = MagicMock()
    
    s3_client.put_object.side_effect = ClientError(
        {
            "Error": {
                "Code": "AccessDenied",
                "Message": "Access denied"
            }
        },
        "PutObject"
        )
    saver = APIS3Ingestion(s3_client)
    
    data = {'NasaPower' : {'data': [1,2,3], 'status': 'success'}}
    with caplog.at_level(logging.WARNING): 
        saver.save('bronze', data , 'bucket_falso')
    assert 'injetar' in caplog.text
@patch('src.data_ingestion.implementations.api_s3_ingestion.json.dumps')
def test_json_error(mock_dumps, caplog): 
    mock_dumps.side_effect = TypeError("Erro ao serializar o json")
    s3_client = MagicMock()
    saver = APIS3Ingestion(s3_client)
    data = {'NasaPower' : {'data': [1,2,3], 'status': 'success'}}
    with caplog.at_level(logging.WARNING):
        saver.save('bronze', data , 'bucket_falso')
    assert 'serializar' in caplog.text
