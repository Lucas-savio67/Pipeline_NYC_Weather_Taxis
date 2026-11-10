from config.logging_config import logging 
from src.data_reading.data_reading import DataReading
from src.data_ingestion.data_ingestion import DataIngestion
from src.data_extraction.data_extraction import DataExtraction
from src.data_transforming.data_transforming import DataTransforming
import boto3
from config.aws_credencials import load_aws_credencials, CredencialsErrors
from config.stage_settings.reading_config.reading_settings import ReadingOrchestration
from config.stage_settings.reading_config.reading_data import return_read_data
from config.stage_settings.ingestion_config.ingestion_data import return_ingestion_data 
from config.stage_settings.ingestion_config.ingestion_settings import IngestionOrchestration

logger = logging.getLogger(__name__)
from config.settings import  extraction_settings, specific_transforming_settings, generic_transformations_settings
def main():
    try :
        credencials = load_aws_credencials()
        s3_client = boto3.client(
            credencials['service'] , 
            aws_access_key_id = credencials['aws_access_key_id'] , 
            aws_secret_access_key = credencials['aws_secret_access_key'] , 
            region_name = credencials['region_name']
            )
        reading = ReadingOrchestration(DataReading)
        read_data_info = return_read_data()
        read_data = reading.orchestrate_reading(read_data_info)
        ingestion = IngestionOrchestration(DataIngestion)
        ingestion_data_info = return_ingestion_data(s3_client, credencials['bucket_name'], 'bronze', read_data)
        ingest_data = ingestion.orchestrate_ingestion(ingestion_data_info)
        print(ingest_data)
        settings =   extraction_settings(s3_client, credencials['bucket_name'])
        extracted_data = {}
        for nome, implementations in settings.items(): 
            extraction = DataExtraction(implementations[0])
            extract = extraction.extract_general_data(implementations[1], 'bronze')
            extracted_data[nome] = extract
        settings = specific_transforming_settings()
        transformed_data = {}
        for tipo, info in extracted_data.items(): 
            if tipo == "JSON": 
                jsons = settings.get('JSON')
                for nome, implementation in jsons.items(): 
                    transforming = DataTransforming(implementation)
                    transform = transforming.transform_general_data(info[nome], nome)
                    transformed_data= transform
            else: 
                parquets = settings.get('parquets')
                for nome, implementation in parquets.items(): 
                    transforming = DataTransforming(implementation)
                    transform = transforming.transform_general_data(info, nome)                
                    transformed_data = transform 
        settings = generic_transformations_settings()
        transforming = DataTransforming(settings)
        transform = transforming.transform_general_data(transformed_data, 'generic')
        print(transform)
                
        return 'Fluxo finalizado com sucesso! '
    except CredencialsErrors as e: 
        logger.warning(f"Erro ao carregar credenciais AWS, impossível iniciar o fluxo: {str(e)}")
    except Exception as e: 
        logger.warning(f"Erro {str(e)} ao executar o Pipeline! ")
    
print(main())