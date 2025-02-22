from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QHBoxLayout, QMessageBox
)
from app.ui.canal_dialogs import ClienteDialog

class GestionClientes(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Gestión de Clientes")
        self.resize(600, 400)

        # Layout principal
        layout = QVBoxLayout()

        # Tabla para mostrar clientes
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Código de Cliente"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)

        # Botones de acción
        button_layout = QHBoxLayout()
        btn_agregar = QPushButton("Agregar Cliente")
        btn_editar = QPushButton("Editar Cliente")
        btn_eliminar = QPushButton("Eliminar Cliente")

        btn_agregar.clicked.connect(self.agregar_cliente)
        btn_editar.clicked.connect(self.editar_cliente)
        btn_eliminar.clicked.connect(self.eliminar_cliente)

        button_layout.addWidget(btn_agregar)
        button_layout.addWidget(btn_editar)
        button_layout.addWidget(btn_eliminar)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        # Cargar datos iniciales
        self.cargar_datos()

    def cargar_datos(self):
        """Carga los clientes desde la base de datos."""
        self.table.setRowCount(0)  # Limpia la tabla
        clientes = self.controller.obtener_clientes()
        self.table.setRowCount(len(clientes))
        for row, cliente in enumerate(clientes):
            for col, valor in enumerate(cliente):
                self.table.setItem(row, col, QTableWidgetItem(str(valor)))

    def agregar_cliente(self):
        """Abre un formulario para agregar un nuevo cliente."""
        dialog = ClienteDialog()
        if dialog.exec_():
            datos = dialog.obtener_datos()
            if all(datos):
                self.controller.agregar_cliente(datos)
                self.cargar_datos()
                QMessageBox.information(self, "Éxito", "Cliente agregado correctamente.")
            else:
                QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")

    def editar_cliente(self):
        """Edita el cliente seleccionado."""
        fila = self.table.currentRow()
        if fila == -1:
            QMessageBox.warning(self, "Error", "Selecciona un cliente para editar.")
            return

        cliente_id = self.table.item(fila, 0).text()
        nombre = self.table.item(fila, 1).text()
        codigo = self.table.item(fila, 2).text()

        dialog = ClienteDialog((nombre, codigo))
        if dialog.exec_():
            nuevos_datos = dialog.obtener_datos()
            if all(nuevos_datos):
                self.controller.editar_cliente(cliente_id, nuevos_datos)
                self.cargar_datos()
                QMessageBox.information(self, "Éxito", "Cliente editado correctamente.")
            else:
                QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")

    def eliminar_cliente(self):
        """Elimina el cliente seleccionado."""
        fila = self.table.currentRow()
        if fila == -1:
            QMessageBox.warning(self, "Error", "Selecciona un cliente para eliminar.")
            return

        cliente_id = self.table.item(fila, 0).text()
        confirmar = QMessageBox.question(
            self, "Eliminar Cliente", "¿Seguro que deseas eliminar este cliente?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirmar == QMessageBox.Yes:
            self.controller.eliminar_cliente(cliente_id)
            self.cargar_datos()
            QMessageBox.information(self, "Éxito", "Cliente eliminado correctamente.")
