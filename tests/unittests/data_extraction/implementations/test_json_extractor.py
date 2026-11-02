import json
import logging
from unittest.mock import MagicMock

import pytest
from botocore.exceptions import ClientError

from src.data_extraction.implementations.json_extractor import (
    JSONExtractorErrors,
    JsonExtractor,
)


def test_success_json_extraction():
    key = "bronze/JSONs/NasaPower/NasaPower.json"
    expected_json = {"data": [1, 2, 3], "status": "success"}
    s3_client = MagicMock()
    s3_client.get_paginator.return_value.paginate.return_value = [
        {"Contents": [{"Key": key}]}
    ]
    s3_client.get_object.return_value = {"Body": MagicMock()}
    s3_client.get_object.return_value["Body"].read.return_value = json.dumps(
        expected_json
    ).encode("utf-8")

    extracted, errors = JsonExtractor(s3_client).extract("bucket_falso", "bronze")

    assert extracted == {key: expected_json}
    assert errors == {}


def test_no_content(caplog):
    s3_client = MagicMock()
    s3_client.get_paginator.return_value.paginate.return_value = [
        {"Fake_content": [1, 2]}
    ]

    with caplog.at_level(logging.WARNING):
        extracted, errors = JsonExtractor(s3_client).extract(
            "bucket_falso", "bronze"
        )

    assert "objeto" in caplog.text
    assert extracted == {}
    assert errors == {"empty_page": {"error": "No_object"}}


def test_list_objects_client_error():
    s3_client = MagicMock()
    s3_client.get_paginator.return_value.paginate.side_effect = ClientError(
        {"Error": {"Code": "AccessDenied", "Message": "Access denied"}},
        "ListObjectsV2",
    )

    with pytest.raises(JSONExtractorErrors):
        JsonExtractor(s3_client).extract("bucket_falso", "bronze")


def test_get_object_client_error():
    key = "bronze/JSONs/NasaPower/NasaPower.json"
    s3_client = MagicMock()
    s3_client.get_paginator.return_value.paginate.return_value = [
        {"Contents": [{"Key": key}]}
    ]
    s3_client.get_object.side_effect = ClientError(
        {"Error": {"Code": "AccessDenied", "Message": "Access denied"}},
        "GetObject",
    )

    extracted, errors = JsonExtractor(s3_client).extract("bucket_falso", "bronze")

    assert extracted == {}
    assert "AccessDenied" in errors[key]["error"]


def test_invalid_json():
    key = "bronze/JSONs/NasaPower/NasaPower.json"
    s3_client = MagicMock()
    s3_client.get_paginator.return_value.paginate.return_value = [
        {"Contents": [{"Key": key}]}
    ]
    s3_client.get_object.return_value = {"Body": MagicMock()}
    s3_client.get_object.return_value["Body"].read.return_value = b"{invalid}"

    extracted, errors = JsonExtractor(s3_client).extract("bucket_falso", "bronze")

    assert extracted == {}
    assert key in errors


def test_invalid_utf8():
    key = "bronze/JSONs/NasaPower/NasaPower.json"
    s3_client = MagicMock()
    s3_client.get_paginator.return_value.paginate.return_value = [
        {"Contents": [{"Key": key}]}
    ]
    s3_client.get_object.return_value = {"Body": MagicMock()}
    s3_client.get_object.return_value["Body"].read.return_value = b"\xff"

    extracted, errors = JsonExtractor(s3_client).extract("bucket_falso", "bronze")

    assert extracted == {}
    assert key in errors


def test_missing_body():
    key = "bronze/JSONs/NasaPower/NasaPower.json"
    s3_client = MagicMock()
    s3_client.get_paginator.return_value.paginate.return_value = [
        {"Contents": [{"Key": key}]}
    ]
    s3_client.get_object.return_value = {"Body": None}

    extracted, errors = JsonExtractor(s3_client).extract("bucket_falso", "bronze")

    assert extracted == {}
    assert key in errors
