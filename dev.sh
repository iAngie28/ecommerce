#!/bin/bash
# ========================================================================
# SCRIPT DE DESARROLLO - Levanta Django + React DIRECTAMENTE
# ========================================================================
# SIN NGINX - Solo para testing rápido
# Uso:
#   ./dev.sh
#
# Requisitos:
#   - Python 3.8+
#   - Node.js 14+
#   - PostgreSQL instalado y corriendo
# ========================================================================

set -e

# ========================================================================
# ACTIVAR ENTORNO VIRTUAL PYTHON (Backend)
# ========================================================================
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "$PROJECT_ROOT/backend/venv/bin/activate" ]; then
    source "$PROJECT_ROOT/backend/venv/bin/activate"
else
    echo "[WARN] Entorno virtual no encontrado en: $PROJECT_ROOT/backend/venv/bin/activate"
    echo "[INFO] Creando entorno virtual en backend..."
    python3 -m venv "$PROJECT_ROOT/backend/venv"
    source "$PROJECT_ROOT/backend/venv/bin/activate"
fi

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_command() {
    if ! command -v $1 &> /dev/null; then
        log_error "$1 no instalado"
        exit 1
    fi
}

# ========================================================================
# VERIFICACIONES
# ========================================================================
log_info "Verificando requisitos..."
check_command python
check_command node
check_command npm

# ========================================================================
# CREAR .env SI NO EXISTE (ÚNICO .env en la raíz)
# ========================================================================
if [ ! -f .env ]; then
    log_warn ".env no existe"
    if [ -f .env.example ]; then
        cp .env.example .env
        log_success ".env creado desde .env.example"
    else
        log_error ".env.example tampoco existe"
        exit 1
    fi
fi

# Copiar .env a backend y frontend para que lo lean
cp .env backend/.env
cp .env frontend/.env
log_success ".env copiado a backend/ y frontend/"

# ========================================================================
# SETUP BACKEND
# ========================================================================
log_info "Configurando Backend..."

cd backend

if [ ! -d "venv" ]; then
    log_info "Creando virtual environment..."
    python -m venv venv
fi

source venv/bin/activate

log_info "Instalando dependencias..."
pip install -q -r requirements.txt

log_info "Ejecutando migraciones..."
python manage.py migrate --skip-checks

cd ..

log_success "Backend listo"

# ========================================================================
# SETUP FRONTEND
# ========================================================================
log_info "Configurando Frontend..."

cd frontend

if [ ! -d "node_modules" ]; then
    log_info "Instalando dependencias..."
    npm install
fi

cd ..

log_success "Frontend listo"

# ========================================================================
# INICIAR SERVICIOS
# ========================================================================
log_info "Iniciando servicios (sin Nginx)..."
log_warn "DESARROLLO LOCAL: Sin Nginx, acceso directo"

log_success "Abriendo terminales por separado:"
echo ""
echo "Terminal 1 - BACKEND:"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  python manage.py runserver 127.0.0.1:8001"
echo ""
echo "Terminal 2 - FRONTEND:"
echo "  cd frontend"
echo "  PORT=3000 npm start"
echo ""
echo "ACCESOS:"
echo "  Frontend:  http://localhost:3000"
echo "  Backend:   http://localhost:8001"
echo "  Admin:     http://localhost:8001/admin"
echo "  API:       http://localhost:8001/api"
echo ""
log_warn "Abre dos terminales nuevas y copia los comandos de arriba"

