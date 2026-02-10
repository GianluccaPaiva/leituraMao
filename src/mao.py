import mediapipe as mp
import math

# =========================
# FUNÇÕES MATEMÁTICAS (PURO)
# =========================
def distancia(p1, p2):
    return math.sqrt(
        (p1.x - p2.x) ** 2 +
        (p1.y - p2.y) ** 2 +
        (p1.z - p2.z) ** 2
    )

def tamanho_mao(landmarks):
    # punho (0) até ponta do dedo médio (12)
    return distancia(landmarks[0], landmarks[12])


# =========================
# CLASSE DE DETECÇÃO (MEDIAPIPE)
# =========================
class DetectorMao:
    def __init__(self):
        self.modulo_mao = mp.solutions.hands
        self.detector = self.modulo_mao.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.desenho = mp.solutions.drawing_utils

    def processar(self, frame_rgb):
        return self.detector.process(frame_rgb)

    def desenhar(self, frame, hand_landmarks):
        self.desenho.draw_landmarks(
            frame,
            hand_landmarks,
            self.modulo_mao.HAND_CONNECTIONS
        )
