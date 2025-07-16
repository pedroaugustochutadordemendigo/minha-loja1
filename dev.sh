#!/bin/bash

# Script de desenvolvimento do projeto PACKS E-commerce
echo "🚀 Iniciando ambiente de desenvolvimento..."

# Verificar se está no diretório correto
if [ ! -f "README.md" ]; then
    echo "❌ Execute este script a partir do diretório raiz do projeto"
    exit 1
fi

# Função para cleanup ao sair
cleanup() {
    echo ""
    echo "🛑 Parando servidores..."
    kill $(jobs -p) 2>/dev/null
    exit 0
}

# Capturar sinais para cleanup
trap cleanup SIGINT SIGTERM

# Iniciar backend
echo "🐍 Iniciando backend..."
cd backend

# Ativar ambiente virtual se existir
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Iniciar backend em background
python run.py &
BACKEND_PID=$!

cd ..

# Aguardar um pouco para o backend inicializar
sleep 3

# Iniciar frontend
echo "🎨 Iniciando frontend..."
cd frontend

# Iniciar frontend em background
npm run dev -- --host &
FRONTEND_PID=$!

cd ..

echo ""
echo "✅ Servidores iniciados!"
echo "🌐 Frontend: http://localhost:5173"
echo "🔧 Backend:  http://localhost:5000"
echo ""
echo "💡 Pressione Ctrl+C para parar os servidores"

# Aguardar os processos
wait

