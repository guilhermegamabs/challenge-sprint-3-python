import logging
from datetime import datetime
from db import conectar
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "auditoria.log"

# Configuração básica do logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def registrar_evento(usuario, operacao, entidade, referencia, nivel="INFO"):
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Registrar no console
    print(f"[{nivel}] {data_hora} | {usuario} | {operacao} | {entidade} | {referencia}")
    
    # Registrar no log
    if nivel.upper() == "INFO":
        logging.info(f"{usuario} | {operacao} | {entidade} | {referencia}")
    else:
        logging.error(f"{usuario} | {operacao} | {entidade} | {referencia}")
    
    # Registrar na tabela auditoria do SQLite
    with conectar() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO auditoria (usuario, operacao, entidade, referencia, data_hora, nivel)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (usuario, operacao, entidade, referencia, data_hora, nivel))
        conn.commit()
