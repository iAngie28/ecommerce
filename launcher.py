#!/usr/bin/env python3
# ========================================================================
# LANZADOR UNIVERSAL - WINDOWS / LINUX / MAC
# ========================================================================
# Menu interactivo multiplataforma
# Con colores, animaciones, UTF-8 support
# Uso: python launcher.py
#
# Características:
#   ✓ Funciona en Windows, Linux y Mac
#   ✓ Colores automáticos (sin dependencias externas)
#   ✓ Animaciones de carga
#   ✓ Soporte UTF-8 para acentos
#   ✓ Activa entorno virtual automáticamente
# ========================================================================

import os
import sys
import subprocess
import time
import platform
from pathlib import Path

# ========================================================================
# DETECTAR SO
# ========================================================================
SISTEMA_OPERATIVO = platform.system()
ES_WINDOWS = SISTEMA_OPERATIVO == "Windows"
ES_LINUX = SISTEMA_OPERATIVO == "Linux"
ES_MAC = SISTEMA_OPERATIVO == "Darwin"

# ========================================================================
# COLORES ANSI (Funcionan en todos los SO)
# ========================================================================
class Colors:
    # Colores
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'
    
    # Estilos
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'
    
    # Símbolos
    CHECK = '✓'
    CROSS = '✗'
    INFO = 'ℹ'
    WARN = '⚠'
    BULLET = '•'

# ========================================================================
# RUTAS
# ========================================================================
PROJECT_ROOT = Path(__file__).parent
BACKEND_DIR = PROJECT_ROOT / 'backend'
FRONTEND_DIR = PROJECT_ROOT / 'frontend'
SCRIPTS_DIR = PROJECT_ROOT / 'scripts_utiles'

# ========================================================================
# CARGAR .ENV (Manual para no depender de python-dotenv en el host)
# ========================================================================
def load_env_manual():
    """Carga variables del .env de la raíz de forma manual"""
    env_vars = {}
    env_path = PROJECT_ROOT / '.env'
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    key, value = line.split('=', 1)
                    # Quitar comillas si existen
                    value = value.strip().strip("'").strip('"')
                    env_vars[key.strip()] = value
    return env_vars

# Cargar variables iniciales
ENV_CONFIG = load_env_manual()
DJANGO_PORT = ENV_CONFIG.get('DJANGO_PORT', '8001')
REACT_PORT = ENV_CONFIG.get('REACT_PORT', '3000')

# ========================================================================
# VENV
# ========================================================================
def activate_venv():
    """Activa el entorno virtual del backend"""
    venv_path = BACKEND_DIR / ('venv' if not ES_WINDOWS else 'venv')
    
    if ES_WINDOWS:
        activate_script = venv_path / 'Scripts' / 'activate.bat'
    else:
        activate_script = venv_path / 'bin' / 'activate'
    
    if not activate_script.exists():
        print(f"{Colors.YELLOW}[WARN]{Colors.RESET} Entorno virtual no encontrado")
        print(f"{Colors.BLUE}[INFO]{Colors.RESET} Creando entorno virtual en {venv_path}...")
        
        # Crear venv
        subprocess.run([sys.executable, '-m', 'venv', str(venv_path)], check=True)
        print(f"{Colors.GREEN}[OK]{Colors.RESET} Entorno virtual creado")
    
    # Nota: En Python, no necesitamos activar explícitamente
    # podemos usar sys.executable del venv directamente

# ========================================================================
# FUNCIONES DE PRESENTACIÓN
# ========================================================================
def clear_screen():
    """Limpia la pantalla"""
    os.system('cls' if ES_WINDOWS else 'clear')

def print_header(text):
    """Imprime un encabezado"""
    print()
    print(f"{Colors.CYAN}{'='*70}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}✦ {text}{Colors.RESET}")
    print(f"{Colors.CYAN}{'='*70}{Colors.RESET}\n")

def print_section(text):
    """Imprime una sección"""
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.RESET}")

def print_option(text):
    """Imprime una opción de menú"""
    print(f"  {text}")

