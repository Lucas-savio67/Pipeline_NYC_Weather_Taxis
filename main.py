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
from config.stage_settings.extraction_config.extraction_data import return_extraction_data 
from config.stage_settings.extraction_config.extraction_settings import ExtractiongOrchestration
from config.stage_settings.transformation_config.transformation_settings import TransformingOrchestration 
from config.stage_settings.transformation_config.transformation_data import return_specific_transforming_data, return_generic_transforming_data

logger = logging.getLogger(__name__)
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
        #ingest_data = ingestion.orchestrate_ingestion(ingestion_data_info)
        extraction = ExtractiongOrchestration(DataExtraction)
        extract_data_info = return_extraction_data(s3_client, credencials['bucket_name'], 'bronze')
        extracted = extraction.orchestrate_extraction(extract_data_info)
        transformation = TransformingOrchestration(DataTransforming)
        transform_data_info = return_specific_transforming_data(extracted)
        specific_transform = transformation.orchestrate_transforming(transform_data_info)
        generic_transform_data_info = return_generic_transforming_data(specific_transform)
        generic_transform = transformation.orchestrate_transforming(generic_transform_data_info)
        return 'Fluxo finalizado com sucesso! '
    except CredencialsErrors as e: 
        logger.warning(f"Erro ao carregar credenciais AWS, impossível iniciar o fluxo: {str(e)}")
    except Exception as e: 
        logger.warning(f"Erro {str(e)} ao executar o Pipeline! ")
if __name__ == '__main__':
    main()