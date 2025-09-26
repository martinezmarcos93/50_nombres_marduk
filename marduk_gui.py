# app_marduk_pyqt6.py
# -*- coding: utf-8 -*-
"""
Port de ipywidgets -> PyQt6
- Heurística para detectar carpeta de sigilos
- Normalización y búsqueda de archivos
- UI con combo de nombres, botones y área de salida + imagen
"""

from __future__ import annotations

import sys
import os
import unicodedata
from pathlib import Path
from typing import Optional, Tuple, List

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QTextEdit, QPushButton,
    QHBoxLayout, QVBoxLayout, QComboBox, QMessageBox, QStatusBar, QFileDialog
)

# --- OPCIONAL: podés setear manualmente la carpeta de sigilos ---
# Ejemplo: SIGILOS_DIR = r"C:\ruta\a\mis\sigilos"
SIGILOS_DIR: Optional[str] = None

MIN_IMG_COUNT = 5
IMG_EXTS = (".png", ".jpg", ".jpeg")


# ==========================
# Utilidades de archivos
# ==========================
def _count_images_in_dir(d: Path) -> int:
    try:
        return sum(1 for f in d.iterdir() if f.is_file() and f.suffix.lower() in IMG_EXTS)
    except Exception:
        return 0


def _auto_detect_dir(base: Path) -> Optional[Path]:
    # 1) Preferir ./sigilos si existe y tiene imágenes
    sig = base / "sigilos"
    if sig.is_dir() and _count_images_in_dir(sig) >= 1:
        return sig

    # 2) Buscar recursivamente carpetas con >= MIN_IMG_COUNT imágenes
    candidates: List[Tuple[int, Path]] = []
    for p in base.rglob("*"):
        if p.is_dir():
            n = _count_images_in_dir(p)
            if n >= MIN_IMG_COUNT:
                candidates.append((n, p))
    if candidates:
        candidates.sort(reverse=True, key=lambda x: x[0])  # mayor cantidad primero
        return candidates[0][1]

    return None


def resolve_sigilos_path() -> Optional[Path]:
    base_dir = Path(".").resolve()
    # Prioridad: variable SIGILOS_DIR si existe y es válida
    if SIGILOS_DIR:
        p = Path(SIGILOS_DIR).expanduser().resolve()
        if p.is_dir():
            return p
        else:
            raise RuntimeError(f"SIGILOS_DIR apunta a algo que no es carpeta: {p}")
    return _auto_detect_dir(base_dir)


# ==========================
# Normalización y búsqueda
# ==========================
def _norm(s: str) -> str:
    """
    Normaliza cadenas: casefold, quita acentos y no alfanuméricos.
    """
    return ''.join(
        c for c in unicodedata.normalize('NFKD', s).casefold()
        if c.isalnum()
    )


def buscar_sigilo(nombre: str, base_dir: Optional[Path]) -> Optional[str]:
    """
    Busca una imagen cuyo nombre comience con el nombre del sigilo (normalizado)
    dentro de base_dir y subcarpetas. Acepta .png/.jpg/.jpeg.
    """
    if not base_dir or not base_dir.is_dir():
        return None

    base = _norm(nombre)
    for root, _, files in os.walk(base_dir):
        for f in files:
            if f.lower().endswith(IMG_EXTS):
                if _norm(f).startswith(base):
                    return str(Path(root) / f)

    # Intento directo exacto en la raíz
    for ext in IMG_EXTS:
        p = base_dir / f"{nombre}{ext}"
        if p.exists():
            return str(p)

    return None


