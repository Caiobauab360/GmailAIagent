#!/bin/bash

echo "========================================"
echo "   Gmail AI Assistant - Instalador"
echo "========================================"
echo

echo "[1/4] Instalando dependencias..."
pip install -r requirements.txt

echo
echo "[2/4] Instalando CLI..."
pip install -e .

echo
echo "[3/4] Verificando instalacao..."
python -m gmail_ai_assistant.cli --version

echo
echo "[4/4] Configuracao..."
echo
echo "Para usar o CLI, voce precisa:"
echo "1. Colocar o arquivo credentials.json na pasta atual"
echo "2. Configurar a API Key do Gemini:"
echo "   - Acesse: https://makersuite.google.com/app/apikey"
echo "   - Crie uma API Key"
echo "   - Configure a variavel de ambiente GEMINI_API_KEY"
echo "   export GEMINI_API_KEY='sua_chave_aqui'"
echo
echo "Exemplos de uso:"
echo "  python -m gmail_ai_assistant.cli analyze"
echo "  python -m gmail_ai_assistant.cli emails"
echo "  python -m gmail_ai_assistant.cli events"
echo "  python -m gmail_ai_assistant.cli setup"
echo
echo "Instalacao concluida!" 