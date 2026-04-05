#!/usr/bin/env python
# ========================================================================
# CONFIGURADOR DE NGINX Y SERVICIOS
# ========================================================================
# Gestión de Nginx, servicios systemd, y logs
# Lee configuración de .env y crea servicios systemd
# Uso: python scripts_utiles/nginx_config.py

import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).parent.parent
ENV_FILE = PROJECT_ROOT / '.env'

# Cargar .env
load_dotenv(ENV_FILE)

# ========================================================================
# COLORES Y ESTILOS
# ========================================================================
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

def print_header(text):
    print(f"\n{Colors.CYAN}{'='*70}{Colors.ENDC}")
    print(f"{Colors.CYAN}{Colors.BOLD}✦ {text}{Colors.ENDC}")
    print(f"{Colors.CYAN}{'='*70}{Colors.ENDC}\n")

def print_success(text):
    print(f"{Colors.GREEN}✓{Colors.ENDC} {text}")

def print_error(text):
    print(f"{Colors.RED}✗{Colors.ENDC} {text}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ{Colors.ENDC} {text}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠{Colors.ENDC} {text}")

# ========================================================================
# CARGAR CONFIGURACIÓN DE .ENV
# ========================================================================

def get_env_config():
    """Obtiene configuración de .env"""
    config = {
        'DJANGO_PORT': os.getenv('DJANGO_PORT', '8001'),
        'REACT_PORT': os.getenv('REACT_PORT', '3000'),
        'NGINX_PORT': os.getenv('NGINX_PORT', '80'),
        'ENVIRONMENT': os.getenv('ENVIRONMENT', 'development'),
        'DOMAIN_MAIN': os.getenv('DOMAIN_MAIN', 'localhost'),
        'DATABASE_HOST': os.getenv('DATABASE_HOST', '127.0.0.1'),
        'DATABASE_PORT': os.getenv('DATABASE_PORT', '5432'),
        'DATABASE_NAME': os.getenv('DATABASE_NAME', 'mi_saas_db'),
        'DATABASE_USER': os.getenv('DATABASE_USER', 'postgres'),
    }
    return config

def show_env_config():
    """Muestra la configuración del .env"""
    print_header("CONFIGURACIÓN DESDE .env")
    
    config = get_env_config()
    
    print(f"{Colors.BOLD}Servicios:{Colors.ENDC}")
    print(f"  Django Port:    {Colors.YELLOW}{config['DJANGO_PORT']}{Colors.ENDC}")
    print(f"  React Port:     {Colors.YELLOW}{config['REACT_PORT']}{Colors.ENDC}")
    print(f"  Nginx Port:     {Colors.YELLOW}{config['NGINX_PORT']}{Colors.ENDC}")
    
    print(f"\n{Colors.BOLD}Ambiente:{Colors.ENDC}")
    print(f"  Environment:    {Colors.CYAN}{config['ENVIRONMENT']}{Colors.ENDC}")
    print(f"  Domain:         {Colors.CYAN}{config['DOMAIN_MAIN']}{Colors.ENDC}")
    
    print(f"\n{Colors.BOLD}Base de Datos:{Colors.ENDC}")
    print(f"  Host:           {Colors.CYAN}{config['DATABASE_HOST']}{Colors.ENDC}")
    print(f"  Port:           {Colors.CYAN}{config['DATABASE_PORT']}{Colors.ENDC}")
    print(f"  Database:       {Colors.CYAN}{config['DATABASE_NAME']}{Colors.ENDC}")
    print(f"  User:           {Colors.CYAN}{config['DATABASE_USER']}{Colors.ENDC}")
    print()

# ========================================================================
# CREAR SERVICIOS
# ========================================================================

def service_exists(service_name):
    """Verifica si un servicio ya existe"""
    result = subprocess.run(['systemctl', 'list-unit-files', service_name + '.service'], 
                          capture_output=True, text=True)
    return service_name in result.stdout

