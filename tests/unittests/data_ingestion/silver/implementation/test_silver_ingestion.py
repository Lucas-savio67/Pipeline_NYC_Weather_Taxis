from src.data_ingestion.silver.implementation.df_parquet_ingestion import DfParquetIngestion, DfParquetIngestionErrors 
import pandas as pd
from unittest.mock import MagicMock
import logging 
logger = logging.getLogger(__name__)
import pytest
from botocore.exceptions import BotoCoreError, ClientError, ParamValidationError
def test_success_silver_ingestion(): 
    client_mock = MagicMock()
    fake_data = { 
        'NasaPower': pd.DataFrame({
            'data': [1,2,3] , 
            'status': 'success'
        })
    }
    ingestion = DfParquetIngestion(client_mock)
    ingest = ingestion.save('silver', fake_data, 'bucket_falso')
    kwargs = client_mock.put_object.call_args.kwargs
    assert ingest.ingested_data == {'NasaPower': True}
    assert ingest.errors == {}

    assert kwargs["Bucket"] == "bucket_falso"
    assert kwargs["Key"] == "silver/NasaPower/NasaPower.parquet"
def test_clienterror_ingestion(caplog): 
    client_mock = MagicMock()
    
    client_mock.put_object.side_effect = ClientError(
        {
            "Error": {
                "Code": "AccessDenied",
                "Message": "Access denied"
            }
        },
        "PutObject"
        )
    ingestion = DfParquetIngestion(client_mock)
    
    data = {'NasaPower' :pd.DataFrame({'data': [1,2,3], 'status': 'success'})}
    with pytest.raises(DfParquetIngestionErrors): 
        ingestion.save('bronze', data , 'bucket_falso')
    
def test_no_data(): 
    client_mock = MagicMock()
    ingestion = DfParquetIngestion(client_mock)
    with pytest.raises(DfParquetIngestionErrors): 
        ingestion.save('silver', {}, 'bucket_falso')
def test_paramvalidator_error(caplog ): 
    
    client_mock = MagicMock()
    client_mock.put_object.side_effect = ParamValidationError(
        report="Invalid parameter value"
    )
    ingestion = DfParquetIngestion(client_mock)
    data = {'NasaPower': pd.DataFrame({'data': [1, 2, 3], 'status': 'success'})}

    with caplog.at_level(logging.WARNING): 
        ingest = ingestion.save('silver', data, 'bucket_falso')

    assert ingest.ingested_data == {'NasaPower': False}
    assert ingest.errors == {'NasaPower': {'error': 'Parameter validation failed:\nInvalid parameter value'}}
def test_botocoreerror(): 
    client_mock = MagicMock()
    client_mock.put_object.side_effect = BotoCoreError(
            motivo='Erro interno'
        )
    ingestion = DfParquetIngestion(client_mock)
    data = {'NasaPower': pd.DataFrame({'data': [1, 2, 3], 'status': 'success'})}
    
    with pytest.raises(DfParquetIngestionErrors): 
        ingest = ingestion.save('silver', data, 'bucket_falso')
    
    
    