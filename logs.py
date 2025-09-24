import logging
import os

if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/sistema.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

def log_info(mensagem):
    logging.info(mensagem)

def log_error(mensagem):
    logging.error(mensagem)
