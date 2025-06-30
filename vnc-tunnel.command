#!/bin/bash

THIS_FILE=$(basename "$0")
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

export LANG=en_US.UTF-8

cd "$SCRIPT_DIR" || { echo "Falha ao acessar o diretório do script."; exit 1; }

clear

echo "Pasta atual: $(pwd)"
echo "Abertura de conexão VNC..."
echo ""

if command -v python3 &>/dev/null; then
    python3 ssh_Tunnel_v2.py
elif command -v python &>/dev/null; then
    python ssh_Tunnel_v2.py
else
    echo "Python não encontrado. Instale o Python para continuar."
    exit 1
fi

read -n 1 -s -r -p "Pressione qualquer tecla para sair..."
echo ""

# Fechar janela do Terminal (apenas no macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    osascript -e 'tell application "Terminal" to close (every window whose name contains "'"$THIS_FILE"'")' &
fi

exit