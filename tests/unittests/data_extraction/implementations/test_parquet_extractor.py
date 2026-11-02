import io
import logging
from unittest.mock import MagicMock

import pandas as pd
import pyarrow as pa
import pytest
from botocore.exceptions import ClientError

from src.data_extraction.implementations.parquet_extractor import (
    ParquetExtractor,
    ParquetExtractorErrors,
)


def test_success_parquet_extraction(caplog):
    key = "bronze/parquets/yellow_taxis_trips/trips.parquet"
    expected_df = pd.DataFrame({"data": [1, 2, 3]})
    parquet_file = io.BytesIO()
    expected_df.to_parquet(parquet_file, engine="pyarrow")

    s3_client = MagicMock()
    s3_client.get_paginator.return_value.paginate.return_value = [
        {"Contents": [{"Key": key}]}
    ]
    s3_client.get_object.return_value = {"Body": MagicMock()}
    s3_client.get_object.return_value["Body"].read.return_value = (
        parquet_file.getvalue()
    )

    with caplog.at_level(logging.INFO):
        extracted, errors = ParquetExtractor(s3_client).extract(
            "bucket_falso", "bronze"
        )

    pd.testing.assert_frame_equal(extracted[key], expected_df)
    assert errors == {}
    assert f"O parquet {key} foi extraído" in caplog.text


def test_no_content():
    s3_client = MagicMock()
    s3_client.get_paginator.return_value.paginate.return_value = [
        {"Fake_content": [1, 2]}
    ]

    extracted, errors = ParquetExtractor(s3_client).extract(
        "bucket_falso", "bronze"
    )

    assert extracted == {}
    assert errors == {}


def test_list_objects_client_error(caplog):
    s3_client = MagicMock()
    s3_client.get_paginator.return_value.paginate.side_effect = ClientError(
        {"Error": {"Code": "AccessDenied", "Message": "Access denied"}},
        "ListObjectsV2",
    )

    with caplog.at_level(logging.WARNING):
        with pytest.raises(ParquetExtractorErrors):
            ParquetExtractor(s3_client).extract("bucket_falso", "bronze")

    assert "Erro ao listar os objetos" in caplog.text


def test_get_object_client_error(caplog):
    key = "bronze/parquets/yellow_taxis_trips/trips.parquet"
    s3_client = MagicMock()
    s3_client.get_paginator.return_value.paginate.return_value = [
        {"Contents": [{"Key": key}]}
    ]
    s3_client.get_object.side_effect = ClientError(
        {"Error": {"Code": "AccessDenied", "Message": "Access denied"}},
        "GetObject",
    )

    with caplog.at_level(logging.WARNING):
        extracted, errors = ParquetExtractor(s3_client).extract(
            "bucket_falso", "bronze"
        )

    assert extracted == {}
    assert "AccessDenied" in errors[key]["error"]
    assert f"Erro ao obter o objeto {key}" in caplog.text


def test_invalid_parquet():
    key = "bronze/parquets/yellow_taxis_trips/trips.parquet"
    s3_client = MagicMock()
    s3_client.get_paginator.return_value.paginate.return_value = [
        {"Contents": [{"Key": key}]}
    ]
    s3_client.get_object.return_value = {"Body": MagicMock()}
    s3_client.get_object.return_value["Body"].read.return_value = b"invalid"

    with pytest.raises(pa.ArrowInvalid):
        ParquetExtractor(s3_client).extract("bucket_falso", "bronze")


def test_missing_body(caplog):
    key = "bronze/parquets/yellow_taxis_trips/trips.parquet"
    s3_client = MagicMock()
    s3_client.get_paginator.return_value.paginate.return_value = [
        {"Contents": [{"Key": key}]}
    ]
    s3_client.get_object.return_value = {"Body": None}

    with caplog.at_level(logging.WARNING):
        extracted, errors = ParquetExtractor(s3_client).extract(
            "bucket_falso", "bronze"
        )

    assert extracted == {}
    assert key in errors
    assert f"O corpo de {key} não pôde ser lido" in caplog.text
