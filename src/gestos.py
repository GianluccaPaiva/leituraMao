import math
from src.mao import distancia, tamanho_mao

class Gestos:
    def __init__(self):
        # Buffer para armazenar a trajetória dos dedos (sequência de frames)
        self.historico_posicoes = []
        self.limite_historico = 15 
        
    def extrair_features(self, landmarks):
        t = tamanho_mao(landmarks)
        if t == 0: return None

        # Características estáticas + Distâncias ao pulso (wrist) para precisão
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
        """Adiciona a posição atual do dedo ao histórico de frames."""
        self.historico_posicoes.append((ponto.x, ponto.y))
        if len(self.historico_posicoes) > self.limite_historico:
            self.historico_posicoes.pop(0)

    def limpar_historico(self):
        """Limpa a sequência de frames para evitar detecções falsas."""
        self.historico_posicoes = []

    def detectar_desenho_j(self):
        """Lógica facilitada para o movimento do J (mindinho)."""
        if len(self.historico_posicoes) < 8: return False
        inicio = self.historico_posicoes[0]
        fim = self.historico_posicoes[-1]
        # Verifica se desceu no eixo Y e moveu-se no eixo X
        return (fim[1] - inicio[1] > 0.10) and (abs(fim[0] - inicio[0]) > 0.05)

    def detectar_desenho_z(self):
        """Lógica facilitada para o zig-zag do Z (indicador)."""
        if len(self.historico_posicoes) < 10: return False
        p1 = self.historico_posicoes[0]
        p2 = self.historico_posicoes[len(self.historico_posicoes)//2]
        p3 = self.historico_posicoes[-1]
        # Verifica a mudança de direção lateral (zig-zag)
        return abs(p1[0] - p2[0]) > 0.07 and abs(p2[0] - p3[0]) > 0.07