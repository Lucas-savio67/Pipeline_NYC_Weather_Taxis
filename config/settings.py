from src.data_reading.implementations.api_reading import APIReading 
from data.apis.apis_config import apis
def reading_settings(): 
    implementations = {
        'APIs': APIReading(apis),
        
    }
    return implementations