from src.data_transforming.generic_implementation.generic_implementations import GenericTransforming
import pandas as pd 

def test_null_filling(): 
    fake_data = pd.DataFrame(
        {'campo_1': [1,pd.NA, 2], 
        'campo_2': [4,5,6]}) 
    fake_generic_rules = { 
        'yellow_taxis_trips': { 
            'fill_null_columns': {'campo_1': 0}
        }
    }
    expected_df = pd.DataFrame({
        'campo_1': pd.Series([1,0,2], dtype=object),
        'campo_2': [4,5,6]
    })
    taxis_trips_rules = fake_generic_rules['yellow_taxis_trips']
    transforming = GenericTransforming(fake_generic_rules)
    transformed_data, info, errors = transforming.fill_null_values(fake_data, 'yellow_taxis_trips', taxis_trips_rules)
    pd.testing.assert_frame_equal(transformed_data, expected_df)
    assert errors == {}
    assert info == {'qtd_nulos': {'nulos_antes': 1, 'depois': 0}}