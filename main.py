from config.logging_config import logging 
from src.data_reading.data_reading import DataReading
from src.data_ingestion.data_ingestion import DataIngestion
from src.data_extraction.data_extraction import DataExtraction
from src.data_transforming.data_transforming import DataTransforming
import boto3
from config.aws_credencials import load_aws_credencials, CredencialsErrors
logger = logging.getLogger(__name__)
from config.settings import reading_settings, ingestion_settings, extraction_settings, specific_transforming_settings, generic_transformations_settings
def main():
    try :
        credencials = load_aws_credencials()
        s3_client = boto3.client(
            credencials['service'] , 
            aws_access_key_id = credencials['aws_access_key_id'] , 
            aws_secret_access_key = credencials['aws_secret_access_key'] , 
            region_name = credencials['region_name']
            )
        settings = reading_settings()
        read_data = {}
        for nome, implementations in settings.items(): 

            reading = DataReading(implementations)
            read = reading.read_general_data()
            read_data[nome] = read 
        settings = ingestion_settings(s3_client, credencials['bucket_name'])
        for nome, implementations in settings.items(): 
            ingestion = DataIngestion(implementations[0])
            if nome == 'Parquets': 
                ingest = ingestion.ingest_general_data('bronze', implementations[2], implementations[1] )
            else: 

                ingest = ingestion.ingest_general_data('bronze', read_data[nome], implementations[1])
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