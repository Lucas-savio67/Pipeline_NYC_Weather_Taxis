from config.logging_config import logging 
from src.data_reading.data_reading import DataReading 
from src.data_ingestion.data_ingestion import DataIngestion
from config.settings import reading_settings, ingestion_settings
def main():
    settings = reading_settings()
    read_data = {}
    for nome, implementations in settings.items(): 

        reading = DataReading(implementations)
        read = reading.read_general_data()
        read_data[nome] = read 
    settings = ingestion_settings()
    for nome, implementations in settings.items(): 
        ingestion = DataIngestion(implementations[0])
        if nome == 'Parquets': 
            ingest = ingestion.ingest_general_data('bronze', implementations[2], implementations[1] )
        else: 

            ingest = ingestion.ingest_general_data('bronze', read_data[nome], implementations[1])
        
    return 'Fluxo finalizado com sucesso! '
print(main())