# Sistema de Seguros – Challenge Sprint 3 Python

## Integrantes do Grupo

- **Carolina Novakc Moraes** | RM: 565621  
- **Guilherme Gama Bitencourt Souza** | RM: 565293  

---

## Descrição do Projeto

Este projeto é um sistema de gerenciamento de seguros, desenvolvido para evoluir para um nível "quase-produção". Ele inclui funcionalidades para:  

- Cadastro e gerenciamento de **clientes**.  
- Emissão e controle de **seguros/apólices** (automóvel, vida, residencial).  
- Registro e acompanhamento de **sinistros**.  
- Controle de **usuários** com diferentes perfis (**admin** e **comum**), com autenticação e persistência em SQLite.  
- **Auditoria** completa das operações sensíveis com **logs** detalhados em arquivo e no banco de dados.  
- Geração de **relatórios** financeiros e operacionais, com exportação em CSV.  
- **Tratamento de erros** robusto e validações reforçadas para garantir a integridade dos dados.  
- **Experiência no terminal (CLI)** aprimorada, com navegação intuitiva e confirmações para ações destrutivas.

O sistema é totalmente baseado em **Python**, utilizando SQLite como banco de dados para persistência robusta.

---

## Pré-requisitos

- Python 3.10 ou superior  
- Pacotes Python: `sqlite3` (builtin), `hashlib` (builtin), `pathlib` (builtin)  
  *Nenhuma instalação adicional de pacotes via `pip` é estritamente necessária, pois as bibliotecas utilizadas são nativas do Python.*  
- Sistema operacional compatível com execução de scripts Python.

> Não é necessário instalar bancos de dados externos, pois o sistema utiliza SQLite, que é um banco de dados embarcado baseado em arquivo.

---

## Instalação

1. **Clone o repositório** ou baixe o ZIP do projeto:

```bash
git clone <URL_DO_REPOSITORIO>
cd challenge-sprint-3-python
```

2. Configuração Inicial e Migração de Dados (Sprint 2 para Sprint 3)

1. Inicializar o Banco de Dados (Criar Schema)Inicializar o Banco de Dados (Criar Schema)

   Antes de rodar o sistema, é necessário criar o arquivo do banco de dados SQLite e as tabelas.

   Execute o script inicializar_banco.py:

   python inicializar_banco.py

2. Inicialização do Sistema Principal (CLI)
   
   No terminal:
   
   ```bash
   python cli.py
   ```
---

## Exemplos Rápidos de Uso

Ao iniciar o cli.py, você será apresentado à tela de login e, em seguida, ao menu principal.

1. Login

   Usuário Admin Padrão:
   
   Login: admin
   
   Senha: 123456

   Um usuário comum pode ter permissões limitadas, como apenas consulta e relatórios.

2. Emissão de Apólice (Fluxo Admin)

   Faça login como admin.
   
   No menu principal, selecione a opção para Gerenciar Apólices ou Emitir Nova Apólice.
   
   O sistema solicitará os dados do cliente (se já cadastrado, será associado; caso contrário, será criado um novo) e os detalhes da apólice (tipo de seguro, valor segurado, prêmio, data de início/fim).
   
   Confirme a emissão quando solicitado.
   
   A operação será registrada nos logs de auditoria.

3. Registro de Sinistro (Fluxo Admin)

   Faça login como admin.
   
   No menu principal, selecione a opção Gerenciar Sinistros ou Registrar Sinistro.
   
   O sistema solicitará o número da apólice associada ao sinistro e detalhes do ocorrido (data, descrição, status inicial).
   
   Confirme o registro.
   
   A operação será registrada nos logs de auditoria.

4. Geração de Relatórios (Fluxo Admin ou Comum para consultas)

   Faça login com um usuário (admin ou comum).
   
   No menu principal, selecione a opção Relatórios.
   
   Escolha o tipo de relatório desejado (ex: "Receita Mensal Prevista", "Top Clientes por Valor Segurado", "Sinistros por Status e Período").
   
   O relatório será exibido no terminal de forma tabular.
   
   O sistema também perguntará se você deseja exportar o relatório para CSV. Se confirmar, o arquivo será gerado na pasta exports/.

5. Navegação no Terminal

   Utilize os números das opções para navegar pelos menus.
   
   Ações destrutivas (como cancelar uma apólice) exigirão uma confirmação explícita (s/n) antes de serem executadas.
   
   Buscas rápidas podem ser feitas por CPF, número de apólice ou nome, dependendo do contexto do menu.
   

> **Observação:**  
> O JSON utilizado em versões anteriores do sistema não é compatível diretamente com a nova arquitetura de tabelas do SQLite nesta Sprint 3.  
> Entretanto, ele pode ser utilizado normalmente dentro da **função de migração**, que converte os dados antigos para o novo esquema do banco de dados.



