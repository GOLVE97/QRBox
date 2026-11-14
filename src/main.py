import sys
from pathlib import Path

import qrcode
from qrcode.constants import ERROR_CORRECT_M
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QApplication, QComboBox, QFileDialog, QFrame, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QMessageBox, QPushButton, QVBoxLayout, QWidget,
)


class QRBox(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QRBox | NICOLUSA")
        self.setMinimumSize(760, 620)
        self.qr_image = None
        self.setStyleSheet("""
            QMainWindow, QWidget { background: #10141d; color: #eef2f8; font-family: Segoe UI; }
            QLabel#brand { font-size: 27px; font-weight: 700; color: #f5f7fb; }
            QLabel#sub { color: #98a4b8; font-size: 13px; }
            QLabel#section { font-size: 15px; font-weight: 600; }
            QLineEdit, QComboBox { background: #1a2230; border: 1px solid #303c50; border-radius: 9px; padding: 12px; color: #f5f7fb; font-size: 14px; }
            QPushButton { background: #6c8cff; color: #08101f; border: 0; border-radius: 9px; padding: 12px 18px; font-weight: 700; }
            QPushButton:hover { background: #86a0ff; }
            QPushButton:disabled { background: #39445a; color: #8792a7; }
            QPushButton#secondary { background: #202a3a; color: #eaf0fa; border: 1px solid #344158; }
            QFrame#panel { background: #151c28; border: 1px solid #293548; border-radius: 15px; }
            QLabel#preview { background: #f7f8fa; border-radius: 12px; color: #687386; }
        """)
        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(16)

        header = QHBoxLayout()
        brand_col = QVBoxLayout()
        brand = QLabel("✦ QRBox")
        brand.setObjectName("brand")
        subtitle = QLabel("Un generador de códigos QR de NICOLUSA")
        subtitle.setObjectName("sub")
        brand_col.addWidget(brand)
        brand_col.addWidget(subtitle)
        header.addLayout(brand_col)
        header.addStretch()
        tag = QLabel("WINDOWS • MVP")
        tag.setStyleSheet("color:#9aabc7; font-size:11px; font-weight:700;")
        header.addWidget(tag, alignment=Qt.AlignTop)
        layout.addLayout(header)

        panel = QFrame()
        panel.setObjectName("panel")
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(20, 20, 20, 20)
        panel_layout.setSpacing(12)
        title = QLabel("¿Qué quieres convertir en un QR?")
        title.setObjectName("section")
        panel_layout.addWidget(title)

        self.kind = QComboBox()
        self.kind.addItems(["Enlace", "Texto"])
        panel_layout.addWidget(self.kind)

        self.content = QLineEdit()
        self.content.setPlaceholderText("https://ejemplo.com")
        self.content.returnPressed.connect(self.generate_qr)
        panel_layout.addWidget(self.content)

        actions = QHBoxLayout()
        generate = QPushButton("Generar código QR")
        generate.clicked.connect(self.generate_qr)
        actions.addWidget(generate)
        self.save_btn = QPushButton("Descargar PNG")
        self.save_btn.setObjectName("secondary")
        self.save_btn.setEnabled(False)
        self.save_btn.clicked.connect(self.save_png)
        actions.addWidget(self.save_btn)
        panel_layout.addLayout(actions)
        layout.addWidget(panel)

        preview_panel = QFrame()
        preview_panel.setObjectName("panel")
        preview_layout = QVBoxLayout(preview_panel)
        preview_layout.setContentsMargins(20, 18, 20, 18)
        preview_layout.setSpacing(10)
        preview_title = QLabel("Vista previa")
        preview_title.setObjectName("section")
        preview_layout.addWidget(preview_title)
        self.preview = QLabel("Tu código QR aparecerá aquí")
        self.preview.setObjectName("preview")
        self.preview.setAlignment(Qt.AlignCenter)
        self.preview.setMinimumHeight(310)
        preview_layout.addWidget(self.preview, 1)
        self.status = QLabel("Introduce un enlace o texto para comenzar.")
        self.status.setObjectName("sub")
        preview_layout.addWidget(self.status)
        layout.addWidget(preview_panel, 1)

        footer = QLabel("Generación local • Tu contenido no se envía a ningún servidor")
        footer.setObjectName("sub")
        footer.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer)

    def generate_qr(self):
        value = self.content.text().strip()
        if not value:
            QMessageBox.warning(self, "Falta contenido", "Escribe un enlace o texto para generar el QR.")
            return
        if self.kind.currentText() == "Enlace" and not value.lower().startswith(("https://", "http://")):
            value = "https://" + value
            self.content.setText(value)

        qr = qrcode.QRCode(
            version=None,
            error_correction=ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        qr.add_data(value)
        qr.make(fit=True)
        self.qr_image = qr.make_image(fill_color="#10141d", back_color="white").convert("RGB")
        image_data = self.qr_image.tobytes("raw", "RGB")
        image = QImage(
            image_data, self.qr_image.width, self.qr_image.height,
            self.qr_image.width * 3, QImage.Format_RGB888,
        ).copy()
        pixmap = QPixmap.fromImage(image).scaled(
            280, 280, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.preview.setPixmap(pixmap)
        self.save_btn.setEnabled(True)
        self.status.setText("QR generado correctamente. Puedes descargarlo como PNG.")

    def save_png(self):
        if self.qr_image is None:
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Guardar código QR", "qrbox-code.png", "Imagen PNG (*.png)"
        )
        if path:
            if not path.lower().endswith(".png"):
                path += ".png"
            self.qr_image.save(path, format="PNG")
            self.status.setText(f"Archivo guardado: {Path(path).name}")
            QMessageBox.information(self, "QRBox", "Tu código QR se guardó correctamente.")


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("QRBox")
    window = QRBox()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
