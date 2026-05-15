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
        valor_total = produto["quantidade"] * produto["valor"]

        prioridade = (dias * 2) + produto["quantidade"] + (valor_total / 10)
        return prioridade

    def identificar_criticos(self):
        self.fila.fila.clear()

        for p in self.lista.exibir():
            prioridade = self.calcular_prioridade(p)
            p["prioridade"] = prioridade

            if prioridade > 100:
                self.fila.enqueue(p)

    def salvar_em_arquivo(self, caminho="data/produtos.json"):
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(self.lista.exibir(), f, indent=4, ensure_ascii=False)

    def carregar_de_arquivo(self, caminho="data/produtos.json"):
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                conteudo = f.read().strip()

                if not conteudo:
                    return  # arquivo vazio → ignora

                dados = json.loads(conteudo)

                self.lista.produtos = []

                for produto in dados:
                    self.lista.inserir(produto)

        except FileNotFoundError:
            print("Arquivo não encontrado. Iniciando com lista vazia.")

        except json.JSONDecodeError:
            print("Erro ao ler JSON. Arquivo pode estar corrompido.")
