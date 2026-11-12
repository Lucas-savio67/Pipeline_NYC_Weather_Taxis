from src.data_extraction.data_extraction import DataExtraction
from typing import Any
class ExtractiongOrchestration: 
    def __init__(self, data_extraction:DataExtraction) -> None: 
        self.extraction = data_extraction 
    def orchestrate_extraction(self,implementations:dict[str, Any]) -> dict[str, Any]: 
        extracted_data = {}
        for tipo, model in implementations.items(): 
            extraction = self.extraction(model.implementation).extract_general_data(model.bucket_name, model.layer)
            extracted_data[tipo] = extraction 
        return extracted_data
