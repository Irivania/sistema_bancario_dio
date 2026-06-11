from abc import ABC, abstractmethod
from datetime import datetime
import functools

# ==========================
# DECORADOR DE LOG
# ==========================
def log_transacao(func):
    @functools.wraps(func)
    def envelope(*args, **kwargs):
        resultado = func(*args, **kwargs)
        print(f"\n[LOG] {datetime.now().strftime('%d-%m-%Y %H:%M:%S')} - Função '{func.__name__}' executada.")
        return resultado
    return envelope

# ==========================
# ITERADOR PERSONALIZADO
# ==========================
class ContaIterador:
    def __init__(self, contas):
        self.contas = contas
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self.contas):
            conta = self.contas[self._index]
            self._index += 1
            return (f"Agência: {conta.agencia} | Conta: {conta.numero} | "
                    f"Titular: {conta.cliente.nome} | Saldo: R$ {conta.saldo:.2f}")
        raise StopIteration

# ==========================
# CLASSES
# ==========================
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        })

    def gerar_relatorio(self, tipo_transacao=None):
        for transacao in self._transacoes:
            if tipo_transacao is None or transacao["tipo"].lower() == tipo_transacao.lower():
                yield transacao

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self): return self._saldo
    @property
    def numero(self): return self._numero
    @property
    def agencia(self): return self._agencia
    @property
    def cliente(self): return self._cliente
    @property
    def historico(self): return self._historico

    def verificar_limite_diario(self):
        hoje = datetime.now().strftime("%d-%m-%Y")
        transacoes_hoje = [t for t in self._historico.transacoes if t["data"].startswith(hoje)]
        return len(transacoes_hoje) >= 10

    @log_transacao
    def sacar(self, valor):
        if valor > self._saldo:
            print("\nOperação falhou! Saldo insuficiente.")
            return False
        self._saldo -= valor
        print("\nSaque realizado com sucesso!")
        return True

    @log_transacao
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\nDepósito realizado com sucesso!")
            return True
        return False

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

# ==========================
# TRANSAÇÕES
# ==========================
class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self): pass
    @abstractmethod
    def registrar(self, conta): pass

class Saque(Transacao):
    def __init__(self, valor): self._valor = valor
    @property
    def valor(self): return self._valor
    def registrar(self, conta):
        if conta.verificar_limite_diario():
            print("\nErro: Limite de 10 transações diárias excedido!")
            return
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor): self._valor = valor
    @property
    def valor(self): return self._valor
    def registrar(self, conta):
        if conta.verificar_limite_diario():
            print("\nErro: Limite de 10 transações diárias excedido!")
            return
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [c for c in clientes if c.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

# ==========================
# MAIN
# ==========================
def main():
    clientes = []
    contas = []

    while True:
        menu = "\n[d] Depósito [s] Saque [e] Extrato [nu] Novo Cliente [nc] Nova Conta [lc] Listar Contas [q] Sair => "
        opcao = input(menu)

        if opcao == "nu":
            cpf = input("CPF: ")
            if filtrar_cliente(cpf, clientes):
                print("Erro: Cliente já cadastrado!")
            else:
                nome = input("Nome: ")
                clientes.append(PessoaFisica(nome, "00/00/0000", cpf, "Endereço"))
                print("Cliente criado!")

        elif opcao == "nc":
            cpf = input("CPF: ")
            cliente = filtrar_cliente(cpf, clientes)
            if not cliente:
                print("Erro: Cliente não encontrado!")
            else:
                conta = ContaCorrente(len(contas) + 1, cliente)
                contas.append(conta)
                cliente.adicionar_conta(conta)
                print("Conta criada!")

        elif opcao == "lc":
            print("\n--- LISTA DE CONTAS ---")
            for conta_info in ContaIterador(contas):
                print(conta_info)

        elif opcao in ("d", "s"):
            cpf = input("CPF: ")
            cliente = filtrar_cliente(cpf, clientes)
            if not cliente or not cliente.contas:
                print("Erro: Cliente ou conta não encontrados!")
            else:
                try:
                    valor = float(input(f"Valor para {'depósito' if opcao == 'd' else 'saque'}: R$ "))
                    transacao = Deposito(valor) if opcao == "d" else Saque(valor)
                    cliente.realizar_transacao(cliente.contas[0], transacao)
                except ValueError:
                    print("Erro: Valor inválido!")

        elif opcao == "e":
            cpf = input("CPF: ")
            cliente = filtrar_cliente(cpf, clientes)
            if not cliente or not cliente.contas:
                print("Erro: Cliente ou conta não encontrados!")
            else:
                print("\n--- EXTRATO DETALHADO ---")
                for t in cliente.contas[0].historico.gerar_relatorio():
                    print(f"{t['data']} | {t['tipo']}: R$ {t['valor']:.2f}")
                print(f"Saldo atual: R$ {cliente.contas[0].saldo:.2f}")

        elif opcao == "q":
            break

if __name__ == "__main__":
    main()