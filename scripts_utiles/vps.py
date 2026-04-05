#!/usr/bin/env python
# ========================================================================
# SCRIPT VPS - HERRAMIENTAS DE ADMINISTRACIÓN
# ========================================================================
# Gestiona configuración de VPS: usuarios, dominios, servicios, etc.
# Uso: python scripts_utiles/vps.py [comando]

import os
import sys
import subprocess
import platform
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

def is_linux():
    """Verifica si es Linux/Unix"""
    return platform.system() in ['Linux', 'Darwin']

def is_root():
    """Verifica si corre como root"""
    if is_linux():
        return os.geteuid() == 0
    return False

def create_user(username, password, home_dir=None):
    """Crea usuario del sistema"""
    if not is_linux():
        print("[ERROR] Este comando solo funciona en Linux")
        return False
    
    if not is_root():
        print("[ERROR] Debes ejecutar como root (sudo)")
        return False
    
    print(f"[+] Creando usuario: {username}")
    
    if home_dir:
        cmd = f"useradd -d {home_dir} -s /bin/bash -m {username}"
    else:
        cmd = f"useradd -s /bin/bash -m {username}"
    
    result = subprocess.run(cmd, shell=True)
    
    if result.returncode == 0:
        print(f"[OK] Usuario {username} creado")
        print(f"[+] Configurando contraseña...")
        subprocess.run(f"echo '{username}:{password}' | chpasswd", shell=True)
        print(f"[OK] Contraseña configurada")
        return True
    return False

def create_domain(domain, ip, vps_dir):
    """Crea configuración de dominio"""
    if not is_linux():
        print("[ERROR] Este comando solo funciona en Linux")
        return False
    
    print(f"[+] Creando dominio: {domain}")
    
    # Crear directorio
    domain_dir = Path(vps_dir) / domain
    domain_dir.mkdir(parents=True, exist_ok=True)
    
    # HTML básico
    html_file = domain_dir / 'index.html'
    with open(html_file, 'w') as f:
        f.write(f"""<!DOCTYPE html>
<html>
<head>
    <title>{domain}</title>
</head>
<body>
    <h1>Dominio: {domain}</h1>
    <p>Configurado correctamente en {ip}</p>
    <p>Timestamp: $(date)</p>
</body>
</html>""")
    
    print(f"[OK] Directorio creado: {domain_dir}")
    print(f"[i] HTML: {html_file}")
    
    return str(domain_dir)

def setup_nginx_ssl(domain, vps_dir):
    """Instala certificado SSL con Let's Encrypt"""
    if not is_linux():
        print("[ERROR] Este comando solo funciona en Linux")
        return False
    
    if not is_root():
        print("[ERROR] Debes ejecutar como root (sudo)")
        return False
    
    print(f"[+] Instalando SSL para {domain}...")
    
    # Verificar que certbot esté instalado
    result = subprocess.run("which certbot", shell=True, capture_output=True)
    if result.returncode != 0:
        print("[!] certbot no está instalado. Instalando...")
        subprocess.run("apt-get install -y certbot python3-certbot-nginx", shell=True)
    
    # Obtener certificado
    cmd = f"certbot certonly --nginx -d {domain} --agree-tos -m admin@{domain} --non-interactive"
    result = subprocess.run(cmd, shell=True)
    
    if result.returncode == 0:
        print(f"[OK] SSL configurado para {domain}")
        return True
    else:
        print(f"[ERROR] No se pudo instalar SSL")
        return False

def check_services():
    """Verifica estado de servicios"""
    if not is_linux():
        print("[ERROR] Este comando solo funciona en Linux")
        return
    
    services = ['nginx', 'postgresql', 'supervisor']
    
    print("\n" + "="*50)
    print("ESTADO DE SERVICIOS")
    print("="*50)
    
    for service in services:
        result = subprocess.run(
            f"systemctl is-active {service}",
            shell=True,
            capture_output=True,
            text=True
        )
        status = "✓ ACTIVO" if result.returncode == 0 else "✗ INACTIVO"
        print(f"  {service:<20} {status}")
    
    print("="*50 + "\n")

def reload_nginx():
    """Recarga configuración de nginx"""
    if not is_linux():
        print("[ERROR] Este comando solo funciona en Linux")
        return
    
    if not is_root():
        print("[ERROR] Debes ejecutar como root (sudo)")
        return
    
    print("[+] Recargando nginx...")
    result = subprocess.run("nginx -t && nginx -s reload", shell=True)
    
    if result.returncode == 0:
        print("[OK] Nginx recargado")
    else:
        print("[ERROR] Error al recargar nginx")

def restart_services():
    """Reinicia servicios principales"""
    if not is_linux():
        print("[ERROR] Este comando solo funciona en Linux")
        return
    
    if not is_root():
        print("[ERROR] Debes ejecutar como root (sudo)")
        return
    
    services = ['nginx', 'supervisor']
    
    for service in services:
        print(f"[+] Reiniciando {service}...")
        subprocess.run(f"systemctl restart {service}", shell=True)
    
    print("[OK] Servicios reiniciados")

def show_logs():
    """Muestra logs de servicios"""
    if not is_linux():
        print("[ERROR] Este comando solo funciona en Linux")
        return
    
    print("[+] Logs de nginx (últimas 20 líneas):")
    subprocess.run("tail -20 /var/log/nginx/error.log", shell=True)
    
    print("\n[+] Logs de supervisor:")
    subprocess.run("tail -20 /var/log/supervisor/supervisord.log", shell=True)

def main():
    if len(sys.argv) < 2:
        print("Uso: python vps.py [comando] [args]")
        print("\nComandos disponibles (Linux/VPS):")
        print("  user CREATE user password  - Crear usuario del sistema")
        print("  domain CREATE domain ip dir - Crear configuración de dominio")
        print("  ssl SETUP domain           - Instalar SSL (Let's Encrypt)")
        print("  services STATUS            - Ver estado de servicios")
        print("  services RELOAD            - Recargar nginx")
        print("  services RESTART           - Reiniciar servicios")
        print("  logs SHOW                  - Mostrar logs")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == 'user' and len(sys.argv) >= 4:
        subcmd = sys.argv[2]
        if subcmd == 'CREATE' and len(sys.argv) >= 5:
            create_user(sys.argv[3], sys.argv[4])
    
    elif cmd == 'domain' and len(sys.argv) >= 4:
        subcmd = sys.argv[2]
        if subcmd == 'CREATE' and len(sys.argv) >= 6:
            create_domain(sys.argv[3], sys.argv[4], sys.argv[5])
    
    elif cmd == 'ssl' and len(sys.argv) >= 4:
        subcmd = sys.argv[2]
        if subcmd == 'SETUP' and len(sys.argv) >= 4:
            setup_nginx_ssl(sys.argv[3], '/var/www')
    
    elif cmd == 'services' and len(sys.argv) >= 3:
        subcmd = sys.argv[2]
        if subcmd == 'STATUS':
            check_services()
        elif subcmd == 'RELOAD':
            reload_nginx()
        elif subcmd == 'RESTART':
            restart_services()
    
    elif cmd == 'logs' and len(sys.argv) >= 3:
        subcmd = sys.argv[2]
        if subcmd == 'SHOW':
            show_logs()
    
    else:
        print(f"[ERROR] Comando o argumentos inválidos")
        sys.exit(1)

if __name__ == '__main__':
    main()
