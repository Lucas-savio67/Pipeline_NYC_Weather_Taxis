import json
import boto3
import pandas as pd
from moto import mock_aws

from src.data_extraction.data_extraction import DataExtraction
from src.data_extraction.implementations.json_extractor import JsonExtractor
from src.data_transforming.data_transforming import DataTransforming
from src.data_transforming.implementations.jsons.nasa_power_transformation import (
    NasaPowerTransformation,
)

@mock_aws
def test_success_extraction_transforming():
    bucket = "bucket_falso"
    key = "bronze/JSONs/NasaPower/NasaPower.json"
    json_falso = {
        "data": {
            "data_2": {
                "data_hora": ["2020010100", "2020010101"],
                "data_3": [1, 2],
                "data_4": [4, 5],
            }
        }
    }

    s3_client = boto3.client("s3", region_name="us-east-1")
    s3_client.create_bucket(Bucket=bucket)
    s3_client.put_object(
        Bucket=bucket,
        Key=key,
        Body=json.dumps(json_falso),
    )

    extraction = DataExtraction(JsonExtractor(s3_client))
    dados_extraidos = extraction.extract_general_data(bucket, "bronze")

    regras = {
        "important_columns": ["data", "data_2", "data_index"],
        "datetime_columns": {
            "data_hora": {"format": "%Y%m%d%H"}
        },
    }
    transforming = DataTransforming(NasaPowerTransformation(regras))
    resultado = transforming.transform_general_data(
        dados_extraidos[key], "NasaPower"
    )

    esperado = pd.DataFrame({
        "data_index": [0, 1],
        "data_hora": pd.to_datetime(
            ["2020010100", "2020010101"], format="%Y%m%d%H"
        ),
        "data_3": [1, 2],
        "data_4": [4, 5],
    })
    pd.testing.assert_frame_equal(resultado["NasaPower"], esperado)
