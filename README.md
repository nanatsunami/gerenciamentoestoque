# Sistema de Gerenciamento de Estoque
## Descrição
Este projeto consiste em um sistema de gerenciamento de estoque desenvolvido em Python, com o objetivo de auxiliar na organização e análise de produtos em pequenos e médios comércios.
O sistema permite cadastrar, atualizar e remover produtos, além de identificar itens que necessitam de maior atenção com base em critérios como tempo em estoque, quantidade, valor e, quando aplicável, data de validade.

--------------------------------------------------------------------------------------------------------

## Funcionalidades
* Cadastro de produtos (nome, quantidade, valor unitário e data de entrada)
* Indicação de produtos perecíveis com registro de data de validade
* Atualização e remoção de produtos
* Busca de produtos pelo nome
* Ordenação por diferentes critérios:
  * quantidade
  * tempo em estoque
  * valor total
  * índice de prioridade
  * identificação de produtos críticos

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

## Autoras
* Natsumi Goto
* Vitória Alessandra das Neves