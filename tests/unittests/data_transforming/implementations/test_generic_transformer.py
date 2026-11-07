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


def test_column_renaming():
    fake_data = pd.DataFrame({
        'campo_1': [1, 2, 3],
        'campo_2': [4, 5, 6]
    })
    fake_rules = {
        'columns_to_rename': {'campo_1': 'nome_novo'}
    }
    expected_df = pd.DataFrame({
        'nome_novo': [1, 2, 3],
        'campo_2': [4, 5, 6]
    })

    transforming = GenericTransforming({})
    transformed_data, info, errors = transforming.rename_columns(
        fake_data, 'yellow_taxis_trips', fake_rules
    )

    pd.testing.assert_frame_equal(transformed_data, expected_df)
    assert errors == {}
    assert info == {
        'renomeação_colunas': {
            'antes': ['campo_1', 'campo_2'],
            'depois': ['nome_novo', 'campo_2']
        }
    }


def test_duplicate_removal():
    fake_data = pd.DataFrame({
        'campo_1': [1, 2, 2],
        'campo_2': [4, 5, 5]
    })
    fake_rules = {
        'drop_duplicates': {'all_columns': []}
    }
    expected_df = pd.DataFrame({
        'campo_1': [1, 2],
        'campo_2': [4, 5]
    })

    transforming = GenericTransforming({})
    transformed_data, info, errors = transforming.remove_duplicates(
        fake_data, 'yellow_taxis_trips', fake_rules
    )

    pd.testing.assert_frame_equal(transformed_data, expected_df)
    assert errors == {}
    assert info == {'qtd_duplicatas': {'antes': 1, 'depois': 0}}


def test_generic_transforming_end_to_end():
    fake_data = {
        'yellow_taxis_trips': pd.DataFrame({
            'campo_1': [1, pd.NA, 2, 2],
            'campo_2': [4, 5, 6, 6]
        })
    }
    fake_rules = {
        'yellow_taxis_trips': {
            'drop_duplicates': {'all_columns': []},
            'fill_null_columns': {'campo_1': 0},
            'columns_to_rename': {'campo_1': 'nome_novo'}
        }
    }
    expected_df = pd.DataFrame({
        'nome_novo': pd.Series([1, 0, 2], dtype=object),
        'campo_2': [4, 5, 6]
    })

    transforming = GenericTransforming(fake_rules)
    transformed_data = transforming.transform(fake_data)

    result = transformed_data['yellow_taxis_trips']
    pd.testing.assert_frame_equal(result['data'], expected_df)
    assert result['errors'] == {
        'yellow_taxis_trips': {'errors': [{}, {}, {}]}
    }
    assert result['info'] == {
        'yellow_taxis_trips': {
            'info': [
                {'qtd_duplicatas': {'antes': 1, 'depois': 0}},
                {'qtd_nulos': {'nulos_antes': 1, 'depois': 0}},
                {
                    'renomeação_colunas': {
                        'antes': ['campo_1', 'campo_2'],
                        'depois': ['nome_novo', 'campo_2']
                    }
                }
            ]
        }
    }