def print_success(text):
    """Imprime un mensaje de éxito"""
    print(f"{Colors.GREEN}{Colors.CHECK}{Colors.RESET} {text}")

def print_error(text):
    """Imprime un mensaje de error"""
    print(f"{Colors.RED}{Colors.CROSS}{Colors.RESET} {text}")

def print_info(text):
    """Imprime un mensaje de información"""
    print(f"{Colors.BLUE}{Colors.INFO}{Colors.RESET} {text}")

def print_warning(text):
    """Imprime una advertencia"""
    print(f"{Colors.YELLOW}{Colors.WARN}{Colors.RESET} {text}")

# ========================================================================
# ANIMACIONES
# ========================================================================
def loading_animation(duration=2, text="Cargando"):
    """Muestra una animación de carga"""
    spinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    end_time = time.time() + duration
    idx = 0
    
    while time.time() < end_time:
        print(f"\r{Colors.CYAN}{spinner[idx % len(spinner)]}{Colors.RESET} {text}...", end='', flush=True)
        idx += 1
        time.sleep(0.1)
    
    print(f"\r{Colors.GREEN}{Colors.CHECK}{Colors.RESET} {text}... {Colors.GREEN}Hecho{Colors.RESET}    ")

# ========================================================================
# UTILIDADES
# ========================================================================
def run_python_script(script_name, *args, use_venv=True):
    """Ejecuta un script Python, priorizando el venv si use_venv=True"""
    script_path = SCRIPTS_DIR / script_name
    
    if not script_path.exists():
        print_error(f"Script no encontrado: {script_path}")
        return
    
    # Determinar qué ejecutable usar
    python_exe = sys.executable
    if use_venv:
        if ES_WINDOWS:
            venv_path = BACKEND_DIR / 'venv' / 'Scripts' / 'python.exe'
        else:
            venv_path = BACKEND_DIR / 'venv' / 'bin' / 'python'
        
        if venv_path.exists():
            python_exe = str(venv_path)
        else:
            print_warning("Venv no encontrado, usando Python del sistema...")

    # IMPORTANTE: Cambiar al directorio backend para scripts que usan Django
    # Y añadirlo al PYTHONPATH para que encuentren 'config.settings'
    old_cwd = os.getcwd()
    os.chdir(BACKEND_DIR)
    
    current_env = os.environ.copy()
    # Poner el backend al PRINCIPIO para que Django gane
    backend_path = str(BACKEND_DIR)
    if "PYTHONPATH" in current_env:
        current_env["PYTHONPATH"] = f"{backend_path};{current_env['PYTHONPATH']}" if ES_WINDOWS else f"{backend_path}:{current_env['PYTHONPATH']}"
    else:
        current_env["PYTHONPATH"] = backend_path

    try:
        cmd = [python_exe, str(script_path)] + list(args)
        subprocess.run(cmd, env=current_env)
    except Exception as e:
        print_error(f"Error ejecutando script: {e}")
    finally:
        os.chdir(old_cwd)

def run_command(cmd, shell=False):
    """Ejecuta un comando"""
    try:
        subprocess.run(cmd, shell=shell, check=True)
    except subprocess.CalledProcessError as e:
        print_error(f"Error ejecutando comando: {str(e)}")

def pause():
    """Pausa y espera que el usuario presione Enter"""
    input(f"\n{Colors.BOLD}Presiona ENTER para continuar...{Colors.RESET}")