# ==========================
# Datos (50 nombres de Marduk)
# ==========================
nombres_marduk = {
    "MARDUK": {"descripcion": "Señor de Señores, Amo de los Magos. Solo debe ser invocado en casos de extrema necesidad.", "palabra_poder": "DUGGA"},
    "MARUKKA": {"descripcion": "Conoce todos los secretos del mundo, humanos y divinos.", "palabra_poder": "Invocar con deseo puro."},
    "MARUTUKKU": {"descripcion": "Maestro en las Artes de la Protección, posee la Estrella ARRA.", "palabra_poder": "ARRA"},
    "BARASHAKUSHU": {"descripcion": "Hacedor de Milagros, el más amable y benefactor de los 50.", "palabra_poder": "BAALDURU"},
    "LUGGALDIMERANKIA": {"descripcion": "Puso orden en el caos, comandante de legiones de demonios del viento.", "palabra_poder": "BANUTUKKU"},
    "NARILUGGALDIMMERANKIA": {"descripcion": "Vigilante de los IGIGI y ANUNNAKI, detecta todo lo que sucede en el mundo superior e inferior.", "palabra_poder": "BANRABISHU"},
    "ASARULUDU": {"descripcion": "Portador de la Espada Flamígera, otorga protección en tareas peligrosas.", "palabra_poder": "BANMASKIM"},
    "NAMTILLAKU": {"descripcion": "Posee el conocimiento de resucitar a los muertos y comunicarse con ellos.", "palabra_poder": "BANUTUKUKUTUKKU"},
    "NAMRU": {"descripcion": "Otorga sabiduría y conocimiento en todas las cosas, especialmente en la ciencia de los metales.", "palabra_poder": "BAKAKALAMU"},
    "ASARU": {"descripcion": "Conoce todas las plantas y árboles, y los hace prosperar incluso en desiertos.", "palabra_poder": "BAALPRIKU"},
    "ASARUALIM": {"descripcion": "Brilla como una luz en la oscuridad, otorga consejo y sabiduría en todas las cosas.", "palabra_poder": "BARRMARATU"},
    "ASARUALIMNUNNA": {"descripcion": "Protector en la batalla, otorga armaduras y conocimientos de estrategia militar.", "palabra_poder": "BANATATU"},
    "TUTU": {"descripcion": "Silencia la angustia y da alegría a los corazones rotos.", "palabra_poder": "DIRRIGUGIM"},
    "ZIUKKINNA": {"descripcion": "Da conocimiento sobre los movimientos de las estrellas y su significado.", "palabra_poder": "GIBBILANNU"},
    "ZIKU": {"descripcion": "Otorga riquezas y revela la ubicación de tesoros escondidos.", "palabra_poder": "GIGGIMAGANPA"},
    "AGAKU": {"descripcion": "Puede dar vida al que ya está muerto por un corto periodo de tiempo.", "palabra_poder": "MASHGARZANNA"},
    "TUKU": {"descripcion": "Protector contra maldiciones y ataques mágicos.", "palabra_poder": "MASHSHAMMASHTI"},
    "SHAZU": {"descripcion": "Conoce los pensamientos de los demás y revela secretos ocultos.", "palabra_poder": "MASHSHANANNA"},
    "ZISI": {"descripcion": "Reconciliador de enemigos, silenciador de disputas.", "palabra_poder": "MASHINANNA"},
    "SUHRIM": {"descripcion": "Busca y destruye a los adoradores de los Antiguos.", "palabra_poder": "MASSHANGERGAL"},
    "SUHGURIM": {"descripcion": "Descubre enemigos y puede atacarlos si se le ordena.", "palabra_poder": "MASHSHADAR"},
    "ZAHRIM": {"descripcion": "Guerrero supremo, destructor de ejércitos enteros.", "palabra_poder": "MASHSHAGARANNU"},
    "ZAHGURIM": {"descripcion": "Asesino letal que mata lentamente de formas misteriosas.", "palabra_poder": "MASHTISHADDU"},
    "ENBILULU": {"descripcion": "Conoce los secretos de los ríos y del agua en la tierra.", "palabra_poder": "BANATATU"},
    "EPADUN": {"descripcion": "Señor de la irrigación, trae agua a los lugares secos.", "palabra_poder": "EYUNGINAKANPA"},
    "ENBILULUGUGAL": {"descripcion": "Preside sobre todo crecimiento y abastece a las ciudades hambrientas.", "palabra_poder": "AGGHA"},
    "HEGAL": {"descripcion": "Señor de la agricultura y de la fertilidad humana.", "palabra_poder": "BURDISHU"},
    "SIRSIR": {"descripcion": "Destructor de TIAMAT, maestro sobre la serpiente.", "palabra_poder": "APIRIKUBABADAZUZUKANPA"},
    "MALAH": {"descripcion": "Otorga valentía y coraje en situaciones difíciles.", "palabra_poder": "BACHACHADUGG"},
    "GIL": {"descripcion": "Hace que la cebada crezca y potencia la fertilidad.", "palabra_poder": "AGGABAL"},
    "GILMA": {"descripcion": "Fundador de ciudades, Poseedor del Conocimiento de la Arquitectura, creador de todo lo que es permanente y nunca se mueve.", "palabra_poder": "AKABAL"},
    "AGILMA": {"descripcion": "El que trae la lluvia, puede causar tormentas o lluvias suaves.", "palabra_poder": "MASHSHAYEGURRA"},
    "ZULUM": {"descripcion": "Conoce dónde y cuándo plantar, da consejo en negocios y protege contra fraudes.", "palabra_poder": "ABBABAAL"},
    "MUMMU": {"descripcion": "Otorga conocimientos sobre la condición de la vida antes de la creación y la estructura del universo.", "palabra_poder": "ALALALABAAAL"},
    "ZULUMMAR": {"descripcion": "Otorga gran fuerza y vitalidad.", "palabra_poder": "ANNDARABAAL"},
    "LUGALABDUBUR": {"descripcion": "Destructor de los Dioses de TIAMAT, venció a sus hordas y encadenó a KUTULU.", "palabra_poder": "AGNIBAAL"},
    "PAGALGUENNA": {"descripcion": "Posee infinita inteligencia y conocimiento de lo aún no creado.", "palabra_poder": "ARRABABAAL"},
    "LUGALDURMAH": {"descripcion": "Señor de los Lugares Elevados, vigilante de los cielos y de todo lo que viaja en él.", "palabra_poder": "ARATAAGARBAL"},
    "ARANUNNA": {"descripcion": "Dador de sabiduría, conocedor del Pacto Mágico y de las Leyes.", "palabra_poder": "ARAMANNGI"},
    "DUMUDUKU": {"descripcion": "Poseedor del Bastón de Lapislázuli, conocedor del Nombre y Número Secreto.", "palabra_poder": "ARATAGIGI"},
    "LUGALANNA": {"descripcion": "Conoce la esencia del mundo antes de la división entre Ancianos y Antiguos.", "palabra_poder": "BALDIKHU"},
    "LUGALUGGA": {"descripcion": "Conoce la esencia de todos los espíritus, vivos y muertos.", "palabra_poder": "ZIDUR"},
    "IRKINGU": {"descripcion": "Capturó a KINGU y conoce los orígenes de la humanidad.", "palabra_poder": "BARERIMU"},
    "KINMA": {"descripcion": "Juez de los Dioses, vigilante del cumplimiento del Pacto.", "palabra_poder": "ENGAIGAL"},
    "ESIZKUR": {"descripcion": "Conoce la duración de la vida de todas las cosas.", "palabra_poder": "NENIGEGAL"},
    "GIBIL": {"descripcion": "Señor del fuego y la forja, purificador de los metales y el alma.", "palabra_poder": "BAALAGNITARRA"},
    "ADDU": {"descripcion": "Controlador de tormentas y vientos celestiales.", "palabra_poder": "KAKODAMMU"},
    "ASHARRU": {"descripcion": "Conocedor de los caminos traicioneros y dador de inteligencia sobre el futuro.", "palabra_poder": "BAXTANDABAL"},
    "NEBIRU": {"descripcion": "Guardián de la Puerta de Marduk y regulador de los astros.", "palabra_poder": "DIRGIRGIRI"},
    "NINNUAM": {"descripcion": "Poder supremo de Marduk, juez de jueces.", "palabra_poder": "GASHDIG"}
}


