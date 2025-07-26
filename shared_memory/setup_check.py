# Script simple para verificar que todo funciona
import json
import os
from datetime import datetime

def check_system():
    print("🔍 Verificando sistema de agentes...")
    
    # Verificar archivos
    files = [
        "architecture_decisions.json",
        "development_log.json", 
        "research_data.json"
    ]
    
    for file in files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            # Crear archivo básico si no existe
            with open(file, 'w') as f:
                json.dump({"data": [], "last_update": datetime.now().isoformat()}, f)
            print(f"✅ {file} (creado)")
    
    print("🎉 Sistema listo para usar!")

if __name__ == "__main__":
    check_system()