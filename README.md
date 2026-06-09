# Sistema Bancário em Python - Versão 2

## Descrição

Este projeto foi desenvolvido como parte do desafio prático da DIO (Digital Innovation One) com o objetivo de aprimorar um sistema bancário simples utilizando funções em Python.

A aplicação permite realizar operações bancárias básicas, como depósitos, saques e consulta de extrato, além de cadastrar usuários, criar contas correntes e listar contas cadastradas.

O projeto aplica conceitos importantes da linguagem Python, como funções, listas, dicionários, parâmetros posicionais e nomeados, modularização de código e boas práticas de programação.

---

## Funcionalidades

### Depósito

* Permite realizar depósitos em conta.
* Aceita apenas valores positivos.
* Registra todas as movimentações no extrato.

### Saque

* Limite de 3 saques por execução.
* Limite de R$ 500,00 por saque.
* Não permite saque sem saldo suficiente.
* Registra todas as movimentações no extrato.

### Extrato

* Exibe todas as movimentações realizadas.
* Exibe o saldo atual da conta.
* Informa quando não houver movimentações.

### Cadastro de Usuários

* Armazena usuários em uma lista.
* Cada usuário possui:

  * Nome
  * Data de nascimento
  * CPF
  * Endereço
* Não permite CPF duplicado.

### Cadastro de Contas Correntes

* Agência fixa: 0001.
* Número da conta gerado automaticamente de forma sequencial.
* Cada conta é vinculada a um usuário através do CPF.
* Um usuário pode possuir várias contas.

### Listagem de Contas

* Exibe todas as contas cadastradas.
* Mostra agência, número da conta e titular.

---

## Tecnologias Utilizadas

* Python 3

---

## Estrutura do Projeto

```text
sistema_bancario_dio/
│
├── sistema_bancario.py
└── README.md
```

---

## Conceitos Aplicados

* Funções
* Listas
* Dicionários
* Estruturas condicionais
* Estruturas de repetição
* Modularização de código
* Parâmetros posicionais (`/`)
* Parâmetros nomeados (`*`)
* Manipulação de strings

---

## Regras Implementadas

### Depósito

Recebe argumentos apenas por posição:

```python
depositar(saldo, valor, extrato, /)
```

### Saque

Recebe argumentos apenas por nome:

```python
sacar(
    *,
    saldo,
    valor,
    extrato,
    limite,
    numero_saques,
    limite_saques
)
```

### Extrato

Recebe argumentos posicionais e nomeados:

```python
exibir_extrato(
    saldo,
    /,
    *,
    extrato
)
```

---

## Como Executar

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/sistema_bancario_dio.git
```

2. Entre na pasta do projeto:

```bash
cd sistema_bancario_dio
```

3. Execute o programa:

```bash
python sistema_bancario.py
```

---

## Exemplo de Menu

```text
================ MENU ================

[d] Depositar
[s] Sacar
[e] Extrato
[nu] Novo Usuário
[nc] Nova Conta
[lc] Listar Contas
[q] Sair

=>
```

---

## Autor

Projeto desenvolvido como parte dos desafios de Python da DIO para prática de lógica de programação, estruturas de dados e modularização de código.
