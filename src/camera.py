import time
from gestos import Gestos
from libras import Libras
from camera_manager import CameraManager

# Inicializa gerenciador de câmera
camera = CameraManager()

# Inicializa módulos de reconhecimento
cfg_validacao = camera.config.get("validacao_dedos", {})
gestos = Gestos(cfg_validacao)
libras = Libras()
ultima = None
tempo = 0

# Loop principal
while True:
    # Captura frame da câmera
    if not camera.capturar_frame():
        break
    
    # Desenha landmarks
    camera.desenhar_landmarks()
    
    # Processa cada mão detectada
    for idx, hand in enumerate(camera.obter_landmarks()):
        features = gestos.extrair_features(hand.landmark)
        if features:
            letra, erro = libras.reconhecer(features)
            
            # Valida espaçamento entre dedos
            if not gestos.validar_espacamento_dedos(features, letra):
                continue

            if erro < 0.35:
                agora = time.time()
                if letra != ultima or agora - tempo > 1:
                    print(f"Mão {idx}: Letra: {letra}")
                    ultima = letra
                    tempo = agora

                # Posiciona cada mão em uma posição diferente
                pos_x = 40 + (idx * 200)
                import cv2
                cv2.putText(
                    camera.frame,
                    letra,
                    (pos_x, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    2,
                    (0, 255, 0),
                    4
                )
    
    # Exibe frame e verifica tecla
    tecla = camera.exibir_frame("LIBRAS")
    if tecla == ord("q"):
        break

# Fecha recursos
camera.fechar()
