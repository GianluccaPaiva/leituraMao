import json

class Libras:
    def __init__(self, path="dados/alfabeto.json"):
        with open(path, "r") as f:
            self.ref = json.load(f)

    def erro(self, a, b):
    # Soma dos quadrados das diferenças (mais preciso que a soma simples)
        return sum((a[k] - b[k]) ** 2 for k in a if k in b)
    
    def reconhecer(self, features):
        melhor = None
        menor = float("inf")

        for letra, padrao in self.ref.items():
            e = self.erro(features, padrao)
            if e < menor:
                menor = e
                melhor = letra

        return melhor, menor
