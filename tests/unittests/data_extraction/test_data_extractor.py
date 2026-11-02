from src.data_extraction.data_extraction import DataExtraction, DataReadingErrors 
from src.data_extraction.implementations.json_extractor import JsonExtractor 
from unittest.mock import MagicMock
import json
import logging
def test_success_data_extraction(caplog): 
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
    
    json_extraction = JsonExtractor(s3_client)
    extraction = DataExtraction(json_extraction)
    with caplog.at_level(logging.INFO):
        extract = extraction.extract_general_data('bucket_falso' ,'bronze')
    expected_outcome = {key:expected_json}
    assert f"Arquivos extraídos com sucesso: {expected_outcome.keys()}" in caplog.text
    assert extract== {key:expected_json}