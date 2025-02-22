from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QFileDialog, QMessageBox
from openpyxl import Workbook

class GenerarInformes(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Generar Reportes")
        self.resize(600, 400)

        layout = QVBoxLayout()

        # Botón de reporte de consumos
        btn_reporte_consumos = QPushButton("Generar Reporte de Consumos por Cliente")
        btn_reporte_consumos.clicked.connect(self.reporte_consumos)
        layout.addWidget(btn_reporte_consumos)

        # Botón de reporte de comisiones
        btn_reporte_comisiones = QPushButton("Generar Reporte de Comisiones por Canal")
        btn_reporte_comisiones.clicked.connect(self.reporte_comisiones)
        layout.addWidget(btn_reporte_comisiones)

        self.setLayout(layout)

    def exportar_excel(self, datos, columnas, nombre_archivo):
        """Exporta los datos a un archivo Excel."""
        file_path, _ = QFileDialog.getSaveFileName(self, "Guardar Reporte", nombre_archivo, "Archivos Excel (*.xlsx)")
        if file_path:
            workbook = Workbook()
            sheet = workbook.active
            sheet.append(columnas)
            for row in datos:
                sheet.append(row)
            workbook.save(file_path)
            QMessageBox.information(self, "Éxito", f"Reporte guardado en: {file_path}")

    def reporte_consumos(self):
        """Genera un reporte de consumos por cliente."""
        datos = self.controller.obtener_reporte_consumos()
        columnas = ["Cliente", "Total de Consumos"]
        self.exportar_excel(datos, columnas, "reporte_consumos.xlsx")

    def reporte_comisiones(self):
        """Genera un reporte de comisiones por canal."""
        datos = self.controller.obtener_reporte_comisiones()
        columnas = ["Canal", "Total de Comisiones"]
        self.exportar_excel(datos, columnas, "reporte_comisiones.xlsx")
