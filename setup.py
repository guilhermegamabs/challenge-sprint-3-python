import sqlite3
from dao import criar_cliente, criar_seguro
from usuarios import criar_usuario
from db import conectar

def setup_inicial():
    with conectar() as conn:
        cur = conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            username TEXT PRIMARY KEY,
            senha TEXT NOT NULL,
            perfil TEXT NOT NULL
        )
        """)

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

        cur.execute("""
        CREATE TABLE IF NOT EXISTS seguros (
            numero_apolice TEXT PRIMARY KEY,
            tipo TEXT,
            cpf TEXT,
            valor_mensal REAL,
            ativo INTEGER DEFAULT 1,
            created_at TEXT,
            FOREIGN KEY(cpf) REFERENCES clientes(cpf)
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS sinistros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_apolice TEXT,
            descricao TEXT,
            data_ocorrencia TEXT,
            status TEXT DEFAULT 'ABERTO',
            FOREIGN KEY(numero_apolice) REFERENCES seguros(numero_apolice)
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS seguro_automovel (
            numero_apolice TEXT PRIMARY KEY,
            modelo TEXT,
            ano INTEGER,
            placa TEXT,
            cor TEXT,
            valor_segurado REAL,
            FOREIGN KEY(numero_apolice) REFERENCES seguros(numero_apolice)
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS seguro_vida (
            numero_apolice TEXT PRIMARY KEY,
            valor_segurado REAL,
            beneficiarios TEXT,
            FOREIGN KEY(numero_apolice) REFERENCES seguros(numero_apolice)
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS seguro_residencial (
            numero_apolice TEXT PRIMARY KEY,
            endereco TEXT,
            cep TEXT,
            valor_imovel REAL,
            FOREIGN KEY(numero_apolice) REFERENCES seguros(numero_apolice)
        )
        """)

        conn.commit()

    try:
        criar_usuario("admin", "123456", "admin", usuario_ativo="sistema")
        print("Usuário admin criado ou já existia.")
    except Exception as e:
        print(f"Erro ao criar usuário admin: {e}")

    try:
        criar_cliente("12345678901", "João Silva", "1980-05-12", "Rua A, 100", "1112345678", "joao@email.com", usuario="admin")
        criar_cliente("98765432100", "Maria Oliveira", "1990-08-25", "Rua B, 200", "11987654321", "maria@email.com", usuario="admin")
        criar_cliente("01508190569", "Andréa", "1985-03-05", "Av. C, 300", "11999998888", "andrea@email.com", usuario="admin")
        print("Clientes iniciais cadastrados ou já existiam.")
    except Exception as e:
        print(f"Erro ao criar clientes: {e}")

    try:
        criar_seguro("AP1001", "Automovel", "12345678901", 2000.0, usuario="admin")
        criar_seguro("AP1002", "Vida", "98765432100", 200.0, usuario="admin")
        criar_seguro("AP1003", "Residencial", "01508190569", 100.0, usuario="admin")
        criar_seguro("AP1004", "Automóvel", "12345678901", 1500.0, usuario="admin")
        print("Seguros iniciais cadastrados ou já existiam.")
    except Exception as e:
        print(f"Erro ao criar seguros: {e}")

if __name__ == "__main__":
    setup_inicial()
