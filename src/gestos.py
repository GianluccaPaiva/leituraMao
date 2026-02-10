import time
import math
from src.mao import distancia, tamanho_mao

class Gestos:
    def __init__(self):
        self.historico_posicoes = []
        self.limite_historico = 15
        
    def extrair_features(self, landmarks):
        t = tamanho_mao(landmarks)
        if t == 0: return None

        return {
            "thumb_index": distancia(landmarks[4], landmarks[8]) / t,
            "index_middle": distancia(landmarks[8], landmarks[12]) / t,
            "middle_ring": distancia(landmarks[12], landmarks[16]) / t,
            "ring_pinky": distancia(landmarks[16], landmarks[20]) / t,
            "thumb_wrist": distancia(landmarks[4], landmarks[0]) / t,
            "index_wrist": distancia(landmarks[8], landmarks[0]) / t,
            "middle_wrist": distancia(landmarks[12], landmarks[0]) / t,
            "ring_wrist": distancia(landmarks[16], landmarks[0]) / t,
            "pinky_wrist": distancia(landmarks[20], landmarks[0]) / t
        }

    def rastrear_movimento(self, ponto):
        self.historico_posicoes.append((ponto.x, ponto.y))
        if len(self.historico_posicoes) > self.limite_historico:
            self.historico_posicoes.pop(0)

    def limpar_historico(self):
        self.historico_posicoes = []

    def detectar_desenho_j(self):
        if len(self.historico_posicoes) < 12: return False
        inicio = self.historico_posicoes[0]
        fim = self.historico_posicoes[-1]
        # J: Desce bastante e curva lateralmente
        return (fim[1] - inicio[1] > 0.15) and (abs(fim[0] - inicio[0]) > 0.08)

    def detectar_desenho_z(self):
        if len(self.historico_posicoes) < 15: return False
        p1 = self.historico_posicoes[0]
        p2 = self.historico_posicoes[len(self.historico_posicoes)//2]
        p3 = self.historico_posicoes[-1]
        # Z: Movimento em zig-zag (X vai e volta)
        return abs(p1[0] - p2[0]) > 0.1 and abs(p2[0] - p3[0]) > 0.1