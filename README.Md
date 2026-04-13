# Sistema de Monitorización de Plantas con IoT 🌿

Este proyecto consiste en el diseño e implementación de un **Sistema de Monitorización Inteligente** basado en una arquitectura distribuida (múltiples MCUs) para el seguimiento en tiempo real de variables críticas en plantas, asegurando la persistencia de datos y la capacidad de reacción mediante un sistema de alertas.

---

## 🛠️ Estructura del Sistema

El sistema se divide en tres componentes principales:

### 📡 Nodo 1: Sensorización
Encargado de la recolección de datos ambientales de la planta.
- **Sensor Fotovoltaico:** Medición de intensidad lumínica.
- **Sensor de Humedad/Temperatura:** Control del ambiente aéreo.
- **Sensor de Humedad en Suelo:** Medición directa de la hidratación de la planta.

### 📟 Nodo 2: Interacción y Alertas
Encargado de mostrar información local y estados del sistema.
- **Pantalla LCD:** Visualización de mensajes en tiempo real sobre el estado de las plantas.
- **LED Semáforo:** Indicador visual rápido (OK / Advertencia / Error).

### 🖥️ Servidor Central
Centro de control y procesamiento de datos.
- **Monitorización:** Panel de control con gráficas en tiempo real de los parámetros.
- **Persistencia:** Almacenamiento histórico de lecturas para análisis posterior.
- **Alertas Inteligentes:** Lógica centralizada para disparar acciones en el Nodo 2.

---

## 📋 Requisitos del Proyecto

Basado en la guía docente para la entrega del **24 de abril de 2026**:

### Requisitos Técnicos
- [ ] 1. **Arquitectura:** Al menos dos dispositivos MCU comunicados entre sí o con un servidor central.
- [ ] 2. **Programación:** Uso obligatorio de la biblioteca `TaskScheduler`.
- [ ] 3. **Conectividad:** Punto de acceso Wi-Fi o conexión a infraestructura existente.
- [x] 4. **Protocolo:** Comunicación mediante **MQTT**.
- [ ] 5. **Componentes:** Integración de al menos cinco tipos de sensores/actuadores (3 vistos en clase + 2 adicionales).
- [x] 6. **Base de Datos:** Implementación para almacenamiento histórico (series temporales).
- [x] 7. **Dashboard:** Panel de control con gráficas históricas y en tiempo real.
- [x] 8. **Notificaciones:** Sistema de alertas automáticas integrado en la web.

### Documentación Requerida
El documento final (10-12 páginas) debe incluir:
1. Portada con datos del grupo.
2. Índice detallado.
3. Introducción (propósito, alcance y objetivos).
4. Descripción detallada del sistema y escenarios de uso.
5. Listado completo de hardware y software.
6. Esquemáticos de conexión (Fritzing).
7. Arquitectura de red y modelo de datos.
8. Análisis de la interfaz de visualización.
9. Pruebas y resultados (incluyendo enlace a vídeo).
10. Conclusiones y referencias (Anexo con `docker-compose.yml`).

---

## 🚀 Sugerencias Tecnológicas

*   **Base de Datos:** `InfluxDB` (recomendado para series temporales), `MongoDB` o `MySQL`.
*   **Visualización:** `Grafana` para dashboards avanzados o aplicaciones web propias.
*   **Despliegue:** Uso de `Docker` y `Docker Compose` para orquestar el broker MQTT, base de datos y dashboard.
*   **Optimización:** Implementación de modos de bajo consumo (`deep sleep`) en los nodos sensores.

---

## 📁 Entrega
- **Documento:** PDF siguiendo el formato A4, Times New Roman 12.
- **Código:** Repositorio completo o archivo ZIP con el código fuente.