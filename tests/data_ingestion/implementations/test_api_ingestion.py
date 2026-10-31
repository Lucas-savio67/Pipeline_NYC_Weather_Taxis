from unittest.mock import MagicMock
from pathlib import Path
import json
from src.data_ingestion.implementations.api_s3_ingestion import APIS3Ingestion
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