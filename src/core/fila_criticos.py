class FilaCriticos:
    def __init__(self):
        self.fila = []

    def enqueue(self, produto):
        self.fila.append(produto)

    def dequeue(self):
        if self.esta_vazia():
            return None
        return self.fila.pop(0)

    def frente(self):
        if self.esta_vazia():
            return None
        return self.fila[0]

    def esta_vazia(self):
        return len(self.fila) == 0
