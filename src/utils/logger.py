import logging
from datetime import datetime

def get_logger(name: str):
    logging.basicConfig(
        filename=f"logs/{datetime.now().strftime('%Y-%m-%d')}.log",
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger(name)
