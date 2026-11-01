from src.data_reading.data_reading import DataReading 
from src.data_reading.implementations.api_reading import APIReading
from unittest.mock import Mock, patch
import logging 

@patch('src.data_reading.implementations.api_reading.requests.get')
def test_success_data_reading(mock_get): 
    mock_response = Mock()
    mock_response.json.return_value = {'data': [1,2,3],'status': 'success'}
    mock_get.return_value = mock_response
    fake_apis = {
        'NasaPower': { 
            'url': 'fake_url'
        }
    }
    implementation = APIReading(fake_apis)
    reading = DataReading(implementation)
    read = reading.read_general_data()
    assert read == {'NasaPower': {'data': [1,2,3], 'status': 'success'}}
def test_critical_error(caplog): 
    implementation = APIReading({})
    reading = DataReading(implementation)
    with caplog.at_level(logging.WARNING):
        read = reading.read_general_data()
    assert 'crítico' in caplog.text
