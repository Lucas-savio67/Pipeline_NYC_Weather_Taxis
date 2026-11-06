from src.data_transforming.implementations.jsons.nasa_power_transformation import NasaPowerTransformation, NasaPowerErrors 
import pandas as pd
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
    transform, errors = transforming.create_datetime_column(fake_df,fake_rules)
    assert transform['data_hora'].dtype == '<M8[us]'
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
