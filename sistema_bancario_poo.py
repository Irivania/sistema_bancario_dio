from abc import ABC, abstractmethod
from datetime import datetime
from textwrap import dedent


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


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):

        excedeu_saldo = valor > self._saldo

        if excedeu_saldo:
            print("\nOperação falhou! Saldo insuficiente.")

        elif valor > 0:
            self._saldo -= valor
            print("\nSaque realizado com sucesso!")
            return True

        else:
            print("\nOperação falhou! Valor inválido.")

        return False

    def depositar(self, valor):

        if valor > 0:
            self._saldo += valor
            print("\nDepósito realizado com sucesso!")
            return True

        print("\nOperação falhou! Valor inválido.")
        return False


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):

        numero_saques = len(
            [
                transacao
                for transacao in self.historico.transacoes
                if transacao["tipo"] == Saque.__name__
            ]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\nOperação falhou! Valor excede o limite de saque.")

        elif excedeu_saques:
            print("\nOperação falhou! Número máximo de saques excedido.")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""
Agência:\t{self.agencia}
Conta:\t\t{self.numero}
Titular:\t{self.cliente.nome}
"""


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):

        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )


class Transacao(ABC):

    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):

        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):

        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


# ==========================
# FUNÇÕES AUXILIARES
# ==========================

def menu():
    menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[nu] Novo usuário
[nc] Nova conta
[lc] Listar contas
[q] Sair

=> """

    return input(dedent(menu))


def filtrar_cliente(cpf, clientes):

    clientes_filtrados = [
        cliente for cliente in clientes if cliente.cpf == cpf
    ]

    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):

    if not cliente.contas:
        print("\nCliente não possui conta.")
        return

    return cliente.contas[0]


# ==========================
# OPERAÇÕES
# ==========================

def criar_cliente(clientes):

    cpf = input("Informe o CPF (somente números): ")

    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\nJá existe cliente com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input(
        "Informe a data de nascimento (dd-mm-aaaa): "
    )

    endereco = input(
        "Informe o endereço "
        "(logradouro, número - bairro - cidade/sigla estado): "
    )

    cliente = PessoaFisica(
        nome=nome,
        data_nascimento=data_nascimento,
        cpf=cpf,
        endereco=endereco,
    )

    clientes.append(cliente)

    print("\nCliente criado com sucesso!")


def criar_conta(numero_conta, clientes, contas):

    cpf = input("Informe o CPF do cliente: ")

    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado.")
        return

    conta = ContaCorrente.nova_conta(
        cliente=cliente,
        numero=numero_conta
    )

    cliente.adicionar_conta(conta)
    contas.append(conta)

    print("\nConta criada com sucesso!")


def listar_contas(contas):

    for conta in contas:
        print("=" * 50)
        print(str(conta))
        print("=" * 50)


def depositar(clientes):

    cpf = input("Informe o CPF do cliente: ")

    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado.")
        return

    conta = recuperar_conta_cliente(cliente)

    if not conta:
        return

    valor = float(input("Informe o valor do depósito: R$ "))

    transacao = Deposito(valor)

    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):

    cpf = input("Informe o CPF do cliente: ")

    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado.")
        return

    conta = recuperar_conta_cliente(cliente)

    if not conta:
        return

    valor = float(input("Informe o valor do saque: R$ "))

    transacao = Saque(valor)

    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):

    cpf = input("Informe o CPF do cliente: ")

    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado.")
        return

    conta = recuperar_conta_cliente(cliente)

    if not conta:
        return

    print("\n================ EXTRATO ================")

    transacoes = conta.historico.transacoes

    if not transacoes:
        print("Não foram realizadas movimentações.")

    else:
        for transacao in transacoes:
            print(
                f"{transacao['tipo']}: "
                f"R$ {transacao['valor']:.2f}"
            )

    print(f"\nSaldo: R$ {conta.saldo:.2f}")
    print("==========================================")


# ==========================
# MAIN
# ==========================

def main():

    clientes = []
    contas = []

    while True:

        opcao = menu()

        if opcao == "nu":

            criar_cliente(clientes)

        elif opcao == "nc":

            numero_conta = len(contas) + 1

            criar_conta(
                numero_conta,
                clientes,
                contas
            )

        elif opcao == "lc":

            listar_contas(contas)

        elif opcao == "d":

            depositar(clientes)

        elif opcao == "s":

            sacar(clientes)

        elif opcao == "e":

            exibir_extrato(clientes)

        elif opcao == "q":

            print("\nObrigado por utilizar nosso sistema bancário!")
            break

        else:

            print("\nOperação inválida. Tente novamente.")


if __name__ == "__main__":
    main()