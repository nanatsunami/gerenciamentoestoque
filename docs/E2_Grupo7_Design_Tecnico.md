# Design Técnico e MVP — E2
**Estrutura de Dados**
**Prazo:** 14/05 | **Peso na nota:** 25% da nota final

---

## Identificação do Grupo

|       Campo        |                    Preenchimento                    |
|--------------------|-----------------------------------------------------|
| Nome do projeto    | Sistema de Gerenciamento de Estoque                 |
| Repositório GitHub | https://github.com/nanatsunami/gerenciamentoestoque/|
| Integrante 1       | Natsumi Goto — 42865433                             |
| Integrante 2       | Vitória Alessandra das Neves — 41812182             |

---

## 1. Escolha e Justificativa das Estruturas de Dados

### Estrutura 1 — Lista

**Nome completo e categoria:**
Lista dinâmica (Array/List em Python) — estrutura linear sequencial

**Complexidade das operações principais:**

| Operação | Tempo | Espaço |                     Observação                     |
|----------|-------|--------|----------------------------------------------------|
| Inserção |  O(1) |  O(1)  | Inserção no final da lista                         |
| Remoção  |  O(n) |  O(1)  | Pode exigir deslocamento dos elementos subsequentes|
| Busca    |  O(n) |  O(1)  | Busca sequencial                                   |
| Acesso   |  O(1) |  O(1)  | Acesso direto por índice                           |

**Justificativa de escolha:**
A lista foi escolhida como estrutura principal para armazenamento dos produtos devido à sua simplicidade e flexibilidade. O sistema precisa armazenar um conjunto dinâmico de itens, cujo tamanho pode variar ao longo do tempo, o que torna estruturas estáticas inadequadas.
Além disso, a lista permite a aplicação eficiente do algoritmo de ordenação  Insertion Sort, fundamental para a organização dos produtos com base em critérios como quantidade, tempo em estoque, valor investido e índice de prioridade.
A estrutura também facilita operações de travessia, necessárias para cálculo de métricas, verificação de validade e identificação de produtos críticos.

**Alternativa descartada:**
Array estático — descartado devido à necessidade de redimensionamento dinâmico, já que o número de produtos não é previamente conhecido.

**Limitações conhecidas:**
A principal limitação da lista é o custo da busca sequencial (O(n)), que pode impactar o desempenho com grandes volumes de dados. Além disso, operações de remoção podem exigir deslocamento de elementos, aumentando o custo computacional.

**Referência bibliográfica:**
CORMEN, Thomas H. et al. Introdução a Algoritmos. 3. ed. Rio de Janeiro: Elsevier, 2012.

---

### Estrutura 2 — Fila

**Nome completo e categoria:**
Fila (Queue) — estrutura linear do tipo FIFO (First In, First Out)

**Complexidade das operações principais:**

| Operação | Tempo | Espaço |         Observação         |
|----------|-------|--------|----------------------------|
| Inserção |  O(1) |  O(1)  | Inserção no final da fila  |
| Remoção  |  O(1) |  O(1)  | Remoção do início da fila  |
| Busca    |  O(n) |  O(1)  | Não é operação típica      |
| Acesso   |  O(1) |  O(1)  | Acesso ao primeiro elemento|

**Justificativa de escolha:**
A fila foi implementada para representar o processamento sequencial dos produtos classificados como críticos, permitindo futura expansão do sistema para rotinas automatizadas de análise.
O uso da estrutura FIFO garante que os produtos sejam processados na ordem em que foram identificados como críticos, evitando que itens relevantes sejam ignorados ou analisados fora de sequência.
Essa abordagem permite organizar o fluxo de análise sem interferir na estrutura principal de armazenamento, mantendo a separação entre organização dos dados (lista) e processamento (fila).

**Alternativa descartada:**
Pilha (Stack) — descartada por não representar o comportamento necessário ao sistema, já que a análise dos produtos não segue lógica LIFO, mas sim um fluxo sequencial de processamento.

