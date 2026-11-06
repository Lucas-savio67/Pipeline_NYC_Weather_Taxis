from src.data_transforming.implementations.jsons.nasa_power_transformation import NasaPowerTransformation, NasaPowerErrors 
import pandas as pd
import pytest 
import logging
def test_success_np_structuring(): 
    fake_data = { 
        'data': {
            'data_2': { 
                'data_3': [1,2,3]  ,
                'data_4': [4,5,6]
            }
        }
    }
    
    fake_rules = { 
        'important_columns': ['data', 'data_2', 'data_index'],
        
    }
    
    expected_df = { 
        'data_index': [0,1,2], 
        'data_3': [1,2,3] , 
        'data_4': [4,5,6]
    }
    
    transforming = NasaPowerTransformation(fake_rules)
    transform = transforming.structure_json(fake_data, fake_rules)
    pd.testing.assert_frame_equal(transform, pd.DataFrame(expected_df))
def test_success_np_datetime_column(): 
    fake_df = pd.DataFrame({ 
        'data_hora': ['2020010100', '2020010101', '2020010102']
    })

    fake_rules = { 
            'datetime_columns': { 
                'data_hora': {'format': '%Y%m%d%H'}
            },
            
        }
    transforming = NasaPowerTransformation(fake_rules)
    transformed_data, errors = transforming.create_datetime_column(fake_df,fake_rules)
    assert transformed_data['data_hora'].dtype == '<M8[us]'
    assert errors == {}
def test_success_np_transforming_end_to_end(): 
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
    transforming = NasaPowerTransformation(fake_rules)
    transformed_data, errors = transforming.transform(fake_data, 'NasaPower')

    expected_df = pd.DataFrame({
        'data_index': [0, 1, 2],
        'data_hora': pd.to_datetime(
            ['2020010100', '2020010101', '2020010102'],
            format='%Y%m%d%H',
        ),
        'data_3': [1, 2, 3],
        'data_4': [4, 5, 6],
    })

    
    pd.testing.assert_frame_equal(transformed_data['NasaPower'], expected_df)
    assert errors == {}
def test_no_data(): 
    fake_rules = { 
        'rules_fake': 'fake'
    }
    transforming = NasaPowerTransformation(fake_rules)
    with pytest.raises(NasaPowerErrors):
        transforming.transform({}, 'NasaPower')
def test_key_error(): 
    fake_rules = { 
        'important_columns': ['data_fake']
    }
    fake_data = { 
        'data': { 
            'data_2'
        }
    }
    transforming = NasaPowerTransformation(fake_rules)
    with pytest.raises(NasaPowerErrors):
        transforming.structure_json(fake_data, fake_rules)
def test_no_critical_error_datetime_column(caplog): 
    fake_rules = { 
        'datetime_columns':{ 
            'fake_column': {'format': 'fake_format'}
        }
    }
    fake_data = pd.DataFrame({
        'data_1': [4,5,6], 
        'data_2': [1,2,3]
    })
    transforming = NasaPowerTransformation(fake_rules)
    with caplog.at_level(logging.WARNING):
        transformed_data, errors = transforming.create_datetime_column(fake_data, fake_rules)
    
    assert errors == {'fake_column': {'error': "'fake_column'"}}
    pd.testing.assert_frame_equal(transformed_data, pd.DataFrame(fake_data))
    assert 'Parece que a coluna fake_column' in caplog.text