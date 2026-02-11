import math
from src.mao import distancia, tamanho_mao

class Gestos:
    def __init__(self, config_validacao=None):
        # Buffer para armazenar a trajetória dos dedos (sequência de frames)
        self.historico_posicoes = []
        self.limite_historico = 15 
        
        # Configurações de validação de espaçamento entre dedos
        if config_validacao is None:
            config_validacao = {}
        
        self.limiar_dedos_juntos = config_validacao.get("limiar_dedos_juntos", 0.18)
        self.limiar_dedos_afastados = config_validacao.get("limiar_dedos_afastados", 0.20)
        self.letras_dedos_juntos = config_validacao.get("letras_dedos_juntos", ["B", "D", "F", "G", "P", "Q"])
        self.letras_dedos_afastados = config_validacao.get("letras_dedos_afastados", ["V", "W", "Y"])
        
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
    
    def validar_espacamento_dedos(self, features, letra_detectada):
        """
        Valida se a letra detectada tem características de espaçamento coerentes
        Letras com dedos juntos (B): index_middle, middle_ring, ring_pinky devem ser pequenos
        Letras com dedos afastados (V): essas distâncias devem ser maiores
        Retorna True se a validação passar ou False se for incoerente
        """
        # Calcula distância média entre dedos consecutivos
        distancia_media_dedos = (
            features["index_middle"] + 
            features["middle_ring"] + 
            features["ring_pinky"]
        ) / 3
        
        # Validação para letras com dedos juntos
        if letra_detectada in self.letras_dedos_juntos:
            if distancia_media_dedos > self.limiar_dedos_juntos:  # Dedos abertos demais
                return False
        
        # Validação para letras com dedos afastados
        elif letra_detectada in self.letras_dedos_afastados:
            if distancia_media_dedos < self.limiar_dedos_afastados:  # Dedos fechados demais
                return False
        
        return True

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

    def detectar_desenho_l(self):
        """Lógica facilitada para o movimento do L (mao-esquerda)."""
        if len(self.historico_posicoes) < 8: return False
        inicio = self.historico_posicoes[0]
        fim = self.historico_posicoes[-1]
        # Verifica se desceu no eixo Y e moveu-se no eixo X
        return (fim[1] - inicio[1] > 0.10) and (abs(fim[0] - inicio[0]) > 0.05)
    
    def detectar_enter(self, features):
        """
        Detecta o gesto de 'positivo' (polegar levantado e outros fechados).
        Valores de wrist baixos (~0.3-0.4) indicam dedos dobrados.
        Valores de wrist altos (>0.5) indicam dedos esticados.
        """
        if not features: return False
        
        polegar_aberto = features["thumb_wrist"] > 0.5
        indicador_fechado = features["index_wrist"] < 0.45
        medio_fechado = features["middle_wrist"] < 0.45
        anelar_fechado = features["ring_wrist"] < 0.45
        mindinho_fechado = features["pinky_wrist"] < 0.45

        return polegar_aberto and indicador_fechado and medio_fechado and \
               anelar_fechado and mindinho_fechado