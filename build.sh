#!/bin/bash

# Script de build do projeto PACKS E-commerce
echo "🏗️ Iniciando build do projeto..."

# Verificar se está no diretório correto
if [ ! -f "README.md" ]; then
    echo "❌ Execute este script a partir do diretório raiz do projeto"
    exit 1
fi

# Build do frontend
echo "🎨 Fazendo build do frontend..."
cd frontend

# Instalar dependências se necessário
if [ ! -d "node_modules" ]; then
    echo "📥 Instalando dependências do frontend..."
    npm install
fi

# Build do frontend
npm run build

if [ $? -ne 0 ]; then
    echo "❌ Erro no build do frontend"
    exit 1
fi

cd ..

# Copiar build do frontend para o backend
echo "📁 Copiando build para o backend..."
rm -rf backend/static
mkdir -p backend/static
cp -r frontend/dist/* backend/static/

# Configurar backend para produção
echo "🐍 Configurando backend para produção..."
cd backend

# Ativar ambiente virtual se existir
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Instalar dependências se necessário
if [ ! -d "venv" ] || [ ! -f "venv/bin/activate" ]; then
    echo "📥 Configurando ambiente Python..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
fi

cd ..

echo "✅ Build concluído!"
echo ""
echo "📋 Arquivos gerados:"
echo "  - frontend/dist/     - Build do frontend"
echo "  - backend/static/    - Frontend integrado ao backend"
echo ""
echo "🚀 Para executar em produção:"
echo "  cd backend && python run.py"

