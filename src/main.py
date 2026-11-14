import sys
from pathlib import Path

import qrcode
from qrcode.constants import ERROR_CORRECT_M
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QApplication, QFileDialog, QFrame, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QMessageBox, QPushButton, QVBoxLayout, QWidget,
)


class QRBox(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QRBox | NICOLUSA")
        self.setMinimumSize(900, 620)
        self.resize(1080, 700)
        self.qr_image = None
        self.current_kind = "Enlace"
        self._apply_style()
        self._build_ui()

    def _apply_style(self):
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background: #f4f6fb;
                color: #172033;
                font-family: "Segoe UI";
                font-size: 14px;
            }
            QLabel#brand { font-size: 25px; font-weight: 750; color: #172033; }
            QLabel#eyebrow { color: #73809a; font-size: 10px; font-weight: 700; letter-spacing: 1px; }
            QLabel#subtitle { color: #77839a; font-size: 13px; }
            QLabel#section { color: #1d2940; font-size: 15px; font-weight: 700; }
            QLabel#muted { color: #8390a5; font-size: 12px; }
            QLabel#preview { background: #ffffff; border: 1px dashed #d8dfeb; border-radius: 16px; color: #8793a8; }
            QFrame#card { background: #ffffff; border: 1px solid #e4e9f2; border-radius: 18px; }
            QFrame#hero { background: #ffffff; border: 1px solid #e4e9f2; border-radius: 20px; }
            QLineEdit {
                background: #f8faff; border: 1px solid #dce3ef; border-radius: 11px;
                padding: 14px 15px; color: #172033; selection-background-color: #dce6ff;
                font-size: 14px;
            }
            QLineEdit:focus { border: 1px solid #557cf5; background: #ffffff; }
            QPushButton {
                background: #557cf5; color: #ffffff; border: 0; border-radius: 11px;
                padding: 13px 18px; font-weight: 700;
            }
            QPushButton:hover { background: #4269e7; }
            QPushButton:pressed { background: #3157d1; }
            QPushButton:disabled { background: #dce3ef; color: #929db0; }
            QPushButton#secondary {
                background: #ffffff; color: #33415c; border: 1px solid #dce3ef;
            }
            QPushButton#secondary:hover { background: #f5f7fc; border-color: #bdc9dc; }
            QPushButton#type {
                background: #f7f9fd; color: #66738a; border: 1px solid #e2e8f2;
                padding: 10px 14px; font-weight: 600;
            }
            QPushButton#type:checked {
                background: #edf2ff; color: #315bd5; border: 1px solid #aebfff;
            }
            QPushButton#clear {
                background: transparent; color: #71809a; padding: 8px 10px;
            }
            QPushButton#clear:hover { color: #315bd5; background: #f2f5fc; }
        """)

    def _build_ui(self):
        root = QWidget()
        self.setCentralWidget(root)
        outer = QVBoxLayout(root)
        outer.setContentsMargins(30, 24, 30, 24)
        outer.setSpacing(20)

        header = QHBoxLayout()
        brand_col = QVBoxLayout()
        brand_col.setSpacing(3)
        brand = QLabel("✦ QRBox")
        brand.setObjectName("brand")
        subtitle = QLabel("Crea códigos QR en segundos.")
        subtitle.setObjectName("subtitle")
        brand_col.addWidget(brand)
        brand_col.addWidget(subtitle)
        header.addLayout(brand_col)
        header.addStretch()
        local = QLabel("●  GENERACIÓN LOCAL")
        local.setStyleSheet("color:#38836b; background:#e8f6f0; border-radius:10px; padding:8px 12px; font-size:10px; font-weight:800;")
        header.addWidget(local, alignment=Qt.AlignVCenter)
        outer.addLayout(header)

        columns = QHBoxLayout()
        columns.setSpacing(18)
        outer.addLayout(columns, 1)

        # Creation panel
        create_card = QFrame()
        create_card.setObjectName("hero")
        create_layout = QVBoxLayout(create_card)
        create_layout.setContentsMargins(24, 24, 24, 24)
        create_layout.setSpacing(15)

        eyebrow = QLabel("CREADOR DE QR")
        eyebrow.setObjectName("eyebrow")
        create_layout.addWidget(eyebrow)
        title = QLabel("¿Qué quieres compartir?")
        title.setStyleSheet("font-size:23px; font-weight:750; color:#172033;")
        create_layout.addWidget(title)
        description = QLabel("Elige un formato y escribe el contenido de tu código.")
        description.setObjectName("subtitle")
        description.setWordWrap(True)
        create_layout.addWidget(description)

        types = QHBoxLayout()
        types.setSpacing(8)
        self.link_btn = QPushButton("↗  Enlace")
        self.text_btn = QPushButton("▤  Texto")
        for button in (self.link_btn, self.text_btn):
            button.setObjectName("type")
            button.setCheckable(True)
            button.setMinimumHeight(42)
            types.addWidget(button)
        self.link_btn.setChecked(True)
        self.link_btn.clicked.connect(lambda: self.set_kind("Enlace"))
        self.text_btn.clicked.connect(lambda: self.set_kind("Texto"))
        create_layout.addLayout(types)

        field_label = QLabel("CONTENIDO")
        field_label.setObjectName("eyebrow")
        create_layout.addWidget(field_label)
        self.content = QLineEdit()
        self.content.setPlaceholderText("https://ejemplo.com")
        self.content.setMinimumHeight(50)
        self.content.returnPressed.connect(self.generate_qr)
        self.content.setAccessibleName("Contenido para generar el código QR")
        create_layout.addWidget(self.content)

        self.hint = QLabel("Puedes pegar una dirección web con o sin https://")
        self.hint.setObjectName("muted")
        self.hint.setWordWrap(True)
        create_layout.addWidget(self.hint)

        create_layout.addStretch(1)
        self.generate_btn = QPushButton("Generar código QR   →")
        self.generate_btn.setMinimumHeight(50)
        self.generate_btn.clicked.connect(self.generate_qr)
        create_layout.addWidget(self.generate_btn)

        privacy = QLabel("🔒  Tu contenido permanece en este equipo.")
        privacy.setStyleSheet("color:#71809a; font-size:12px; padding-top:7px;")
        privacy.setWordWrap(True)
        create_layout.addWidget(privacy)
        columns.addWidget(create_card, 5)

        # Preview panel
        preview_card = QFrame()
        preview_card.setObjectName("card")
        preview_layout = QVBoxLayout(preview_card)
        preview_layout.setContentsMargins(22, 22, 22, 22)
        preview_layout.setSpacing(12)

        preview_head = QHBoxLayout()
        preview_title = QLabel("Vista previa")
        preview_title.setObjectName("section")
        preview_head.addWidget(preview_title)
        preview_head.addStretch()
        self.clear_btn = QPushButton("Limpiar")
        self.clear_btn.setObjectName("clear")
        self.clear_btn.clicked.connect(self.clear_preview)
        preview_head.addWidget(self.clear_btn)
        preview_layout.addLayout(preview_head)

        self.preview = QLabel("Tu código QR aparecerá aquí")
        self.preview.setObjectName("preview")
        self.preview.setAlignment(Qt.AlignCenter)
        self.preview.setMinimumSize(300, 330)
        self.preview.setWordWrap(True)
        preview_layout.addWidget(self.preview, 1)

        self.status = QLabel("Listo para crear tu primer código.")
        self.status.setObjectName("muted")
        self.status.setAlignment(Qt.AlignCenter)
        preview_layout.addWidget(self.status)

        self.save_btn = QPushButton("↓   Descargar PNG")
        self.save_btn.setObjectName("secondary")
        self.save_btn.setMinimumHeight(48)
        self.save_btn.setEnabled(False)
        self.save_btn.clicked.connect(self.save_png)
        preview_layout.addWidget(self.save_btn)
        columns.addWidget(preview_card, 6)

        footer = QHBoxLayout()
        footer_label = QLabel("NICOLUSA  ·  Herramientas simples, ideas útiles")
        footer_label.setObjectName("muted")
        footer.addWidget(footer_label)
        footer.addStretch()
        version = QLabel("QRBox 0.1.0")
        version.setObjectName("muted")
        footer.addWidget(version)
        outer.addLayout(footer)

    def set_kind(self, kind):
        self.current_kind = kind
        self.link_btn.setChecked(kind == "Enlace")
        self.text_btn.setChecked(kind == "Texto")
        if kind == "Enlace":
            self.content.setPlaceholderText("https://ejemplo.com")
            self.hint.setText("Puedes pegar una dirección web con o sin https://")
        else:
            self.content.setPlaceholderText("Escribe aquí tu mensaje...")
            self.hint.setText("El código QR contendrá exactamente el texto que escribas.")
        self.content.setFocus()

    def generate_qr(self):
        value = self.content.text().strip()
        if not value:
            QMessageBox.information(self, "Contenido vacío", "Escribe algo para generar tu código QR.")
            self.content.setFocus()
            return
        if self.current_kind == "Enlace" and not value.lower().startswith(("https://", "http://")):
            value = "https://" + value
            self.content.setText(value)

        try:
            qr = qrcode.QRCode(
                version=None, error_correction=ERROR_CORRECT_M, box_size=12, border=4
            )
            qr.add_data(value)
            qr.make(fit=True)
            self.qr_image = qr.make_image(fill_color="#172033", back_color="white").convert("RGB")
            image_data = self.qr_image.tobytes("raw", "RGB")
            image = QImage(
                image_data, self.qr_image.width, self.qr_image.height,
                self.qr_image.width * 3, QImage.Format_RGB888,
            ).copy()
            pixmap = QPixmap.fromImage(image).scaled(
                300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.preview.setText("")
            self.preview.setPixmap(pixmap)
            self.save_btn.setEnabled(True)
            self.status.setText("✓  Código generado correctamente")
        except Exception as exc:
            QMessageBox.critical(self, "No se pudo generar el QR", str(exc))

    def clear_preview(self):
        self.qr_image = None
        self.preview.setPixmap(QPixmap())
        self.preview.setText("Tu código QR aparecerá aquí")
        self.save_btn.setEnabled(False)
        self.status.setText("Listo para crear tu primer código.")

    def save_png(self):
        if self.qr_image is None:
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Guardar código QR", "qrbox-code.png", "Imagen PNG (*.png)"
        )
        if not path:
            return
        if not path.lower().endswith(".png"):
            path += ".png"
        try:
            self.qr_image.save(path, format="PNG")
            self.status.setText(f"✓  Guardado: {Path(path).name}")
        except Exception as exc:
            QMessageBox.critical(self, "Error al guardar", str(exc))


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("QRBox")
    window = QRBox()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
