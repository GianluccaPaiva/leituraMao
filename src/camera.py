import cv2
import mediapipe as mp
import time

from gestos import extrair_features
from libras import Libras

mp_mao = mp.solutions.hands
detector = mp_mao.Hands(max_num_hands=1)
desenho = mp.solutions.drawing_utils

libras = Libras()

cap = cv2.VideoCapture(0)
ultima = None
tempo = 0

while True:
    ok, frame = cap.read()
    if not ok:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    res = detector.process(rgb)

    if res.multi_hand_landmarks:
        for hand in res.multi_hand_landmarks:
            desenho.draw_landmarks(frame, hand, mp_mao.HAND_CONNECTIONS)

            features = extrair_features(hand.landmark)
            if features:
                letra, erro = libras.reconhecer(features)

                if erro < 0.35:
                    agora = time.time()
                    if letra != ultima or agora - tempo > 1:
                        print("Letra:", letra)
                        ultima = letra
                        tempo = agora

                    cv2.putText(
                        frame,
                        letra,
                        (40, 80),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        2,
                        (0, 255, 0),
                        4
                    )

    cv2.imshow("LIBRAS", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
