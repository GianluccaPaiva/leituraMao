import pyttsx3

class Falador:
    def __init__(self, alfabeto):
        self.alfabeto = alfabeto
        self.letras_da_frase = []
        # Inicializa o motor uma única vez
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 1.0)

    def calcular_distancia(self, mao, caracteristicas):
        # Garante o uso do erro quadrático para precisão
        return sum((mao[k] - caracteristicas[k]) ** 2 for k in caracteristicas if k in mao)

    def processar_comando(self, comando):
        if comando == "ENTER":
            frase = self.formarFrase()
            if frase.strip():
                print(f"📢 Falando: {frase}")
                
                # Correção: Forçar o processamento da fala
                if self.engine._inLoop:
                    self.engine.endLoop()
                
                self.engine.say(frase)
                self.engine.runAndWait()
            
            self.letras_da_frase = [] # Zerar o array após falar
            return "FRASE_ENVIADA"

        elif comando == "ESPACO":
            self.letras_da_frase.append(" ")
        elif comando == "BACKSPACE":
            if len(self.letras_da_frase) > 0:
                self.letras_da_frase.pop()
        else:
            self.letras_da_frase.append(comando)
            
        return self.formarFrase()

    def formarFrase(self):
        return ''.join(self.letras_da_frase)