**Limitações conhecidas:**
A fila não permite acesso direto a elementos intermediários, sendo limitada ao acesso do primeiro elemento. Além disso, não é adequada para operações de ordenação ou busca eficiente, sendo utilizada apenas para controle de fluxo de processamento.

**Referência bibliográfica:**
 CORMEN, Thomas H. et al. Introdução a Algoritmos. 3. ed. Rio de Janeiro: Elsevier, 2012.


---

## 2. Arquitetura em Camadas

**Diagrama:**
┌──────────────────────────────┐
│  Camada de Apresentação      │
│  (UI - interface.py)         │
│  Interface gráfica Tkinter   │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│   Camada de Aplicação        │
│ (Service - estoque_service)  │
│ Regras de negócio, cálculo   │
│ de prioridade e ordenação    │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│      Camada de Domínio       │
│ (Core - lista/fila)          │
│ Estruturas de dados e        │
│ operações fundamentais       │
└──────────────────────────────┘

**Descrição das camadas:**

|         Camada        | Nome no seu projeto | Responsabilidade |
|-----------------------|---------------------|-----------------|
| Apresentação (UI/CLI) |    interface.py     |Responsável pela interface gráfica do sistema, permitindo ao usuário cadastrar, editar, remover, buscar e visualizar produtos |
| Aplicação (Service)   |  estoque_service.py |Responsável pelas regras de negócio, cálculo de prioridade, ordenação dos produtos, leitura/escrita em JSON e processamento dos dados |
| Domínio (Core)        | lista_produtos.py e fila_criticos.py|Responsável pela implementação das estruturas de dados utilizadas no sistema e suas operações principais |

**Como as camadas se comunicam:**
A interface gráfica (interface.py) recebe as ações do usuário, como cadastro, edição, remoção e ordenação de produtos. Essas informações são enviadas para a camada de aplicação (estoque_service.py), que processa as regras de negócio, realiza cálculos de prioridade, aplica o algoritmo de ordenação Insertion Sort e coordena o armazenamento dos dados.

A camada de aplicação se comunica com a camada de domínio (lista_produtos.py e fila_criticos.py) para executar operações sobre as estruturas de dados, como inserção, remoção, busca e processamento de produtos críticos.

Após o processamento, os resultados retornam para a interface gráfica, onde são exibidos ao usuário de forma organizada.

---

## 3. Estrutura de Diretórios

/gerenciamentoestoque
├── src/
│   ├── core/
│   │   ├── lista_produtos.py
│   │   └── fila_criticos.py
│   ├── service/
│   │   └── estoque_service.py
│   └── ui/
│       └── interface.py
├── data/
│   └── produtos.json
├── tests/
├── doc/
└── README.md

**Justificativa de desvios (se houver):**
Nenhum desvio.

---

## 4. Backlog do Projeto

### In-Scope — O que será implementado

**Item 1:** Cadastro de Produto

Critério de aceite:
> **Dado** que o usuário está no sistema,
> **quando** ele informa nome, quantidade, valor unitário e data de entrada,
> **então** o produto deve ser armazenado corretamente na lista de produtos.

---

**Item 2:** Identificação de produto perecível

Critério de aceite:
> **Dado** que o usuário está cadastrando um produto,
> **quando** ele indicar que o produto é perecível,
> **então** o sistema deve solicitar e armazenar a data de validade do produto.

---

**Item 3:** Cálculo do índice de prioridade

Critério de aceite:
> **Dado** que um produto foi cadastrado,
> **quando** o sistema processar seus dados,
> **então** deve calcular automaticamente o índice de prioridade com base em tempo em estoque, quantidade e valor total investido.

---

**Item 4:** Ordenação de produtos

Critério de aceite:
> **Dado** que existem produtos cadastrados,
> **quando** o usuário selecionar um critério de ordenação,
> **então** o sistema deve exibir a lista ordenada conforme o critério escolhido.

---

**Item 5:** Identificação de produtos críticos
Critério de aceite:
> **Dado** que os produtos possuem índice de prioridade calculado,
> **quando** o sistema identificar valores acima de um limite definido,
> **então** os produtos devem ser classificados como críticos.

---

