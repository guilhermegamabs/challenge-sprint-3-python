import re
from datetime import datetime

class CpfInvalido(Exception): pass
class ApoliceInexistente(Exception): pass
class OperacaoNaoPermitida(Exception): pass

def validar_cpf(cpf: str) -> bool:
    cpf = re.sub(r"\D", "", cpf)
    if len(cpf) != 11:
        raise CpfInvalido("CPF inválido")
    return True

def validar_data(data_texto: str) -> bool:
    formatos = ("%d/%m/%Y", "%Y-%m-%d")
    for fmt in formatos:
        try:
            datetime.strptime(data_texto, fmt)
            return True
        except ValueError:
            continue
    raise ValueError("Data inválida. Use formato DD/MM/YYYY ou YYYY-MM-DD")

def verificar_status_seguro(ativo: int):
    if ativo == 0:
        raise OperacaoNaoPermitida("Seguro já cancelado")
