from src.data_reading.implementations.parquet_reading import ParquetReading, ParquetReadingErrors 
import pytest 
import pandas as pd 
import logging 
logger = logging.getLogger(__name__)
def test_success_parquet_reading(tmp_path): 
    fake_df_1 = pd.DataFrame({ 
        '1': [1,2,3] , 
        '2': [4,5,6]
    })
    fake_df_2 = pd.DataFrame({ 
        '1': [7,8,9] , 
        '2': [10,11,12]
    })
    directory = tmp_path / "trips"
    directory.mkdir()
    file_1 = directory / 'trip_1.parquet'
    file_2 = directory / 'trip_2.parquet'
    fake_df_1.to_parquet(file_1)
    fake_df_2.to_parquet(file_2)
    parquets_files = { 
        'trips': [file_1, file_2]
    }    
    fake_final_df = pd.DataFrame({ 
        '1': [1,2,3, 7,8,9], 
        '2': [4,5,6,10,11,12] , 
        
    })
    
    reading = ParquetReading(parquets_files)
    read = reading.read_data()
    pd.testing.assert_frame_equal(fake_final_df, read['trips'])
def test_no_parquets(): 
    reading = ParquetReading({})
    with pytest.raises(ParquetReadingErrors):
        read = reading.read_data()
def test_no_files(caplog): 
    reading = ParquetReading({'trips': []})
    with caplog.at_level(logging.WARNING): 
        read = reading.read_data()
    assert 'Nenhum' in caplog.text