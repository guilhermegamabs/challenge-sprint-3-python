import csv
from db import conectar
from datetime import datetime
from pathlib import Path

EXPORT_DIR = Path("exports")
EXPORT_DIR.mkdir(exist_ok=True)

def receita_mensal():
    with conectar() as conn:
        cur = conn.cursor()
        cur.execute("SELECT SUM(valor_mensal) FROM seguros WHERE ativo=1")
        total = cur.fetchone()[0] or 0
        return total

def top_clientes(n=5):
    with conectar() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT c.nome, SUM(s.valor_mensal) as total
            FROM clientes c
            JOIN seguros s ON c.cpf = s.cpf
            WHERE s.ativo=1
            GROUP BY c.nome
            ORDER BY total DESC
            LIMIT ?
        """, (n,))
        return cur.fetchall()

def sinistros_por_status():
    with conectar() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT status, COUNT(*) FROM sinistros GROUP BY status
        """)
        return cur.fetchall()

def exportar_csv(nome_arquivo, dados, cabecalho):
    arquivo = EXPORT_DIR / f"{nome_arquivo}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(arquivo, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(cabecalho)
        writer.writerows(dados)
    print(f"Relatório exportado para: {arquivo}")
