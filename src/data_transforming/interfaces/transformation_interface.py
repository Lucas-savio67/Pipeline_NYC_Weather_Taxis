from abc import ABC, abstractmethod
import pandas as pd 
from typing import Any 
class TransformingInterface(ABC): 
    @abstractmethod 
    def transform(self, data:Any, nome:str) -> tuple[dict[str,pd.DataFrame] , dict[str,dict]] : 
        pass 