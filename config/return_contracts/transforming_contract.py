from dataclasses import dataclass 
import pandas as pd
from typing import Any
@dataclass(frozen=True)
class TransformingInfo: 
    real_transformed_data:dict[str, pd.DataFrame]
    transformed_data:dict[str, bool]
    errors:dict[str, list]
    info:dict[str, list]