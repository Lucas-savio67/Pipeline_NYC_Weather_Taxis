from unittest.mock import patch, Mock 
from src.data_reading.implementations.api_reading import APIReading, APIReadingErrors
import json
import requests
import pytest
import logging 
logger = logging.getLogger(__name__)
@patch('src.data_reading.implementations.api_reading.requests.get') 
def test_success_api_reading(mock_get, caplog): 
    mock_response = Mock()
    mock_response.status_code = 200 
    mock_response.json.return_value = {'data': [1,2,3], 'status': 'success'}
    mock_get.return_value = mock_response 
    fake_apis = { 
        'NasaPower': { 
            'url': 'url_fake'
        }
    }
    reading = APIReading(fake_apis)
    with caplog.at_level(logging.INFO):
        read = reading.read_data()
    assert read[0] == {'NasaPower': {'data': [1,2,3], 'status': 'success'}}
    assert 'sucesso' in caplog.text
@patch('src.data_reading.implementations.api_reading.requests.get')
def test_request_error(mock_get, caplog): 
    mock_get.side_effect = requests.exceptions.RequestException("Erro na requisição")
    fake_apis = { 
            'NasaPower': { 
                'url': 'url_fake'
            }
        }
    reading = APIReading(fake_apis)
    with caplog.at_level(logging.WARNING):
            read = reading.read_data()
    assert 'ao enviar' in caplog.text
    assert read[1] == {'NasaPower': {'error': 'Erro na requisição'}}
def test_no_apis(): 
    
    reading = APIReading({})
    
    with pytest.raises(APIReadingErrors): 
        read = reading.read_data()
@patch('src.data_reading.implementations.api_reading.requests.get')
def test_json_decode_error(mock_get, caplog): 
    
    mock_json = Mock()
    mock_json.json.side_effect = json.JSONDecodeError("Json inválido! ", 'Resposta inválida', 0)
    mock_get.return_value = mock_json
    fake_apis = { 
                'NasaPower': { 
                    'url': 'url_fake'
                }
            }
    reading = APIReading(fake_apis)
    with caplog.at_level(logging.WARNING):
        read = reading.read_data()
    assert 'inválido' in caplog.text
    assert read[1] == {'NasaPower': {'error': 'Json inválido! : line 1 column 1 (char 0)'}}