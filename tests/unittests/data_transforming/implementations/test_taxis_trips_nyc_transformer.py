from src.data_transforming.implementations.parquets.taxis_trips_nyc_transformer import TaxisTripsTransformer
from src.data_transforming.implementations.parquets.taxis_trips_nyc_transformer import TaxisTripsErrors
from utils.schema_validator import validate_schema
import pandas as pd
import pytest
import logging

def test_success_taxis_trips_concatenation():
    fake_rules = {
        "essential_schema": ["VendorID"],
        "columns_types": ["int32"],
    }
    first_df = pd.DataFrame({"VendorID": pd.Series([1, 2], dtype="int32")})
    second_df = pd.DataFrame({"VendorID": pd.Series([3], dtype="int32")})

    transforming = TaxisTripsTransformer(validate_schema, fake_rules)
    transformed_data, errors = transforming.concatenate_dfs(
        {"january": first_df, "february": second_df}
    )

    expected_df = pd.DataFrame({"VendorID": pd.Series([1, 2, 3], dtype="int32")})
    pd.testing.assert_frame_equal(transformed_data, expected_df)
    assert errors == {}


def test_success_taxis_trips_transforming():
    fake_rules = {
        "essential_schema": ["VendorID"],
        "columns_types": ["int32"], 
        'new_columns': { 
            'VendorName': { 
                'column_data': { 
                    '1': 'FakeVendor' , 
                    '2': 'FakeVendor2' , 
                    '3':'FakeVendor3'
                } ,
                'column': 'VendorID'
            }
        }
    }
    fake_data = {
        "january": pd.DataFrame({"VendorID": pd.Series([1, 2], dtype="int32")}),
        "february": pd.DataFrame({"VendorID": pd.Series([3], dtype="int32")}),
    }

    transforming = TaxisTripsTransformer(validate_schema, fake_rules)
    transform = transforming.transform(fake_data)
    expected_df = pd.DataFrame({"VendorID": pd.Series([1, 2, 3], dtype="int32") , 'VendorName': ['FakeVendor', 'FakeVendor2', 'FakeVendor3']})
    
    pd.testing.assert_frame_equal(
        transform.real_transformed_data['yellow_taxis_trips'], expected_df
    )
    assert transform.errors == {'yellow_taxis_trips': {'concatenation': {}, 'columns': {}}}


def test_no_data():
    fake_rules = {
        "essential_schema": ["VendorID"],
        "columns_types": ["int32"],
    }
    transforming = TaxisTripsTransformer(validate_schema, fake_rules)

    with pytest.raises(TaxisTripsErrors):
        transforming.transform({})


def test_no_rules():
    fake_data = {
        "january": pd.DataFrame({"VendorID": pd.Series([1], dtype="int32")})
    }
    transforming = TaxisTripsTransformer(validate_schema, {})

    with pytest.raises(TaxisTripsErrors):
        transforming.transform(fake_data)


def test_no_valid_dataframes():
    fake_rules = {
        "essential_schema": ["VendorID"],
        "columns_types": ["int32"],
    }
    fake_data = {"january": pd.DataFrame({"invalid_column": [1]})}
    transforming = TaxisTripsTransformer(validate_schema, fake_rules)

    with pytest.raises(TaxisTripsErrors):
        transforming.transform(fake_data)
def test_success_columns_creating(): 
    fake_rules = { 
        'new_columns': { 
            'fake_column_1': { 
                'column_data': { 
                    '1': 'teste_1' , 
                    '2': 'teste_2'
                } , 
                'column': 'fake_column_2'
            }
        }
    }
    fake_data = pd.DataFrame({ 
        'fake_column_2': [1,2]
    })
    expected_df = pd.DataFrame({ 
        'fake_column_2': [1,2] , 
        'fake_column_1': ['teste_1', 'teste_2']
    })
    
    transforming = TaxisTripsTransformer(validate_schema , fake_rules)
    df, errors = transforming.create_new_columns(fake_data, fake_rules)
    pd.testing.assert_frame_equal(df,expected_df)
    assert errors == {}
def test_no_column_rule(): 
    fake_rules = { 
            'no_rule_here' : {}
        }
    fake_data = pd.DataFrame({ 
            'fake_column_2': [1,2]
        })
    
        
    transforming = TaxisTripsTransformer(validate_schema , fake_rules)
    with pytest.raises(TaxisTripsErrors):
        transforming.create_new_columns(fake_data, fake_rules)
def test_no_column_info(caplog): 
    fake_rules = { 
                'new_columns': { 
                    'VendorName': {}
                }
            }
    fake_data = pd.DataFrame({ 
                'fake_column_2': [1,2]
            })
        
            
    transforming = TaxisTripsTransformer(validate_schema , fake_rules)
    with caplog.at_level(logging.WARNING):
        df, errors = transforming.create_new_columns(fake_data, fake_rules)
    assert errors == {'VendorName': {'error': 'no_info'}}