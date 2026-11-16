from abc import ABC, abstractmethod
import pandas as pd 
from typing import Generic, TypeVar 
T = TypeVar('T')
from config.return_contracts.transforming_contract import TransformingInfo
class TransformingInterface(ABC, Generic[T]): 
    @abstractmethod 
    def transform(self, data:T) -> TransformingInfo : 
        pass 