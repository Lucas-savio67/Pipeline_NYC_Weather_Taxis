from unittest.mock import patch, Mock 
from src.data_reading.implementations.api_reading import APIReading
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
    assert read == {'NasaPower': {'data': [1,2,3], 'status': 'success'}}
    assert 'sucesso' in caplog.text