def create_django_service():
    """Crea servicio systemd para Django"""
    print_header("CREAR SERVICIO DJANGO")
    
    if os.geteuid() != 0:
        print_error("Debes ejecutar como root (sudo)")
        return
    
    config = get_env_config()
    show_env_config()
    
    print(f"{Colors.BOLD}Servicio a crear:{Colors.ENDC}")
    print(f"  Nombre:         {Colors.YELLOW}django_saas{Colors.ENDC}")
    print(f"  Puerto:         {Colors.YELLOW}{config['DJANGO_PORT']}{Colors.ENDC}")
    print(f"  Usuario:        {Colors.YELLOW}www-data{Colors.ENDC}")
    print()
    
    service_name = "django_saas"
    service_file = f"/etc/systemd/system/{service_name}.service"
    
    confirm = input(f"{Colors.BOLD}¿Crear/Reemplazar servicio? (s/n): {Colors.ENDC}").lower()
    
    if confirm != 's':
        print_warning("Cancelado")
        return
    
    django_port = config['DJANGO_PORT']
    project_path = str(PROJECT_ROOT)
    
    service_content = f"""[Unit]
Description=Django SaaS Application
After=network.target postgresql.service

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory={project_path}/backend
Environment="PATH={project_path}/backend/venv/bin"
ExecStart={project_path}/backend/venv/bin/python manage.py runserver 0.0.0.0:{django_port}
Restart=on-failure
RestartSec=5s
StandardOutput=append:/var/log/django_saas.log
StandardError=append:/var/log/django_saas_error.log

[Install]
WantedBy=multi-user.target
"""
    
    try:
        # Detener servicio si existe
        if service_exists(service_name):
            print_info(f"Deteniendo servicio existente {service_name}...")
            subprocess.run(['systemctl', 'stop', service_name], timeout=10)
        
        # Crear/reemplazar archivo
        with open(service_file, 'w') as f:
            f.write(service_content)
        
        # Reload systemctl
        subprocess.run(['systemctl', 'daemon-reload'], check=True)
        print_success(f"Servicio creado/reemplazado: {service_file}")
        
        if input(f"\n{Colors.BOLD}¿Habilitar al iniciar? (s/n): {Colors.ENDC}").lower() == 's':
            subprocess.run(['systemctl', 'enable', service_name], check=True)
            print_success(f"{service_name} habilitado al inicio")
        
        if input(f"{Colors.BOLD}¿Iniciar servicio ahora? (s/n): {Colors.ENDC}").lower() == 's':
            subprocess.run(['systemctl', 'start', service_name], check=True)
            print_success(f"{service_name} iniciado")
            
    except Exception as e:
        print_error(f"Error: {str(e)}")

def create_frontend_service():
    """Crea servicio systemd para Frontend (React)"""
    print_header("CREAR SERVICIO FRONTEND (REACT)")
    
    if os.geteuid() != 0:
        print_error("Debes ejecutar como root (sudo)")
        return
    
    config = get_env_config()
    show_env_config()
    
    print(f"{Colors.BOLD}Servicio a crear:{Colors.ENDC}")
    print(f"  Nombre:         {Colors.YELLOW}frontend_saas{Colors.ENDC}")
    print(f"  Puerto:         {Colors.YELLOW}{config['REACT_PORT']}{Colors.ENDC}")
    print(f"  Usuario:        {Colors.YELLOW}www-data{Colors.ENDC}")
    print()
    
    service_name = "frontend_saas"
    service_file = f"/etc/systemd/system/{service_name}.service"
    
    confirm = input(f"{Colors.BOLD}¿Crear/Reemplazar servicio? (s/n): {Colors.ENDC}").lower()
    
    if confirm != 's':
        print_warning("Cancelado")
        return
    
    react_port = config['REACT_PORT']
    project_path = str(PROJECT_ROOT)
    
    service_content = f"""[Unit]
Description=React Frontend SaaS
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory={project_path}/frontend
Environment="PATH={project_path}/frontend/node_modules/.bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin"
Environment="PORT={react_port}"
ExecStart=/usr/bin/npm start
Restart=on-failure
RestartSec=5s
StandardOutput=append:/var/log/frontend_saas.log
StandardError=append:/var/log/frontend_saas_error.log

[Install]
WantedBy=multi-user.target
"""
    
    try:
        # Detener servicio si existe
        if service_exists(service_name):
            print_info(f"Deteniendo servicio existente {service_name}...")
            subprocess.run(['systemctl', 'stop', service_name], timeout=10)
        
        # Crear/reemplazar archivo
        with open(service_file, 'w') as f:
            f.write(service_content)
        
        # Reload systemctl
        subprocess.run(['systemctl', 'daemon-reload'], check=True)
        print_success(f"Servicio creado/reemplazado: {service_file}")
        
        if input(f"\n{Colors.BOLD}¿Habilitar al iniciar? (s/n): {Colors.ENDC}").lower() == 's':
            subprocess.run(['systemctl', 'enable', service_name], check=True)
            print_success(f"{service_name} habilitado al inicio")
        
        if input(f"{Colors.BOLD}¿Iniciar servicio ahora? (s/n): {Colors.ENDC}").lower() == 's':
            subprocess.run(['systemctl', 'start', service_name], check=True)
            print_success(f"{service_name} iniciado")
            
    except Exception as e:
        print_error(f"Error: {str(e)}")

