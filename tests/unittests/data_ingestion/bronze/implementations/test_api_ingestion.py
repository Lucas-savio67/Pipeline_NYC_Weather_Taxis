from unittest.mock import MagicMock, patch
from pathlib import Path
import json
from src.data_ingestion.bronze.implementations.api_s3_ingestion import APIS3Ingestion, APIIngestionErrors
from botocore.exceptions import ClientError, BotoCoreError
import logging 
import pytest
def test_success_api_ingestion():


    s3_client = MagicMock()
    saver = APIS3Ingestion(s3_client)

    data = {'NasaPower' : {'data': [1,2,3], 'status': 'success'}}

    save = saver.save('bronze', data , 'bucket_falso')

    s3_client.put_object.assert_called_once()

    kwargs = s3_client.put_object.call_args.kwargs

    assert kwargs["Bucket"] == "bucket_falso"
    assert kwargs["Key"] == "bronze/JSONs/NasaPower/NasaPower.json"
    assert json.loads(kwargs["Body"]) == data['NasaPower']
    assert save.ingested_data == {'NasaPower': True}
    assert save.errors == {}
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
    with pytest.raises(APIIngestionErrors): 
        saver.save('bronze', data , 'bucket_falso')
    assert 'injetar' in caplog.text
@patch('src.data_ingestion.bronze.implementations.api_s3_ingestion.json.dumps')
def test_json_error(mock_dumps, caplog): 
    mock_dumps.side_effect = TypeError("Erro ao serializar o json")
    s3_client = MagicMock()
    saver = APIS3Ingestion(s3_client)
    data = {'NasaPower' : {'data': [1,2,3], 'status': 'success'}}
    with caplog.at_level(logging.WARNING):
        save = saver.save('bronze', data , 'bucket_falso')
    assert 'serializar' in caplog.text
    assert save.ingested_data == {'NasaPower': False}
    assert save.errors == {'NasaPower': {'error': 'Erro ao serializar o json'}}
def test_no_data(): 
    s3_client = MagicMock()
    saver = APIS3Ingestion(s3_client)
    with pytest.raises(APIIngestionErrors): 
        saver.save('bronze', {} , 'bucket_falso')
def test_botocorre_error(): 
    s3_client = MagicMock()
    fake_data = {'NasaPower': {'data': [1,2,3]}}
    s3_client.put_object.side_effect = BotoCoreError( 
        motivo='Erro interno'
    )
    saver = APIS3Ingestion(s3_client)
    with pytest.raises(APIIngestionErrors):
        saver.save('bronze', fake_data, 'bucket_falso')