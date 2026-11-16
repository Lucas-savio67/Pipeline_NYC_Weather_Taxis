from dataclasses import dataclass,field 
import pandas as pd
from typing import Any
@dataclass(frozen=True)
class TransformingInfo: 
    real_transformed_data:dict[str, pd.DataFrame] = field(default_factory=dict)
    transformed_data:dict[str, Any] = field(default_factory=dict)
    errors:dict[str, list] = field(default_factory=dict)
    info:dict[str, Any] = field(default_factory=dict) 