def delete_service():
    """Elimina un servicio systemd"""
    print_header("ELIMINAR SERVICIO")
    
    if os.geteuid() != 0:
        print_error("Debes ejecutar como root (sudo)")
        return
    
    print("1. Eliminar Django service (django_saas)")
    print("2. Eliminar Frontend service (frontend_saas)")
    print("0. Cancelar")
    print()
    
    choice = input("Selecciona: ").strip()
    
    services = {
        '1': 'django_saas',
        '2': 'frontend_saas',
    }
    
    if choice not in services:
        print_warning("Cancelado")
        return
    
    service_name = services[choice]
    service_file = f"/etc/systemd/system/{service_name}.service"
    
    confirm = input(f"\n{Colors.RED}¿ELIMINAR {service_name}? (s/n): {Colors.ENDC}").lower()
    
    if confirm != 's':
        print_warning("Cancelado")
        return
    
    try:
        # Detener servicio
        print_info(f"Deteniendo {service_name}...")
        subprocess.run(['systemctl', 'stop', service_name], timeout=10)
        
        # Desabilitar
        subprocess.run(['systemctl', 'disable', service_name], timeout=10)
        
        # Eliminar archivo
        os.remove(service_file)
        
        # Reload systemctl
        subprocess.run(['systemctl', 'daemon-reload'], check=True)
        
        print_success(f"Servicio {service_name} eliminado")
        
    except Exception as e:
        print_error(f"Error: {str(e)}")

def view_service_status():
    """Ver estado de los servicios"""
    print_header("ESTADO DE SERVICIOS")
    
    services = ['django_saas', 'frontend_saas', 'nginx', 'postgresql']
    
    for service in services:
        try:
            result = subprocess.run(
                ['systemctl', 'is-active', service],
                capture_output=True,
                text=True,
                timeout=2
            )
            status = result.stdout.strip()
            
            if status == 'active':
                print(f"{Colors.GREEN}✓{Colors.ENDC} {service:<20} {Colors.GREEN}ACTIVO{Colors.ENDC}")
            else:
                print(f"{Colors.RED}✗{Colors.ENDC} {service:<20} {Colors.RED}{status.upper()}{Colors.ENDC}")
        except subprocess.TimeoutExpired:
            print(f"{Colors.YELLOW}⚠{Colors.ENDC} {service:<20} {Colors.YELLOW}TIMEOUT{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.YELLOW}?{Colors.ENDC} {service:<20} No disponible")
    
    print()

