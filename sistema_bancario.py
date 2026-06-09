
from textwrap import dedent

AGENCIA = "0001"
LIMITE_SAQUES = 3


def menu():
    return input(dedent("""
    ================ MENU ================

    [d] Depositar
    [s] Sacar
    [e] Extrato
    [nu] Novo Usuário
    [nc] Nova Conta
    [lc] Listar Contas
    [q] Sair

    => """))


def depositar(saldo, valor, extrato, /):

    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print("\nDepósito realizado com sucesso!")

    else:
        print("\nOperação falhou! Valor inválido.")

    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):

    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\nOperação falhou! Saldo insuficiente.")

    elif excedeu_limite:
        print("\nOperação falhou! O valor excede o limite permitido.")

    elif excedeu_saques:
        print("\nOperação falhou! Número máximo de saques excedido.")

    elif valor > 0:

        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1

        print("\nSaque realizado com sucesso!")

    else:
        print("\nOperação falhou! Valor inválido.")

    return saldo, extrato, numero_saques


def exibir_extrato(saldo, /, *, extrato):

    print("\n================ EXTRATO ================")

    if not extrato:
        print("Não foram realizadas movimentações.")
    else:
        print(extrato)

    print(f"Saldo: R$ {saldo:.2f}")
    print("==========================================")


def filtrar_usuario(cpf, usuarios):

    usuarios_filtrados = [
        usuario for usuario in usuarios if usuario["cpf"] == cpf
    ]

    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_usuario(usuarios):

    cpf = input("Informe o CPF (somente números): ").strip()

    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\nJá existe um usuário com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input(
        "Informe a data de nascimento (dd-mm-aaaa): "
    )

    endereco = input(
        "Informe o endereço "
        "(logradouro, número, bairro, cidade/sigla estado): "
    )

    usuarios.append({
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    })

    print("\nUsuário criado com sucesso!")


def criar_conta(agencia, numero_conta, usuarios):

    cpf = input("Informe o CPF do usuário: ")

    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:

        print("\nConta criada com sucesso!")

        return {
            "agencia": agencia,
            "numero_conta": numero_conta,
            "usuario": usuario
        }

    print("\nUsuário não encontrado.")
    return None


def listar_contas(contas):

    if not contas:
        print("\nNenhuma conta cadastrada.")
        return

    for conta in contas:

        linha = f"""
        Agência:\t{conta['agencia']}
        Conta:\t\t{conta['numero_conta']}
        Titular:\t{conta['usuario']['nome']}
        CPF:\t\t{conta['usuario']['cpf']}
        """

        print("=" * 40)
        print(dedent(linha))
        print("=" * 40)


def main():

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0

    usuarios = []
    contas = []

    while True:

        opcao = menu()

        if opcao == "d":

            valor = float(
                input("Informe o valor do depósito: R$ ")
            )

            saldo, extrato = depositar(
                saldo,
                valor,
                extrato
            )

        elif opcao == "s":

            valor = float(
                input("Informe o valor do saque: R$ ")
            )

            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES
            )

        elif opcao == "e":

            exibir_extrato(
                saldo,
                extrato=extrato
            )

        elif opcao == "nu":

            criar_usuario(usuarios)

        elif opcao == "nc":

            numero_conta = len(contas) + 1

            conta = criar_conta(
                AGENCIA,
                numero_conta,
                usuarios
            )

            if conta:
                contas.append(conta)

        elif opcao == "lc":

            listar_contas(contas)

        elif opcao == "q":

            print("\nObrigado por utilizar nosso sistema bancário!")
            break

        else:

            print("\nOperação inválida. Tente novamente.")


main()
