import json
import paho.mqtt.client as mqtt

# Configuración del broker MQTT
BROKER_HOST = "test.mosquitto.org"  # Broker público para pruebas. Se puede cambiar a localhost si se usa uno propio.
BROKER_PORT = 1883
TOPIC_SUBSCRIPTION = "planta/+/sensores"  # El '+' permite suscribirse a cualquier planta (ej. planta/1/sensores)
TOPIC_ACTUADORES = "planta/{}/actuadores"  # Para enviar a LCD/Semaforo en Nodo 2

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print(f"[OK] Conectado al broker MQTT en {BROKER_HOST}:{BROKER_PORT}")
        # Suscribirse al topic al conectarse (o reconectarse)
        client.subscribe(TOPIC_SUBSCRIPTION)
        print(f"[INFO] Suscrito a: {TOPIC_SUBSCRIPTION}")
    else:
        print(f"[ERROR] Fallo al conectar. Código de razón: {reason_code}")

def on_message(client, userdata, msg):
    """
    Función que se ejecuta cuando se recibe un mensaje de los nodos.
    Se espera que el payload sea en formato JSON.
    """
    try:
        # Decodificar payload a JSON
        payload_str = msg.payload.decode("utf-8")
        datos = json.loads(payload_str)
        
        print(f"\n[DATOS RECIBIDOS] Topic: {msg.topic}")
        print("-" * 30)
        #TODO: Procesar de forma diferente según el tipo de nodo (fotovoltaico, temp/humedad)
        # o guardarlo en una Base de Datos y usarlo para la web / gráficas.
        
        for key, value in datos.items():
            print(f"  {key}: {value}")
            
        print("-" * 30)

        #TODO: Lógica de control para determinar si enviar mensaje al Nodo 2 (LCD/LED Semaforo)
        # Ejemplo: si humedad < 20, enviar advertencia
        # check_and_notify_node2(client, "1", datos)

    except json.JSONDecodeError:
        print(f"[ERROR] El mensaje recibido en {msg.topic} no es un JSON válido: {msg.payload}")
    except Exception as e:
        print(f"[ERROR] Error inesperado al procesar mensaje: {e}")

# //TODO: Implementar función check_and_notify_node2 para mandar mensaje a Node 2


def main():
    print("Iniciando Servidor de Monitorización...")
    
    # Creamos el cliente MQTT (Version 2 para paho-mqtt >= 2.0.0)
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="Servidor_Monitorizacion")
    
    # Asignamos las funciones de callback
    client.on_connect = on_connect
    client.on_message = on_message
    
    try:
        # Intentamos conectar al broker
        client.connect(BROKER_HOST, BROKER_PORT, 60)
        
        # Mantenemos el cliente en bucle para escuchar mensajes
        client.loop_forever()
        
    except KeyboardInterrupt:
        print("\n[INFO] Servidor detenido por el usuario (Ctrl+C).")
        client.disconnect()
    except Exception as e:
        print(f"[ERROR] No se pudo iniciar el servidor: {e}")

if __name__ == "__main__":
    main()
