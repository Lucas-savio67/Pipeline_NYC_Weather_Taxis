from src.data_transforming.implementations.parquets.taxis_trips_nyc_transformer import TaxisTripsTransformer
from src.data_transforming.implementations.parquets.taxis_trips_nyc_transformer import TaxisTripsErrors
from utils.schema_validator import validate_schema
import pandas as pd
import pytest


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
    }
    fake_data = {
        "january": pd.DataFrame({"VendorID": pd.Series([1, 2], dtype="int32")}),
        "february": pd.DataFrame({"VendorID": pd.Series([3], dtype="int32")}),
    }

    transforming = TaxisTripsTransformer(validate_schema, fake_rules)
    transformed_data, errors = transforming.transform(fake_data)

    expected_df = pd.DataFrame({"VendorID": pd.Series([1, 2, 3], dtype="int32")})
    pd.testing.assert_frame_equal(
        transformed_data["yellow_taxis_trips"], expected_df
    )
    assert errors == {}


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
