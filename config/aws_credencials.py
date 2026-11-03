class CredencialsErrors(Exception): 
    pass 
import os 
from dotenv import load_dotenv 
from typing import Any
load_dotenv()
def load_aws_credencials() -> dict[str,Any]: 
    aws_credencials_dict = { 
        'service': 's3', 
        'aws_secret_access_key': os.getenv("AWS_SECRET_ACCESS_KEY") ,
        'aws_access_key_id': os.getenv('AWS_ACCESS_KEY_ID') ,
        'region_name': os.getenv("AWS_REGION") , 
        'bucket_name': os.getenv("AWS_BUCKET_NAME")
    }
    for nome, credencial in aws_credencials_dict.items(): 
        if credencial is None: 
            raise CredencialsErrors(f"Erro, a variável AWS {nome} retornou None! ")
        else: 
            continue 
    return aws_credencials_dict