from abc import ABC, abstractmethod 
from config.return_contracts.reading_contract import ReadingInfo
class ReadingInterface(ABC): 
    @abstractmethod
    def read_data(self) -> ReadingInfo: 
        pass 
    