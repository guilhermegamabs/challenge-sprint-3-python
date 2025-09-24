import sqlite3
from pathlib import Path

DB_FILE = Path("sprint3_seguro.db")

def conectar():
    return sqlite3.connect(DB_FILE)

def criar_tabelas():
    with conectar() as conn:
        cur = conn.cursor()
        # Clientes
        cur.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            cpf TEXT PRIMARY KEY,
            nome TEXT NOT NULL,
            data_nascimento TEXT,
            endereco TEXT,
            telefone TEXT,
            email TEXT
        )
        """)
        # Seguros / Apólices
        cur.execute("""
        CREATE TABLE IF NOT EXISTS seguros (
            numero_apolice TEXT PRIMARY KEY,
            tipo TEXT NOT NULL,
            cpf TEXT NOT NULL,
            valor_mensal REAL NOT NULL,
            ativo INTEGER DEFAULT 1,
            created_at TEXT,
            FOREIGN KEY(cpf) REFERENCES clientes(cpf)
        )
        """)
        # Seguro Automóvel
        cur.execute("""
        CREATE TABLE IF NOT EXISTS seguro_automovel (
            numero_apolice TEXT PRIMARY KEY,
            modelo TEXT, ano INTEGER, placa TEXT, cor TEXT, valor_segurado REAL,
            FOREIGN KEY(numero_apolice) REFERENCES seguros(numero_apolice)
        )
        """)
        # Seguro Vida
        cur.execute("""
        CREATE TABLE IF NOT EXISTS seguro_vida (
            numero_apolice TEXT PRIMARY KEY,
            valor_segurado REAL, beneficiarios TEXT,
            FOREIGN KEY(numero_apolice) REFERENCES seguros(numero_apolice)
        )
        """)
        # Seguro Residencial
        cur.execute("""
        CREATE TABLE IF NOT EXISTS seguro_residencial (
            numero_apolice TEXT PRIMARY KEY,
            endereco TEXT, cep TEXT, valor_imovel REAL,
            FOREIGN KEY(numero_apolice) REFERENCES seguros(numero_apolice)
        )
        """)
        # Sinistros
        cur.execute("""
        CREATE TABLE IF NOT EXISTS sinistros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_apolice TEXT NOT NULL,
            descricao TEXT,
            data_ocorrencia TEXT,
            status TEXT DEFAULT 'ABERTO',
            FOREIGN KEY(numero_apolice) REFERENCES seguros(numero_apolice)
        )
        """)
        # Usuários
        cur.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            username TEXT PRIMARY KEY,
            senha TEXT NOT NULL,
            perfil TEXT CHECK(perfil IN ('admin','comum')) NOT NULL
        )
        """)
        # Auditoria
        cur.execute("""
        CREATE TABLE IF NOT EXISTS auditoria (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT,
            operacao TEXT,
            entidade TEXT,
            referencia TEXT,
            data_hora TEXT,
            nivel TEXT
        )
        """)
        conn.commit()
