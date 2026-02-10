import time
import webbrowser
from src.mao import distancia, tamanho_mao

class Gestos:
    def __init__(self):
        self.ultimo_x = None
        self.direcao_anterior = None
        self.ultimo_oi = 0
        self.ultimo_spider = 0
        self.URL = "https://www.google.com"

    def gesto_oi(self, x_atual):
        if self.ultimo_x is None:
            self.ultimo_x = x_atual
            return

        delta = x_atual - self.ultimo_x
        direcao = None

        if delta > 0.01:
            direcao = "direita"
        elif delta < -0.01:
            direcao = "esquerda"

        if direcao and self.direcao_anterior and direcao != self.direcao_anterior:
            agora = time.time()
            if agora - self.ultimo_oi > 1:
                print("Oi 👋")
                self.ultimo_oi = agora

        self.direcao_anterior = direcao
        self.ultimo_x = x_atual

    def homem_aranha(self, estado_dedos):
        if (
            estado_dedos["polegar"] and
            estado_dedos["mindinho"] and
            estado_dedos["indicador"] and
            not estado_dedos["medio"] and
            not estado_dedos["anelar"]
        ):
            agora = time.time()
            if agora - self.ultimo_spider > 2:
                print("🕷️ Homem-Aranha!")
                webbrowser.open(self.URL)
                self.ultimo_spider = agora
                
    def extrair_features(self, landmarks):
        t = tamanho_mao(landmarks)
        if t == 0:
            return None

        return {
            "thumb_index": distancia(landmarks[4], landmarks[8]) / t,
            "index_middle": distancia(landmarks[8], landmarks[12]) / t,
            "middle_ring": distancia(landmarks[12], landmarks[16]) / t,
            "ring_pinky": distancia(landmarks[16], landmarks[20]) / t
        }
