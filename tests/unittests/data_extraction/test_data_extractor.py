from src.data_extraction.data_extraction import DataExtraction
from src.data_extraction.implementations.json_extractor import JsonExtractor, JSONExtractorErrors
from unittest.mock import MagicMock
import pytest 
from botocore.exceptions import ClientError
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
    extracted_data = {'bronze/JSONs/NasaPower/NasaPower.json': True}
    assert f"Informações de extração: \nDados extraídos: {extracted_data} \nErros: {{}}"
    assert extract== {key:expected_json}
def test_critical_error(caplog):
    s3_client = MagicMock()
    s3_client.get_paginator.return_value.paginate.side_effect = ClientError(
            {"Error": {"Code": "AccessDenied", "Message": "Access denied"}},
            "ListObjectsV2",
    )
    
    json_extractor = JsonExtractor(s3_client) 
    
    with caplog.at_level(logging.ERROR):
            extraction = DataExtraction(json_extractor).extract_general_data(
                'bucket_falso', 'bronze'
            )

    assert "Erro crítico, impossível extrair os dados: " in caplog.text
    assert extraction == None
def test_no_critical_error(caplog): 
    key = "bronze/JSONs/NasaPower/NasaPower.json"
    s3_client = MagicMock()
    s3_client.get_paginator.return_value.paginate.return_value = [
            {"Contents": [{"Key": key}]}
    ]
    s3_client.get_object.return_value = {"Body": MagicMock()}
    s3_client.get_object.return_value["Body"].read.return_value = b"{invalid}"
    
    json_extractor = JsonExtractor(s3_client)
    
    with caplog.at_level(logging.INFO):
        extraction =  DataExtraction(json_extractor).extract_general_data('bucket_falso', 'bronze')
    extracted_data = {'bronze/JSONs/NasaPower/NasaPower.json': False}
    error = {'bronze/JSONs/NasaPower/NasaPower.json': {'error': 'Expecting property name enclosed in double quotes: line 1 column 2 (char 1)'}}
    assert f"Informações de extração: \nDados extraídos: {extracted_data} \nErros: {error}" in caplog.text