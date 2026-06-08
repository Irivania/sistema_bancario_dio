# sistema_bancario_dio

Sistema Bancário em Python
Descrição

Este projeto consiste no desenvolvimento de um Sistema Bancário simples utilizando Python. O objetivo é simular operações bancárias básicas, permitindo que o usuário realize depósitos, saques e consulte o extrato da conta através de um menu interativo no terminal.

O projeto foi desenvolvido como prática dos conceitos fundamentais da linguagem Python, incluindo estruturas condicionais, laços de repetição, manipulação de variáveis e formatação de saída.

Funcionalidades
Depósito
Permite realizar depósitos em conta.
Aceita apenas valores positivos.
Todos os depósitos são registrados no extrato.
Saque
Permite realizar saques da conta.
Limite máximo de R$ 500,00 por saque.
Limite de 3 saques por execução do sistema.
Não permite saques com saldo insuficiente.
Todos os saques são registrados no extrato.
Extrato
Exibe todas as movimentações realizadas.
Apresenta o saldo atual da conta.
Caso não existam movimentações, informa ao usuário.
Tecnologias Utilizadas
Python 3
Como Executar o Projeto
Certifique-se de ter o Python instalado em sua máquina.
Faça o download ou clone este repositório:
git clone https://github.com/seu-usuario/sistema-bancario-python.git
Acesse a pasta do projeto:
cd sistema-bancario-python
Execute o arquivo principal:
python sistema_bancario.py
Exemplo de Uso
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> d
Informe o valor do depósito: R$ 100

=> s
Informe o valor do saque: R$ 50

=> e

================ EXTRATO ================
Depósito: R$ 100.00
Saque: R$ 50.00

Saldo: R$ 50.00
=========================================
Estrutura do Projeto
sistema-bancario-python/
│
├── sistema_bancario.py
└── README.md
Objetivos de Aprendizagem

Este projeto permite praticar:

Sintaxe básica do Python;
Estruturas de decisão (if, elif, else);
Estruturas de repetição (while);
Manipulação de strings;
Controle de fluxo;
Desenvolvimento de aplicações em linha de comando (CLI).
Melhorias Futuras
Cadastro de clientes;
Criação de múltiplas contas;
Transferências entre contas;
Persistência de dados em arquivos ou banco de dados;
Interface gráfica.
Autor

Projeto desenvolvido como parte dos estudos de Python e dos desafios práticos da plataforma DIO (Digital Innovation One). 🚀