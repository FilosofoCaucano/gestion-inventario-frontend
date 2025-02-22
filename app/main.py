from PyQt5.QtWidgets import QApplication
from app.ui.main_window import MainWindow
from app.logic.controller import Controller
from app.Database.db_manager import DBManager

if __name__ == "__main__":
    app = QApplication([])

    # Inicializar el gestor de base de datos
    db_manager = DBManager()

    # Inicializar el controlador y la ventana principal
    controller = Controller(db_manager)
    main_window = MainWindow(controller)
    controller.view = main_window

    # Mostrar la ventana principal
    main_window.show()
    app.exec_()
