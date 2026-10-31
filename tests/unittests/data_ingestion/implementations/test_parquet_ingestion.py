from src.data_ingestion.implementations.parquet_ingestion import ParquetIngestionErrors, ParquetIngestionS3 
from unittest.mock import MagicMock
from pathlib import Path
import logging 
from botocore.exceptions import ClientError
import pytest
def test_success_parquet_ingestion(): 
    s3_client = MagicMock()
    saver = ParquetIngestionS3(s3_client) 
    saver.save(
        'bronze' , 
        {'yellow_taxis_trips': ['taxis_trips.parquet']} , 
        'bucket_falso'
    )

    s3_client.upload_file.assert_called_once_with(
        "taxis_trips.parquet",
        "bucket_falso",
        "bronze/parquets/yellow_taxis_trips/taxis_trips.parquet"
    )
def test_no_data(): 
    s3_client = MagicMock()
    saver = ParquetIngestionS3(s3_client) 
    with pytest.raises(ParquetIngestionErrors): 
        saver.save(
                'bronze' , 
                {} , 
                'bucket_falso'
            )
def test_clienterror(caplog): 
    s3_client = MagicMock()
    s3_client.upload_file.side_effect = ClientError(
        {
            "Error": {
                "Code": "AccessDenied",
                "Message": "Access denied"
            }
        },
        "UploadFile"
        )
    saver = ParquetIngestionS3(s3_client)
    with caplog.at_level(logging.WARNING):
        saver.save(
                        'bronze' , 
                        {'yellow_taxis_trips': ['taxis_trips.parquet']} , 
                        'bucket_falso'
                    )
    assert 'injetar' in caplog.text
def test_no_parquet_file(caplog): 
    s3_client = MagicMock()
    saver = ParquetIngestionS3(s3_client)
    with caplog.at_level(logging.WARNING):
        saver.save(
                                'bronze' , 
                                {'yellow_taxis_trips': []} , 
                                'bucket_falso'
                            )
    assert 'referente' in caplog.text