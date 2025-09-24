import json
from dao import criar_cliente, criar_seguro, registrar_sinistro
from usuarios import criar_usuario

def importar_jsons(path_json_clientes, path_json_seguros, path_json_sinistros, path_json_usuarios):
    with open(path_json_clientes, "r", encoding="utf-8") as f:
        clientes = json.load(f)
        for c in clientes:
            try:
                criar_cliente(
                    c["cpf"], 
                    c["nome"], 
                    c.get("data_nascimento"), 
                    c.get("endereco"), 
                    c.get("telefone"), 
                    c.get("email"), 
                    usuario="sistema"
                )
            except Exception as e:
                print(f"Erro ao importar cliente {c['cpf']}: {e}")

    with open(path_json_seguros, "r", encoding="utf-8") as f:
        seguros = json.load(f)
        for s in seguros:
            try:
                criar_seguro(
                    s["numero_apolice"], 
                    s["tipo"], 
                    s["cpf"], 
                    s["valor_mensal"], 
                    usuario="sistema"
                )
            except Exception as e:
                print(f"Erro ao importar seguro {s['numero_apolice']}: {e}")

    with open(path_json_sinistros, "r", encoding="utf-8") as f:
        sinistros = json.load(f)
        for sin in sinistros:
            try:
                registrar_sinistro(
                    sin["numero_apolice"], 
                    sin["descricao"], 
                    sin["data_ocorrencia"], 
                    usuario="sistema"
                )
            except Exception as e:
                print(f"Erro ao importar sinistro {sin['numero_apolice']}: {e}")

    with open(path_json_usuarios, "r", encoding="utf-8") as f:
        usuarios = json.load(f)
        for u in usuarios:
            try:
                criar_usuario(
                    u["username"], 
                    u["senha"], 
                    u["perfil"], 
                    usuario_ativo="sistema"
                )
            except Exception as e:
                print(f"Erro ao importar usuário {u['username']}: {e}")
