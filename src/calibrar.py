import cv2
import json
import os
from src.mao import DetectorMao
from src.gestos import Gestos

def salvar_no_json(letra, dados, caminho_arquivo='dados/alfabeto.json'):
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, 'r') as f:
            alfabeto = json.load(f)
    else:
        alfabeto = {}

    alfabeto[letra.upper()] = dados
    
    with open(caminho_arquivo, 'w') as f:
        json.dump(alfabeto, f, indent=2)
    print(f"✅ Sinal '{letra.upper()}' calibrado e salvo!")

detector = DetectorMao()
gestos = Gestos()
cap = cv2.VideoCapture(0)

print("\n--- MODO DE CALIBRAÇÃO EXPANDIDO ---")
print("1. Faça o sinal (ex: Positivo para ENTER).")
print("2. Pressione a tecla desejada para mapear este sinal.")
print("3. Pressione 'ESC' para sair.\n")

while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    frame = cv2.flip(frame, 1)
    res = detector.processar(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    if res.multi_hand_landmarks:
        for hand_landmarks in res.multi_hand_landmarks:
            detector.desenhar(frame, hand_landmarks)
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == 27: # ESC
                cap.release()
                cv2.destroyAllWindows()
                exit()
            elif key != 255: # Qualquer outra tecla
                if key == 32:
                    nome_sinal = "ESPACO"
                elif key == 13:
                    nome_sinal = "ENTER"
                else:
                    nome_sinal = chr(key).upper()
                
                features = gestos.extrair_features(hand_landmarks.landmark)
                if features:
                    salvar_no_json(nome_sinal, features)

    cv2.imshow("Calibrador - Qualquer Tecla", frame)