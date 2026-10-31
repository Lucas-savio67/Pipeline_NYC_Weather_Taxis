from config.logging_config import logging 
from src.data_reading.data_reading import DataReading 
from config.settings import reading_settings
def main(): 
    settings = reading_settings()
    read_data = {}
    for nome, implementations in settings.items(): 

        reading = DataReading(implementations)
        read = reading.read_general_data()
        read_data[nome] = read 
    return 'Fluxo finalizado com sucesso! '
print(main())