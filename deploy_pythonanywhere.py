#!/usr/bin/env python3
"""
Script para automatizar el deploy en PythonAnywhere
Actualiza código, dependencias, migraciones y archivos estáticos
"""
import requests
import time
import json
import sys
import os

class PythonAnywhereDeployer:
    def __init__(self, username, api_token, console_id):
        self.username = username
        self.api_token = api_token
        self.console_id = console_id
        self.base_url = f"https://www.pythonanywhere.com/api/v0/user/{username}"
        self.headers = {
            'Authorization': f'Token {api_token}',
            'Content-Type': 'application/json'
        }

    def send_command(self, command, wait_time=3):
        """Envía un comando al bash console de PythonAnywhere"""
        console_url = f"{self.base_url}/consoles/{self.console_id}/send_input/"

        payload = {
            'input': command + '\n'
        }

        print(f"📤 Ejecutando: {command}")

        try:
            response = requests.post(console_url, headers=self.headers, json=payload)

            if response.status_code == 200:
                print(f"✅ Comando enviado exitosamente")
                time.sleep(wait_time)  # Esperar a que se ejecute
                return True
            else:
                print(f"❌ Error al enviar comando: {response.status_code}")
                print(f"Respuesta: {response.text}")
                return False

        except requests.exceptions.RequestException as e:
            print(f"❌ Error de conexión: {e}")
            return False

    def get_console_output(self):
        """Obtiene el output del console"""
        console_url = f"{self.base_url}/consoles/{self.console_id}/get_latest_output/"

        try:
            response = requests.get(console_url, headers=self.headers)
            if response.status_code == 200:
                return response.json().get('output', '')
            else:
                print(f"❌ Error al obtener output: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Error de conexión: {e}")
            return None

    def reload_webapp(self, domain_name):
        """Reinicia la aplicación web"""
        webapp_url = f"{self.base_url}/webapps/{domain_name}/reload/"

        print(f"🔄 Reiniciando webapp: {domain_name}")

        try:
            response = requests.post(webapp_url, headers=self.headers)

            if response.status_code == 200:
                print(f"✅ Webapp reiniciada exitosamente")
                return True
            else:
                print(f"❌ Error al reiniciar webapp: {response.status_code}")
                print(f"Respuesta: {response.text}")
                return False

        except requests.exceptions.RequestException as e:
            print(f"❌ Error de conexión: {e}")
            return False

    def deploy(self, project_path="/home/INGLAT/inglat", domain_name="inglat.pythonanywhere.com"):
        """Ejecuta el proceso completo de deploy"""
        print("🚀 Iniciando proceso de deploy en PythonAnywhere...")
        print("=" * 50)

        # Lista de comandos a ejecutar
        commands = [
            f"cd {project_path}",
            "pwd",  # Verificar directorio
            "cp db.sqlite3 db.sqlite3.backup",  # Backup BD
            "git pull origin main",  # Actualizar código
            "pip3.10 install --user -r requirements.txt",  # Instalar dependencias
            "python3.10 manage.py makemigrations",  # Crear migraciones
            "python3.10 manage.py migrate",  # Aplicar migraciones
            "python3.10 manage.py collectstatic --noinput",  # Archivos estáticos
            "echo '✅ Deploy completado - Código actualizado'"
        ]

        # Ejecutar comandos secuencialmente
        for i, command in enumerate(commands, 1):
            print(f"\n[{i}/{len(commands)}] {command}")

            if not self.send_command(command, wait_time=5):
                print("❌ Error en el comando, abortando deploy")
                return False

            # Mostrar output para comandos importantes
            if command in ["git pull origin main", "python3.10 manage.py migrate"]:
                time.sleep(2)
                output = self.get_console_output()
                if output:
                    print(f"📋 Output:\n{output[-500:]}")  # Últimas 500 chars

        print("\n" + "=" * 50)
        print("🔄 Reiniciando aplicación web...")

        # Reiniciar webapp
        if self.reload_webapp(domain_name):
            print("🎉 ¡Deploy completado exitosamente!")
            print(f"🌐 Tu sitio está actualizado en: https://{domain_name}")
            return True
        else:
            print("⚠️ Código actualizado pero falló el reinicio de webapp")
            print("Reinicia manualmente desde el dashboard de PythonAnywhere")
            return False

def main():
    # Configuración
    USERNAME = "INGLAT"
    CONSOLE_ID = "41762790"
    DOMAIN_NAME = "inglat.pythonanywhere.com"

    # Obtener API token
    api_token = input("🔑 Ingresa tu API Token de PythonAnywhere: ").strip()

    if not api_token:
        print("❌ API Token requerido")
        sys.exit(1)

    # Crear deployer y ejecutar
    deployer = PythonAnywhereDeployer(USERNAME, api_token, CONSOLE_ID)

    print(f"🎯 Usuario: {USERNAME}")
    print(f"🖥️ Console: {CONSOLE_ID}")
    print(f"🌐 Dominio: {DOMAIN_NAME}")
    print("\n¿Continuar con el deploy? (y/N): ", end="")

    if input().lower() in ['y', 'yes', 's', 'si']:
        deployer.deploy()
    else:
        print("❌ Deploy cancelado")

if __name__ == "__main__":
    main()