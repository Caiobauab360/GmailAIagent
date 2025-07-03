# 🍎 Guia de Instalação para Mac

## ⚡ Instalação Rápida (Recomendado)

### 1. Abra o Terminal
- Pressione `Cmd + Space` e digite "Terminal"
- Ou vá em `Aplicativos > Utilitários > Terminal`

### 2. Execute o instalador automático
```bash
curl -fsSL https://raw.githubusercontent.com/Caiobauab360/GmailAIagent/main/install_mac.sh | bash
```

### 3. Ou clone e execute manualmente
```bash
git clone https://github.com/Caiobauab360/GmailAIagent.git
cd GmailAIagent
chmod +x install_mac.sh
./install_mac.sh
```

---

## 🔧 Configuração

### 1. Google Cloud Console
- Acesse: https://console.cloud.google.com/
- Crie um projeto
- Ative: **Gmail API** e **Google Calendar API**
- Crie credenciais OAuth 2.0 → Baixe `credentials.json`

### 2. Gemini API
- Acesse: https://makersuite.google.com/app/apikey
- Crie uma API Key

### 3. Configure as credenciais
```bash
# Coloque o credentials.json na pasta do projeto
cp ~/Downloads/credentials.json GmailAIagent/

# Configure a API Key
export GEMINI_API_KEY="sua_chave_aqui"
```

---

## 🚀 Como Usar

### Teste a instalação
```bash
cd GmailAIagent
python3 -m gmail_ai_assistant.cli setup
```

### Análise completa
```bash
python3 -m gmail_ai_assistant.cli analyze
```

### Listar e-mails
```bash
python3 -m gmail_ai_assistant.cli emails --max 5
```

### Listar eventos
```bash
python3 -m gmail_ai_assistant.cli events --max 5
```

---

## 🆘 Solução de Problemas

### Erro: "command not found: python3"
```bash
# Instalar Python via Homebrew
brew install python
```

### Erro: "command not found: brew"
```bash
# Instalar Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Erro de permissão
```bash
# Dar permissão de execução
chmod +x install_mac.sh
```

### Primeira execução
- Será necessário autorizar o acesso ao Google
- Uma janela do navegador abrirá para login

---

## 📞 Suporte

- **Documentação**: README.md
- **Comando de Ajuda**: `python3 -m gmail_ai_assistant.cli setup`
- **Repositório**: https://github.com/Caiobauab360/GmailAIagent

---

**🎉 Pronto! Seu assistente de IA está funcionando no Mac!** 