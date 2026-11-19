from src.data_ingestion.silver.implementation.df_parquet_ingestion import DfParquetIngestion, DfParquetIngestionErrors 
import pandas as pd
from unittest.mock import MagicMock
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