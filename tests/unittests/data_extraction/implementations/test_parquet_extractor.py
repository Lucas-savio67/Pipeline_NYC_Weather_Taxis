import io
from unittest.mock import MagicMock

import pandas as pd


from src.data_extraction.implementations.parquet_extractor import ParquetExtractor


def test_success_parquet_extraction():
    key = "bronze/parquets/yellow_taxis_trips_NYC/yellow_taxis_trips_2026-08.parquet"
    expected_df = pd.DataFrame({"data": [1, 2, 3], "data_2": [4, 5, 6]})
    parquet_file = io.BytesIO()
    expected_df.to_parquet(parquet_file, engine="pyarrow")

    s3_client = MagicMock()
    s3_client.get_paginator.return_value.paginate.return_value = [
        {"Contents": [{"Key": key}]}
    ]
    s3_client.get_object.return_value = {
        "Body": MagicMock(read=MagicMock(return_value=parquet_file.getvalue()))
    }

    extracted, errors = ParquetExtractor(s3_client).extract(
        "bucket_falso", "bronze"
    )

    pd.testing.assert_frame_equal(extracted[key], expected_df)
    assert errors == {}
