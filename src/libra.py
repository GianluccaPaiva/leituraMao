import cv2
import mediapipe as mp
import time
import json
from src.gestos import Gestos
from src.libras import Libras
from src.falador_frase import Falador

# Configurações para eliminar "fantasmas"
with open("dados/config.json") as f:
    config = json.load(f)

cfg_libras = config["libras"]
LIMITE_ESTABILIDADE = cfg_libras["limite_estabilidade"]
LIMIAR_ERRO_ESTRITO = cfg_libras["limiar_erro_estrito"]
LIMIAR_MOVIMENTO_MAO = cfg_libras["limiar_movimento_mao"]
TEMPO_ENTRE_LETRAS = cfg_libras["tempo_entre_letras"]
DELAY_BACKSPACE = cfg_libras["delay_backspace"]

palabra = []
gestos = Gestos()
libras = Libras("dados/alfabeto.json")
mp_mao = mp.solutions.hands
detector = mp_mao.Hands(**config["mediapipe"])
desenho = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
letra_candidata = None
contador_estabilidade = 0
ultima_letra_confirmada = ""
ultimo_tempo_backspace = 0  # Controla delay do backspace
posicao_mao_anterior = None  # Rastreia posição anterior da mão para detectar movimento

falador = Falador(libras.ref)

def calcular_distancia_euclidiana(p1, p2):
    """Calcula distância euclidiana entre dois pontos"""
    return ((p1.x - p2.x)**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2)**0.5

def detectar_movimento_mao(landmark_atual, landmark_anterior, limiar=LIMIAR_MOVIMENTO_MAO):
    """Detecta se a mão se moveu além do limiar"""
    if landmark_anterior is None:
        return False
    distancia = calcular_distancia_euclidiana(landmark_atual, landmark_anterior)
    return distancia > limiar

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
            
            # Rastreia posição do pulso (landmark 0) para detectar movimento
            pulso_atual = hand_landmarks.landmark[0]
            movimento_detectado = detectar_movimento_mao(pulso_atual, posicao_mao_anterior)
            posicao_mao_anterior = pulso_atual

            if features:
                letra_detectada, erro = libras.reconhecer(features)

                # Prioridade 1: Comandos Especiais (ENTER / ESPAÇO / BACKSPACE) com estabilidade
                if letra_detectada == "ENTER":
                    if erro < 0.15: # Limiar rigoroso para comandos
                        contador_estabilidade += 1
                        if contador_estabilidade >= 20: # Mais estável para não errar o comando
                            if letra_detectada != ultima_letra_confirmada:  # Evita múltiplos ENTER
                                print("⌨️ COMANDO EXECUTADO: ENTER")
                                falador.processar_comando("ENTER")
                                ultima_letra_confirmada = letra_detectada
                            contador_estabilidade = 0
                            letra_candidata = None
                
                elif letra_detectada == "ESPACO":
                    if erro < 0.15:
                        contador_estabilidade += 1
                        if contador_estabilidade >= 20:
                            if letra_detectada != ultima_letra_confirmada:  # Evita múltiplos ESPAÇO
                                print("⌨️ COMANDO EXECUTADO: ESPAÇO")
                                falador.processar_comando("ESPACO")
                                ultima_letra_confirmada = letra_detectada
                            contador_estabilidade = 0
                            letra_candidata = None
                
                elif letra_detectada == "\b":
                    if erro < 0.15:
                        contador_estabilidade += 1
                        if contador_estabilidade >= 20:
                            # Verifica se passou o delay desde o último backspace
                            tempo_agora = time.time()
                            if tempo_agora - ultimo_tempo_backspace >= DELAY_BACKSPACE:
                                print("⌨️ COMANDO EXECUTADO: BACKSPACE")
                                falador.processar_comando("\b")
                                ultimo_tempo_backspace = tempo_agora  # Atualiza tempo
                            contador_estabilidade = 0  # Reset imediato
                            letra_candidata = None
                    else:
                        # Quando sai da pose de backspace, reseta para permitir novo
                        if letra_candidata == "\b":
                            letra_candidata = None
                            contador_estabilidade = 0
                            ultima_letra_confirmada = ""  # Limpa para permitir novo backspace
                            
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
                        # Se detectou ENTER, processa idependente da última letra ser ENTER
                        if letra_detectada == "ENTER":
                            resultado = falador.processar_comando("ENTER")
                            print("✅ Frase falada e zerada.")
                            # IMPORTANTE: Resetar para permitir novo ENTER em seguida
                            ultima_letra_confirmada = "" 
                            contador_estabilidade = 0 
                            letra_candidata = None
                        
                        # Lógica normal para as outras letras: aceita nova letra se for diferente
                        # OU se for IGUAL mas houve movimento significativo da mão
                        elif letra_detectada != ultima_letra_confirmada or (letra_detectada == ultima_letra_confirmada and movimento_detectado):
                            resultado = falador.processar_comando(letra_detectada)
                            print(f"📝 Frase: {resultado}")
                            ultima_letra_confirmada = letra_detectada
                            posicao_mao_anterior = None  # Reseta posição para próximo movimento
                else:
                    contador_estabilidade = 0
                    letra_candidata = None

    cv2.imshow("Sistema LIBRAS - Estabilidade e Movimento", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"): break

cap.release()
cv2.destroyAllWindows()