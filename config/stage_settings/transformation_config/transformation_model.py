from dataclasses import dataclass 
from src.data_transforming.interfaces.transformation_interface import TransformingInterface
from typing import Any
@dataclass(frozen=True) 
class TransformationModel: 
    implementation:TransformingInterface 
    data:Any 
    nome:str 