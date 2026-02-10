import cv2
import mediapipe as mp
import time
from src.gestos import Gestos
from src.libras import Libras

# Configurações otimizadas para a tabela
LIMITE_ESTABILIDADE = 12   # Equilíbrio entre velocidade e precisão
LIMIAR_ERRO_ESTRITO = 0.18 # Ligeiramente mais permissivo para facilitar o uso
TEMPO_ENTRE_LETRAS = 1.0

gestos = Gestos()
libras = Libras("dados/alfabeto.json")
mp_mao = mp.solutions.hands
detector = mp_mao.Hands(max_num_hands=1, min_detection_confidence=0.75)
desenho = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
letra_candidata = None
contador_estabilidade = 0
ultima_letra_confirmada = ""

while True:
    ok, frame = cap.read()
    if not ok: break
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resultados = detector.process(rgb)

    if resultados.multi_hand_landmarks:
        for hand_landmarks in resultados.multi_hand_landmarks:
            desenho.draw_landmarks(frame, hand_landmarks, mp_mao.HAND_CONNECTIONS)
            features = gestos.extrair_features(hand_landmarks.landmark)

            if features:
                letra_detectada, erro = libras.reconhecer(features)

                # Prioridade para Letras com Movimento (J e Z)
                # J começa com pose de I, Z começa com pose de D
                if letra_detectada == "I" or letra_detectada == "J":
                    gestos.rastrear_movimento(hand_landmarks.landmark[20]) # Mindinho
                    if gestos.detectar_desenho_j(): 
                        letra_detectada = "J"
                        contador_estabilidade = LIMITE_ESTABILIDADE # Força detecção rápida
                
                elif letra_detectada == "D" or letra_detectada == "Z":
                    gestos.rastrear_movimento(hand_landmarks.landmark[8]) # Indicador
                    if gestos.detectar_desenho_z(): 
                        letra_detectada = "Z"
                        contador_estabilidade = LIMITE_ESTABILIDADE
                else:
                    gestos.limpar_historico()

                # Filtro de Estabilidade
                if erro < LIMIAR_ERRO_ESTRITO:
                    if letra_detectada == letra_candidata:
                        contador_estabilidade += 1
                    else:
                        letra_candidata = letra_detectada
                        contador_estabilidade = 0

                    if contador_estabilidade >= LIMITE_ESTABILIDADE:
                        if letra_detectada != ultima_letra_confirmada:
                            print(f"✅ LETRA: {letra_detectada}")
                            ultima_letra_confirmada = letra_detectada
                else:
                    contador_estabilidade = 0

    cv2.imshow("Reconhecimento Otimizado LIBRAS", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"): break

cap.release()
cv2.destroyAllWindows()