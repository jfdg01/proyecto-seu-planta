import json
import paho.mqtt.client as mqtt

# Configuración del broker MQTT
# Requisito 4: Comunicación mediante MQTT
# Sugerencia: Uso de Docker y Docker Compose para orquestar el broker MQTT
BROKER_HOST = "127.0.0.1"  # Broker local orquestado por Docker
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
        
        for key, value in datos.items():
            print(f"  {key}: {value}")
            
        print("-" * 30)

        # //TODO: Requisito 6 - Base de Datos (InfluxDB)
        # Almacenar los datos de 'datos' como serie temporal para análisis histórico.
        
        # //TODO: Requisito 8 - Notificaciones y Alertas Automáticas
        # Evaluar 'datos' y si se excede un umbral, enviar notificación/alerta al dashboard.
        
        # //TODO: Lógica de interacción con Nodo 2
        # Si hay un error, enviar un mensaje MQTT a TOPIC_ACTUADORES para actualizar LCD/Semáforo.

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
