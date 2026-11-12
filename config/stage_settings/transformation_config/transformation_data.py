from src.data_transforming.implementations.jsons.nasa_power_transformation import NasaPowerTransformation
from src.data_transforming.implementations.parquets.taxis_trips_nyc_transformer import TaxisTripsTransformer
from src.data_transforming.generic_implementation.generic_implementations import GenericTransforming
from config.stage_settings.transformation_config.transformation_model import TransformationModel
from config.transformations_rules.specific_rules.nasa_power_rules import nasa_power_rules
from config.transformations_rules.specific_rules.taxis_trips_rules import taxis_trips_rules
from config.transformations_rules.generic_rules.generic_rules import generic_rules
from typing import Any
import pandas as pd
from utils.schema_validator import validate_schema
def return_specific_transforming_data(extracted_data:dict[str,Any]) -> dict[str, TransformationModel]: 
    json_data = extracted_data['JSON']
    parquet_data = extracted_data['Parquets']
    implementations = { 
        'yellow_taxis_trips': TransformationModel(TaxisTripsTransformer(validate_schema, taxis_trips_rules), parquet_data, 'yellow_taxis_trips'),
        'bronze/JSONs/NasaPower/NasaPower.json': TransformationModel(NasaPowerTransformation(nasa_power_rules), json_data['bronze/JSONs/NasaPower/NasaPower.json'], 'NasaPower') , }
    return implementations
def return_generic_transforming_data(transformed_data:dict[str,pd.DataFrame]) -> dict[str,TransformationModel]: 
    implementations = { 
        'bronze/JSONs/NasaPower/NasaPower.json': TransformationModel(GenericTransforming(generic_rules), transformed_data, 'generic')
    }
    return implementations