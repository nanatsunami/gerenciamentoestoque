import unittest

from src.core.lista_produtos import ListaProdutos
from src.core.fila_criticos import FilaCriticos
from src.service.estoque_service import EstoqueService

class TestListaProdutos(unittest.TestCase):
    # Primeiro teste lista
    def test_inserir_produto(self):
        lista = ListaProdutos()
        produto = {"nome": "Papel", "quantidade": 10}

        lista.inserir(produto)

        self.assertEqual(lista.exibir()[0]["nome"], "Papel")

    # Segundo teste
    def test_buscar_lista_vazia(self):
        lista = ListaProdutos()

        resultado = lista.buscar("Papel")

        self.assertIsNone(resultado)

    # Terceiro teste
    def test_buscar_multiplos_produtos(self):
        lista = ListaProdutos()

        lista.inserir({"nome": "Papel", "quantidade": 10})
        lista.inserir({"nome": "Lápis", "quantidade": 5})
        lista.inserir({"nome": "Borracha", "quantidade": 20})

        resultado = lista.buscar("Papel")

        self.assertEqual(resultado["nome"], "Papel")


class TestFilaCriticos(unittest.TestCase):
    # Primeiro teste fila
    def test_enqueue_produto(self):
        fila = FilaCriticos()
        produto = {"nome": "Papel", "prioridade": 8}

        fila.enqueue(produto)

        self.assertEqual(fila.frente()["nome"], "Papel")


    # Segundo teste
    def test_dequeue_fila_vazia(self):
        fila = FilaCriticos()

        resultado = fila.dequeue()

        self.assertIsNone(resultado)

    # Terceiro teste
    def test_fifo_multiplos_produtos(self):
        fila = FilaCriticos()

        fila.enqueue({"nome": "Papel"})
        fila.enqueue({"nome": "Lápis"})
        fila.enqueue({"nome": "Borracha"})

        primeiro = fila.dequeue()

        self.assertEqual(primeiro["nome"], "Papel")
        
class TestEstoqueService(unittest.TestCase):

    def test_classificacao_prioridade(self):
        service = EstoqueService(None, None)

        produto = {
            "nome": "Leite",
            "quantidade": 50,
            "preco": 10,
            "data": "01/01/2025"
        }

        resultado = service.classificar_prioridade(produto)

        self.assertIn(
            resultado,
            ["ALTA !!!", "MÉDIA !!", "BAIXA !"]
        )


if __name__ == "__main__":
    unittest.main()
