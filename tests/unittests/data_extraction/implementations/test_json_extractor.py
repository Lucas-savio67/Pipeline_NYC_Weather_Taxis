import json
import logging
from unittest.mock import MagicMock

import pytest
from botocore.exceptions import ClientError

from src.data_extraction.implementations.json_extractor import (
    JSONExtractorErrors,
    JsonExtractor,
)


def test_success_json_extraction(caplog):
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

    with caplog.at_level(logging.INFO):
        extraction = JsonExtractor(s3_client).extract(
            "bucket_falso", "bronze"
        )

    assert extraction.real_extracted_data == {key: expected_json}
    assert extraction.extracted_data == {key:True}
    assert extraction.errors == {}
    assert f"O JSON referente a {key} foi extraído com sucesso!" in caplog.text


def test_no_content(caplog):
    s3_client = MagicMock()
    s3_client.get_paginator.return_value.paginate.return_value = [
        {"Fake_content": [1, 2]}
    ]

    with caplog.at_level(logging.WARNING):
        extraction = JsonExtractor(s3_client).extract(
            "bucket_falso", "bronze"
        )

    assert "objeto" in caplog.text
    assert extraction.errors == {"empty_page": {"error": "No_object"}}
    assert extraction.real_extracted_data == {}

def test_list_objects_client_error(caplog):
    s3_client = MagicMock()
    s3_client.get_paginator.return_value.paginate.side_effect = ClientError(
        {"Error": {"Code": "AccessDenied", "Message": "Access denied"}},
        "ListObjectsV2",
    )

    with caplog.at_level(logging.WARNING):
        with pytest.raises(JSONExtractorErrors):
            JsonExtractor(s3_client).extract("bucket_falso", "bronze")

    assert "Erro ao listar os objetos" in caplog.text


def test_get_object_client_error(caplog):
    key = "bronze/JSONs/NasaPower/NasaPower.json"
    s3_client = MagicMock()
    s3_client.get_paginator.return_value.paginate.return_value = [
        {"Contents": [{"Key": key}]}
    ]
    s3_client.get_object.side_effect = ClientError(
        {"Error": {"Code": "AccessDenied", "Message": "Access denied"}},
        "GetObject",
    )

    with caplog.at_level(logging.WARNING):
        extraction = JsonExtractor(s3_client).extract(
            "bucket_falso", "bronze"
        )

    assert extraction.real_extracted_data == {}
    assert "AccessDenied" in extraction.errors[key]["error"]
    assert f"Erro ao obter o objeto {key}" in caplog.text


def test_invalid_json(caplog):
    key = "bronze/JSONs/NasaPower/NasaPower.json"
    s3_client = MagicMock()
    s3_client.get_paginator.return_value.paginate.return_value = [
        {"Contents": [{"Key": key}]}
    ]
    s3_client.get_object.return_value = {"Body": MagicMock()}
    s3_client.get_object.return_value["Body"].read.return_value = b"{invalid}"

    with caplog.at_level(logging.WARNING):
        extraction = JsonExtractor(s3_client).extract(
            "bucket_falso", "bronze"
        )

    assert extraction.errors == {'bronze/JSONs/NasaPower/NasaPower.json': {'error': 'Expecting property name enclosed in double quotes: line 1 column 2 (char 1)'}}
    assert extraction.real_extracted_data == {}
    assert extraction.extracted_data == {'bronze/JSONs/NasaPower/NasaPower.json': False}
    assert f"Erro decodificar o JSON {key}" in caplog.text


def test_invalid_utf8(caplog):
    key = "bronze/JSONs/NasaPower/NasaPower.json"
    s3_client = MagicMock()
    s3_client.get_paginator.return_value.paginate.return_value = [
        {"Contents": [{"Key": key}]}
    ]
    s3_client.get_object.return_value = {"Body": MagicMock()}
    s3_client.get_object.return_value["Body"].read.return_value = b"\xff"

    with caplog.at_level(logging.WARNING):
        extraction = JsonExtractor(s3_client).extract(
            "bucket_falso", "bronze"
        )

    assert extraction.real_extracted_data == {}
    assert extraction.errors == {'bronze/JSONs/NasaPower/NasaPower.json': {'error': "'utf-8' codec can't decode byte 0xff in position 0: invalid start byte"}}
    assert extraction.extracted_data == {'bronze/JSONs/NasaPower/NasaPower.json': False}
    assert f"Erro de decodificação para o JSON {key}" in caplog.text


def test_missing_body(caplog):
    key = "bronze/JSONs/NasaPower/NasaPower.json"
    s3_client = MagicMock()
    s3_client.get_paginator.return_value.paginate.return_value = [
        {"Contents": [{"Key": key}]}
    ]
    s3_client.get_object.return_value = {"Body": None}

    with caplog.at_level(logging.WARNING):
        extraction= JsonExtractor(s3_client).extract(
            "bucket_falso", "bronze"
        )

    assert extraction.real_extracted_data== {}
    assert extraction.errors == {
        key: {"error": "'NoneType' object has no attribute 'read'"}
    }
    assert extraction.extracted_data == {'bronze/JSONs/NasaPower/NasaPower.json': False }
    assert f"Erro, JSON {key} com Body ausente" in caplog.text
