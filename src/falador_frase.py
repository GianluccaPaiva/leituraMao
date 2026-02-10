import asyncio
import edge_tts
import tempfile
import os
import pygame
import time

class Falador:
    def __init__(self, alfabeto):
        self.alfabeto = alfabeto
        self.letras_da_frase = []
        self.voice = "pt-BR-AntonioNeural"  # Voz em português
        self.rate = "+0%"  # Velocidade neutra
        # Inicializa pygame mixer para reproduzir MP3
        pygame.mixer.init()

    def calcular_distancia(self, mao, caracteristicas):
        # Garante o uso do erro quadrático para precisão
        return sum((mao[k] - caracteristicas[k]) ** 2 for k in caracteristicas if k in mao)

    async def _falar_async(self, frase):
        """Realiza a síntese de fala de forma assíncrona"""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp_path = tmp.name
        
        try:
            communicate = edge_tts.Communicate(frase, self.voice, rate=self.rate)
            await communicate.save(tmp_path)
            
            # Reproduz o MP3 usando pygame
            pygame.mixer.music.load(tmp_path)
            pygame.mixer.music.play()
            
            # Aguarda a música terminar
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
        finally:
            # Remove o arquivo temporário
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def falar(self, frase):
        """Wrapper síncrono para falar"""
        try:
            asyncio.run(self._falar_async(frase))
        except Exception as e:
            print(f"❌ Erro ao falar: {e}")

    def processar_comando(self, comando):
        if comando == "ENTER":
            frase = self.formarFrase()
            if frase.strip():
                print(f"📢 Falando: {frase}")
                self.falar(frase)
            
            self.letras_da_frase = [] # Zerar o array após falar
            return "FRASE_ENVIADA"

        elif comando == "ESPACO":
            self.letras_da_frase.append(" ")
        elif comando == "\b":
            if len(self.letras_da_frase) > 0:
                self.letras_da_frase.pop()
        elif comando == "\u0000":
            self.letras_da_frase = []
        else:
            self.letras_da_frase.append(comando)
            
        return self.formarFrase()

    def formarFrase(self):
        return ''.join(self.letras_da_frase)