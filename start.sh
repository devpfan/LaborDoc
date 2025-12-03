#!/bin/bash

echo "🚀 Iniciando Gestor de Labor Docente"
echo "===================================="
echo ""

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para verificar si un puerto está en uso
check_port() {
    lsof -i :$1 > /dev/null 2>&1
    return $?
}

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no está instalado"
    exit 1
fi

# Verificar si Node está instalado
if ! command -v node &> /dev/null; then
    echo "❌ Node.js no está instalado"
    exit 1
fi

echo "✅ Python3: $(python3 --version)"
echo "✅ Node.js: $(node --version)"
echo ""

# Verificar puertos
if check_port 8000; then
    echo "⚠️  Puerto 8000 (Backend) ya está en uso"
else
    echo "✅ Puerto 8000 (Backend) disponible"
fi

if check_port 4200; then
    echo "⚠️  Puerto 4200 (Frontend) ya está en uso"
else
    echo "✅ Puerto 4200 (Frontend) disponible"
fi

echo ""
echo "${BLUE}Para iniciar el proyecto:${NC}"
echo ""
echo "${GREEN}1. Backend (Python/FastAPI):${NC}"
echo "   cd backend"
echo "   python -m venv venv"
echo "   source venv/bin/activate"
echo "   pip install -r requirements.txt"
echo "   uvicorn app.main:app --reload"
echo "   → http://localhost:8000/docs"
echo ""
echo "${GREEN}2. Frontend (Angular):${NC}"
echo "   cd frontend"
echo "   npm start"
echo "   → http://localhost:4200"
echo ""
echo "===================================="
