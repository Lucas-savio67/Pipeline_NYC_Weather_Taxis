from src.data_transforming.data_transforming import DataTransforming
from typing import Any
class TransformingOrchestration: 
    def __init__(self, data_transforming:DataTransforming) -> None: 
        self.transforming = data_transforming 
    def orchestrate_transforming(self, implementations:dict[str, Any]) -> dict[str]: 
        transformed_data = {}
        for nome, model in implementations.items(): 
            transform = self.transforming(model.implementation).transform_general_data(model.data, model.nome) 
            transformed_data.update(transform)
        return transformed_data