**Item 6:** Processamento de produtos críticos (uso da fila)
Critério de aceite:
> **Dado** que existem produtos classificados como críticos,
> **quando** o sistema iniciar o processamento,
> **então** os produtos devem ser inseridos em uma fila e processados sequencialmente, respeitando a ordem de inserção.

---

**Item 7:** Atualização de produtos
Critério de aceite:
> **Dado** que um produto já está cadastrado,
> **quando** o usuário alterar seus dados,
> **então** as informações devem ser atualizadas corretamente na lista.

---

**Item 8:** Remoção de produtos
Critério de aceite:
> **Dado** que um produto está cadastrado,
> **quando** o usuário solicitar sua remoção,
> **então** o produto deve ser removido da lista de forma consistente.

---

**Item 9:** Interface de usuário (CLI/GUI)
Critério de aceite:
> **Dado** que o usuário inicia o sistema,
> **quando** interage com o menu ou interface,
> **então** deve conseguir acessar as funcionalidades de forma clara e organizada.
---

### Out-of-Scope — O que não será implementado

> Mínimo 3 itens. Explique brevemente por que cada item ficou fora do escopo.

|              Funcionalidade                  | Motivo de exclusão |
|----------------------------------------------|--------------------|
| Sistema automático de definição de promoções | Exige regras de negócio mais avançadas, não sendo foco da aplicação de estruturas de dados |
| Controle multiusuário com autenticação       | Aumenta a complexidade sem contribuir diretamente para o objetivo principal da disciplina |
| Integração com banco de dados | O sistema utiliza armazenamento em JSON para reduzir complexidade e manter foco nas estruturas de dados |

---

## 5. Repositório GitHub

**Link do repositório:** https://github.com/nanatsunami/gerenciamentoestoque/

**Checklist do repositório:**

- [V] Repositório público com nome descritivo
- [V] `.gitignore` configurado para a linguagem escolhida
- [V] `README.md` com nome, descrição e instruções de execução
- [V] Mínimo de 5 commits com prefixos semânticos (`feat:`, `fix:`, `test:`, `docs:`, `refactor:`)

**O que não deve subir no repositório**:

Variáveis de ambiente → .env, .env.local
Credenciais e chaves → secrets.json, arquivos de certificado
Dependências → node_modules/, venv/
Builds gerados → dist/, build/
Arquivos do sistema → .DS_Store, Thumbs.db
Logs → *.log

**Como executar o projeto** *(resumo — o completo deve estar no README.md)*:

```
pip install tkcalendar
py -m src.ui.interface  
```

---

## 6. Implementação do Núcleo

### 6.1 Estrutura implementada: Lista de Produtos

**Linguagem:** Python 3.11

**Localização no repositório:** `src/service/estoque_service`

**Operações implementadas:**

| Operação | Implementada? |        Observação          |
|----------|---------------|----------------------------|
|inserir	 |      ✅	     | Adiciona produto à lista    |
|remover	 |      ✅      | Remove produto selecionado  |
|buscar    |      ✅	     | Busca por nome              |
|exibir    |      ✅	     | Exibe produtos organizados  |

**Trecho representativo do código**:

```python
def insertion_sort(self, produtos, criterio):
    produtos_ordenados = produtos.copy()

    for i in range(1, len(produtos_ordenados)):
        atual = produtos_ordenados[i]
        valor_atual = self.obter_valor(atual, criterio)

        j = i - 1

        while j >= 0 and self.obter_valor(produtos_ordenados[j], criterio) > valor_atual:
            produtos_ordenados[j + 1] = produtos_ordenados[j]
            j -= 1

        produtos_ordenados[j + 1] = atual

    return produtos_ordenados

**Leitura de arquivo:**
O sistema utiliza arquivos no formato JSON para armazenar os dados dos produtos cadastrados. A leitura é realizada pela camada de aplicação (estoque_service.py) por meio da biblioteca nativa json do Python.

O arquivo esperado está localizado em:
Exemplo de arquivo de entrada: data/produtos.json

```
    {
        "nome": "Café",
        "quantidade": 100,
        "valor": 19.9,
        "data": "15/05/2026",
        "validade": "28/10/2026"
    },
    {
        "nome": "Mouse",
        "quantidade": 100,
        "custo": 45.0,
        "preco": 91.0,
        "data": "15/05/2026"
    }
