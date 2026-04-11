#!/usr/bin/env python3
# ========================================================================
# LANZADOR UNIVERSAL - WINDOWS / LINUX / MAC
# ========================================================================
# Menu interactivo multiplataforma
# Con colores, animaciones, UTF-8 support
# Uso: python launcher.py
#
# Características:
#   * Funciona en Windows, Linux y Mac
#   * Colores automáticos (sin dependencias externas)
#   * Animaciones de carga
#   * Soporte UTF-8 para acentos
#   * Activa entorno virtual automáticamente
# ========================================================================

import os
import sys
import subprocess
import time
import platform
import shutil
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
    CHECK = '[OK]'
    CROSS = '[X]'
    INFO = '[i]'
    WARN = '[!]'
    BULLET = '*'

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
    print(f"{Colors.CYAN}{Colors.BOLD}{text}{Colors.RESET}")
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
    except KeyboardInterrupt:
        print_warning("\nProceso cancelado por el usuario.")
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
    """Inicia el servidor Django en /backend con máxima robustez"""
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
    
    # Si venv no existe, crearlo automáticamente
    if not venv_python.exists():
        print_warning("Entorno virtual no encontrado, intentando crear...")
        venv_path = BACKEND_DIR / 'venv'
        try:
            subprocess.run([sys.executable, '-m', 'venv', str(venv_path)], check=True)
            print_success("Entorno virtual creado exitosamente")
            # Re-verificar ruta tras creación
            if not venv_python.exists():
                 print_error("Error crítico: El venv se creó pero no se encuentra el ejecutable.")
                 pause()
                 return
        except Exception as e:
            print_error(f"Error fatal creando venv: {e}")
            pause()
            return
    
    # Verificar manage.py
    manage_py = BACKEND_DIR / 'manage.py'
    if not manage_py.exists():
        print_error(f"manage.py no encontrado en {BACKEND_DIR}")
        pause()
        return
    
    print_info(f"Usando: {venv_python}")
    print_info(f"URL: http://127.0.0.1:{DJANGO_PORT}")
    print_warning("Presiona CTRL+C para detener el servidor")
    print("-" * 70)
    
    try:
        os.chdir(BACKEND_DIR)
        # Usamos subprocess.run directamente para heredar el terminal interactivo
        subprocess.run([str(venv_python), 'manage.py', 'runserver', DJANGO_PORT])
    except KeyboardInterrupt:
        print_warning("\nServidor Django detenido por el usuario")
    except Exception as e:
        print_error(f"Error inesperado: {e}")
    finally:
        os.chdir(PROJECT_ROOT)
        time.sleep(1)

def find_npm():
    """Busca npm en el PATH del sistema"""
    npm_path = shutil.which('npm')
    if npm_path:
        return npm_path
    
    # Fallback para Windows si shutil.which falla en ciertos entornos
    if ES_WINDOWS:
        common_paths = [
            'C:\\Program Files\\nodejs\\npm.cmd',
            'C:\\Program Files (x86)\\nodejs\\npm.cmd',
        ]
        for path in common_paths:
            if os.path.exists(path):
                return path
    return None

def start_frontend():
    """Inicia el servidor React con máxima robustez"""
    global REACT_PORT
    ENV_CONFIG = load_env_manual()
    REACT_PORT = ENV_CONFIG.get('REACT_PORT', '3000')
    
    clear_screen()
    print_header("INICIAR FRONTEND (REACT)")
    
    if not FRONTEND_DIR.exists():
        print_error("Directorio frontend no encontrado")
        pause()
        return
    
    npm_cmd = find_npm()
    if not npm_cmd:
        print_error("npm no encontrado. Instala Node.js para continuar.")
        pause()
        return
    
    # Verificar node_modules
    node_modules = FRONTEND_DIR / 'node_modules'
    if not node_modules.exists():
        print_warning("node_modules no encontrado, ejecutando 'npm install'...")
        try:
            os.chdir(FRONTEND_DIR)
            subprocess.run([npm_cmd, 'install'], check=True, shell=ES_WINDOWS)
            print_success("Dependencias instaladas")
        except Exception as e:
            print_error(f"Error instalando dependencias: {e}")
            pause()
            return
    
    print_info(f"URL: http://127.0.0.1:{REACT_PORT}")
    print_warning("Presiona CTRL+C para detener el servidor")
    print("-" * 70)
    
    try:
        os.chdir(FRONTEND_DIR)
        # shell=ES_WINDOWS es vital para comandos .cmd/.bat en Windows
        subprocess.run([npm_cmd, 'start'], shell=ES_WINDOWS)
    except KeyboardInterrupt:
        print_warning("\nServidor React detenido por el usuario")
    except Exception as e:
        print_error(f"Error: {e}")
    finally:
        os.chdir(PROJECT_ROOT)
        time.sleep(1)

