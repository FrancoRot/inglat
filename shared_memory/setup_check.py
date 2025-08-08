# Script simple para verificar que todo funciona
import json
import os
from datetime import datetime

def check_system():
    print("🔍 Verificando sistema de agentes...")
    
    # Obtener directorio actual del script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Verificar archivos
    files = [
        "architecture_decisions.json",
        "development_log.json", 
        "research_data.json"
    ]
    
    for file in files:
        file_path = os.path.join(script_dir, file)
        if os.path.exists(file_path):
            # Verificar si el archivo tiene contenido válido
            try:
                with open(file_path, 'r') as f:
                    content = f.read().strip()
                    if content:
                        json.loads(content)
                        print(f"✅ {file}")
                    else:
                        raise ValueError("Archivo vacío")
            except (json.JSONDecodeError, ValueError):
                # Recrear archivo con estructura básica
                with open(file_path, 'w') as f:
                    json.dump({"data": [], "last_update": datetime.now().isoformat()}, f, indent=2)
                print(f"✅ {file} (reparado)")
        else:
            # Crear archivo básico si no existe
            with open(file_path, 'w') as f:
                json.dump({"data": [], "last_update": datetime.now().isoformat()}, f, indent=2)
            print(f"✅ {file} (creado)")
    
    print("🎉 Sistema listo para usar!")

if __name__ == "__main__":
    check_system()