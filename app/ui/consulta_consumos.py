from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QFileDialog, QMessageBox, QLabel, QDateEdit
)
from PyQt5.QtCore import QDate
from openpyxl import Workbook
from datetime import datetime

class ConsultaConsumos(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Consulta de Consumos")
        self.resize(600, 500)

        layout = QVBoxLayout()

        # Campos de filtro por fechas
        layout.addWidget(QLabel("Desde:"))
        self.fecha_inicio = QDateEdit(QDate.currentDate())
        self.fecha_inicio.setCalendarPopup(True)
        layout.addWidget(self.fecha_inicio)

        layout.addWidget(QLabel("Hasta:"))
        self.fecha_fin = QDateEdit(QDate.currentDate())
        self.fecha_fin.setCalendarPopup(True)
        layout.addWidget(self.fecha_fin)

        # Tabla de consumos
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "ID", "Placa", "Fecha Factura", "Servicio Propio", "Producto",
            "Repuesto", "Servicio Terceros", "Total Factura"
        ])
        layout.addWidget(self.table)

        # Botones
        btn_cargar = QPushButton("Cargar Consumos")
        btn_cargar.clicked.connect(self.cargar_consumos)
        layout.addWidget(btn_cargar)

        btn_exportar = QPushButton("Exportar a Excel")
        btn_exportar.clicked.connect(self.exportar_excel)
        layout.addWidget(btn_exportar)

        self.setLayout(layout)

    def cargar_consumos(self):
        """Carga los consumos desde la base de datos con filtro de fechas."""
        try:
            fecha_inicio = self.fecha_inicio.date().toString("yyyy-MM-dd")
            fecha_fin = self.fecha_fin.date().toString("yyyy-MM-dd")

            query = """
            SELECT id, placa, fecha_factura, servicio_propios, producto, repuesto,
                   serv_terceros, total_factura 
            FROM consumos
            WHERE fecha_factura BETWEEN ? AND ?
            """
            datos = self.controller.db_manager.obtener_datos(query, (fecha_inicio, fecha_fin))

            if not datos:
                QMessageBox.warning(self, "Sin Datos", "No hay registros en el rango de fechas seleccionado.")
                return

            # Actualizar la tabla con los datos
            self.table.setRowCount(len(datos))
            for row, consumo in enumerate(datos):
                for col, valor in enumerate(consumo):
                    self.table.setItem(row, col, QTableWidgetItem(str(valor)))

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar los consumos: {e}")

    def exportar_excel(self):
        """Exporta los datos de la tabla a un archivo Excel con nombre dinámico."""
        try:
            fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"consumos_{fecha_actual}.xlsx"

            file_path, _ = QFileDialog.getSaveFileName(self, "Guardar Informe", nombre_archivo, "Archivos Excel (*.xlsx)")
            if not file_path:
                return  # Usuario canceló

            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "Consumos"

            # Encabezados
            headers = [
                "ID", "Placa", "Fecha Factura", "Servicio Propio", 
                "Producto", "Repuesto", "Servicio Terceros", "Total Factura"
            ]
            sheet.append(headers)

            # Datos
            for row in range(self.table.rowCount()):
                sheet.append([
                    self.table.item(row, col).text() if self.table.item(row, col) else ""
                    for col in range(8)
                ])

            workbook.save(file_path)
            QMessageBox.information(self, "Éxito", f"Datos exportados a: {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo exportar el archivo: {e}")
