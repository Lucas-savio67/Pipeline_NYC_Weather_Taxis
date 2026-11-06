import pandas as pd
from typing import Any

def validate_schema(df: pd.DataFrame, rules:dict[str,Any]) -> tuple[bool, dict[str, str]]:

    columns = df.columns.to_list

    essential = all(column in columns for column in rules['essential_schema'])
    if essential: 
        difference = [coluna for coluna in rules['essential_schema'] if coluna not in columns]
        types = df[rules['essential_schema']].dtypes.astype(str).tolist()
        if types== rules['columns_types']: 
            return True, {}
        else: 
            column_difference = [tipo for tipo in rules['columns_types'] if tipo not in types]
            return False, column_difference
    else: 
        return essential, difference
