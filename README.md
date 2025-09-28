🏺 Rituales del Necronomicón — Interfaz PyQt6
Este proyecto es una aplicación de escritorio hecha en Python + PyQt6 que permite explorar y ejecutar rituales basados en los 50 Nombres de Marduk.
Incluye detección automática de carpeta de sigilos, interfaz gráfica intuitiva y visualización de imágenes asociadas.
✨ Características principales
- Interfaz gráfica (PyQt6) con:
  • Selector desplegable de los 50 Nombres de Marduk.
  • Botón para mostrar instrucciones generales.
  • Área de texto con descripción y pasos del ritual.
  • Área para mostrar el sigilo correspondiente (imagen).
- Auto-detección de carpeta de sigilos (prioriza ./sigilos, busca recursivamente si no existe).
- Búsqueda inteligente de archivos (normaliza nombres y soporta .png/.jpg/.jpeg).
- Cambio manual de carpeta desde la interfaz.
- Instrucciones pre-cargadas según el Necronomicón de Simón.
⚙️ Requisitos
- Python 3.8+
- Dependencias:
  - PyQt6

Instalación:
pip install PyQt6
🚀 Ejecución
Clona el repositorio y ejecuta:

python app_marduk_pyqt6.py

Si tienes una carpeta con sigilos personalizada, edita la línea SIGILOS_DIR o elige la carpeta manualmente desde la interfaz.
📂 Estructura recomendada
50_nombres_marduk/
│
├── app_marduk_pyqt6.py       # Código principal
├── sigilos/                  # Carpeta con imágenes de sigilos
│   ├── MARDUK.png
│   └── ...
└── README.md
📜 Uso
1. Abre la aplicación.
2. Selecciona un nombre en el desplegable.
3. Haz clic en 'Ejecutar Ritual' para ver descripción, palabra de poder y pasos.
4. Usa 'Ver Instrucciones Generales' para ver el procedimiento estándar.
5. Usa 'Elegir carpeta de sigilos...' para cargar imágenes personalizadas.
⚠️ Aviso
Este software es para fines de estudio y experimentación personal.
El uso en prácticas mágicas o espirituales queda bajo la responsabilidad del usuario.
📖 Licencia
MIT — Libre para modificar y compartir.
