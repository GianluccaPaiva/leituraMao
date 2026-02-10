import cv2
import mediapipe as mp
import time
from src.gestos import Gestos
from src.libras import Libras

# --- CONFIGURAÇÃO ANTI-FANTASMA ---
LIMITE_ESTABILIDADE = 15  # Aumentado para exigir mais tempo na mesma pose
LIMIAR_ERRO_ESTRITO = 0.15 # Reduzido para ser mais exigente na precisão
TEMPO_ENTRE_LETRAS = 1.2   # Intervalo para não repetir a mesma letra

gestos = Gestos()
libras = Libras("dados/alfabeto.json")
mp_mao = mp.solutions.hands
detector = mp_mao.Hands(max_num_hands=1, min_detection_confidence=0.8) # Aumentado
desenho = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

letra_candidata = None
contador_estabilidade = 0
ultima_letra_confirmada = ""
ultimo_tempo_print = 0

while True:
    ok, frame = cap.read()
    if not ok: break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resultados = detector.process(rgb)

    letra_atual_display = "..."

    if resultados.multi_hand_landmarks:
        for hand_landmarks in resultados.multi_hand_landmarks:
            desenho.draw_landmarks(frame, hand_landmarks, mp_mao.HAND_CONNECTIONS)
            features = gestos.extrair_features(hand_landmarks.landmark)

            if features:
                letra_detectada, erro = libras.reconhecer(features)

                # Tratamento de movimento
                if letra_detectada == "I":
                    gestos.rastrear_movimento(hand_landmarks.landmark[20])
                    if gestos.detectar_desenho_j(): letra_detectada = "J"
                elif letra_detectada == "D":
                    gestos.rastrear_movimento(hand_landmarks.landmark[8])
                    if gestos.detectar_desenho_z(): letra_detectada = "Z"
                else:
                    gestos.limpar_historico()

                # --- FILTRO DE ESTABILIDADE REFORÇADO ---
                if erro < LIMIAR_ERRO_ESTRITO:
                    if letra_detectada == letra_candidata:
                        contador_estabilidade += 1
                    else:
                        letra_candidata = letra_detectada
                        contador_estabilidade = 0

                    if contador_estabilidade >= LIMITE_ESTABILIDADE:
                        agora = time.time()
                        if letra_detectada != ultima_letra_confirmada or (agora - ultimo_tempo_print) > TEMPO_ENTRE_LETRAS:
                            print(f"Letra Confirmada: {letra_detectada} (Erro: {erro:.3f})")
                            ultima_letra_confirmada = letra_detectada
                            ultimo_tempo_print = agora
                        letra_atual_display = letra_detectada
                else:
                    # Se o erro subir, resetamos tudo para evitar "fantasmas" de transição
                    contador_estabilidade = 0
                    letra_candidata = None

    # Interface Visual
    cv2.rectangle(frame, (0, 0), (250, 120), (0, 0, 0), -1)
    cv2.putText(frame, f"LETRA: {letra_atual_display}", (20, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
    cv2.putText(frame, f"ESTAVEL: {contador_estabilidade}", (20, 90), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

    cv2.imshow("LIBRAS - Sem Fantasmas", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"): break

cap.release()
cv2.destroyAllWindows()