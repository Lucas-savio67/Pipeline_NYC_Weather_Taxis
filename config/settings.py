from src.data_reading.implementations.api_reading import APIReading 
from src.data_reading.implementations.parquet_reading import ParquetReading
from utils.discover_parquets import discover_parquets
from data.apis.apis_config import apis
def reading_settings(): 
    files = { 
        'yellow_taxis_trips': 'data/parquets/yellow_taxis_trips_NYC'
    }
    parquets = discover_parquets(files)
    implementations = {
        'APIs': APIReading(apis),
        'Parquets': ParquetReading(parquets),
    }
    return implementations