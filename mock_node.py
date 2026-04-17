import time
import json
import random
import paho.mqtt.client as mqtt

BROKER_HOST = "127.0.0.1"
BROKER_PORT = 1883
# Vamos a simular que somos el "Nodo 1" de la "Planta 1"
TOPIC_PUBLISH = "planta/1/sensores"

def main():
    print(f"Iniciando Nodo Simulado (Planta 1)... conectando a {BROKER_HOST}:{BROKER_PORT}")
    
    # Creamos cliente (usamos VERSION2 por si acaso, igual que en el server.py)
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="Nodo1_Mock_Planta1")
    
    try:
        client.connect(BROKER_HOST, BROKER_PORT, 60)
        client.loop_start()  # Iniciar hilo de red en segundo plano
        
        while True:
            # Generamos datos aleatorios simulando los 3 sensores requeridos
            datos_simulados = {
                "luz": random.randint(50, 4095),           # ADC crudo LDR (0-4095)
                "temperatura_aire": round(random.uniform(15.0, 38.0), 2),  # °C directo del DHT
                "humedad_aire": round(random.uniform(30.0, 80.0), 2),      # % directo del DHT
                "humedad_suelo": random.randint(1200, 3690),  # ADC crudo: 1200=mojado, 3690=seco
            }
            
            payload = json.dumps(datos_simulados)
            
            print(f"[ENVIANDO] Topic: {TOPIC_PUBLISH} | Datos: {payload}")
            client.publish(TOPIC_PUBLISH, payload)
            
            # Enviar cada 5 segundos
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\n[INFO] Deteniendo el nodo simulado (Ctrl+C).")
        client.loop_stop()
        client.disconnect()
    except Exception as e:
        print(f"[ERROR] Error de conexión: {e}")

if __name__ == "__main__":
    main()
