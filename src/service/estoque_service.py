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
        quantidade = produto["quantidade"]
        valor_total = quantidade * produto["preco"]

        # ===== NORMALIZAÇÃO =====
        dias_score = min(dias / 30, 1) * 10
        qtd_score = min(quantidade / 100, 1) * 10
        valor_score = min(valor_total / 1000, 1) * 10

        # ===== PESOS =====
        peso_dias = 0.4
        peso_qtd = 0.3
        peso_valor = 0.3

        prioridade = (
            dias_score * peso_dias +
            qtd_score * peso_qtd +
            valor_score * peso_valor
        )

        # ===== VALIDADE =====
        if "validade" in produto:
            data_validade = datetime.strptime(produto["validade"], "%d/%m/%Y")
            dias_validade = (data_validade - hoje).days

            if dias_validade <= 0:
                prioridade = 10
            elif dias_validade <= 7:
                prioridade += 2

        return round(prioridade, 2)
    
    def classificar_prioridade(self, produto):
        prioridade = self.calcular_prioridade(produto)

        if prioridade >= 150:
            return "ALTA"
        elif prioridade >= 80:
            return "MÉDIA"
        else:
            return "BAIXA"

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