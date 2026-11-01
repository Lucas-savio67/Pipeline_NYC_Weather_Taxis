from src.data_reading.interfaces.reading_interface import ReadingInterface
from typing import Any
import json
import requests 
import logging 
logger = logging.getLogger(__name__)
class APIReadingErrors(Exception): 
    pass
class APIReading(ReadingInterface): 
    def __init__(self, apis:dict[str,dict]) -> None: 
        self.apis = apis
        self.read_apis: dict[str, Any] = {}
    #Send GET requisitions to the declarated APIs in self.apis 
    def read_data(self) -> dict[str,Any]:
        errors = {}
        if not self.apis: 
            logger.error("Erro, nenhum API foi declarada! ")
            raise APIReadingErrors('Erro, nenhum API foi declarada! ')
        logger.info('Iniciando o fluxo de leitura de APIs! ')
        for nome, info_api in self.apis.items(): 
            logger.info(f'Lendo a API {nome}...')
            url = info_api.get('url', None)
            if not url: 
                logger.warning(f'A API de {nome} não possui URL declarada! ')
            else: 
                params = info_api.get('params', None)
                headers = info_api.get('headers', None)
                try :
                    response = requests.get(url=url, params=params, headers=headers)
                    response.raise_for_status()
                    data = response.json()
                    logger.info(f'A API {nome} foi lida com sucesso! ')
                    self.read_apis[nome] = data 
                except requests.exceptions.RequestException as e: 
                    logger.warning(f"Erro, {e} ao enviar a requisição! ")
                    errors[nome] = {'error': str(e)}
                except json.JSONDecodeError as e: 
                    
                    logger.warning("Erro, json inválido encontrado ")
                    errors[nome] = {'error': str(e)}
                except Exception as e: 
                    logger.warning(f"Erro: {str(e)}! ")
                    errors[nome] = {'error': str(e)}
        logger.info("Finalizando o fluxo de leitura de APIs! ")
        return self.read_apis, errors


