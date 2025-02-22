from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QComboBox, QMessageBox
)
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QDateEdit


class RegistroConsumos(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Registro de Consumos")
        self.resize(400, 600)

        # Layout principal
        layout = QVBoxLayout()

        # Campos del formulario
        layout.addWidget(QLabel("Placa del Vehículo:"))
        self.placa_input = QLineEdit()
        layout.addWidget(self.placa_input)

        layout.addWidget(QLabel("Servicio Propio:"))
        self.servicio_propios_input = QLineEdit()
        layout.addWidget(self.servicio_propios_input)

        layout.addWidget(QLabel("Producto:"))
        self.producto_input = QLineEdit()
        layout.addWidget(self.producto_input)

        layout.addWidget(QLabel("Repuesto:"))
        self.repuesto_input = QLineEdit()
        layout.addWidget(self.repuesto_input)

        layout.addWidget(QLabel("Servicio de Terceros:"))
        self.serv_terceros_input = QLineEdit()
        layout.addWidget(self.serv_terceros_input)

        layout.addWidget(QLabel("Fecha de la Factura:"))
        self.fecha_input = QDateEdit(QDate.currentDate())
        self.fecha_input.setCalendarPopup(True)
        layout.addWidget(self.fecha_input)

        layout.addWidget(QLabel("Cliente (Dejar vacío para Cliente Fiel):"))
        self.cliente_input = QComboBox()
        self.cliente_input.addItems([""] + self.controller.obtener_lista_clientes())
        layout.addWidget(self.cliente_input)

        layout.addWidget(QLabel("Canal (opcional):"))
        self.canal_input = QComboBox()
        self.canal_input.addItems([""] + self.controller.obtener_lista_canales())
        layout.addWidget(self.canal_input)

        # Botones
        button_layout = QHBoxLayout()
        btn_guardar = QPushButton("Guardar")
        btn_cancelar = QPushButton("Cancelar")
        button_layout.addWidget(btn_guardar)
        button_layout.addWidget(btn_cancelar)

        btn_guardar.clicked.connect(self.guardar_consumo)
        btn_cancelar.clicked.connect(self.close)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def guardar_consumo(self):
        """Guarda el consumo en la base de datos."""
        try:
            # Validar la placa (obligatoria)
            placa = self.placa_input.text().strip()
            if not placa:
                QMessageBox.warning(self, "Error", "La Placa del Vehículo es obligatoria.")
                return

            # Validar campos numéricos
            try:
                servicio_propios = float(self.servicio_propios_input.text() or 0.0)
                producto = float(self.producto_input.text() or 0.0)
                repuesto = float(self.repuesto_input.text() or 0.0)
                serv_terceros = float(self.serv_terceros_input.text() or 0.0)
            except ValueError:
                QMessageBox.warning(self, "Error", "Por favor, ingrese valores numéricos en los campos de montos.")
                return

            fecha_factura = self.fecha_input.date().toString("yyyy-MM-dd")
            canal_nombre = self.canal_input.currentText()
            cliente_nombre = self.cliente_input.currentText()

            total_factura = servicio_propios + producto + repuesto + serv_terceros

            # Obtener o registrar cliente fiel
            if cliente_nombre:  # Cliente seleccionado de la lista
                cliente_id = self.controller.obtener_id_cliente(cliente_nombre)
                if cliente_id is None:  # Manejar si no se encuentra el cliente
                    raise ValueError("Cliente no encontrado en la base de datos.")
            else:  # Cliente fiel con nombre igual a la placa
                cliente_id = self.controller.registrar_cliente_fiel(placa)

            # Obtener canal_id si existe
            canal_id = self.controller.obtener_id_canal(canal_nombre) if canal_nombre else None

            # Datos a insertar en consumos
            datos = (
                cliente_id,
                placa,
                fecha_factura,
                servicio_propios,
                producto,
                repuesto,
                serv_terceros,
                total_factura,
                canal_id
            )

            # Guardar en la base de datos
            self.controller.registrar_consumo(datos)
            QMessageBox.information(self, "Éxito", "Consumo registrado correctamente.")
            self.close()

        except ValueError as ve:
            QMessageBox.warning(self, "Error", f"Error en los datos: {ve}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar el consumo: {e}")
