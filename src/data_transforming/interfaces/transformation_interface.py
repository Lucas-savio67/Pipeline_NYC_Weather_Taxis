from abc import ABC, abstractmethod
import pandas as pd 
from typing import Generic, TypeVar 
T = TypeVar('T')

class TransformingInterface(ABC, Generic[T]): 
    @abstractmethod 
    def transform(self, data:T) -> tuple[pd.DataFrame , dict[str,dict]] : 
        pass 