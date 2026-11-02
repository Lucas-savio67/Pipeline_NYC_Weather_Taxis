import json
from io import BytesIO
from unittest.mock import MagicMock

from src.data_extraction.implementations.json_extractor import JsonExtractor


def test_success_json_extraction():
    key = "bronze/JSONs/NasaPower/NasaPower.json"
    expected_json = {'data': [1,2,3], 'status': 'success'}

    s3_client = MagicMock()
    paginator = s3_client.get_paginator.return_value
    paginator.paginate.return_value = [{"Contents": [{"Key": key}]}]
    s3_client.get_object.return_value = {
        "Body": BytesIO(json.dumps(expected_json).encode("utf-8"))
    }

    extracted_json, errors = JsonExtractor(s3_client).extract(
        bucket_name="bucket_falso", layer="bronze"
    )

    assert extracted_json == {key: expected_json}
    assert errors == {}
    s3_client.get_object.assert_called_once_with(
        Bucket="bucket_falso", Key=key
    )
