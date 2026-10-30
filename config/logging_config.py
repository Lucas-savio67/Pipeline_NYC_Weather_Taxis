import logging 
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='pipeline_logs/logs',  # Opcional: salva em arquivo em vez do console
    filemode='a'         # 'a' para adicionar (append), 'w' para sobrescrever
)