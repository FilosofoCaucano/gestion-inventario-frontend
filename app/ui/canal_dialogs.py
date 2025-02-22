from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout

# Diálogo para gestionar Canales
class CanalDialog(QDialog):
    def __init__(self, datos=None):
        super().__init__()
        self.setWindowTitle("Agregar Canal" if not datos else "Editar Canal")
        self.resize(300, 200)

        layout = QVBoxLayout()

        # Campos del formulario
        self.nombre_input = QLineEdit(datos[0] if datos else "")
        self.tipo_input = QLineEdit(datos[1] if datos else "")
        self.cuenta_input = QLineEdit(datos[2] if datos else "")

        layout.addWidget(QLabel("Nombre del Canal:"))
        layout.addWidget(self.nombre_input)
        layout.addWidget(QLabel("Tipo del Canal:"))
        layout.addWidget(self.tipo_input)
        layout.addWidget(QLabel("Cuenta Bancaria:"))
        layout.addWidget(self.cuenta_input)

        # Botones
        button_layout = QHBoxLayout()
        btn_guardar = QPushButton("Guardar")
        btn_cancelar = QPushButton("Cancelar")
        button_layout.addWidget(btn_guardar)
        button_layout.addWidget(btn_cancelar)

        btn_guardar.clicked.connect(self.accept)
        btn_cancelar.clicked.connect(self.reject)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def obtener_datos(self):
        """Devuelve los datos ingresados en el formulario."""
        return self.nombre_input.text(), self.tipo_input.text(), self.cuenta_input.text()


# Diálogo para gestionar Clientes
class ClienteDialog(QDialog):
    def __init__(self, datos=None):
        super().__init__()
        self.setWindowTitle("Agregar Cliente" if not datos else "Editar Cliente")
        self.resize(300, 200)

        layout = QVBoxLayout()

        self.nombre_input = QLineEdit(datos[0] if datos else "")
        self.codigo_input = QLineEdit(datos[1] if datos else "")

        layout.addWidget(QLabel("Nombre del Cliente:"))
        layout.addWidget(self.nombre_input)
        layout.addWidget(QLabel("Código de Cliente:"))
        layout.addWidget(self.codigo_input)

        button_layout = QHBoxLayout()
        btn_guardar = QPushButton("Guardar")
        btn_cancelar = QPushButton("Cancelar")

        btn_guardar.clicked.connect(self.accept)
        btn_cancelar.clicked.connect(self.reject)

        button_layout.addWidget(btn_guardar)
        button_layout.addWidget(btn_cancelar)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def obtener_datos(self):
        """Devuelve los datos ingresados en el formulario."""
        return self.nombre_input.text(), self.codigo_input.text()
