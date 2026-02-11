# Guia de Configurações Otimizadas para Detecção de Mãos

## Melhorias Implementadas

### 1. MediaPipe (config.json)
- **min_detection_confidence**: 0.3 → 0.6
  - Detecção mais rigorosa, reduz falsos positivos
  
- **min_tracking_confidence**: 0.3 → 0.6  
  - Rastreamento mais estável e preciso

### 2. Estabilidade de Letras (config.json)
- **limite_estabilidade**: 12 → 18 frames
  - Requer mais confirmação para aceitar uma letra
  - Reduz tremores acidentais

- **limiar_erro_estrito**: 0.18 → 0.16
  - Mais exigente com a precisão dos gestos

### 3. Detecção de Movimento (config.json)
- **limiar_movimento_mao**: 0.05 → 0.07
  - Menos sensível a micro-movimentos involuntários
  
- **limiar_movimento_minimo**: 0.08 (novo)
  - Garante que movimento para repetição seja intencional

### 4. Comandos Especiais (config.json)
- **limiar_erro_comando**: 0.12 (novo)
  - Limiares mais rigorosos para ENTER, ESPAÇO, BACKSPACE
  
- **frames_confirmacao_comando**: 25 (novo)
  - Requer 25 frames consecutivos para confirmar comando
  - Evita acionamentos acidentais

- **delay_backspace**: 1.0 → 1.2 segundos
  - Intervalo maior entre backspaces

## Ajustes para Sua Necessidade

Se ainda precisar de mais precisão, você pode:

### Para Detecção Mais Rigorosa:
```json
{
  "mediapipe": {
    "min_detection_confidence": 0.7,
    "min_tracking_confidence": 0.7
  },
  "libras": {
    "limite_estabilidade": 22,
    "limiar_erro_estrito": 0.14
  }
}
```

### Para Detecção Mais Rápida (menos precisa):
```json
{
  "mediapipe": {
    "min_detection_confidence": 0.5,
    "min_tracking_confidence": 0.5
  },
  "libras": {
    "limite_estabilidade": 14,
    "limiar_erro_estrito": 0.18,
    "frames_confirmacao_comando": 20
  }
}
```

## Como Testar

Execute `main.py` com opção 2 - Reconhecimento
Observe se há melhorias em:
- [ ] Menos falsos positivos
- [ ] Detecção mais estável
- [ ] Repetição de letras apenas com movimento intencional
- [ ] Menos erros em comandos
