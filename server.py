import json
import paho.mqtt.client as mqtt

class MQTTManager:
    """Clase encargada de la comunicación MQTT con el broker."""
    def __init__(self, host, port, on_message_callback):
        self.host = host
        self.port = port
        self.on_message_callback = on_message_callback
        
        # Tema general para escuchar sensores (ej: planta/1/sensores)
        self.topic_subscription = "planta/+/sensores"
        
        # Creamos el cliente MQTT (Version 2 para paho-mqtt >= 2.0.0)
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="Servidor_Monitorizacion")
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

    def _on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            print(f"[OK] Conectado al broker MQTT en {self.host}:{self.port}")
            self.client.subscribe(self.topic_subscription)
            print(f"[INFO] Suscrito a: {self.topic_subscription}")
        else:
            print(f"[ERROR] Fallo al conectar. Código de razón: {reason_code}")

    def _on_message(self, client, userdata, msg):
        try:
            payload_str = msg.payload.decode("utf-8")
            datos = json.loads(payload_str)
            # Pasamos los datos recibidos al callback proporcionado por el servidor
            self.on_message_callback(msg.topic, datos)
        except json.JSONDecodeError:
            print(f"[ERROR] El mensaje recibido en {msg.topic} no es un JSON válido: {msg.payload}")
        except Exception as e:
            print(f"[ERROR] Error inesperado al procesar mensaje: {e}")

    def connect_and_loop(self):
        try:
            self.client.connect(self.host, self.port, 60)
            self.client.loop_forever()
        except KeyboardInterrupt:
            print("\n[INFO] Servidor detenido por el usuario (Ctrl+C).")
            self.client.disconnect()
        except Exception as e:
            print(f"[ERROR] No se pudo iniciar el cliente MQTT: {e}")

    def publish(self, topic, payload):
        """Publica un mensaje (diccionario) en el topic indicado."""
        payload_str = json.dumps(payload)
        self.client.publish(topic, payload_str)
        print(f"[ENVIADO] Topic: {topic} | Payload: {payload_str}")


class DatabaseManager:
    """Clase para interactuar con InfluxDB u otra base de datos de series temporales."""
    # //TODO: Requisito 6 - Base de Datos (InfluxDB)
    def __init__(self, host, port, token, org, bucket):
        self.host = host
        self.port = port
        self.token = token
        self.org = org
        self.bucket = bucket
        # //TODO: Inicializar el cliente (instalar influxdb-client)
        # self.client = InfluxDBClient(...)
    
    def save_sensor_data(self, topic, data):
        # //TODO: Almacenar los datos de 'data' como serie temporal para análisis histórico.
        # Por ahora es solo un "placeholder" de la función
        pass


class DataAnalyzer:
    """Clase para procesar reglas de alertas, validar thresholds e implementar la lógica de negocio."""
    # //TODO: Requisito 8 - Notificaciones y Alertas Automáticas
    def __init__(self):
        # Inicialmente podemos establecer algún umbral de ejemplo
        self.temp_max = 35.0
        self.humedad_suelo_min = 20.0

    def check_thresholds(self, data):
        """
        Evalúa 'data' y si se excede un umbral, retorna el tipo de alerta.
        Retorna 'OK' si todo está correcto.
        """
        if data.get("temperatura_aire", 0) > self.temp_max:
            return "ALERTA_TEMPERATURA_ALTA"
        if data.get("humedad_suelo", 100) < self.humedad_suelo_min:
            return "ALERTA_HUMEDAD_BAJA"
        return "OK"


class MonitoringServer:
    """Clase principal orquestadora. Conecta MQTT, Base de datos y el motor de Reglas."""
    def __init__(self):
        print("Inicializando Servidor de Monitorización...")
        # Instanciamos la conexión a DB
        # //TODO: Rellenar con los tokens correctos
        self.db = DatabaseManager(
            host="localhost", 
            port=8086, 
            token="adminpassword", 
            org="proyecto_plantas", 
            bucket="sensores"
        )
        
        # Instanciamos la lógica
        self.analyzer = DataAnalyzer()
        
        # Instanciamos MQTT y pasamos el método para manejar mensajes como callback
        self.mqtt = MQTTManager(
            host="127.0.0.1", 
            port=1883, 
            on_message_callback=self.process_incoming_data
        )

    def process_incoming_data(self, topic, data):
        """Flujo principal cuando un paquete MQTT entra al sistema."""
        print(f"\n[DATOS RECIBIDOS] Topic: {topic}")
        print("-" * 30)
        for key, value in data.items():
            print(f"  {key}: {value}")
        print("-" * 30)

        # 1. Guardar data en base de datos
        self.db.save_sensor_data(topic, data)

        # 2. Analizar condiciones y generar alertas
        status = self.analyzer.check_thresholds(data)

        # 3. Lógica de interacción con Nodo 2 (Actuadores/Semáforo)
        if status != "OK":
            # Extraemos la ID de la planta del topic 'planta/1/sensores' -> '1'
            try:
                planta_id = topic.split('/')[1]
                topic_actuadores = f"planta/{planta_id}/actuadores"
                
                # //TODO: Implementar función check_and_notify_node2 real para mandar mensaje a Node 2
                comando = {
                    "comando": "encender_alerta",
                    "motivo": status
                }
                self.mqtt.publish(topic_actuadores, comando)
            except IndexError:
                print(f"[WARNING] Topic mal formado: {topic}")

    def start(self):
        self.mqtt.connect_and_loop()


def main():
    app = MonitoringServer()
    app.start()

if __name__ == "__main__":
    main()
