from src.data_reading.interfaces.reading_interface import ReadingInterface
import logging 
logger = logging.getLogger(__name__)
import pandas as pd
class ParquetReadingErrors(Exception): 
    pass
class ParquetReading(ReadingInterface): 
    def __init__(self, parquet_files:dict[str,list[str]]) -> None: 
        self.parquet_files = parquet_files
        self.read_parquet :dict[str,pd.DataFrame] = {}
    def read_data(self) -> dict[str, pd.DataFrame]: 
        #Read Parquet files, transforming them on pandas DataFrames 
        if not self.parquet_files: 
            logger.error("Nenhum arquivo parquet foi declarado! ")
            raise ParquetReadingErrors('Nenhum arquivo parquet foi declarado! ')
        logger.info("Iniciando o fluxo de leitura de arquivos parquet...")
        for nome, files in self.parquet_files.items(): 
            logger.info(f'Lendo arquivos parquets no diretório {nome}...')
            concatenated_df = []
            if not files: 
                logger.warning(f"Nenhuma arquivo parquet em {nome} existe! ")
            else:
                for file in files: 
                    concatenated_df.append(pd.read_parquet(file))
                df = pd.concat(concatenated_df, ignore_index=True)
                self.read_parquet[nome] = df 
        logger.info("Finalizando o fluxo de leitura de parquets! ")
        return self.read_parquet