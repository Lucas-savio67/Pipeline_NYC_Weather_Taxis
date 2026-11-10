import pandas as pd 
from src.data_transforming.data_transforming import DataTransforming 
from src.data_transforming.implementations.jsons.nasa_power_transformation import NasaPowerTransformation
import logging
def test_success_data_transforming(caplog): 
    fake_data = { 
            'data': { 
                'data_2':  {
                    'data_hora': ['2020010100', '2020010101', '2020010102'],
                    'data_3': [1,2,3], 
                    'data_4': [4,5,6],
                    
                }
            }
        }
    fake_rules = { 
            'important_columns': ['data', 'data_2', 'data_index'],
            'datetime_columns': { 
                        'data_hora': {'format': '%Y%m%d%H'}
                },
                    
        }
    json_transforming = NasaPowerTransformation(fake_rules)
    
    
    expected_df = pd.DataFrame({
            'data_index': [0, 1, 2],
            'data_hora': pd.to_datetime(
                ['2020010100', '2020010101', '2020010102'],
                format='%Y%m%d%H',
            ),
            'data_3': [1, 2, 3],
            'data_4': [4, 5, 6],
        })
    transforming = DataTransforming(json_transforming)
    with caplog.at_level(logging.INFO):
        transform = transforming.transform_general_data(fake_data, 'NasaPower')
    success_transforming = {'NasaPower': 'data_example'}
    pd.testing.assert_frame_equal(transform['NasaPower'], expected_df)
    assert f'{success_transforming.keys()}' in caplog.text
def test_critical_error(caplog): 
    fake_rules = {
        'fake_rule': 'fake'
    }
    json_transforming = NasaPowerTransformation(fake_rules) 
    transforming = DataTransforming(json_transforming)
    with caplog.at_level(logging.ERROR): 
        transforming.transform_general_data({}, 'NasaPower')
    assert 'crítico' in caplog.text
def test_no_critical_error(caplog): 
    fake_rules = { 
                'important_columns': ['data', 'data_2', 'data_index'],
                'datetime_columns': { 
                            'data_hora_fake': {'format': '%Y%m%d%H'}
                    },
                        
            }
    fake_data = { 
                'data': { 
                    'data_2':  {
                        'data_hora': ['2020010100', '2020010101', '2020010102'],
                        'data_3': [1,2,3], 
                        'data_4': [4,5,6],
                        
                    }
                }
            }
    json_transforming = NasaPowerTransformation(fake_rules)
    transforming = DataTransforming(json_transforming) 
    with caplog.at_level(logging.WARNING): 
        transforming.transform_general_data(fake_data, 'NasaPower')
    error = {'data_hora_fake': {'error': "'data_hora_fake'"}}
    assert f"Erros de transformação de NasaPower: {error}! " in caplog.text