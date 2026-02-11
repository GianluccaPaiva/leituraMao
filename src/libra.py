import runpy
import cv2
import time
from src.gestos import Gestos
from src.libras import Libras
from src.falador_frase import Falador
from src.camera_manager import CameraManager

# Inicializa o gerenciador de câmera centralizado
camera = CameraManager()

# Carrega configurações de LIBRAS
cfg_libras = camera.obter_config_libras()
LIMITE_ESTABILIDADE = cfg_libras["limite_estabilidade"]
LIMIAR_ERRO_ESTRITO = cfg_libras["limiar_erro_estrito"]
LIMIAR_MOVIMENTO_MAO = cfg_libras["limiar_movimento_mao"]
TEMPO_ENTRE_LETRAS = cfg_libras["tempo_entre_letras"]
DELAY_BACKSPACE = cfg_libras["delay_backspace"]
LIMIAR_ERRO_COMANDO = cfg_libras.get("limiar_erro_comando", 0.12)
LIMIAR_MOVIMENTO_MINIMO = cfg_libras.get("limiar_movimento_minimo", 0.08)
FRAMES_CONFIRMACAO_COMANDO = cfg_libras.get("frames_confirmacao_comando", 25)

# Inicializa módulos
palabra = []
cfg_validacao = camera.config.get("validacao_dedos", {})
gestos = Gestos(cfg_validacao)
libras = Libras("dados/alfabeto.json")
falador = Falador(libras.ref)

# Estado de reconhecimento
letra_candidata = None
contador_estabilidade = 0
ultima_letra_confirmada = ""
ultimo_tempo_backspace = 0  # Controla delay do backspace
posicao_mao_anterior = None  # Rastreia posição anterior da mão para detectar movimento

def calcular_distancia_euclidiana(p1, p2):
    """Calcula distância euclidiana entre dois pontos"""
    return ((p1.x - p2.x)**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2)**0.5

def detectar_movimento_mao(landmark_atual, landmark_anterior, limiar=LIMIAR_MOVIMENTO_MAO):
    """Detecta se a mão se moveu além do limiar (ignora pequenos tremores)"""
    if landmark_anterior is None:
        return False
    distancia = calcular_distancia_euclidiana(landmark_atual, landmark_anterior)
    return distancia > limiar

# Loop principal
while True:
    # Captura frame da câmera
    if not camera.capturar_frame():
        break
    
    # Desenha landmarks
    camera.desenhar_landmarks()
    
    # Processa cada mão detectada
    for hand_landmarks in camera.obter_landmarks():
        features = gestos.extrair_features(hand_landmarks.landmark)
        
        # Rastreia posição do pulso (landmark 0) para detectar movimento
        pulso_atual = hand_landmarks.landmark[0]
        movimento_detectado = detectar_movimento_mao(pulso_atual, posicao_mao_anterior)
        posicao_mao_anterior = pulso_atual

        if features:
            letra_detectada, erro = libras.reconhecer(features)
            
            # Validação de espaçamento entre dedos (B, V, etc)
            # Rejeita detecção se espaçamento for incoerente com a letra
            if not gestos.validar_espacamento_dedos(features, letra_detectada):
                # Trata como erro e não processa
                contador_estabilidade = 0
                letra_candidata = None
                continue

            # Prioridade 1: Comandos Especiais (ENTER / ESPAÇO / BACKSPACE) com estabilidade reforçada
            if letra_detectada == "ENTER":
                if erro < LIMIAR_ERRO_COMANDO:
                    contador_estabilidade += 1
                    if contador_estabilidade >= FRAMES_CONFIRMACAO_COMANDO:
                        if letra_detectada != ultima_letra_confirmada:
                            print("⌨️ COMANDO EXECUTADO: ENTER")
                            falador.processar_comando("ENTER")
                            ultima_letra_confirmada = letra_detectada
                        contador_estabilidade = 0
                        letra_candidata = None
                else:
                    contador_estabilidade = 0
            
            elif letra_detectada == "ESPACO":
                if erro < LIMIAR_ERRO_COMANDO:
                    contador_estabilidade += 1
                    if contador_estabilidade >= FRAMES_CONFIRMACAO_COMANDO:
                        if letra_detectada != ultima_letra_confirmada:
                            print("⌨️ COMANDO EXECUTADO: ESPAÇO")
                            falador.processar_comando("ESPACO")
                            ultima_letra_confirmada = letra_detectada
                        contador_estabilidade = 0
                        letra_candidata = None
                else:
                    contador_estabilidade = 0
            
            elif letra_detectada == "\b":
                if erro < LIMIAR_ERRO_COMANDO:
                    contador_estabilidade += 1
                    if contador_estabilidade >= FRAMES_CONFIRMACAO_COMANDO:
                        tempo_agora = time.time()
                        if tempo_agora - ultimo_tempo_backspace >= DELAY_BACKSPACE:
                            print("⌨️ COMANDO EXECUTADO: BACKSPACE")
                            falador.processar_comando("\b")
                            ultimo_tempo_backspace = tempo_agora
                        contador_estabilidade = 0
                        letra_candidata = None
                else:
                    contador_estabilidade = 0
                        
            elif letra_detectada == "\u0000":
                if erro < LIMIAR_ERRO_COMANDO:
                    contador_estabilidade += 1
                    if contador_estabilidade >= FRAMES_CONFIRMACAO_COMANDO:
                        tempo_agora = time.time()
                        if tempo_agora - ultimo_tempo_backspace >= DELAY_BACKSPACE:
                            print("⌨️ COMANDO EXECUTADO: DELETE")
                            falador.processar_comando("\u0000")
                            ultimo_tempo_backspace = tempo_agora
                        contador_estabilidade = 0
                        letra_candidata = None
                else:
                    contador_estabilidade = 0
                        
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
                    # OU se for IGUAL mas houve movimento significativo da mão (acima do limiar mínimo)
                    elif letra_detectada != ultima_letra_confirmada:
                        resultado = falador.processar_comando(letra_detectada)
                        print(f"📝 Frase: {resultado}")
                        ultima_letra_confirmada = letra_detectada
                        posicao_mao_anterior = None  # Reseta posição para próximo movimento
                    elif letra_detectada == ultima_letra_confirmada and movimento_detectado:
                        # Verifica se o movimento foi significativo (acima do limiar mínimo)
                        if posicao_mao_anterior and calcular_distancia_euclidiana(pulso_atual, posicao_mao_anterior) > LIMIAR_MOVIMENTO_MINIMO:
                            resultado = falador.processar_comando(letra_detectada)
                            print(f"📝 Frase: {resultado} (repetido por movimento)")
                            posicao_mao_anterior = None
            else:
                contador_estabilidade = 0
                letra_candidata = None
                

    # 1. Obter a frase atual que está sendo construída
    frase_atual = falador.formarFrase()

    # 2. Desenhar um fundo (retângulo) para melhorar a legibilidade
    cv2.rectangle(camera.frame, (10, 10), (630, 60), (0, 0, 0), -1)

    # 3. Escrever o texto da frase no frame da câmera
    cv2.putText(
        camera.frame, 
        f"Frase: {frase_atual}", 
        (20, 45), 
        cv2.FONT_HERSHEY_SIMPLEX, 
        1, 
        (255, 255, 255), 
        2
    )

    # Exibe frame e verifica tecla
    tecla = camera.exibir_frame("Sistema LIBRAS - Estabilidade e Movimento")
    if tecla == 27:  # ESC
        camera.fechar()
        runpy.run_module("main", run_name="__main__")

# Fecha recursos
camera.fechar()
