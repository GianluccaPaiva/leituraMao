import cv2
import mediapipe as mp
import time

from src.gestos import Gestos
from src.libras import Libras

gestos = Gestos()


# =========================
# MEDIAPIPE
# =========================
mp_mao = mp.solutions.hands
detector = mp_mao.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

desenho = mp.solutions.drawing_utils

# =========================
# LIBRAS
# =========================
libras = Libras("dados/alfabeto.json")

# =========================
# CÂMERA
# =========================
cap = cv2.VideoCapture(0)

ultima_letra = None
ultimo_tempo = 0

# =========================
# LOOP PRINCIPAL
# =========================
while True:
    ok, frame = cap.read()
    if not ok:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    resultados = detector.process(rgb)

    if resultados.multi_hand_landmarks:
        for hand_landmarks in resultados.multi_hand_landmarks:

            # desenha a mão
            desenho.draw_landmarks(
                frame,
                hand_landmarks,
                mp_mao.HAND_CONNECTIONS
            )

            # =========================
            # EXTRAI FEATURES
            # =========================
            features = gestos.extrair_features(hand_landmarks.landmark)

            if features:
                letra, erro = libras.reconhecer(features)

                # limiar de confiança
                if erro < 0.35:
                    agora = time.time()

                    if letra != ultima_letra or agora - ultimo_tempo > 1:
                        print(f"Letra detectada: {letra}")
                        ultima_letra = letra
                        ultimo_tempo = agora

                    cv2.putText(
                        frame,
                        f"{letra}",
                        (40, 80),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        2,
                        (0, 255, 0),
                        4
                    )

    cv2.imshow("Leitura de LIBRAS", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# =========================
# FINALIZAÇÃO
# =========================
cap.release()
cv2.destroyAllWindows()
