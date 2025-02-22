from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt
from app.ui.canal_dialogs import CanalDialog


class GestionCanales(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Gestión de Canales")
        self.resize(600, 400)

        # Layout principal
        layout = QVBoxLayout()

        # Tabla para mostrar canales
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Tipo", "Cuenta Bancaria"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)

        # Botones de acción
        button_layout = QHBoxLayout()
        btn_agregar = QPushButton("Agregar Canal")
        btn_editar = QPushButton("Editar Canal")
        btn_eliminar = QPushButton("Eliminar Canal")

        btn_agregar.clicked.connect(self.agregar_canal)
        btn_editar.clicked.connect(self.editar_canal)
        btn_eliminar.clicked.connect(self.eliminar_canal)

        button_layout.addWidget(btn_agregar)
        button_layout.addWidget(btn_editar)
        button_layout.addWidget(btn_eliminar)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        # Cargar datos iniciales
        self.cargar_datos()

    def cargar_datos(self):
        """Carga los canales desde la base de datos."""
        canales = self.controller.obtener_canales()
        self.table.setRowCount(len(canales))
        for row, canal in enumerate(canales):
            for col, valor in enumerate(canal):
                self.table.setItem(row, col, QTableWidgetItem(str(valor)))

    def agregar_canal(self):
        """Abre un formulario para agregar un nuevo canal."""
        dialog = CanalDialog()
        if dialog.exec_():
            datos = dialog.obtener_datos()
            self.controller.agregar_canal(datos)
            self.cargar_datos()

    def editar_canal(self):
        """Edita el canal seleccionado."""
        fila = self.table.currentRow()
        if fila == -1:
            QMessageBox.warning(self, "Error", "Por favor, selecciona un canal para editar.")
            return
        canal_id = self.table.item(fila, 0).text()
        nombre = self.table.item(fila, 1).text()
        tipo = self.table.item(fila, 2).text()
        cuenta = self.table.item(fila, 3).text()

        dialog = CanalDialog((nombre, tipo, cuenta))
        if dialog.exec_():
            datos = dialog.obtener_datos()
            self.controller.editar_canal(canal_id, datos)
            self.cargar_datos()

    def eliminar_canal(self):
        """Elimina el canal seleccionado."""
        fila = self.table.currentRow()
        if fila == -1:
            QMessageBox.warning(self, "Error", "Por favor, selecciona un canal para eliminar.")
            return

        canal_id = self.table.item(fila, 0).text()
        confirmar = QMessageBox.question(self, "Eliminar Canal", "¿Estás seguro de eliminar este canal?",
                                         QMessageBox.Yes | QMessageBox.No)
        if confirmar == QMessageBox.Yes:
            self.controller.eliminar_canal(canal_id)
            self.cargar_datos()
