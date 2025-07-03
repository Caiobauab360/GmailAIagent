# 🤖 Gmail AI Assistant

Assistente de IA profissional para Gmail e Google Calendar que lê e-mails, resume conteúdo usando Gemini e gerencia eventos do calendário.

## ✨ Funcionalidades

- 📧 **Leitura de E-mails**: Acessa automaticamente sua caixa de entrada do Gmail
- 🧠 **Resumo Inteligente**: Usa Gemini para resumir e analisar e-mails
- 📅 **Gestão de Calendário**: Lista e analisa próximos eventos
- 🎯 **Análise Executiva**: Fornece insights e recomendações personalizadas
- 🖥️ **Interface CLI**: Comando simples e intuitivo para uso profissional

## 🚀 Instalação

### Opção 1: Instalação Local (Desenvolvimento)

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/gmail-ai-assistant.git
cd gmail-ai-assistant

# Instale as dependências
pip install -r requirements.txt

# Instale o CLI localmente
pip install -e .
```

### Opção 2: Instalação via PyPI (Futuro)

```bash
pip install gmail-ai-assistant
```

## ⚙️ Configuração

### 1. Google Cloud Console

1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um novo projeto
3. Ative as APIs:
   - Gmail API
   - Google Calendar API
4. Crie credenciais OAuth 2.0:
   - Tipo: Aplicativo para computador
   - Baixe o arquivo `credentials.json`

### 2. Gemini API

1. Acesse [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Crie uma API Key
3. Configure a variável de ambiente:
   ```bash
   export GEMINI_API_KEY="sua_chave_aqui"
   ```

## 📖 Como Usar

### Comando Principal

```bash
# Análise completa com IA
gmail-assistant analyze

# Com prompt personalizado
gmail-assistant analyze "Analise meus e-mails de trabalho e priorize as tarefas"

# Com opções personalizadas
gmail-assistant analyze --emails 5 --events 3 "Resuma minha semana"
```

### Comandos Específicos

```bash
# Listar e-mails recentes
gmail-assistant emails --max 10

# Listar próximos eventos
gmail-assistant events --max 5

# Guia de configuração
gmail-assistant setup
```

### Opções Disponíveis

```bash
# Ver todas as opções
gmail-assistant --help

# Ver opções de um comando específico
gmail-assistant analyze --help
```

## 🛠️ Exemplos de Uso

### Análise Diária
```bash
gmail-assistant analyze "Forneça um resumo executivo do meu dia e priorize minhas tarefas"
```

### Análise de E-mails de Trabalho
```bash
gmail-assistant analyze --emails 10 "Identifique e-mails urgentes e sugira ações"
```

### Planejamento Semanal
```bash
gmail-assistant analyze --events 10 "Analise meus compromissos da semana e sugira otimizações"
```

## 📁 Estrutura do Projeto

```
gmail-ai-assistant/
├── gmail_ai_assistant/          # Pacote principal
│   ├── __init__.py
│   ├── agent.py                 # Classe principal do agente
│   ├── tools.py                 # Ferramentas (Gmail, Calendar)
│   └── cli.py                   # Interface de linha de comando
├── setup.py                     # Configuração do pacote
├── requirements.txt             # Dependências
├── README.md                    # Este arquivo
└── credentials.json             # Suas credenciais Google
```

## 🔧 Desenvolvimento

### Instalação para Desenvolvimento

```bash
# Clone e instale em modo desenvolvimento
git clone https://github.com/seu-usuario/gmail-ai-assistant.git
cd gmail-ai-assistant
pip install -e .
```

### Executando Testes

```bash
# Teste básico
python -m gmail_ai_assistant.cli setup

# Teste com credenciais
gmail-assistant analyze --api-key "sua_chave"
```

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🆘 Suporte

- 📧 Email: seu.email@exemplo.com
- 🐛 Issues: [GitHub Issues](https://github.com/seu-usuario/gmail-ai-assistant/issues)
- 📖 Documentação: [Wiki](https://github.com/seu-usuario/gmail-ai-assistant/wiki)

## 🙏 Agradecimentos

- Google Cloud Platform pelas APIs
- Google Gemini pela IA
- Comunidade Python pelos pacotes utilizados

---

**Desenvolvido com ❤️ para tornar sua produtividade mais inteligente!** 