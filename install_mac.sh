#!/bin/bash

echo "🍎 Gmail AI Assistant - Instalador para Mac"
echo "=========================================="
echo

# Verificar se o Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado!"
    echo "📦 Instalando Python via Homebrew..."
    
    if ! command -v brew &> /dev/null; then
        echo "❌ Homebrew não encontrado!"
        echo "📦 Instalando Homebrew primeiro..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    
    brew install python
    echo "✅ Python instalado!"
else
    echo "✅ Python 3 encontrado: $(python3 --version)"
fi

# Verificar se o Git está instalado
if ! command -v git &> /dev/null; then
    echo "❌ Git não encontrado!"
    echo "📦 Instalando Git via Homebrew..."
    brew install git
    echo "✅ Git instalado!"
else
    echo "✅ Git encontrado: $(git --version)"
fi

echo
echo "📥 Baixando o projeto..."
if [ -d "GmailAIagent" ]; then
    echo "📁 Pasta já existe, atualizando..."
    cd GmailAIagent
    git pull
else
    git clone https://github.com/Caiobauab360/GmailAIagent.git
    cd GmailAIagent
fi

echo
echo "📦 Instalando dependências..."
pip3 install -r requirements.txt

echo
echo "🔧 Instalando CLI..."
pip3 install -e .

echo
echo "✅ Instalação concluída!"
echo
echo "🔧 PRÓXIMOS PASSOS:"
echo "1. Configure suas credenciais:"
echo "   - Baixe credentials.json do Google Cloud Console"
echo "   - Coloque na pasta GmailAIagent"
echo "   - Configure GEMINI_API_KEY"
echo
echo "2. Teste a instalação:"
echo "   python3 -m gmail_ai_assistant.cli setup"
echo
echo "3. Use o CLI:"
echo "   python3 -m gmail_ai_assistant.cli analyze"
echo
echo "📖 Para mais informações, veja o README.md" 