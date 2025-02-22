import sqlite3

class DBManager:
    def __init__(self):
        """Inicializa la conexión con la base de datos SQLite."""
        self.conexion = sqlite3.connect("app_database.db")  # Crea o abre la base de datos local
        self.cursor = self.conexion.cursor()
        self.crear_tablas()

    def crear_tablas(self):
        """Crea las tablas necesarias si no existen y modifica las existentes."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS canales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                tipo TEXT NOT NULL,
                cuenta_bancaria TEXT NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                codigo_cliente TEXT NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS consumos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER,
                placa TEXT NOT NULL,
                fecha_factura TEXT,
                servicio TEXT DEFAULT NULL,
                servicio_propios REAL,
                producto REAL,
                repuesto REAL,
                serv_terceros REAL,
                total_factura REAL,
                canal_id INTEGER,
                FOREIGN KEY (cliente_id) REFERENCES clientes(id),
                FOREIGN KEY (canal_id) REFERENCES canales(id)
            )
        """)


    # Verificar y agregar columnas faltantes
        columnas_necesarias = {
            "cliente_id": "INTEGER",
            "fecha_factura": "TEXT",
            "servicio_propios": "REAL",
            "servicio": "TEXT",
            "producto": "REAL",
            "repuesto": "REAL",
            "serv_terceros": "REAL",
            "total_factura": "REAL",
            "canal_id": "INTEGER"
        }

        for columna, tipo in columnas_necesarias.items():
            try:
                self.cursor.execute(f"ALTER TABLE consumos ADD COLUMN {columna} {tipo}")
            except sqlite3.OperationalError:
                pass  # La columna ya existe, no hacer nada

        self.conexion.commit()




    def obtener_datos(self, query, parametros=None):
        """Ejecuta una consulta SELECT con parámetros opcionales y devuelve los resultados."""
        print(f"Ejecutando consulta: {query} con parámetros: {parametros}")
        if parametros:
            self.cursor.execute(query, parametros)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()



    def ejecutar_consulta(self, query, datos):
        """Ejecuta consultas INSERT, UPDATE o DELETE."""
        print(f"Ejecutando consulta: {query} con datos {datos}")
        self.cursor.execute(query, datos)
        self.conexion.commit()

    def cerrar_conexion(self):
        """Cierra la conexión con la base de datos."""
        self.conexion.close()
