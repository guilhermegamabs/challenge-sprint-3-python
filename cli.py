from dao import (
    criar_cliente, listar_clientes, buscar_cliente, atualizar_cliente, remover_cliente,
    criar_seguro, listar_seguros, buscar_seguro, atualizar_seguro, cancelar_seguro,
    registrar_sinistro, listar_sinistros, buscar_sinistro, atualizar_sinistro
)
from relatorios import receita_mensal, top_clientes, sinistros_por_status, exportar_csv
from usuarios import autenticar, listar_usuarios, criar_usuario, alterar_senha, deletar_usuario
from validacoes import validar_cpf, OperacaoNaoPermitida

def menu_principal():
    print("=== SISTEMA DE SEGUROS ===")
    
    usuario = None
    while not usuario:
        login = input("Login: ")
        senha = input("Senha: ")
        usuario = autenticar(login, senha)
        if not usuario:
            print("Usuário ou senha inválidos! Tente novamente.\n")
    
    username = usuario['username']
    perfil = usuario['perfil']

    print(f"Bem-vindo, {username}! Perfil: {perfil}")

    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1. Clientes")
        print("2. Seguros / Apólices")
        print("3. Sinistros")
        print("4. Relatórios")
        if perfil == "admin":
            print("5. Usuários")
        print("0. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            print("\n--- CLIENTES ---")
            print("1. Cadastrar cliente")
            print("2. Listar clientes")
            print("3. Buscar cliente")
            print("4. Atualizar cliente")
            print("5. Remover cliente")
            print("0. Voltar")
            sub = input("Escolha: ")

            if sub == "1":
                cpf = input("CPF: ")
                nome = input("Nome: ")
                data_nasc = input("Data de nascimento (YYYY-MM-DD): ")
                endereco = input("Endereço: ")
                telefone = input("Telefone: ")
                email = input("Email: ")
                criar_cliente(cpf, nome, data_nasc, endereco, telefone, email, usuario=username)
                print("Cliente cadastrado!")
            elif sub == "2":
                clientes = listar_clientes()
                for c in clientes:
                    print(c)
            elif sub == "3":
                cpf = input("CPF: ")
                cliente = buscar_cliente(cpf)
                print(cliente if cliente else "Cliente não encontrado.")
            elif sub == "4":
                cpf = input("CPF do cliente: ")
                nome = input("Novo nome (ou Enter para manter): ")
                data_nasc = input("Nova data de nascimento (ou Enter para manter): ")
                endereco = input("Novo endereço (ou Enter para manter): ")
                telefone = input("Novo telefone (ou Enter para manter): ")
                email = input("Novo email (ou Enter para manter): ")
                atualizar_cliente(cpf, nome or None, data_nasc or None, endereco or None, telefone or None, email or None, usuario=username)
                print("Cliente atualizado!")
            elif sub == "5":
                cpf = input("CPF do cliente a remover: ")
                confirmar = input(f"Confirma remoção do cliente {cpf}? (s/n): ")
                if confirmar.lower() == "s":
                    remover_cliente(cpf, usuario=username)
                    print("Cliente removido!")
            elif sub == "0":
                continue

        elif opcao == "2":
            print("\n--- SEGUROS / APÓLICES ---")
            print("1. Criar seguro")
            print("2. Listar seguros")
            print("3. Buscar seguro")
            print("4. Atualizar seguro")
            print("5. Cancelar seguro")
            print("0. Voltar")
            sub = input("Escolha: ")

            if sub == "1":
                numero = input("Número da apólice: ")
                tipo = input("Tipo (automóvel/vida/residencial): ")
                cpf = input("CPF do cliente: ")
                while True:
                    try:
                        valor = float(input("Valor mensal: "))
                        break
                    except ValueError:
                        print("Digite um valor válido.")
                criar_seguro(numero, tipo, cpf, valor, usuario=username)
                print("Seguro criado!")
            elif sub == "2":
                seguros = listar_seguros()
                for s in seguros:
                    print(s)
            elif sub == "3":
                numero = input("Número da apólice: ")
                seguro = buscar_seguro(numero)
                print(seguro if seguro else "Seguro não encontrado.")
            elif sub == "4":
                numero = input("Número da apólice: ")
                valor_input = input("Novo valor mensal (ou Enter para manter): ")
                while True:
                    ativo_input = input("Ativo? 1=Sim, 0=Não (ou Enter para manter): ")
                    if ativo_input in ["1", "0", ""]:
                        break
                    print("Valor inválido. Digite 1 para ativo ou 0 para inativo.")
                valor = float(valor_input) if valor_input else None
                ativo = int(ativo_input) if ativo_input else None
                atualizar_seguro(numero, valor_mensal=valor, ativo=ativo, usuario=username)
                print("Seguro atualizado!")
            elif sub == "5":
                numero = input("Número da apólice a cancelar: ")
                try:
                    cancelar_seguro(numero, usuario=username)
                    print("Seguro cancelado!")
                except OperacaoNaoPermitida as e:
                    print(e)
            elif sub == "0":
                continue

        elif opcao == "3":
            print("\n--- SINISTROS ---")
            print("1. Registrar sinistro")
            print("2. Listar sinistros")
            print("3. Buscar sinistro")
            print("4. Atualizar sinistro")
            print("0. Voltar")
            sub = input("Escolha: ")

            if sub == "1":
                numero = input("Número da apólice: ")
                descricao = input("Descrição: ")
                data = input("Data de ocorrência (YYYY-MM-DD): ")
                registrar_sinistro(numero, descricao, data, usuario=username)
                print("Sinistro registrado!")
            elif sub == "2":
                sinistros = listar_sinistros()
                for s in sinistros:
                    print(s)
            elif sub == "3":
                sin_id = int(input("ID do sinistro: "))
                sinistro = buscar_sinistro(sin_id)
                print(sinistro if sinistro else "Sinistro não encontrado.")
            elif sub == "4":
                sin_id = int(input("ID do sinistro: "))
                status = input("Novo status (ABERTO/FECHADO/EM_ANALISE): ")
                descricao = input("Nova descrição (ou Enter para manter): ")
                atualizar_sinistro(sin_id, status=status or None, descricao=descricao or None, usuario=username)
                print("Sinistro atualizado!")
            elif sub == "0":
                continue

        elif opcao == "4":
            print("\n--- RELATÓRIOS ---")
            print("1. Receita mensal")
            print("2. Top clientes")
            print("3. Sinistros por status")
            print("4. Exportar CSV")
            print("0. Voltar")
            sub = input("Escolha: ")

            if sub == "1":
                print("Receita mensal:", receita_mensal())
            elif sub == "2":
                print("Top clientes:", top_clientes())
            elif sub == "3":
                print("Sinistros por status:", sinistros_por_status())
            elif sub == "4":
                exportar_csv("receita_mensal", [(receita_mensal(),)], ["Total"])
                print("CSV exportado!")
            elif sub == "0":
                continue

        elif opcao == "5" and perfil == "admin":
            print("\n--- USUÁRIOS ---")
            print("1. Criar usuário")
            print("2. Listar usuários")
            print("3. Alterar senha")
            print("4. Deletar usuário")
            print("0. Voltar")
            sub = input("Escolha: ")

            if sub == "1":
                login_novo = input("Login: ")
                senha_nova = input("Senha: ")
                perfil_novo = input("Perfil (admin/comum): ")
                criar_usuario(login_novo, senha_nova, perfil_novo, usuario_ativo=username)
                print("Usuário criado!")
            elif sub == "2":
                usuarios = listar_usuarios()
                for u in usuarios:
                    print(u)
            elif sub == "3":
                login_alterar = input("Login: ")
                senha_nova = input("Nova senha: ")
                alterar_senha(login_alterar, senha_nova, usuario_ativo=username)
                print("Senha alterada!")
            elif sub == "4":
                login_del = input("Login: ")
                confirmar = input(f"Confirma exclusão do usuário {login_del}? (s/n): ")
                if confirmar.lower() == "s":
                    deletar_usuario(login_del, usuario_ativo=username)
                    print("Usuário deletado!")
            elif sub == "0":
                continue

        elif opcao == "0":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu_principal()
