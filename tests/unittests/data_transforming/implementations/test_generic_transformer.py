from src.data_transforming.generic_implementation.generic_implementations import (
    GenericTransforming,
    GenericTransformingErrors,
)
import pandas as pd 
import pytest

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


def test_null_filling_missing_column():
    fake_data = pd.DataFrame({'campo_1': [pd.NA]})
    fake_rules = {
        'fill_null_columns': {'coluna_inexistente': 0}
    }

    transforming = GenericTransforming({})
    transformed_data, info, errors = transforming.fill_null_values(
        fake_data, 'yellow_taxis_trips', fake_rules
    )

    pd.testing.assert_frame_equal(transformed_data, fake_data)
    assert errors == {
        'error': {'column_name': "'coluna_inexistente'"}
    }
    assert info == {'qtd_nulos': {'nulos_antes': 1, 'depois': 1}}


def test_null_filling_incompatible_value_type():
    fake_data = pd.DataFrame({'campo_1': [1, pd.NA]})
    fake_rules = {
        'fill_null_columns': {'campo_1': [0, 1]}
    }

    transforming = GenericTransforming({})
    transformed_data, info, errors = transforming.fill_null_values(
        fake_data, 'yellow_taxis_trips', fake_rules
    )

    pd.testing.assert_frame_equal(transformed_data, fake_data)
    assert errors == {'error': {'value_type': list}}
    assert info == {'qtd_nulos': {'nulos_antes': 1, 'depois': 1}}


def test_column_renaming_missing_column():
    fake_data = pd.DataFrame({'campo_1': [1, 2]})
    fake_rules = {
        'columns_to_rename': {'coluna_inexistente': 'nome_novo'}
    }

    transforming = GenericTransforming({})
    transformed_data, info, errors = transforming.rename_columns(
        fake_data, 'yellow_taxis_trips', fake_rules
    )

    pd.testing.assert_frame_equal(transformed_data, fake_data)
    assert errors == {
        'error': {'wrong_name': 'coluna_inexistente'}
    }
    assert info == {
        'renomeação_colunas': {
            'antes': ['campo_1'],
            'depois': ['campo_1']
        }
    }


def test_duplicate_removal_missing_subset_column():
    fake_data = pd.DataFrame({
        'campo_1': [1, 1],
        'campo_2': [2, 2]
    })
    fake_rules = {
        'drop_duplicates': {'subset': ['coluna_inexistente']}
    }

    transforming = GenericTransforming({})
    transformed_data, info, errors = transforming.remove_duplicates(
        fake_data, 'yellow_taxis_trips', fake_rules
    )

    pd.testing.assert_frame_equal(transformed_data, fake_data)
    assert 'coluna_inexistente' in errors['error']['wrong_column']
    assert info == {'qtd_duplicatas': {'antes': 1, 'depois': 1}}


def test_generic_transforming_without_data():
    transforming = GenericTransforming({})

    with pytest.raises(
        GenericTransformingErrors,
        match='Erro, nenhum DF foi encontrado!',
    ):
        transforming.transform({})


def test_generic_transforming_collects_errors():
    fake_data = {
        'yellow_taxis_trips': pd.DataFrame({
            'campo_1': [1, 1],
            'campo_2': [2, 2]
        })
    }
    fake_rules = {
        'yellow_taxis_trips': {
            'drop_duplicates': {
                'subset': ['coluna_inexistente']
            },
            'fill_null_columns': {
                'outra_coluna_inexistente': 0
            },
            'columns_to_rename': {
                'mais_uma_coluna_inexistente': 'nome_novo'
            }
        }
    }

    transforming = GenericTransforming(fake_rules)
    transformed_data = transforming.transform(fake_data)

    result = transformed_data['yellow_taxis_trips']
    pd.testing.assert_frame_equal(result['data'], fake_data['yellow_taxis_trips'])
    errors = result['errors']['yellow_taxis_trips']['errors']
    assert 'coluna_inexistente' in errors[0]['error']['wrong_column']
    assert errors[1] == {
        'error': {'column_name': "'outra_coluna_inexistente'"}
    }
    assert errors[2] == {
        'error': {'wrong_name': 'mais_uma_coluna_inexistente'}
    }