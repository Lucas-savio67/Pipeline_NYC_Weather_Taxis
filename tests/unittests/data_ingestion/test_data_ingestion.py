from src.data_ingestion.data_ingestion import DataIngestion
from src.data_ingestion.implementations.api_s3_ingestion import APIS3Ingestion
from unittest.mock import MagicMock
import logging
from botocore.exceptions import ClientError
def test_success_data_ingestion(): 
    s3_client = MagicMock()
    api_saver = APIS3Ingestion(s3_client)
    saver = DataIngestion(api_saver)
    general =saver.ingest_general_data('bronze', {'NasaPower': {'data': [1,2,3], 'status':'success'}}, 'bucket_falso')
    assert general == 'Dados injetados no S3, verifique se algum deu erro! '
def test_critical_error(caplog): 
    s3_client = MagicMock()
    api_saver = APIS3Ingestion(s3_client)
    saver = DataIngestion(api_saver)
    with caplog.at_level(logging.WARNING):
        general =saver.ingest_general_data('bronze', {}, 'bucket_falso')
    assert 'crítico' in caplog.text
def test_no_critical_error(caplog): 
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
    api_saver = APIS3Ingestion(s3_client)
    saver = DataIngestion(api_saver) 
    
    with caplog.at_level(logging.WARNING): 
        save = saver.ingest_general_data('bronze', {'NasaPower': {'data': [1,2,3], 'status':'success'}} , 'bucket_falso')
    error = {'NasaPower': {'error': 'An error occurred (AccessDenied) when calling the PutObject operation: Access denied'}}
    assert f'Dados com erro: {error}' in caplog.text