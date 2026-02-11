import cv2
import mediapipe as mp
import json
import os


class CameraManager:
    """Gerenciador centralizado de captura de câmera e detecção de mãos"""
    
    def __init__(self, config_path="dados/config.json"):
        # Carrega configurações
        with open(config_path) as f:
            self.config = json.load(f)
        
        # Inicializa MediaPipe
        self.mp_mao = mp.solutions.hands
        self.detector = self.mp_mao.Hands(**self.config["mediapipe"])
        self.desenho = mp.solutions.drawing_utils
        
        # Inicializa câmera
        self.cap = cv2.VideoCapture(0)
        self.frame = None
        self.rgb = None
        self.resultados = None
        
    def capturar_frame(self):
        """Captura e processa um frame da câmera"""
        ok, frame = self.cap.read()
        if not ok:
            return False
        
        # Flip e conversão de cores
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Processa com MediaPipe
        resultados = self.detector.process(rgb)
        
        # Armazena para uso posterior
        self.frame = frame
        self.rgb = rgb
        self.resultados = resultados
        
        return True
    
    def desenhar_landmarks(self, frame=None):
        """Desenha os landmarks na frame"""
        if frame is None:
            frame = self.frame
        
        if self.resultados and self.resultados.multi_hand_landmarks:
            for hand_landmarks in self.resultados.multi_hand_landmarks:
                self.desenho.draw_landmarks(
                    frame, 
                    hand_landmarks, 
                    self.mp_mao.HAND_CONNECTIONS
                )
        
        return frame
    
    def exibir_frame(self, titulo="LIBRAS"):
        """Exibe o frame na tela e retorna a tecla pressionada (-1 se nenhuma)"""
        cv2.imshow(titulo, self.frame)
        tecla = cv2.waitKey(1) & 0xFF
        return tecla
    
    def fechar(self):
        """Fecha a câmera e destroi as janelas"""
        self.cap.release()
        cv2.destroyAllWindows()
    
    def obter_landmarks(self):
        """Retorna lista de landmarks das mãos detectadas"""
        if self.resultados and self.resultados.multi_hand_landmarks:
            return self.resultados.multi_hand_landmarks
        return []
    
    def obter_config_libras(self):
        """Retorna configurações específicas de LIBRAS"""
        return self.config.get("libras", {})
