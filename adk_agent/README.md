# Agente de IA para Gmail e Calendar (ADK)

Este projeto implementa um agente de IA usando o **Agent Development Kit (ADK) do Google** para ler e-mails do Gmail, resumi-los com Gemini e acessar o Google Calendar.

## 🚀 Vantagens do ADK

- **Estrutura padronizada** para agentes de IA
- **Integração nativa** com modelos Google (Gemini)
- **Sistema de ferramentas (Tools)** organizado
- **Memória persistente** para conversas
- **Facilidade de deploy** e escalabilidade

## 📁 Estrutura do Projeto

```
adk_agent/
├── main.py              # Agente principal usando ADK
├── requirements.txt     # Dependências específicas do ADK
└── README.md           # Este arquivo
```

## 🛠️ Instalação

1. **Instalar dependências:**
   ```bash
   cd adk_agent
   pip install -r requirements.txt
   ```

2. **Configurar credenciais:**
   - Copie o `credentials.json` para a pasta pai (`../credentials.json`)
   - Ou ajuste o caminho no `main.py`

## 🎯 Como Usar

```bash
python main.py
```

## 🔧 Funcionalidades

### Ferramentas (Tools) Implementadas:

1. **GmailTool** - Lê e-mails da caixa de entrada
2. **CalendarTool** - Acessa eventos do Google Calendar

### Recursos do ADK:

- **Modelo Gemini Pro** integrado
- **Sistema de memória** para contexto
- **Interface padronizada** para ferramentas
- **Tratamento de erros** robusto

## 🔄 Diferenças da Versão ADK

| Aspecto | Versão Simples | Versão ADK |
|---------|----------------|------------|
| Estrutura | Script único | Framework organizado |
| Ferramentas | Funções simples | Classes Tool padronizadas |
| Modelo IA | Configuração manual | Integração nativa |
| Memória | Não | Sistema de memória |
| Escalabilidade | Limitada | Alta |

## 🚀 Próximos Passos

- Adicionar mais ferramentas (enviar e-mails, criar eventos)
- Implementar interface web
- Adicionar análise de sentimento
- Integrar com outros serviços Google

## 📚 Documentação ADK

- [Agent Development Kit](https://github.com/google/agent-development-kit)
- [Google AI Studio](https://makersuite.google.com/)
- [Google Cloud APIs](https://console.cloud.google.com/) 