import cv2
import json
import os
from src.mao import DetectorMao
from src.gestos import Gestos

def salvar_no_json(letra, dados, caminho_arquivo='dados/alfabeto.json'):
    # Carrega o arquivo existente ou cria um novo
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, 'r') as f:
            alfabeto = json.load(f)
    else:
        alfabeto = {}

    # Atualiza a letra com os novos dados de calibração
    alfabeto[letra.upper()] = dados
    
    with open(caminho_arquivo, 'w') as f:
        json.dump(alfabeto, f, indent=2)
    print(f"✅ Letra {letra.upper()} calibrada e salva com sucesso!")

detector = DetectorMao()
gestos = Gestos()
cap = cv2.VideoCapture(0)

print("\n--- MODO DE CALIBRAÇÃO ---")
print("1. Olhe para a tabela de LIBRAS.")
print("2. Faça o sinal em frente à câmera.")
print("3. Digite a letra correspondente no teclado para salvar.")
print("4. Pressione 'ESC' para sair.\n")

while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    frame = cv2.flip(frame, 1)
    res = detector.processar(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    if res.multi_hand_landmarks:
        for hand_landmarks in res.multi_hand_landmarks:
            detector.desenhar(frame, hand_landmarks)
            
            # Captura a tecla pressionada
            key = cv2.waitKey(1) & 0xFF
            
            if key == 27: # ESC para sair
                cap.release()
                cv2.destroyAllWindows()
                exit()
            elif 97 <= key <= 122 or 65 <= key <= 90: # Se for uma letra (A-Z)
                letra = chr(key).upper()
                features = gestos.extrair_features(hand_landmarks.landmark)
                if features:
                    salvar_no_json(letra, features)

    cv2.imshow("Calibrador - Siga a Tabela", frame)
    if cv2.waitKey(1) & 0xFF == 27: break

cap.release()
cv2.destroyAllWindows()