# ========================================================================
# INICIAR BACKEND Y FRONTEND
# ========================================================================
def start_backend():
    """Inicia el servidor Django en /backend"""
    global DJANGO_PORT
    ENV_CONFIG = load_env_manual()
    DJANGO_PORT = ENV_CONFIG.get('DJANGO_PORT', '8001')
    
    clear_screen()
    print_header("INICIAR BACKEND (DJANGO) - /backend")
    
    if not BACKEND_DIR.exists():
        print_error(f"Directorio backend no encontrado: {BACKEND_DIR}")
        pause()
        return
    
    # Ruta al Python del venv
    if ES_WINDOWS:
        venv_python = BACKEND_DIR / 'venv' / 'Scripts' / 'python.exe'
    else:
        venv_python = BACKEND_DIR / 'venv' / 'bin' / 'python'
    
    # Si venv no existe, crearlo
    if not venv_python.exists():
        print_warning("Entorno virtual no encontrado, creando...")
        venv_path = BACKEND_DIR / 'venv'
        try:
            subprocess.run([sys.executable, '-m', 'venv', str(venv_path)], check=True)
            print_success("Entorno virtual creado")
        except Exception as e:
            print_error(f"Error creando venv: {e}")
            pause()
            return
    
    # Verificar que manage.py existe
    manage_py = BACKEND_DIR / 'manage.py'
    if not manage_py.exists():
        print_error(f"manage.py no encontrado en {BACKEND_DIR}")
        pause()
        return
    
    print_success(f"Python venv: {venv_python}")
    print_info(f"Iniciando Django en {BACKEND_DIR}...")
    print_info(f"URL: http://127.0.0.1:{DJANGO_PORT}")
    print_warning("Presiona CTRL+C para detener el servidor")
    print()
    
    try:
        # Cambiar al directorio backend
        os.chdir(BACKEND_DIR)
        # Ejecutar manage.py con el Python del venv
        subprocess.run([str(venv_python), 'manage.py', 'runserver', DJANGO_PORT])
    except KeyboardInterrupt:
        print_warning("\nServidor Django detenido")
    except Exception as e:
        print_error(f"Error: {e}")
    finally:
        time.sleep(1)

