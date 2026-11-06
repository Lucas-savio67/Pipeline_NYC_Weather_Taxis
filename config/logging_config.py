import logging 
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(
            'pipeline_logs/logs',
            mode='w',
            encoding='utf-8',
        )
    ],
)