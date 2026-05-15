from datetime import datetime
import json


class EstoqueService:
    def __init__(self, lista, fila):
        self.lista = lista
        self.fila = fila

    def calcular_prioridade(self, produto):
        hoje = datetime.now()
        data_entrada = datetime.strptime(produto["data"], "%d/%m/%Y")

        dias = (hoje - data_entrada).days
        quantidade = produto.get("quantidade", 0)

        preco = produto.get("preco")
        custo = produto.get("custo")

        if preco is None:
            preco = produto.get("valor", 0)

        if custo is None:
            custo = preco * 0.7

        valor_total = quantidade * preco

        peso_tempo = 0.4
        peso_quantidade = 0.3
        peso_valor = 0.2
        peso_validade = 0.1

        score = 0

        score += min(dias / 30, 1) * peso_tempo
        score += min(quantidade / 100, 1) * peso_quantidade
        score += min(valor_total / 1000, 1) * peso_valor

        if "validade" in produto:
            data_validade = datetime.strptime(produto["validade"], "%d/%m/%Y")
            dias_para_vencer = (data_validade - hoje).days

            if dias_para_vencer <= 0:
                score += 1 * peso_validade
            elif dias_para_vencer <= 7:
                score += 0.7 * peso_validade
            elif dias_para_vencer <= 30:
                score += 0.4 * peso_validade

        return round(score * 10, 2)

    def classificar_prioridade(self, produto):
        prioridade = self.calcular_prioridade(produto)

        if prioridade >= 7:
            return "ALTA !!!"
        elif prioridade >= 4:
            return "MÉDIA !!"
        else:
            return "BAIXA !"

    def obter_valor(self, produto, criterio):
        if criterio == "Quantidade":
            return produto.get("quantidade", 0)

        elif criterio == "Preço de venda (mais barato)":
            return produto.get("preco", produto.get("valor", 0))

        elif criterio == "Preço de venda (mais caro)":
            return -produto.get("preco", produto.get("valor", 0))

        elif criterio == "Data (mais antigo)":
            return datetime.strptime(produto["data"], "%d/%m/%Y").timestamp()

        elif criterio == "Data (mais recente)":
            return -datetime.strptime(produto["data"], "%d/%m/%Y").timestamp()

        elif criterio == "Prioridade":
            return -self.calcular_prioridade(produto)

        return 0

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

    def identificar_criticos(self):
        self.fila.fila.clear()

        for produto in self.lista.exibir():
            prioridade = self.calcular_prioridade(produto)
            produto["prioridade"] = prioridade

            if prioridade >= 7:
                self.fila.enqueue(produto)

    def salvar_em_arquivo(self, caminho="data/produtos.json"):
        with open(caminho, "w", encoding="utf-8") as arquivo:
            json.dump(self.lista.exibir(), arquivo, indent=4, ensure_ascii=False)

    def carregar_de_arquivo(self, caminho="data/produtos.json"):
        try:
            with open(caminho, "r", encoding="utf-8") as arquivo:
                conteudo = arquivo.read().strip()

                if not conteudo:
                    return

                dados = json.loads(conteudo)

                self.lista.produtos = []

                for produto in dados:
                    if "preco" not in produto and "valor" in produto:
                        produto["preco"] = produto["valor"]

                    if "custo" not in produto:
                        produto["custo"] = produto.get("preco", 0) * 0.7

                    self.lista.inserir(produto)

        except FileNotFoundError:
            print("Arquivo não encontrado. Iniciando com lista vazia.")

        except json.JSONDecodeError:
            print("Erro ao ler JSON. Arquivo pode estar vazio ou corrompido.")