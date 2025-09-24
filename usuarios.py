import hashlib
from db import conectar
from auditoria import registrar_evento

def criar_usuario(username, senha, perfil, usuario_ativo="sistema"):
    with conectar() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuarios WHERE username = ?", (username,))
        if cur.fetchone():
            print(f"Usuário '{username}' já existe.")
            registrar_evento(usuario_ativo, "CRIAR", "USUARIO", username, nivel="ERROR")
            return
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()
        cur.execute("INSERT INTO usuarios (username, senha, perfil) VALUES (?, ?, ?)",
                    (username, senha_hash, perfil))
        conn.commit()
    registrar_evento(usuario_ativo, "CRIAR", "USUARIO", username)
    print(f"Usuário '{username}' criado com sucesso.")

def autenticar(username, senha):
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()
    with conectar() as conn:
        cur = conn.cursor()
        cur.execute("SELECT perfil FROM usuarios WHERE username=? AND senha=?", (username, senha_hash))
        resultado = cur.fetchone()
        if resultado:
            perfil = resultado[0]
            registrar_evento(username, "LOGIN", "USUARIO", username)
            return {"username": username, "perfil": perfil}
    registrar_evento(username, "LOGIN_FALHA", "USUARIO", username, nivel="ERROR")
    return None

def listar_usuarios():
    with conectar() as conn:
        cur = conn.cursor()
        cur.execute("SELECT username, perfil FROM usuarios")
        return cur.fetchall()

def alterar_senha(username, nova_senha, usuario_ativo):
    senha_hash = hashlib.sha256(nova_senha.encode()).hexdigest()
    with conectar() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuarios WHERE username = ?", (username,))
        if not cur.fetchone():
            print(f"Usuário '{username}' não encontrado.")
            registrar_evento(usuario_ativo, "ALTERAR_SENHA_FALHA", "USUARIO", username, nivel="ERROR")
            return
        cur.execute("UPDATE usuarios SET senha=? WHERE username=?", (senha_hash, username))
        conn.commit()
    registrar_evento(usuario_ativo, "ALTERAR_SENHA", "USUARIO", username)
    print(f"Senha do usuário '{username}' alterada com sucesso.")

def deletar_usuario(username, usuario_ativo):
    with conectar() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuarios WHERE username = ?", (username,))
        if not cur.fetchone():
            print(f"Usuário '{username}' não encontrado.")
            registrar_evento(usuario_ativo, "DELETAR_USUARIO_FALHA", "USUARIO", username, nivel="ERROR")
            return
        cur.execute("DELETE FROM usuarios WHERE username=?", (username,))
        conn.commit()
    registrar_evento(usuario_ativo, "DELETAR_USUARIO", "USUARIO", username)
    print(f"Usuário '{username}' deletado com sucesso.")
