# 🚀 Guia de Início Rápido - Gmail AI Assistant

## ⚡ Instalação Rápida

### Windows
```bash
# Execute o instalador
install.bat
```

### Linux/Mac
```bash
# Torne o script executável e execute
chmod +x install.sh
./install.sh
```

## 🔧 Configuração (5 minutos)

### 1. Google Cloud Console
- Acesse: https://console.cloud.google.com/
- Crie um projeto
- Ative: **Gmail API** e **Google Calendar API**
- Crie credenciais OAuth 2.0 → Baixe `credentials.json`

### 2. Gemini API
- Acesse: https://makersuite.google.com/app/apikey
- Crie uma API Key
- Configure: `export GEMINI_API_KEY="sua_chave"`

### 3. Arquivos
- Coloque `credentials.json` na pasta do projeto

## 🎯 Uso Básico

### Análise Completa
```bash
python -m gmail_ai_assistant.cli analyze
```

### Listar E-mails
```bash
python -m gmail_ai_assistant.cli emails --max 5
```

### Listar Eventos
```bash
python -m gmail_ai_assistant.cli events --max 5
```

### Ajuda
```bash
python -m gmail_ai_assistant.cli setup
```

## 💡 Exemplos Práticos

### Análise Diária
```bash
python -m gmail_ai_assistant.cli analyze "Resuma meu dia e priorize tarefas"
```

### E-mails Urgentes
```bash
python -m gmail_ai_assistant.cli analyze --emails 10 "Identifique e-mails urgentes"
```

### Planejamento Semanal
```bash
python -m gmail_ai_assistant.cli analyze --events 10 "Analise minha semana"
```

## 🆘 Solução de Problemas

### Erro de Credenciais
- Verifique se `credentials.json` está na pasta
- Confirme se as APIs estão ativadas no Google Cloud

### Erro de API Key
- Verifique se `GEMINI_API_KEY` está configurada
- Use: `--api-key "sua_chave"` no comando

### Primeira Execução
- Será necessário autorizar o acesso ao Google
- Uma janela do navegador abrirá para login

## 📞 Suporte

- **Documentação**: README.md
- **Comando de Ajuda**: `python -m gmail_ai_assistant.cli setup`
- **Versão**: `python -m gmail_ai_assistant.cli --version`

---

**🎉 Pronto! Seu assistente de IA está funcionando!** 