# Sistema de Gerenciamento de Estoque
## Descrição
Sistema desenvolvido em Python para auxiliar no gerenciamento de estoque de pequenos e médios comércios.  
A aplicação permite cadastrar, editar, remover, buscar e organizar produtos com base em critérios como quantidade, valor, data e prioridade.

--------------------------------------------------------------------------------------------------------

## Funcionalidades
- Cadastro de produtos
- Edição e remoção de itens
- Busca por nome
- Ordenação por:
  - quantidade
  - valor (mais alto/mais baixo)
  - data
  - prioridade
- Identificação de produtos críticos
- Controle de produtos perecíveis
- Armazenamento de dados em arquivo JSON

--------------------------------------------------------------------------------------------------------

##  Índice de Prioridade
Para destacar quais produtos exigem mais atenção, o sistema calcula um índice de prioridade para cada produto com base em:
* quantidade disponível
* tempo em estoque
* validade (quando aplicável)
* valor total investido
Esse índice permite destacar os produtos que exigem maior atenção.

--------------------------------------------------------------------------------------------------------

##  Estrutura de Dados
O sistema utiliza listas como estrutura principal para armazenar e manipular os produtos, permitindo:
* inserção e remoção de dados
* busca por elementos
* aplicação de algoritmos de ordenação

--------------------------------------------------------------------------------------------------------

##  Algoritmos Utilizados
* Quick Sort -> para ordenação geral dos produtos
* Insertion Sort -> para inserções e atualizações

--------------------------------------------------------------------------------------------------------

## Tecnologias Utilizadas

- Python 3.11
- Tkinter
- tkcalendar
- JSON

--------------------------------------------------------------------------------------------------------

## Como Executar

1. Clone o repositório
git clone https://github.com/nanatsunami/gerenciamentoestoque

2. Acesse a pasta do projeto
cd NOME-DO-REPOSITORIO

3. Instale a biblioteca necessária
pip install tkcalendar

4. Execute o sistema
py -m src.ui.interface

--------------------------------------------------------------------------------------------------------

## Autoras
* Natsumi Goto
* Vitória Alessandra das Neves