def start_all():
    """Inicia Backend y Frontend en el MISMO terminal con logs entrelazados"""
    global DJANGO_PORT, REACT_PORT
    ENV_CONFIG = load_env_manual()
    DJANGO_PORT = ENV_CONFIG.get('DJANGO_PORT', '8001')
    REACT_PORT = ENV_CONFIG.get('REACT_PORT', '3000')
    clear_screen()
    print_header("INICIAR TODO (BACKEND + FRONTEND) - MODO DIRECTO")
    
    # 1. Preparar y validar comandos
    if ES_WINDOWS:
        venv_python = BACKEND_DIR / 'venv' / 'Scripts' / 'python.exe'
        npm_cmd = find_npm()
    else:
        venv_python = BACKEND_DIR / 'venv' / 'bin' / 'python'
        npm_cmd = find_npm() or 'npm'

    if not venv_python.exists():
        print_error("Entorno virtual de Python no encontrado.")
        print_info("Ejecuta la Opción 1 (Iniciar Backend) primero para generarlo.")
        pause()
        return

    if not npm_cmd:
        print_error("No se encontró npm / Node.js.")
        print_info("Asegúrate de tener Node.js instalado y accesible en PATH.")
        pause()
        return

    print_info("Iniciando ambos servicios...")
    print_warning("Usa CTRL+C para detener ambos al mismo tiempo")
    print(f"{Colors.GRAY}{'-'*70}{Colors.RESET}")

    try:
        # Iniciamos el Backend
        backend_proc = subprocess.Popen(
            [str(venv_python), 'manage.py', 'runserver', DJANGO_PORT],
            cwd=str(BACKEND_DIR),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        # Iniciamos el Frontend (shell=ES_WINDOWS soluciona errores de ejecución de .cmd en Windows)
        frontend_proc = subprocess.Popen(
            [npm_cmd, 'start'],
            cwd=str(FRONTEND_DIR),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            shell=ES_WINDOWS
        )

        import threading

        def log_output(pipe, prefix, color):
            try:
                for line in iter(pipe.readline, ''):
                    if line:
                        print(f"{color}[{prefix}]{Colors.RESET} {line.strip()}")
            except ValueError:
                pass # Pipe closed

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
        # Asegurarse de cerrar procesos rápida y limpiamente
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
        
        print_section("EJECUCIÓN")
        print_option(f"{Colors.GREEN}1{Colors.RESET} - Iniciar Backend (Django)")
        print_option(f"{Colors.GREEN}2{Colors.RESET} - Iniciar Frontend (React)")
        print_option(f"{Colors.BOLD}{Colors.GREEN}3{Colors.RESET} - {Colors.BOLD}INICIAR TODO (Backend + Frontend){Colors.RESET}")
        
        print_section("DATOS Y USUARIOS")
        print_option(f"{Colors.CYAN}4{Colors.RESET} - Gestión de Base de Datos y Usuarios")
        print_option(f"{Colors.CYAN}5{Colors.RESET} - Gestión de Usuarios (Acceso Rápido)")
        
        print_section("CONFIGURACIÓN Y SISTEMA")
        print_option(f"{Colors.YELLOW}I{Colors.RESET} - Instalación Rápida (Plug & Play)")
        print_option(f"{Colors.CYAN}6{Colors.RESET} - Configuración de Entorno (.env)")
        print_option(f"{Colors.CYAN}7{Colors.RESET} - Servicios Web (Nginx)")
        print_option(f"{Colors.CYAN}8{Colors.RESET} - Mantenimiento del Sistema")
        
        print_section("DESARROLLO")
        print_option(f"{Colors.BLUE}9{Colors.RESET} - Consola de Pruebas (Django Shell)")
        print_option(f"{Colors.BLUE}10{Colors.RESET} - Todos los Scripts (Avanzado)")
        print_option(f"{Colors.BLUE}11{Colors.RESET} - Información del Sistema")
        print_option(f"{Colors.BLUE}12{Colors.RESET} - Ayuda General")
        
        print_option(f"{Colors.RED}0{Colors.RESET} - Salir")

        print_section("PRUEBAS UNITARIAS")
        print_option(f"{Colors.MAGENTA}P{Colors.RESET} - Pruebas Unitarias")
        print()
        
        choice = input(f"{Colors.BOLD}  ? Selecciona: {Colors.RESET}").strip().lower()
        
        if choice == '1':
            start_backend()
        elif choice == '2':
            start_frontend()
        elif choice == '3' or choice == 'a':
            start_all()
        elif choice == '4':
            show_data_management_menu()
        elif choice == '5':
            show_users_menu()
        elif choice == 'i':
            run_python_script('system_setup.py', use_venv=False) 
            pause()
        elif choice == '6':
            show_config_menu()
        elif choice == '7':
            show_nginx_menu()
        elif choice == '8':
            show_system_menu()
        elif choice == '9':
            show_test_shell()
        elif choice == '10':
            show_scripts_menu()
        elif choice == '11':
            show_system_info()
        elif choice == '12':
            show_help()
        elif choice == 'p' or 'P':
            run_python_script('test.py')

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
        print_option(f"{Colors.CYAN}4{Colors.RESET} - Configuración avanzada (project_config.py)")
        
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
        elif choice == '4':
            run_python_script('project_config.py')
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

def show_data_management_menu():
    """Menú unificado de Base de Datos y Gestión de Datos"""
    while True:
        clear_screen()
        print_header("GESTIÓN DE BASE DE DATOS Y DATOS")
        
        print_section("Configuración")
        print_option(f"{Colors.CYAN}1{Colors.RESET} - Configurar Conexión (db_config.py)")
        print_option(f"{Colors.CYAN}2{Colors.RESET} - Probar Conexión")
        
        print_section("Estructura y Migraciones")
        print_option(f"{Colors.BLUE}3{Colors.RESET} - Hacer Migraciones (makemigrations + migrate)")
        print_option(f"{Colors.BLUE}4{Colors.RESET} - Ver historial de Migraciones")
        
        print_section("Contenido y Usuarios")
        print_option(f"{Colors.YELLOW}5{Colors.RESET} - Gestión de Usuarios (CRUD Completo)")
        print_option(f"{Colors.YELLOW}6{Colors.RESET} - Ejecutar Seeders (Poblar con datos de prueba)")
        
        print_section("Limpieza y Reset (CUIDADO)")
        print_option(f"{Colors.RED}7{Colors.RESET} - Resetear BD Completa (Borra todo y recrea estructura)")
        
        print_option(f"{Colors.RED}b{Colors.RESET} - Volver al Menú Principal")
        print()
        
        choice = input(f"{Colors.BOLD}  ? Selecciona: {Colors.RESET}").strip().lower()
        
        if choice == '1':
            run_python_script('db_config.py')
            pause()
        elif choice == '2':
            run_python_script('db_config.py', 'test')
            pause()
        elif choice == '3':
            print_info("Procesando migraciones...")
            run_python_script('migrations.py', 'make')
            run_python_script('migrations.py', 'migrate')
            pause()
        elif choice == '4':
            run_python_script('migrations.py', 'show')
            pause()
        elif choice == '5':
            show_users_menu()
        elif choice == '6':
            run_python_script('db_seed.py')
            pause()
        elif choice == '7':
            confirm = input(f"{Colors.RED}¿ESTÁS SEGURO? Esto borrará todos los datos. (s/n): {Colors.RESET}").lower()
            if confirm == 's':
                run_python_script('db_reset.py', 'all')
            pause()
        elif choice == 'b':
            break
        else:
            print_error("Opción inválida")
            time.sleep(1)

# El menu original de data se ha integrado en show_data_management_menu

def show_users_menu():
    """Menú dedicado a la gestión de usuarios"""
    while True:
        clear_screen()
        print_header("GESTIÓN DE USUARIOS")
        
        print_section("Operaciones Básicas (CRUD)")
        print_option(f"{Colors.YELLOW}1{Colors.RESET} - Crear nuevo usuario")
        print_option(f"{Colors.YELLOW}2{Colors.RESET} - Listar usuarios")
        print_option(f"{Colors.YELLOW}3{Colors.RESET} - Editar usuario (Contraseña, Nombre, Permisos)")
        print_option(f"{Colors.YELLOW}4{Colors.RESET} - Eliminar usuario")
        
        print_section("Estado y Control de Acceso")
        print_option(f"{Colors.CYAN}5{Colors.RESET} - Ver estado (Activo/Inactivo)")
        print_option(f"{Colors.GREEN}6{Colors.RESET} - Activar usuario")
        print_option(f"{Colors.RED}7{Colors.RESET} - Desactivar usuario")
        
        print_option(f"{Colors.RED}b{Colors.RESET} - Volver")
        print()
        
        choice = input(f"{Colors.BOLD}  ? Selecciona: {Colors.RESET}").strip().lower()
        
        if choice == '1':
            run_python_script('manage_users.py', 'create')
            pause()
        elif choice == '2':
            run_python_script('manage_users.py', 'list')
            pause()
        elif choice == '3':
            run_python_script('manage_users.py', 'edit')
            pause()
        elif choice == '4':
            run_python_script('manage_users.py', 'delete')
            pause()
        elif choice == '5':
            run_python_script('manage_users.py', 'status')
            pause()
        elif choice == '6':
            run_python_script('manage_users.py', 'activate')
            pause()
        elif choice == '7':
            run_python_script('manage_users.py', 'disable')
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
        
        print_section(f"Dominios")
        print_option(f"{Colors.CYAN}7{Colors.RESET} - Ver dominios activos (query_domains.py)")
        
        print_section(f"Peligro")
        print_option(f"{Colors.RED}8{Colors.RESET} - Eliminar servicio")
        
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
            run_python_script('query_domains.py')
            pause()
        elif choice == '8':
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
        
        print_section("Gestión de VPS (Avanzado)")
        print_option(f"{Colors.MAGENTA}7{Colors.RESET} - Menú de control VPS (vps.py)")
        
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
        elif choice == '7':
            run_python_script('vps.py')
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
    print(f"  Backend: {BACKEND_DIR} {'[OK]' if BACKEND_DIR.exists() else '[X]'}")
    print(f"  Frontend: {FRONTEND_DIR} {'[OK]' if FRONTEND_DIR.exists() else '[X]'}")
    
    print(f"\n{Colors.BOLD}Node.js:{Colors.RESET}")
    node_exe = shutil.which('node')
    if node_exe:
        try:
            result = subprocess.run([node_exe, '--version'], capture_output=True, text=True)
            print(f"  Version: {result.stdout.strip()}")
            print(f"  Path: {node_exe}")
        except:
            print("  Instalado (Error al obtener version)")
    else:
        print("  No instalado")
    
    print(f"\n{Colors.BOLD}PostgreSQL:{Colors.RESET}")
    psql_exe = shutil.which('psql')
    if psql_exe:
        try:
            result = subprocess.run([psql_exe, '--version'], capture_output=True, text=True)
            print(f"  Version: {result.stdout.strip()}")
            print(f"  Path: {psql_exe}")
        except:
            print("  Instalado (Error al obtener version)")
    else:
        print("  No instalado")
    
    pause()

def show_help():
    """Menú de ayuda"""
    clear_screen()
    print_header("AYUDA")
    
    print(f"{Colors.BOLD}Descripción:{Colors.RESET}")
    print("  Lanzador universal multiplataforma para gestionar desarrollo")
    
    print(f"\n{Colors.BOLD}Funcionalidades:{Colors.RESET}")
    print(f"  {Colors.CHECK} Configuracion de base de datos con presets")
    print(f"  {Colors.CHECK} Gestor de datos y usuarios")
    print(f"  {Colors.CHECK} Gestion de servicios Nginx (Django, React)")
    print(f"  {Colors.CHECK} Actualizacion de dependencias")
    print(f"  {Colors.CHECK} Generador de secrets seguro")
    print(f"  {Colors.CHECK} Reset seguro de sistema (sin joder VPS)")
    print(f"  {Colors.CHECK} Verificacion de salud del sistema")
    
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
