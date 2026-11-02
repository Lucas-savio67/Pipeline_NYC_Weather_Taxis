from abc import ABC, abstractmethod 
from typing import Any


class ExtractionInterface(ABC): 
    @abstractmethod 
    def extract(self, bucket_name: str, layer: str) -> tuple[dict[str, Any], dict[str, dict[str, str]]]:
        pass