def find_npm():
    """Busca npm en el sistema"""
    # Primero, intentar npm directamente
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, check=True)
        return 'npm'
    except:
        pass
    
    # En Windows, buscar en rutas comunes
    if ES_WINDOWS:
        common_paths = [
            'C:\\Program Files\\nodejs\\npm.cmd',
            'C:\\Program Files (x86)\\nodejs\\npm.cmd',
            Path.home() / 'AppData' / 'Local' / 'Programs' / 'nodejs' / 'npm.cmd',
        ]
        
        for npm_path in common_paths:
            if Path(npm_path).exists():
                return str(npm_path)
    
    # En Linux/Mac, buscar en PATH
    else:
        try:
            result = subprocess.run(['which', 'npm'], capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except:
            pass
    
    return None

def start_frontend():
    """Inicia el servidor React"""
    global REACT_PORT
    ENV_CONFIG = load_env_manual()
    REACT_PORT = ENV_CONFIG.get('REACT_PORT', '3000')
    
    clear_screen()
    print_header("INICIAR FRONTEND (REACT)")
    
    if not FRONTEND_DIR.exists():
        print_error("Directorio frontend no encontrado")
        pause()
        return
    
    # Buscar npm
    npm_cmd = find_npm()
    if not npm_cmd:
        print_error("npm no está instalado o no es accesible")
        print_info("Soluciones:")
        print(f"  1. Instala Node.js desde: {Colors.CYAN}https://nodejs.org/{Colors.RESET}")
        print(f"  2. Reinicia tu terminal después de instalar")
        print(f"  3. Verifica: {Colors.CYAN}node --version{Colors.RESET} y {Colors.CYAN}npm --version{Colors.RESET}")
        pause()
        return
    
    print_success(f"npm encontrado en: {npm_cmd}")
    
    # Verificar si node_modules existe
    node_modules = FRONTEND_DIR / 'node_modules'
    if not node_modules.exists():
        print_warning("node_modules no encontrado")
        print_info("Instalando dependencias (npm install)...")
        
        try:
            os.chdir(FRONTEND_DIR)
            subprocess.run([npm_cmd, 'install'], check=True)
        except subprocess.CalledProcessError as e:
            print_error(f"Error instalando dependencias: {e}")
            pause()
            return
    
    print_info(f"Iniciando React en {FRONTEND_DIR}...")
    print_info(f"URL: http://127.0.0.1:{REACT_PORT}")
    print_warning("Presiona CTRL+C para detener el servidor")
    print()
    
    try:
        os.chdir(FRONTEND_DIR)
        subprocess.run([npm_cmd, 'start'])
    except KeyboardInterrupt:
        print_warning("\nServidor React detenido")
    except Exception as e:
        print_error(f"Error: {e}")
    finally:
        time.sleep(1)

def start_all():
    """Inicia Backend y Frontend en el MISMO terminal con logs entrelazados"""
    global DJANGO_PORT, REACT_PORT
    ENV_CONFIG = load_env_manual()
    DJANGO_PORT = ENV_CONFIG.get('DJANGO_PORT', '8001')
    REACT_PORT = ENV_CONFIG.get('REACT_PORT', '3000')
    clear_screen()
    print_header("INICIAR TODO (BACKEND + FRONTEND) - MODO DIRECTO")
    
    # 1. Preparar comandos
    if ES_WINDOWS:
        venv_python = BACKEND_DIR / 'venv' / 'Scripts' / 'python.exe'
        npm_cmd = find_npm()
    else:
        venv_python = BACKEND_DIR / 'venv' / 'bin' / 'python'
        npm_cmd = 'npm'

    # Backend: USAR load-env.js si es necesario o confiar en que ya lo hace
    # Frontend: SIEMPRE usar load-env.js (está en package.json)
    
    print_info("Iniciando ambos servicios...")
    print_warning("Usa CTRL+C para detener ambos al mismo tiempo")
    print(f"{Colors.GRAY}{'-'*70}{Colors.RESET}")

    try:
        # Iniciamos el Backend
        # Nota: Usamos shell=True en Windows para que reconozca los ejecutables en PATH
        backend_proc = subprocess.Popen(
            [str(venv_python), 'manage.py', 'runserver', DJANGO_PORT],
            cwd=str(BACKEND_DIR),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        # Iniciamos el Frontend
        # En el package.json el start ya usa load-env.js
        frontend_proc = subprocess.Popen(
            [npm_cmd, 'start'],
            cwd=str(FRONTEND_DIR),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        import threading

        def log_output(pipe, prefix, color):
            for line in iter(pipe.readline, ''):
                if line:
                    print(f"{color}[{prefix}]{Colors.RESET} {line.strip()}")

        # Hilos para leer logs
        t1 = threading.Thread(target=log_output, args=(backend_proc.stdout, "BACKEND", Colors.BLUE))
        t2 = threading.Thread(target=log_output, args=(frontend_proc.stdout, "FRONTEND", Colors.CYAN))
        
        t1.daemon = True
        t2.daemon = True
        
        t1.start()
        t2.start()

        # Esperar a que alguno termine o interrupción
        while backend_proc.poll() is None and frontend_proc.poll() is None:
            time.sleep(0.5)

    except KeyboardInterrupt:
        print_warning("\nDeteniendo servicios...")
    finally:
        # Asegurarse de cerrar procesos
        try: backend_proc.terminate()
        except: pass
        try: frontend_proc.terminate()
        except: pass
        print_success("Servicios detenidos")
    
    pause()

# ========================================================================
# MENÚS
# ========================================================================
def show_main_menu():
    """Menú principal"""
    while True:
        clear_screen()
        print_header("LANZADOR DE PROYECTO")
        
        print_section(f"Sistema Operativo: {SISTEMA_OPERATIVO}")
        print()
        
        print_option(f"{Colors.GREEN}▶ 1{Colors.RESET} - Iniciar Backend (Django)")
        print_option(f"{Colors.GREEN}▶ 2{Colors.RESET} - Iniciar Frontend (React)")
        print_option(f"{Colors.BOLD}{Colors.GREEN}▶ A{Colors.RESET} - {Colors.BOLD}INICIAR TODO (Backend + Frontend){Colors.RESET}")
        print_option(f"{Colors.YELLOW}▶ I{Colors.RESET} - Instalación Rápida (Plug & Play)")
        print_option(f"{Colors.CYAN}3{Colors.RESET} - Configuración")
        print_option(f"{Colors.CYAN}4{Colors.RESET} - Scripts Utiles")
        print_option(f"{Colors.CYAN}5{Colors.RESET} - Configuración de Base de Datos")
        print_option(f"{Colors.CYAN}6{Colors.RESET} - Gestión de Datos")
        print_option(f"{Colors.CYAN}7{Colors.RESET} - Consola de Pruebas")
        print_option(f"{Colors.CYAN}8{Colors.RESET} - Servicios Nginx")
        print_option(f"{Colors.CYAN}9{Colors.RESET} - Sistema")
        print_option(f"{Colors.BLUE}10{Colors.RESET} - Información del Sistema")
        print_option(f"{Colors.BLUE}11{Colors.RESET} - Ayuda")
        print_option(f"{Colors.RED}0{Colors.RESET} - Salir")
        print()
        
        choice = input(f"{Colors.BOLD}  ? Selecciona: {Colors.RESET}").strip()
        
        if choice == '1':
            start_backend()
        elif choice == '2':
            start_frontend()
        elif choice.lower() == 'a':
            start_all()
        elif choice.lower() == 'i':
            run_python_script('system_setup.py', use_venv=False) 
            pause()
        elif choice == '3':
            show_config_menu()
        elif choice == '4':
            show_scripts_menu()
        elif choice == '5':
            show_db_config_menu()
        elif choice == '6':
            show_data_menu()
        elif choice == '7':
            show_test_shell()
        elif choice == '8':
            show_nginx_menu()
        elif choice == '9':
            show_system_menu()
        elif choice == '10':
            show_system_info()
        elif choice == '11':
            show_help()
        elif choice == '0':
            print_info("¡Adiós!")
            sys.exit(0)
        else:
            print_error("Opción inválida")
            time.sleep(1)

def show_config_menu():
    """Menú de configuración"""
    while True:
        clear_screen()
        print_header("CONFIGURACIÓN")
        
        print_section("Base de Datos")
        print_option(f"{Colors.CYAN}1{Colors.RESET} - Ver configuración .env")
        print_option(f"{Colors.CYAN}2{Colors.RESET} - Editar .env (abrir editor)")
        
        print_section("Proyecto")
        print_option(f"{Colors.CYAN}3{Colors.RESET} - Ver info del proyecto")
        
        print_option(f"{Colors.RED}b{Colors.RESET} - Volver")
        print()
        
        choice = input(f"{Colors.BOLD}  ? Selecciona: {Colors.RESET}").strip().lower()
        
        if choice == '1':
            env_file = PROJECT_ROOT / '.env'
            if env_file.exists():
                print_section("Contenido de .env")
                with open(env_file) as f:
                    print(f.read())
            else:
                print_warning(".env no existe")
            pause()
        elif choice == '2':
            env_file = PROJECT_ROOT / '.env'
            if not env_file.exists():
                print_warning(".env no existe, creando...")
                env_file.touch()
            if ES_WINDOWS:
                os.startfile(env_file)
            elif ES_MAC:
                run_command(['open', str(env_file)])
            else:
                run_command(['xdg-open', str(env_file)])
            print_success("Abierto en editor")
            pause()
        elif choice == '3':
            print_section("Información del Proyecto")
            print(f"  Ruta: {PROJECT_ROOT}")
            print(f"  Backend: {BACKEND_DIR}")
            print(f"  Frontend: {FRONTEND_DIR}")
            print(f"  Scripts: {SCRIPTS_DIR}")
            pause()
        elif choice == 'b':
            break
        else:
            print_error("Opción inválida")
            time.sleep(1)

def show_scripts_menu():
    """Menú de scripts útiles"""
    while True:
        clear_screen()
        print_header("SCRIPTS ÚTILES")
        
        print_option(f"{Colors.CYAN}1{Colors.RESET} - db_reset.py (resetear BD)")
        print_option(f"{Colors.CYAN}2{Colors.RESET} - db_seed.py (popular BD)")
        print_option(f"{Colors.CYAN}3{Colors.RESET} - manage_users.py (gestionar usuarios)")
        print_option(f"{Colors.CYAN}4{Colors.RESET} - test_shell.py (consola de pruebas)")
        print_option(f"{Colors.RED}b{Colors.RESET} - Volver")
        print()
        
        choice = input(f"{Colors.BOLD}  ? Selecciona: {Colors.RESET}").strip().lower()
        
        if choice == '1':
            run_python_script('db_reset.py')
            pause()
        elif choice == '2':
            run_python_script('db_seed.py')
            pause()
        elif choice == '3':
            run_python_script('manage_users.py')
            pause()
        elif choice == '4':
            run_python_script('test_shell.py')
            pause()
        elif choice == 'b':
            break
        else:
            print_error("Opción inválida")
            time.sleep(1)

def show_db_config_menu():
    """Menú de configuración de BD"""
    while True:
        clear_screen()
        print_header("CONFIGURACIÓN DE BASE DE DATOS")
        
        print_option(f"{Colors.CYAN}1{Colors.RESET} - Ver configuración actual")
        print_option(f"{Colors.CYAN}2{Colors.RESET} - Configuración básica (presets)")
        print_option(f"{Colors.CYAN}3{Colors.RESET} - Configuración avanzada")
        print_option(f"{Colors.CYAN}4{Colors.RESET} - Configurar un campo")
        print_option(f"{Colors.CYAN}5{Colors.RESET} - Ver presets disponibles")
        print_option(f"{Colors.CYAN}6{Colors.RESET} - Probar conexión")
        print_option(f"{Colors.RED}b{Colors.RESET} - Volver")
        print()
        
        choice = input(f"{Colors.BOLD}  ? Selecciona: {Colors.RESET}").strip().lower()
        
        if choice == '1':
            loading_animation(1, "Cargando configuración")
            run_python_script('db_config.py')
            pause()
        elif choice == '2':
            run_python_script('db_config.py', 'basic')
            pause()
        elif choice == '3':
            run_python_script('db_config.py', 'advanced')
            pause()
        elif choice == '4':
            run_python_script('db_config.py', 'field')
            pause()
        elif choice == '5':
            run_python_script('db_config.py', 'presets')
            pause()
        elif choice == '6':
            loading_animation(1, "Probando conexión")
            run_python_script('db_config.py', 'test')
            pause()
        elif choice == 'b':
            break
        else:
            print_error("Opción inválida")
            time.sleep(1)

def show_data_menu():
    """Menú de gestión de datos"""
    while True:
        clear_screen()
        print_header("GESTIÓN DE DATOS")
        
        print_section("Resetear")
        print_option(f"{Colors.RED}1{Colors.RESET} - Resetear BD completa (Estructura + Datos)")
        print_option(f"{Colors.RED}2{Colors.RESET} - Resetear y crear superusuario")
        
        print_section("Seeders")
        print_option(f"{Colors.CYAN}3{Colors.RESET} - Ejecutar seeders (Populado de prueba)")
        print_option(f"{Colors.CYAN}4{Colors.RESET} - Ver datos actuales")
        
        print_section("Usuarios")
        print_option(f"{Colors.YELLOW}5{Colors.RESET} - Crear usuario")
        print_option(f"{Colors.YELLOW}6{Colors.RESET} - Listar usuarios")
        print_option(f"{Colors.YELLOW}7{Colors.RESET} - Eliminar usuario")
        
        print_section("Migraciones")
        print_option(f"{Colors.BLUE}8{Colors.RESET} - Hacer migraciones (makemigrations + migrate)")
        print_option(f"{Colors.BLUE}9{Colors.RESET} - Ver historial migraciones")
        
        print_option(f"{Colors.RED}b{Colors.RESET} - Volver")
        print()
        
        choice = input(f"{Colors.BOLD}  ? Selecciona: {Colors.RESET}").strip().lower()
        
        if choice == '1' or choice == '2':
            run_python_script('db_reset.py', 'all')
            pause()
        elif choice == '3':
            run_python_script('db_seed.py')
            pause()
        elif choice == '4':
            run_python_script('manage_users.py', 'list')
            pause()
        elif choice == '5':
            run_python_script('manage_users.py', 'create')
            pause()
        elif choice == '6':
            run_python_script('manage_users.py', 'list')
            pause()
        elif choice == '7':
            run_python_script('manage_users.py', 'delete')
            pause()
        elif choice == '8':
            print_info("Generando nuevas migraciones...")
            run_python_script('migrations.py', 'make')
            print_info("Aplicando migraciones...")
            run_python_script('migrations.py', 'migrate')
            pause()
        elif choice == '9':
            run_python_script('migrations.py', 'show')
            pause()
        elif choice == 'b':
            break
        else:
            print_error("Opción inválida")
            time.sleep(1)

def show_test_shell():
    """Menú de testing"""
    clear_screen()
    print_header("CONSOLA DE PRUEBAS")
    run_python_script('test_shell.py')
    pause()

def show_nginx_menu():
    """Menú de Nginx"""
    while True:
        clear_screen()
        print_header("SERVICIOS NGINX")
        
        print_section(f"{Colors.CHECK} Crear Servicios (muestra .env y pide confirmación)")
        print_option(f"{Colors.CYAN}1{Colors.RESET} - Crear servicio Django")
        print_option(f"{Colors.CYAN}2{Colors.RESET} - Crear servicio Frontend (React)")
        
        print_section(f"{Colors.CHECK} Gestión")
        print_option(f"{Colors.CYAN}3{Colors.RESET} - Ver estado de servicios")
        print_option(f"{Colors.CYAN}4{Colors.RESET} - Ver logs")
        print_option(f"{Colors.CYAN}5{Colors.RESET} - Recargar Nginx")
        print_option(f"{Colors.CYAN}6{Colors.RESET} - Reiniciar servicio")
        
        print_section(f"{Colors.CROSS} Eliminar")
        print_option(f"{Colors.RED}7{Colors.RESET} - Eliminar servicio")
        
        print_option(f"{Colors.RED}b{Colors.RESET} - Volver")
        print()
        
        choice = input(f"{Colors.BOLD}  ? Selecciona: {Colors.RESET}").strip().lower()
        
        if choice == '1':
            loading_animation(1, "Preparando configuración")
            run_python_script('nginx_config.py', 'django-service')
            pause()
        elif choice == '2':
            loading_animation(1, "Preparando configuración")
            run_python_script('nginx_config.py', 'frontend-service')
            pause()
        elif choice == '3':
            run_python_script('nginx_config.py', 'status')
            pause()
        elif choice == '4':
            run_python_script('nginx_config.py', 'logs')
            pause()
        elif choice == '5':
            loading_animation(1, "Recargando")
            run_python_script('nginx_config.py', 'reload-nginx')
            pause()
        elif choice == '6':
            run_python_script('nginx_config.py', 'restart')
            pause()
        elif choice == '7':
            run_python_script('nginx_config.py', 'delete-service')
            pause()
        elif choice == 'b':
            break
        else:
            print_error("Opción inválida")
            time.sleep(1)

def show_system_menu():
    """Menú de sistema"""
    while True:
        clear_screen()
        print_header("GESTIÓN DE SISTEMA")
        
        print_section("Actualizar Dependencias")
        print_option(f"{Colors.GREEN}1{Colors.RESET} - Actualizar Django (pip)")
        print_option(f"{Colors.GREEN}2{Colors.RESET} - Actualizar npm")
        print_option(f"{Colors.GREEN}3{Colors.RESET} - Actualizar sistema (apt)")
        
        print_section("Secretos y Seguridad (se guardan en .env)")
        print_option(f"{Colors.YELLOW}4{Colors.RESET} - Generar secrets (Django, JWT, API, etc)")
        
        print_section("Mantenimiento (REQUIERE ROOT en Linux)")
        print_option(f"{Colors.RED}5{Colors.RESET} - Resetear sistema seguro (SIN JODER VPS)")
        print_option(f"{Colors.YELLOW}6{Colors.RESET} - Verificar salud del sistema")
        
        print_option(f"{Colors.RED}b{Colors.RESET} - Volver")
        print()
        
        choice = input(f"{Colors.BOLD}  ? Selecciona: {Colors.RESET}").strip().lower()
        
        if choice == '1':
            loading_animation(2, "Actualizando")
            run_python_script('system_manager.py', 'update-django')
            pause()
        elif choice == '2':
            loading_animation(2, "Actualizando")
            run_python_script('system_manager.py', 'update-npm')
            pause()
        elif choice == '3':
            loading_animation(3, "Actualizando")
            run_python_script('system_manager.py', 'update-system')
            pause()
        elif choice == '4':
            run_python_script('system_manager.py', 'generate-secrets')
            pause()
        elif choice == '5':
            run_python_script('system_manager.py', 'reset-system')
            pause()
        elif choice == '6':
            run_python_script('system_manager.py', 'health-check')
            pause()
        elif choice == 'b':
            break
        else:
            print_error("Opción inválida")
            time.sleep(1)

def show_system_info():
    """Información del sistema"""
    clear_screen()
    print_header("INFORMACIÓN DEL SISTEMA")
    
    print(f"{Colors.BOLD}Sistema Operativo:{Colors.RESET}")
    print(f"  {SISTEMA_OPERATIVO} {platform.release()}")
    
    print(f"\n{Colors.BOLD}Python:{Colors.RESET}")
    print(f"  Versión: {sys.version}")
    print(f"  Ejecutable: {sys.executable}")
    
    print(f"\n{Colors.BOLD}Proyecto:{Colors.RESET}")
    print(f"  Ruta: {PROJECT_ROOT}")
    print(f"  Backend: {BACKEND_DIR} {'✓' if BACKEND_DIR.exists() else '✗'}")
    print(f"  Frontend: {FRONTEND_DIR} {'✓' if FRONTEND_DIR.exists() else '✗'}")
    
    print(f"\n{Colors.BOLD}Node.js:{Colors.RESET}")
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        print(f"  {result.stdout.strip()}")
    except:
        print("  No instalado")
    
    print(f"\n{Colors.BOLD}PostgreSQL:{Colors.RESET}")
    try:
        result = subprocess.run(['psql', '--version'], capture_output=True, text=True)
        print(f"  {result.stdout.strip()}")
    except:
        print("  No instalado")
    
    pause()

def show_help():
    """Menú de ayuda"""
    clear_screen()
    print_header("AYUDA")
    
    print(f"{Colors.BOLD}Descripción:{Colors.RESET}")
    print("  Lanzador universal multiplataforma para gestionar desarrollo")
    
    print(f"\n{Colors.BOLD}Funcionalidades:{Colors.RESET}")
    print(f"  {Colors.CHECK} Configuración de base de datos con presets")
    print(f"  {Colors.CHECK} Gestor de datos y usuarios")
    print(f"  {Colors.CHECK} Gestión de servicios Nginx (Django, React)")
    print(f"  {Colors.CHECK} Actualización de dependencias")
    print(f"  {Colors.CHECK} Generador de secrets seguro")
    print(f"  {Colors.CHECK} Reset seguro de sistema (sin joder VPS)")
    print(f"  {Colors.CHECK} Verificación de salud del sistema")
    
    print(f"\n{Colors.BOLD}Requisitos:{Colors.RESET}")
    print("  - Python 3.8+")
    print("  - Node.js 14+ (para frontend)")
    print("  - PostgreSQL 12+ (para BD)")
    
    print(f"\n{Colors.BOLD}Licencia:{Colors.RESET}")
    print("  MIT - 2026")
    
    pause()

# ========================================================================
# MAIN
# ========================================================================
def main():
    """Función principal"""
    # Activar venv
    activate_venv()
    
    # Mostrar menú
    show_main_menu()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Cancelado por el usuario{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"{Colors.RED}Error: {str(e)}{Colors.RESET}")
        sys.exit(1)
