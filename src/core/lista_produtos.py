class ListaProdutos:
    def __init__(self):
        self.produtos = []

    def inserir(self, produto):
        self.produtos.append(produto)

    def remover(self, nome):
        for p in self.produtos:
            if p["nome"] == nome:
                self.produtos.remove(p)
                return True
        return False

    def buscar(self, nome):
        for p in self.produtos:
            if p["nome"] == nome:
                return p
        return None

    def exibir(self):
        return self.produtos
