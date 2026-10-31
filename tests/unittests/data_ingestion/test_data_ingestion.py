from src.data_ingestion.data_ingestion import DataIngestion
from src.data_ingestion.implementations.api_s3_ingestion import APIS3Ingestion
from unittest.mock import MagicMock
import logging
def test_success_data_ingestion(): 
    s3_client = MagicMock()
    api_saver = APIS3Ingestion(s3_client)
    saver = DataIngestion(api_saver)
    general =saver.ingest_general_data('bronze', {'NasaPower': {'data': [1,2,3], 'status':'success'}}, 'bucket_falso')
    assert general == 'Dados injetados com sucesso no S3! '
def test_critical_error(caplog): 
    s3_client = MagicMock()
    api_saver = APIS3Ingestion(s3_client)
    saver = DataIngestion(api_saver)
    with caplog.at_level(logging.WARNING):
        general =saver.ingest_general_data('bronze', {}, 'bucket_falso')
    assert 'crítico' in caplog.text
