from src.data_transforming.implementations.parquets.taxis_trips_nyc_transformer import TaxisTripsTransformer
from utils.schema_validator import validate_schema
import pandas as pd


def test_success_taxis_trips_concatenation():
    fake_rules = {
        "essential_schema": ["VendorID"],
        "columns_types": ["int32"],
    }
    first_df = pd.DataFrame({"VendorID": pd.Series([1, 2], dtype="int32")})
    second_df = pd.DataFrame({"VendorID": pd.Series([3], dtype="int32")})

    transforming = TaxisTripsTransformer(validate_schema, fake_rules)
    transformed_data, errors = transforming.concatenate_dfs(
        {"january": first_df, "february": second_df}, fake_rules
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
