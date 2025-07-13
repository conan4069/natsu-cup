#!/usr/bin/env python3
"""
Script de prueba para verificar el guardado de resultados de partidos
"""

import requests
import json

# Configuración
BASE_URL = "http://localhost:8000/api"
TOURNAMENT_ID = 1  # Ajustar según el ID del torneo
MATCH_ID = 1       # Ajustar según el ID del partido

def test_save_match_result():
    """Prueba guardar un resultado de partido"""
    
    # Datos de prueba
    test_data = {
        "goals": {
            "1": 2,  # Team 1 scores 2
            "2": 1   # Team 2 scores 1
        }
    }
    
    print(f"Probando guardar resultado para partido {MATCH_ID}")
    print(f"Datos a enviar: {json.dumps(test_data, indent=2)}")
    
    try:
        # Hacer la petición
        response = requests.post(
            f"{BASE_URL}/matches/{MATCH_ID}/save-result/",
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Resultado guardado exitosamente")
        else:
            print("❌ Error al guardar resultado")
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

def test_get_match():
    """Prueba obtener un partido"""
    
    try:
        response = requests.get(f"{BASE_URL}/matches/{MATCH_ID}/")
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            match_data = response.json()
            print(f"Match data: {json.dumps(match_data, indent=2)}")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

if __name__ == "__main__":
    print("=== Prueba de Guardado de Resultados de Partidos ===")
    
    print("\n1. Obteniendo datos del partido...")
    test_get_match()
    
    print("\n2. Probando guardar resultado...")
    test_save_match_result()
    
    print("\n3. Verificando resultado guardado...")
    test_get_match() 