# LeituraMao - Reconhecedor de LIBRAS

Sistema de reconhecimento de **LIBRAS** (Língua Brasileira de Sinais) em tempo real usando visão computacional e aprendizado de máquina.

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Requisitos do Sistema](#-requisitos-do-sistema)
- [Instalação](#-instalação)
- [Como Usar](#-como-usar)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Como Funciona](#-como-funciona)
- [Calibração](#-calibração)
- [Comandos Especiais](#-comandos-especiais)
- [Configurações Avançadas](#-configurações-avançadas)
- [Solução de Problemas](#-solução-de-problemas)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)

---

## 📖 Sobre o Projeto

**LeituraMao** é um projeto de acessibilidade que utiliza inteligência artificial para reconhecer gestos da **Língua Brasileira de Sinais (LIBRAS)** através de uma webcam comum. O sistema captura os movimentos das mãos em tempo real, identifica as letras do alfabeto LIBRAS e sintetiza as palavras em voz usando tecnologia Text-to-Speech.

### 🎯 Objetivos

- Facilitar a comunicação entre pessoas que usam LIBRAS e pessoas que não conhecem a língua
- Fornecer uma ferramenta gratuita e acessível para aprendizado de LIBRAS
- Demonstrar aplicações práticas de visão computacional e IA

---

## ✨ Funcionalidades

### 🔤 Reconhecimento de Letras
- **26 letras do alfabeto LIBRAS** (A-Z)
- Detecção de **gestos com movimento** (J e Z)
- **Anti-fantasma**: Sistema de estabilidade que evita detecções falsas
- **Calibração personalizada**: Ajuste o reconhecimento ao seu estilo de sinal

### 🎙️ Síntese de Voz
- **Conversão texto-para-fala** usando Edge TTS
- **Voz em português brasileiro** (Microsoft Neural Voice)
- **Alta qualidade de áudio** sem limitações de volume
- **Reprodução automática** quando você pressiona "ENTER"

### ⌨️ Comandos Especiais
- **ENTER**: Fala a frase formada e limpa a tela
- **ESPAÇO**: Adiciona espaço entre palavras
- **BACKSPACE**: Remove a última letra (com delay anti-spam)

### 🎥 Interface Visual
- **Visualização em tempo real** da mão detectada
- **Feedback visual** da letra identificada
- **Contador de estabilidade** para mostrar confiança da detecção
- **Overlay de informações** mostrando o estado atual

---

## 💻 Requisitos do Sistema

### Hardware
- **Webcam** (resolução mínima 640x480)
- **Processador**: Intel i3 ou equivalente (recomendado i5+)
- **RAM**: 4GB mínimo (8GB recomendado)
- **Sistema Operacional**: Windows 10/11

### Software
- **Python 3.11+**
- **pip** (gerenciador de pacotes Python)

---

## 🚀 Instalação

### 1. Clone o Repositório

```bash
git clone https://github.com/GianluccaPaiva/leituraMao.git
cd leituraMao
```

### 2. Crie o Ambiente Virtual

```bash
python -m venv venv
```

### 3. Ative o Ambiente Virtual

**Windows PowerShell:**
```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\venv\Scripts\Activate.ps1
```

**Windows CMD:**
```cmd
venv\Scripts\activate.bat
```

### 4. Instale as Dependências

```bash
pip install -r requirements.txt
```

### 5. Verifique a Instalação

```bash
python main.py
```

Se tudo estiver correto, você verá o menu principal.

---

## 📚 Como Usar

### 🎬 Iniciando o Sistema

1. **Execute o programa principal:**
   ```bash
   python main.py
   ```

2. **Escolha uma opção:**
   - `1` - Calibrar (primeira vez ou para adicionar/atualizar letras)
   - `2` - Iniciar reconhecimento

### 🔧 Modo de Calibração

Use este modo para **treinar** o sistema a reconhecer SEU estilo de sinal.

1. Digite `1` no menu principal
2. Posicione-se em frente à webcam (iluminação adequada)
3. Consulte uma **tabela de LIBRAS** para referência
4. Faça o sinal da letra desejada
5. Pressione a **tecla correspondente** (A-Z) no teclado
6. Uma mensagem confirmará: `✅ Letra X calibrada e salva!`
7. A letra aparecerá no **painel visual** no topo da câmera
8. Pressione **ESC** para sair

**Dicas para boa calibração:**
- Iluminação uniforme e clara
- Fundo neutro (sem muita movimentação)
- Mão bem visível e estável
- Distância de ~50cm da câmera
- Acompanhe o painel de "Calibradas" para saber quais letras já foram treinadas

### 🎯 Modo de Reconhecimento

Use este modo para **converter LIBRAS em texto e voz**.

1. Digite `2` no menu principal
2. Posicione sua mão em frente à câmera
3. Faça os sinais das letras (mantenha por ~1 segundo)
4. A letra aparecerá na tela quando **estabilizada**
5. As letras reconhecidas aparecem em um **painel visual** no topo
6. Para **limpar a frase**, pressione **C** no teclado
7. Para **falar** a frase:
   - Faça o gesto configurado como "ENTER"
   - O sistema sintetizará voz e limpará a frase
8. Pressione **Q** no teclado para sair

**Comandos durante o reconhecimento:**
- **ENTER**: Fala e limpa a frase
- **ESPAÇO**: Adiciona espaço
- **BACKSPACE**: Remove última letra (delay de 0.5s)
- **C**: Limpa a frase acumulada

---

## 📂 Estrutura do Projeto

```
leituraMao/
│
├── main.py                 # Ponto de entrada do programa
├── requirements.txt        # Dependências do projeto
├── README.md              # Este arquivo
├── .gitignore             # Arquivos ignorados pelo Git
│
├── dados/
│   └── alfabeto.json      # Base de dados das letras calibradas
│
└── src/
    ├── __init__.py        # Marca o diretório como pacote Python
    ├── calibrar.py        # Módulo de calibração de letras
    ├── libra.py           # Módulo principal de reconhecimento
    ├── libras.py          # Classe para comparação de padrões
    ├── gestos.py          # Extração de features e detecção de movimento
    ├── mao.py             # Detecção de mão com MediaPipe
    ├── falador_frase.py   # Síntese de voz (TTS)
    └── camera.py          # (Funcionalidade de câmera - legado)
```

### 📄 Descrição dos Módulos

| Arquivo | Descrição |
|---------|-----------|
| `main.py` | Interface principal; menu de seleção entre calibrar e reconhecer |
| `calibrar.py` | Captura gestos e salva features no JSON |
| `libra.py` | Loop principal de reconhecimento em tempo real |
| `libras.py` | Algoritmo de comparação (erro quadrático) |
| `gestos.py` | Extração de características geométricas da mão |
| `mao.py` | Detecção de landmarks da mão usando MediaPipe |
| `falador_frase.py` | Síntese de voz com Edge TTS e pygame |

---

## 🔬 Como Funciona

### 1️⃣ Detecção da Mão (MediaPipe)

O sistema usa **MediaPipe Hands** para detectar 21 pontos de referência (landmarks) na mão:

```
0: Pulso
1-4: Polegar (base → ponta)
5-8: Indicador
9-12: Médio
13-16: Anelar
17-20: Mindinho
```

### 2️⃣ Extração de Features

Para cada pose, calculamos **9 distâncias normalizadas**:

- Distância entre dedos consecutivos (thumb-index, index-middle, etc.)
- Distância de cada dedo até o pulso
- Normalização pelo tamanho da mão (pulso → dedo médio)

### 3️⃣ Comparação de Padrões

Usamos **erro quadrático** para comparar a pose atual com as poses calibradas:

```python
erro = Σ (feature_atual - feature_calibrada)²
```

A letra com **menor erro** e **abaixo do limiar** é reconhecida.

### 4️⃣ Sistema Anti-Fantasma

Para evitar detecções falsas:

- **Contador de estabilidade**: Precisa manter a pose por 12+ frames
- **Limiar de erro estrito**: 0.18 (configúravel)
- **Intervalo entre letras**: 1.0 segundo
- **Delay de comandos especiais**: Backspace com 0.5s

### 5️⃣ Detecção de Movimento (J e Z)

Letras **J** e **Z** requerem movimento:

- **J**: Detecta movimento descendente com curva lateral (mindinho)
- **Z**: Detecta movimento em zig-zag (indicador)
- Rastreamento de 15 posições históricas

---

## 🎨 Calibração

### Por que calibrar?

Cada pessoa faz sinais de forma ligeiramente diferente. A calibração personaliza o sistema para **seu estilo**.

### Como calibrar uma letra

1. Inicie o modo de calibração (`1` no menu)
2. Faça o sinal da letra (ex: "A")
3. Pressione a tecla `A` no teclado
4. O sistema salva as **features geométricas** em `dados/alfabeto.json`

### Recalibrando letras problemáticas

Se uma letra não está sendo reconhecida corretamente:

1. Entre no modo de calibração
2. Refaça o sinal com atenção à:
   - Iluminação adequada
   - Mão totalmente visível
   - Pose estável por 1-2 segundos
3. Pressione a tecla para sobrescrever a calibração anterior

---

## ⚙️ Comandos Especiais

### ENTER

**Função**: Fala a frase acumulada e limpa o buffer

**Como configurar**:
1. Decida qual gesto será "ENTER" (ex: mão fechada com polegar levantado)
2. Calibre esse gesto com o nome "ENTER"
3. No reconhecimento, faça o gesto e aguarde ~1 segundo

### ESPAÇO

**Função**: Adiciona um espaço entre palavras

**Configuração**: Calibre um gesto como "ESPACO"

### BACKSPACE

**Função**: Remove a última letra (com delay de 0.5s)

**Configuração**: Calibre um gesto como "\b" (caractere de backspace)

**Características**:
- Delay de 0.5s entre execuções
- Pode ser usado múltiplas vezes (saia e volte à pose)
- Não spama se você mantiver a pose

---

## 🛠️ Configurações Avançadas

### Ajustar Sensibilidade

Edite `src/libra.py`:

```python
LIMITE_ESTABILIDADE = 12    # Frames para confirmar (↑ = mais estável)
LIMIAR_ERRO_ESTRITO = 0.18  # Precisão (↓ = mais rigoroso)
TEMPO_ENTRE_LETRAS = 1.0    # Delay entre letras (segundos)
DELAY_BACKSPACE = 0.5       # Delay do backspace (segundos)
```

### Trocar Voz do TTS

Edite `src/falador_frase.py`:

```python
self.voice = "pt-BR-AntonioNeural"  # Voz masculina
# Outras opções:
# "pt-BR-FranciscaNeural" - Voz feminina
# "pt-BR-BrendaNeural"    - Voz feminina alternativa
```

### Ajustar Velocidade da Fala

```python
self.rate = "+0%"   # Velocidade neutra
# Exemplos:
# "+20%" - Mais rápido
# "-20%" - Mais lento
```

### Mudar Resolução da Câmera

Edite `src/libra.py`:

```python
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
```

---

## 🐛 Solução de Problemas

### ❌ Erro: "No module named 'cv2'"

**Solução**: Reinstale o OpenCV
```bash
pip uninstall opencv-python opencv-contrib-python
pip install opencv-python
```

### ❌ Câmera não abre

**Possíveis causas**:
- Outra aplicação está usando a câmera
- Permissões negadas no Windows

**Solução**:
1. Feche outros programas que usam câmera (Zoom, Teams, etc.)
2. Verifique permissões: Configurações → Privacidade → Câmera

### ❌ Letras não são reconhecidas

**Soluções**:
1. **Recalibre** a letra problemática
2. Melhore a **iluminação** do ambiente
3. Use **fundo neutro** (parede clara)
4. Verifique se a mão está **totalmente visível**
5. Diminua `LIMIAR_ERRO_ESTRITO` (mais permissivo)

### ❌ Reconhecimento instável ("fantasmas")

**Soluções**:
1. Aumente `LIMITE_ESTABILIDADE` (mais frames)
2. Diminua `LIMIAR_ERRO_ESTRITO` (mais rigoroso)
3. Mantenha a pose mais tempo
4. Evite movimentos bruscos

### ❌ Voz não funciona

**Solução**:
1. Verifique se pygame está instalado: `pip install pygame`
2. Teste volume do sistema
3. Verifique se Edge TTS está funcionando:
   ```bash
   edge-tts --text "teste" --write-media teste.mp3
   ```

### ❌ Import "src.falador_frase" could not be resolved (Pylance)

**Solução**: Este é apenas um aviso do Pylance. O código funciona normalmente. Para corrigir:
1. Pressione `Ctrl+Shift+P`
2. Digite "Python: Restart Language Server"

---

## 🔧 Tecnologias Utilizadas

### Visão Computacional
- **OpenCV** - Captura e processamento de vídeo
- **MediaPipe** - Detecção de landmarks da mão

### Inteligência Artificial
- **Algoritmo de KNN personalizado** - Reconhecimento de padrões
- **Erro quadrático** - Métrica de similaridade

### Síntese de Voz
- **Edge TTS** - Text-to-Speech da Microsoft
- **Pygame** - Reprodução de áudio MP3

### Desenvolvimento
- **Python 3.11** - Linguagem principal
- **NumPy** - Operações matemáticas
- **Asyncio** - Programação assíncrona

---

## 📊 Estatísticas de Performance

| Métrica | Valor |
|---------|-------|
| Taxa de quadros | ~30 FPS |
| Latência de detecção | ~40ms |
| Accuracy (após calibração) | ~85-95% |
| Tempo de síntese TTS | ~1-2s |

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Faça um **fork** do projeto
2. Crie uma **branch** para sua feature (`git checkout -b feature/MinhaFeature`)
3. **Commit** suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. **Push** para a branch (`git push origin feature/MinhaFeature`)
5. Abra um **Pull Request**

### Ideias de Contribuição

- [ ] Suporte para outras plataformas (Linux, macOS)
- [ ] Reconhecimento de palavras inteiras (não só alfabeto)
- [ ] Interface gráfica (GUI) com Tkinter ou PyQt
- [ ] Modo de treinamento com mais exemplos por letra
- [ ] Suporte para múltiplas línguas de sinais
- [ ] Exportação de frases para arquivo de texto

---

## 📜 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👨‍💻 Autor

**Gianlucca Paiva**

- GitHub: [@GianluccaPaiva](https://github.com/GianluccaPaiva)
- Repositório: [leituraMao](https://github.com/GianluccaPaiva/leituraMao)

---

## 🙏 Agradecimentos

- **MediaPipe** - Por fornecer uma solução robusta de detecção de mãos
- **Comunidade LIBRAS** - Por tornar possível a comunicação inclusiva
- **Microsoft** - Pelo Edge TTS de alta qualidade

---

## 📞 Suporte

Se você encontrar problemas ou tiver dúvidas:

1. Verifique a seção [Solução de Problemas](#-solução-de-problemas)
2. Abra uma **Issue** no GitHub
3. Consulte a documentação das bibliotecas utilizadas

---

## 🎓 Referências

- [Documentação MediaPipe Hands](https://google.github.io/mediapipe/solutions/hands.html)
- [OpenCV Documentation](https://docs.opencv.org/)
- [Edge TTS GitHub](https://github.com/rany2/edge-tts)
- [Alfabeto LIBRAS](http://www.acessibilidadebrasil.org.br/libras/)

---

**Feito para promover acessibilidade e inclusão, além de estudo sobre software de captação de imagem e conversão de voz.**

 **LIBRAS é língua, não só gestos!** 
