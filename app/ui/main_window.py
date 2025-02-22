from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
from app.ui.gestion_canales import GestionCanales


class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Gestión de Fidelización de Clientes")
        self.setGeometry(200, 200, 600, 400)  # Tamaño y posición inicial de la ventana
        self.setWindowIcon(QIcon("recursos/logo.ico"))  # Ícono de la aplicación

        # Widget Central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal (vertical)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Etiqueta de bienvenida
        title_label = QLabel("Sistema de Gestión de Clientes")
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Espaciador
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Botones de navegación
        self.btn_gestion_canales = QPushButton("Gestión de Canales")
        self.btn_gestion_canales.setFont(QFont("Arial", 12))
        self.btn_gestion_canales.clicked.connect(self.controller.abrir_gestion_canales)
        layout.addWidget(self.btn_gestion_canales)

        self.btn_gestion_clientes = QPushButton("Gestión de Clientes")
        self.btn_gestion_clientes.setFont(QFont("Arial", 12))
        self.btn_gestion_clientes.clicked.connect(self.controller.abrir_gestion_clientes)
        layout.addWidget(self.btn_gestion_clientes)

        self.btn_registro_consumos = QPushButton("Registro de Consumos")
        self.btn_registro_consumos.setFont(QFont("Arial", 12))
        self.btn_registro_consumos.clicked.connect(self.controller.abrir_registro_consumos)
        layout.addWidget(self.btn_registro_consumos)

        self.btn_consulta_consumos = QPushButton("Consulta de Consumos")
        self.btn_consulta_consumos.setFont(QFont("Arial", 12))
        self.btn_consulta_consumos.clicked.connect(self.controller.abrir_consulta_consumos)
        layout.addWidget(self.btn_consulta_consumos)

        self.btn_generar_informes = QPushButton("Generar Informes")
        self.btn_generar_informes.setFont(QFont("Arial", 12))
        self.btn_generar_informes.clicked.connect(self.controller.abrir_generar_informes)
        layout.addWidget(self.btn_generar_informes)

        # Espaciador inferior
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Establecer el layout al widget central
        central_widget.setLayout(layout)

def abrir_gestion_canales(self):
    self.gestion_canales = GestionCanales(self.controller)
    self.gestion_canales.show()