```
---

## 7. MVP — Mínimo Produto Viável

### 7.1 Tipo de interface

- [ ] CLI (linha de comando)
- [X] GUI desktop (Tkinter)
- [ ] Web (HTML/JS, outro: __________)

### 7.2 Tela 1 — Boas-vindas / Menu Principal

**Descrição:** [O que o usuário vê ao iniciar o programa?]

**Print ou representação textual:**
```
### 7.2 Tela 1 — Boas-vindas / Menu Principal

**Descrição:**
Ao iniciar o sistema, o usuário visualiza a tela principal do gerenciamento de estoque. Nessa tela são exibidos os produtos cadastrados, ferramentas de busca e ordenação, além das opções de cadastro, edição e remoção de itens.

**Print ou representação textual:**

```
========================================================
              GERENCIAMENTO DE ESTOQUE
========================================================

[Buscar produto] [Buscar]

[Quantidade ▼] [Ordenar]

===== PRIORIDADE ALTA =====
Arroz | Qtd: 50 | Custo: R$ 18.50 | Venda: R$ 25.00 |
Entrada: 10/05/2026 | Validade: Não perecível |
Prioridade: ALTA !!!

----- PRIORIDADE MÉDIA -----
Leite | Qtd: 20 | Custo: R$ 4.00 | Venda: R$ 6.50 |
Entrada: 12/05/2026 | Validade: 25/05/2026 |
Prioridade: MÉDIA !!

--------------------------------------------------------

[Cadastrar] [Editar] [Excluir]
```

**Comportamentos implementados nesta tela:**
- [V] Nome do sistema exibido
- [V] Lista de operações disponíveis
- [X] Opção de sair

---

### 7.3 Tela 2 — Entrada de Dados

**Descrição:**
A tela de entrada de dados permite ao usuário cadastrar ou editar produtos no sistema. O usuário informa os dados do produto por meio de campos de texto e seletores de data. Também é possível indicar se o produto é perecível, habilitando o campo de validade.

**Print ou representação textual:**

```
========================================================
                CADASTRO DE PRODUTO
========================================================

Nome:
[____________________________]

Quantidade:
[________]

Custo:
[________]

Preço:
[________]

Data de entrada:
[ 15/05/2026 ▼ ]

[ ] Produto perecível

(Quando marcado)

Validade:
[ 30/05/2026 ▼ ]

--------------------------------------------------------

[Salvar] [Voltar]
```
**Comportamentos implementados nesta tela:**
- [V] Campo ou prompt para inserir valor
- [X] Opção de carregar arquivo
- [X] Confirmação da ação antes de executar

---

### 7.4 Tela 3 — Resultado

**Descrição:**
Após a execução de uma operação, o sistema exibe ao usuário o resultado da ação realizada e o estado atualizado da estrutura de dados. As mensagens podem indicar sucesso no cadastro, edição ou remoção de produtos, além de mensagens de erro quando ocorre uma operação inválida.

**Print ou representação textual:**

```
========================================================
                    RESULTADO
========================================================

Produto salvo com sucesso!

===== PRIORIDADE ALTA =====
Arroz | Qtd: 50 | Custo: R$ 18.50 | Venda: R$ 25.00 |
Entrada: 10/05/2026 | Validade: Não perecível |
Prioridade: ALTA !!!

----- PRIORIDADE MÉDIA -----
Leite | Qtd: 20 | Custo: R$ 4.00 | Venda: R$ 6.50 |
Entrada: 12/05/2026 | Validade: 25/05/2026 |
Prioridade: MÉDIA !!

--------------------------------------------------------

Exemplo de erro:

ERRO: selecione um produto válido.
```
**Comportamentos implementados nesta tela:**
- [V] Resultado da operação executada
- [V] Estado atual completo da estrutura
- [V] Mensagem de erro para operações inválidas (ex.: seleção inválida de produto)