# ==========================
# Ventana principal
# ==========================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Rituales del Necronomicón (PyQt6)")
        self.resize(960, 640)

        # Intentar resolver carpeta de sigilos
        try:
            self.sigilos_path: Optional[Path] = resolve_sigilos_path()
        except Exception as e:
            self.sigilos_path = None
            QMessageBox.critical(self, "Error detectando carpeta", f"{e}")

        # Widgets
        self.combo = QComboBox()
        self.combo.addItems(list(nombres_marduk.keys()))

        self.btn_ejecutar = QPushButton("Ejecutar Ritual")
        self.btn_instrucciones = QPushButton("Ver Instrucciones Generales")
        self.btn_cambiar_dir = QPushButton("Elegir carpeta de sigilos...")

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setMinimumHeight(220)

        self.image_label = QLabel("[No se encontró imagen del sigilo]")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setMinimumSize(QSize(200, 200))
        self.image_label.setWordWrap(True)

        # Layouts
        top_row = QHBoxLayout()
        top_row.addWidget(QLabel("Ritual:"))
        top_row.addWidget(self.combo, stretch=1)
        top_row.addWidget(self.btn_ejecutar)
        top_row.addWidget(self.btn_instrucciones)
        top_row.addWidget(self.btn_cambiar_dir)

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_row)
        main_layout.addWidget(self.output, stretch=1)
        main_layout.addWidget(self.image_label, stretch=2)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Status bar
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self._update_status_sigilos()

        # Signals
        self.btn_ejecutar.clicked.connect(self.on_ejecutar)
        self.btn_instrucciones.clicked.connect(self.on_instrucciones)
        self.btn_cambiar_dir.clicked.connect(self.on_cambiar_dir)

        # Render inicial
        self.render_instrucciones()

    # -----------------------
    # Helpers UI
    # -----------------------
    def _update_status_sigilos(self):
        if self.sigilos_path and self.sigilos_path.is_dir():
            self.status.showMessage(f"Carpeta de sigilos: {self.sigilos_path}")
        else:
            self.status.showMessage("Carpeta de sigilos no detectada")

    def set_image(self, path: Optional[str]):
        if path and Path(path).exists():
            pix = QPixmap(path)
            if pix.isNull():
                self.image_label.setText("[No se pudo cargar la imagen]")
                return
            # Escalado para que encaje manteniendo relación de aspecto
            w = self.image_label.width()
            h = self.image_label.height()
            self.image_label.setPixmap(pix.scaled(w, h, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            self.image_label.setText("[No se encontró imagen del sigilo]")
            self.image_label.setPixmap(QPixmap())  # limpiar

    def resizeEvent(self, event):
        # Reescalar imagen al cambiar tamaño de la ventana
        if self.image_label.pixmap():
            self.set_image(self.current_image_path if hasattr(self, "current_image_path") else None)
        super().resizeEvent(event)

    # -----------------------
    # Render de contenidos
    # -----------------------
    def render_instrucciones(self):
        texto = []
        texto.append("Instrucciones Generales para los Rituales del Necronomicón de Simón:\n")
        pasos = [
            "1. Escribe el sello del nombre en un papel blanco con tinta negra.",
            "2. Encuentra un lugar tranquilo, enciende dos velas y un incienso.",
            "3. Concéntrate en tu objetivo y respira profundamente tres veces.",
            "4. Pronuncia el llamado sagrado para invocar la entidad.",
            "5. Mantén la concentración y visualiza tu objetivo cumplido.",
            "6. Cierra el ritual con las palabras de despedida y agradecimiento.",
            "7. Guarda el sello en un lugar seguro y evita que otros lo vean.",
            "8. Registra los resultados en tu diario de rituales."
        ]
        texto.extend(pasos)
        self.output.setPlainText("\n".join(texto))
        self.current_image_path = None
        self.set_image(None)

    def render_ritual(self, nombre: str):
        det = nombres_marduk.get(nombre, {})
        descripcion = det.get("descripcion", "")
        palabra = det.get("palabra_poder", "")

        bloques = [
            f"Ritual para {nombre}:\n",
            f"Descripción: {descripcion}\n",
            "Pasos a seguir:",
            "1. Escribe el sello de este nombre en un papel blanco con tinta negra.",
            "2. Encuentra un lugar tranquilo, enciende dos velas y un incienso.",
            "3. Concéntrate en tu objetivo y respira profundamente tres veces.",
            "4. Pronuncia el siguiente llamado:",
            "   ZI KIA KANPA, ZI ANNA KANPA",
            f"   Escúchame, oh {nombre}, ven a mí por los poderes de la palabra {palabra}",
            "   ¡Y contesta mi Pedido Urgente!",
            "5. Mantén la concentración y visualiza tu objetivo.",
            "6. Cierra el ritual con:",
            "   ZI DINGIR KIA KANPA, ZI DINGIR ANNA KANPA",
            "7. Guarda el sello en un lugar seguro y no permitas que otros lo vean.",
            "8. Registra el resultado en tu diario de rituales si lo deseas."
        ]
        self.output.setPlainText("\n".join(bloques))

        # Mostrar imagen del sigilo (si existe)
        img_path = buscar_sigilo(nombre, self.sigilos_path)
        self.current_image_path = img_path
        self.set_image(img_path)

    # -----------------------
    # Slots
    # -----------------------
    def on_instrucciones(self):
        self.render_instrucciones()

    def on_ejecutar(self):
        nombre = self.combo.currentText()
        self.render_ritual(nombre)

    def on_cambiar_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Elegí la carpeta de sigilos")
        if dir_path:
            p = Path(dir_path).resolve()
            if not p.is_dir():
                QMessageBox.warning(self, "Directorio inválido", f"No es una carpeta válida: {p}")
                return
            self.sigilos_path = p
            self._update_status_sigilos()
            # Si hay un ritual ya mostrado, actualizar imagen
            if hasattr(self, "current_image_path") and self.current_image_path:
                self.current_image_path = buscar_sigilo(self.combo.currentText(), self.sigilos_path)
                self.set_image(self.current_image_path)


def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
