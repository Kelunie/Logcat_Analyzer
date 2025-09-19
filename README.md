# Logcat Analyzer

![App Icon](https://github.com/Kelunie/Logcat_Analyzer/blob/master/Img/Icon.ico)

**Logcat Analyzer** es una aplicación de escritorio desarrollada en Python que permite analizar archivos de logs de Android, detectando eventos de conectividad WiFi, estado de la red y problemas del sistema. La herramienta genera reportes detallados con un resumen estadístico, eventos detectados y una línea de tiempo de los primeros eventos.

---

## 🔹 Características principales

- Análisis automático de logs de Android.
- Detección de eventos WiFi:
  - Conexiones establecidas.
  - Escaneos de redes.
  - Errores de WiFi.
- Detección de eventos de red y problemas del sistema:
  - Errores y crashes.
  - Advertencias (warnings).
  - Inicio del sistema (boot) y operaciones lentas.
- Generación de reportes en interfaz gráfica con:
  - Resumen estadístico.
  - Detalles de eventos WiFi.
  - Problemas del sistema resaltados con íconos (❌ para errores, ⚠️ para warnings).
  - Línea de tiempo de los primeros 10 eventos.
- Interfaz gráfica amigable con botones redondeados y soporte de íconos.
- Compatible con Python y ejecutable `.exe`.

---

## 🛠 Tecnologías utilizadas

- **Python 3**
- **Tkinter**: Interfaz gráfica.
- **Pillow (PIL)**: Manejo de imágenes e íconos.
- **re**: Expresiones regulares para analizar logs.
- **ttk.Treeview**: Visualización de tablas de errores.
- **scrolledtext**: Mostrar reportes extensos.

---

## 📂 Estructura del proyecto
```
LogcatAnalyzer/
│
├─ img/
│ ├─ subirArchivo.png # Icono para subir logs
│ ├─ close.png # Icono del botón cerrar
│ └─ icon-inteligentec.ico # Icono principal de la app
│
├─ Main.py # Código fuente principal
└─ README.md # Documentación
```

---

## ⚡ Instalación

### 1. Requisitos

- Python 3.7 o superior
- Librerías:
```bash
pip install pillow
```
## 2. Ejecutar el programa
```bash
python Main.py
```
---
## 3. Crear archivo ejecutable (.exe)
Usando PyInstaller:
```bash
pyinstaller --noconsole --onefile --icon=img/icon-inteligentec.ico --add-data "img;img" Main.py
```
- --noconsole: Oculta la consola.

- --onefile: Genera un único .exe.

- --icon: Icono de la aplicación.

- --add-data "img;img": Incluye la carpeta de imágenes. 
---

## 🚀 Uso de la aplicación

Abrir la aplicación (Main.py o .exe generado).

1. Hacer clic en Analizar logs.

2. Seleccionar el archivo .txt de logs.

3. La aplicación mostrará:

   - Ventana con reporte general.

   - Tabla de errores/crashes detectados (si aplica).

4. Para cerrar la aplicación, usar el botón Cerrar.
---
## Ejemplo de la interfaz

### - Menú principal:
```
+-----------------------------+
| Logcat Analyzer             |
|                             |
|  [ Analizar logs ]          |
|                             |
|  [ Cerrar ]                 |
+-----------------------------+
```
---
## Reporte generado:
```
========================================
ANÁLISIS DE LOGS - CONECTIVIDAD Y SISTEMA
========================================
Eventos WiFi detectados: 5
Eventos de red detectados: 3
Problemas del sistema detectados: 2

EVENTOS DE WiFi:
02-11 14:32:10.123 - wifi_connection: CONNECTIVITY_CHANGE detected...
...

PROBLEMAS DEL SISTEMA:
❌ 02-11 14:35:22.456 - crash: FATAL EXCEPTION in ...
⚠️ 02-11 14:36:05.789 - warning: Slow operation detected...

LINEA DE TIEMPO (primeros 10 eventos):
📶 02-11 14:32:10 - wifi/wifi_connection
🌐 02-11 14:33:11 - network/network_state
💥 02-11 14:35:22 - system/crash

```
---
## 🔧 Detalles técnicos

- RoundedButton: Botones con bordes redondeados, iconos y texto centrado, con efectos hover y click.

- LogAnalyzer: Analiza y clasifica eventos en WiFi, red y sistema.

- Función resource_path(): Garantiza rutas absolutas de recursos para PyInstaller.

- UI: Ventanas emergentes para reportes y tabla de errores usando scrolledtext y ttk.Treeview.
---
## 🤝 Contribuciones
**Las contribuciones son bienvenidas:**

- Mejorar la visualización de reportes.

- Exportar reportes a .txt o .csv.

- Añadir filtros avanzados por tipo de evento.

- Optimizar la interfaz y manejo de grandes archivos de logs.
---
## 📝 Licencia

**Este proyecto está bajo la licencia**
***[MIT](https://choosealicense.com/licenses/mit/)***
---
## 👤 Autor

Caleb Rodríguez Cordero
Desarrollador principal

**caleb.cordero1997@gmail.com**