---

### 7.5 Fluxo completo demonstrado

**Cenário:** usuário cadastra um produto perecível e visualiza o estado atualizado do estoque.

```
1. O usuário inicia o sistema.

Tela principal exibida:
GERENCIAMENTO DE ESTOQUE

[Buscar produto] [Buscar] [Quantidade ▼] [Ordenar]

[Cadastrar] [Editar] [Excluir]


2. O usuário clica em "Cadastrar".

Tela de cadastro exibida:
CADASTRO DE PRODUTO

Nome: Leite
Quantidade: 20
Custo: 4.00
Preço: 6.50
Data de entrada: 12/05/2026
[X] Produto perecível
Validade: 25/05/2026

[Salvar] [Voltar]


3. O usuário clica em "Salvar".

Resultado exibido:
Produto salvo com sucesso!


4. O sistema retorna para a tela principal e exibe o estoque atualizado.

GERENCIAMENTO DE ESTOQUE

----- PRIORIDADE MÉDIA -----
Leite | Qtd: 20 | Custo: R$ 4.00 | Venda: R$ 6.50 |
Entrada: 12/05/2026 | Validade: 25/05/2026 |
Prioridade: MÉDIA !!
```

---

## 8. Testes Unitários

**Framework de testes utilizado:** [Ex.: pytest, JUnit, unittest]

**Localização:** `tests/[nome_do_arquivo_de_testes]`

### Estrutura testada: [Nome da Estrutura]

---

**Teste 1 — Caso base**

Descrição: [O que este teste verifica?]

```[linguagem]
[Cole o código do teste aqui]
```

Resultado: ✅ Passando / ❌ Falhando

---

**Teste 2 — Caso vazio**

Descrição: [O que este teste verifica? Ex.: comportamento ao executar pop em pilha vazia]

```[linguagem]
[Cole o código do teste aqui]
```

Resultado: ✅ Passando / ❌ Falhando

---

**Teste 3 — Caso com múltiplos elementos**

Descrição: [O que este teste verifica? Ex.: sequência de operações sobre estrutura populada]

```[linguagem]
[Cole o código do teste aqui]
```

Resultado: ✅ Passando / ❌ Falhando

---

## Checklist de Autoavaliação

Antes de entregar, verifique se você:

**Seção 1 — Estruturas**
- [ ] Big-O preenchido para inserção, remoção, busca e acesso de cada estrutura
- [ ] Pelo menos 1 alternativa descartada com justificativa técnica
- [ ] Limitações conhecidas descritas
- [ ] Referência bibliográfica fornecida

**Seção 2 — Arquitetura**
- [ ] Diagrama com as 3 camadas visíveis
- [ ] Fluxo de comunicação entre camadas descrito

**Seção 3 — Diretórios**
- [ ] Árvore de diretórios presente
- [ ] Desvios do modelo justificados (ou "Nenhum desvio" declarado)

**Seção 4 — Backlog**
- [ ] 5 ou mais itens In-Scope com critério de aceite no formato Dado/Quando/Então
- [ ] 3 ou mais itens Out-of-Scope com justificativa

**Seção 5 — Repositório**
- [ ] Link do repositório público informado
- [ ] README.md com instruções de execução
- [ ] Mínimo de 5 commits semânticos

**Seção 6 — Núcleo**
- [ ] Pelo menos 1 estrutura completamente implementada
- [ ] Leitura de arquivo funcionando
- [ ] Trecho de código representativo incluído no template

**Seção 7 — MVP**
- [ ] 3 telas documentadas com print ou representação textual
- [ ] Fluxo completo de ponta a ponta demonstrado
- [ ] Mensagem de erro para operação inválida implementada
- [ ] Loop de menu funcionando (programa não encerra após 1 operação)

**Seção 8 — Testes**
- [ ] 3 testes por estrutura documentados neste template
- [ ] Resultado de cada teste indicado (✅ / ❌)

---

*Nome do arquivo de entrega: `E2_<grupo>_Design_Tecnico.md`*
*Este arquivo deve estar na pasta `/doc` do repositório.*
