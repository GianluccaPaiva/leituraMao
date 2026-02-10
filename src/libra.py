import cv2
import mediapipe as mp
import time
from src.gestos import Gestos
from src.libras import Libras

# Configurações para eliminar "fantasmas"
LIMITE_ESTABILIDADE = 12   # Frames necessários para confirmar a letra
LIMIAR_ERRO_ESTRITO = 0.18 # Quão parecida a pose deve estar do JSON
TEMPO_ENTRE_LETRAS = 1.0

palabra = []
gestos = Gestos()
libras = Libras("dados/alfabeto.json")
mp_mao = mp.solutions.hands
detector = mp_mao.Hands(max_num_hands=1, min_detection_confidence=0.75, min_tracking_confidence=0.75)
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

                # Prioridade 1: Comandos Especiais (ENTER / ESPAÇO)
                if letra_detectada == "ENTER":
                    if erro < 0.15: # Limiar rigoroso para comandos
                        contador_estabilidade += 1
                        if contador_estabilidade >= 20: # Mais estável para não errar o comando
                            print("⌨️ COMANDO EXECUTADO: ENTER")
                            # Se quiser simular a tecla real: pyautogui.press('enter')
                            contador_estabilidade = LIMITE_ESTABILIDADE # Reset para não repetir infinitamente
                if letra_detectada == "ESPACO":
                    if erro < 0.15:
                        contador_estabilidade += 1
                        if contador_estabilidade >= 20:
                            print("⌨️ COMANDO EXECUTADO: ESPAÇO")
                            # pyautogui.press('space')
                            contador_estabilidade = LIMITE_ESTABILIDADE
                if letra_detectada =="\b":
                    if erro < 0.15:
                        contador_estabilidade += 1
                        if contador_estabilidade >= 20:
                            print("⌨️ COMANDO EXECUTADO: BACKSPACE")
                            # pyautogui.press('backspace')
                            contador_estabilidade = LIMITE_ESTABILIDADE
                            
                # Prioridade 2: Letras com Movimento (J e Z)
                elif letra_detectada in ["I", "J"]:
                    gestos.rastrear_movimento(hand_landmarks.landmark[20])
                    if gestos.detectar_desenho_j(): letra_detectada = "J"

                # Prioridade: Se a pose base for I ou D, verifica movimento para J ou Z
                if letra_detectada in ["I", "J"]:
                    gestos.rastrear_movimento(hand_landmarks.landmark[20]) # Mindinho
                    if gestos.detectar_desenho_j(): 
                        letra_detectada = "J"
                        contador_estabilidade = LIMITE_ESTABILIDADE # Confirmação imediata
                
                elif letra_detectada in ["D", "Z"]:
                    gestos.rastrear_movimento(hand_landmarks.landmark[8]) # Indicador
                    if gestos.detectar_desenho_z(): 
                        letra_detectada = "Z"
                        contador_estabilidade = LIMITE_ESTABILIDADE
                else:
                    gestos.limpar_historico()

                # Filtro de Estabilidade (Anti-Fantasma)
                if erro < LIMIAR_ERRO_ESTRITO:
                    if letra_detectada == letra_candidata:
                        contador_estabilidade += 1
                    else:
                        letra_candidata = letra_detectada
                        contador_estabilidade = 0

                    if contador_estabilidade >= LIMITE_ESTABILIDADE:
                        if letra_detectada != ultima_letra_confirmada:
                            print(f"✅ CONFIRMADA: {letra_detectada}")
                            palabra.append(letra_detectada)
                            time.sleep(TEMPO_ENTRE_LETRAS)
                            ultima_letra_confirmada = letra_detectada
                else:
                    contador_estabilidade = 0
                    letra_candidata = None

    cv2.imshow("Sistema LIBRAS - Estabilidade e Movimento", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"): break

cap.release()
cv2.destroyAllWindows()