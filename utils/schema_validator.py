import pandas as pd
from typing import Any

def validate_schema(df: pd.DataFrame, rules: dict[str, Any]) -> tuple[bool, list[str]]:

    columns = df.columns.to_list()
    difference = [column for column in rules['essential_schema'] if column not in columns]

    essential = all(column in columns for column in rules['essential_schema'])
    if essential: 
        types = df[rules['essential_schema']].dtypes.astype(str).tolist()
        expected_types = rules['columns_types']
        if types == expected_types:
            return True, []
        else: 
            column_difference = [coluna for coluna in  types if coluna not in expected_types]
            return False, column_difference
    else: 
        return essential, difference