def view_logs():
    """Ver logs de servicios"""
    print_header("VER LOGS")
    
    print("1. Django logs")
    print("2. Frontend logs")
    print("3. Nginx error logs")
    print("4. Nginx access logs")
    print("5. PostgreSQL logs")
    print()
    
    choice = input("Selecciona log a ver: ").strip()
    
    logs = {
        '1': '/var/log/django_saas.log',
        '2': '/var/log/frontend_saas.log',
        '3': '/var/log/nginx/error.log',
        '4': '/var/log/nginx/access.log',
        '5': '/var/log/postgresql/postgresql.log',
    }
    
    if choice in logs:
        log_file = logs[choice]
        
        if os.path.exists(log_file):
            print(f"\n{Colors.CYAN}Últimas 50 líneas de {log_file}:{Colors.ENDC}\n")
            
            try:
                result = subprocess.run(
                    ['tail', '-50', log_file],
                    capture_output=True,
                    text=True
                )
                print(result.stdout)
            except Exception as e:
                print_error(f"Error al leer log: {str(e)}")
        else:
            print_warning(f"Log no existe: {log_file}")
    else:
        print_error("Opción inválida")

def reload_nginx():
    """Recarga configuración de Nginx"""
    print_header("RECARGAR NGINX")
    
    if os.geteuid() != 0:
        print_error("Debes ejecutar como root (sudo)")
        return
    
    try:
        print_info("Verificando configuración...")
        result = subprocess.run(['nginx', '-t'], capture_output=True, text=True)
        
        if result.returncode == 0:
            print_success("Configuración válida")
            print_info("Recargando Nginx...")
            subprocess.run(['systemctl', 'reload', 'nginx'], check=True)
            print_success("Nginx recargado")
        else:
            print_error("Configuración inválida")
            print(result.stderr)
    except Exception as e:
        print_error(f"Error: {str(e)}")

def restart_service():
    """Reinicia un servicio"""
    print_header("REINICIAR SERVICIO")
    
    if os.geteuid() != 0:
        print_error("Debes ejecutar como root (sudo)")
        return
    
    print("1. Django")
    print("2. Frontend")
    print("3. Nginx")
    print("4. PostgreSQL")
    print("5. Todos")
    print()
    
    choice = input("Selecciona servicio: ").strip()
    
    services = {
        '1': 'django_saas',
        '2': 'frontend_saas',
        '3': 'nginx',
        '4': 'postgresql',
        '5': ['django_saas', 'frontend_saas', 'nginx', 'postgresql'],
    }
    
    if choice in services:
        svcs = services[choice] if isinstance(services[choice], list) else [services[choice]]
        
        for svc in svcs:
            try:
                print_info(f"Reiniciando {svc}...")
                subprocess.run(['systemctl', 'restart', svc], check=True)
                print_success(f"{svc} reiniciado")
            except subprocess.CalledProcessError:
                print_error(f"Error reiniciando {svc}")
    else:
        print_error("Opción inválida")

def main():
    if len(sys.argv) < 2:
        print_header("CONFIGURADOR DE NGINX Y SERVICIOS")
        
        print("1. Crear servicio Django (o reemplazar)")
        print("2. Crear servicio Frontend (o reemplazar)")
        print("3. Eliminar servicio")
        print("4. Ver estado de servicios")
        print("5. Ver logs")
        print("6. Recargar Nginx")
        print("7. Reiniciar servicio")
        print("0. Salir")
        print()
        
        choice = input("Selecciona opción: ").strip()
        
        if choice == '1':
            create_django_service()
        elif choice == '2':
            create_frontend_service()
        elif choice == '3':
            delete_service()
        elif choice == '4':
            view_service_status()
        elif choice == '5':
            view_logs()
        elif choice == '6':
            reload_nginx()
        elif choice == '7':
            restart_service()
    else:
        cmd = sys.argv[1]
        
        if cmd == 'django-service':
            create_django_service()
        elif cmd == 'frontend-service':
            create_frontend_service()
        elif cmd == 'delete-service':
            delete_service()
        elif cmd == 'status':
            view_service_status()
        elif cmd == 'logs':
            view_logs()
        elif cmd == 'reload-nginx':
            reload_nginx()
        elif cmd == 'restart':
            restart_service()

if __name__ == '__main__':
    main()
