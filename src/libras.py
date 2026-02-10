import json

class Libras:
    def __init__(self, path="dados/alfabeto.json"):
        with open(path, "r") as f:
            self.ref = json.load(f)

    def erro(self, a, b):
        return sum(abs(a[k] - b[k]) for k in a)

    def reconhecer(self, features):
        melhor = None
        menor = float("inf")

        for letra, padrao in self.ref.items():
            e = self.erro(features, padrao)
            if e < menor:
                menor = e
                melhor = letra

        return melhor, menor
