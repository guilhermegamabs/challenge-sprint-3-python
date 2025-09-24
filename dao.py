from db import conectar
from datetime import datetime
from auditoria import registrar_evento
from validacoes import validar_cpf, OperacaoNaoPermitida

# --------------------- CLIENTES ---------------------
def criar_cliente(cpf, nome, data_nasc=None, endereco=None, telefone=None, email=None, usuario="sistema"):
    validar_cpf(cpf)
    with conectar() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM clientes WHERE cpf=?", (cpf,))
        if cur.fetchone():
            print(f"Cliente {cpf} já existe.")
            return
        cur.execute("""
            INSERT INTO clientes (cpf, nome, data_nascimento, endereco, telefone, email)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (cpf, nome, data_nasc, endereco, telefone, email))
        conn.commit()
    registrar_evento(usuario, "CRIAR", "CLIENTE", cpf)

def listar_clientes():
    with conectar() as conn:
        cur = conn.cursor()
        cur.execute("SELECT cpf, nome, data_nascimento, endereco, telefone, email FROM clientes")
        return cur.fetchall()

def buscar_cliente(cpf):
    with conectar() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM clientes WHERE cpf = ?", (cpf,))
        return cur.fetchone()

def atualizar_cliente(cpf, nome=None, data_nasc=None, endereco=None, telefone=None, email=None, usuario="sistema"):
    with conectar() as conn:
        cur = conn.cursor()
        cur.execute("""
            UPDATE clientes
            SET nome = COALESCE(?, nome),
                data_nascimento = COALESCE(?, data_nascimento),
                endereco = COALESCE(?, endereco),
                telefone = COALESCE(?, telefone),
                email = COALESCE(?, email)
            WHERE cpf = ?
        """, (nome, data_nasc, endereco, telefone, email, cpf))
        conn.commit()
    registrar_evento(usuario, "ATUALIZAR", "CLIENTE", cpf)

def remover_cliente(cpf, usuario="sistema"):
    with conectar() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM clientes WHERE cpf = ?", (cpf,))
        conn.commit()
    registrar_evento(usuario, "REMOVER", "CLIENTE", cpf)

# --------------------- SEGUROS ---------------------
def criar_seguro(numero_apolice, tipo, cpf, valor_mensal, usuario="sistema"):
    with conectar() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM seguros WHERE numero_apolice=?", (numero_apolice,))
        if cur.fetchone():
            print(f"Seguro {numero_apolice} já existe.")
            return
        cur.execute("""
            INSERT INTO seguros (numero_apolice, tipo, cpf, valor_mensal, ativo, created_at)
            VALUES (?, ?, ?, ?, 1, ?)
        """, (numero_apolice, tipo, cpf, valor_mensal, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
    registrar_evento(usuario, "CRIAR", "SEGURO", numero_apolice)

def listar_seguros():
    with conectar() as conn:
        cur = conn.cursor()
        cur.execute("SELECT numero_apolice, tipo, cpf, valor_mensal, ativo FROM seguros")
        return cur.fetchall()

def buscar_seguro(numero_apolice):
    with conectar() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM seguros WHERE numero_apolice = ?", (numero_apolice,))
        return cur.fetchone()

def atualizar_seguro(numero_apolice, valor_mensal=None, ativo=None, usuario="sistema"):
    seguro = buscar_seguro(numero_apolice)
    if not seguro:
        raise ValueError("Seguro não encontrado")
    with conectar() as conn:
        cur = conn.cursor()
        cur.execute("""
            UPDATE seguros
            SET valor_mensal = COALESCE(?, valor_mensal),
                ativo = COALESCE(?, ativo)
            WHERE numero_apolice = ?
        """, (valor_mensal, ativo, numero_apolice))
        conn.commit()
    registrar_evento(usuario, "ATUALIZAR", "SEGURO", numero_apolice)

def cancelar_seguro(numero_apolice, usuario="sistema"):
    seguro = buscar_seguro(numero_apolice)
    if not seguro:
        raise ValueError("Seguro não encontrado")
    if seguro[4] == 0:
        raise OperacaoNaoPermitida("Seguro já cancelado")
    atualizar_seguro(numero_apolice, ativo=0, usuario=usuario)
    registrar_evento(usuario, "CANCELAR", "SEGURO", numero_apolice)

# --------------------- SINISTROS ---------------------
def registrar_sinistro(numero_apolice, descricao, data_ocorrencia, usuario="sistema"):
    seguro = buscar_seguro(numero_apolice)
    if not seguro:
        raise ValueError("Seguro não encontrado")
    with conectar() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO sinistros (numero_apolice, descricao, data_ocorrencia, status)
            VALUES (?, ?, ?, 'ABERTO')
        """, (numero_apolice, descricao, data_ocorrencia))
        conn.commit()
    registrar_evento(usuario, "CRIAR", "SINISTRO", numero_apolice)

def listar_sinistros():
    with conectar() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, numero_apolice, descricao, data_ocorrencia, status FROM sinistros")
        return cur.fetchall()

def buscar_sinistro(id_sinistro):
    with conectar() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM sinistros WHERE id = ?", (id_sinistro,))
        return cur.fetchone()

def atualizar_sinistro(id_sinistro, status=None, descricao=None, usuario="sistema"):
    sinistro = buscar_sinistro(id_sinistro)
    if not sinistro:
        raise ValueError("Sinistro não encontrado")
    with conectar() as conn:
        cur = conn.cursor()
        cur.execute("""
            UPDATE sinistros
            SET status = COALESCE(?, status),
                descricao = COALESCE(?, descricao)
            WHERE id = ?
        """, (status, descricao, id_sinistro))
        conn.commit()
    registrar_evento(usuario, "ATUALIZAR", "SINISTRO", str(id_sinistro))

# --------------------- NOVA FUNÇÃO: Atualizar SINISTRO por apólice ---------------------
def atualizar_sinistro_por_apolice(numero_apolice, status=None, descricao=None, usuario="sistema"):
    """Atualiza todos os sinistros de uma apólice específica"""
    with conectar() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id FROM sinistros WHERE numero_apolice=?", (numero_apolice,))
        sinistros = cur.fetchall()
        if not sinistros:
            print("Nenhum sinistro encontrado para essa apólice.")
            return
        for (id_sinistro,) in sinistros:
            cur.execute("""
                UPDATE sinistros
                SET status = COALESCE(?, status),
                    descricao = COALESCE(?, descricao)
                WHERE id = ?
            """, (status, descricao, id_sinistro))
        conn.commit()
    registrar_evento(usuario, "ATUALIZAR", "SINISTRO", numero_apolice)
