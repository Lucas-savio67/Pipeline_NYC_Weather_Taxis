from pathlib import Path 
def discover_parquets(paths:dict) -> dict: 
    discovered = {}
    try :
        for nome,diretorio in paths.items(): 
            discovered[nome] = list(Path(diretorio).rglob("*.parquet"))
        
        return discovered
    except Exception as e: 
        raise str(e)