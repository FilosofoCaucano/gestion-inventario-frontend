import random
from app.ui.gestion_canales import GestionCanales
from app.ui.gestion_clientes import GestionClientes
from app.ui.registro_consumos import RegistroConsumos
from app.ui.consulta_consumos import ConsultaConsumos
from app.ui.generar_informes import GenerarInformes


class Controller:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.gestion_canales_window = None
        self.gestion_clientes_window = None
        self.registro_consumos_window = None
        self.consulta_consumos_window = None
        self.generar_informes_window = None

    def abrir_registro_consumos(self):
        """Abre la ventana de registro de consumos."""
        if self.registro_consumos_window is None:
            self.registro_consumos_window = RegistroConsumos(self)
        self.registro_consumos_window.show()

    def registrar_consumo(self, datos):
        """
        Registra un consumo en la base de datos y aplica descuento si corresponde.
        Datos: (cliente_id, placa, fecha_factura, servicio_propios, producto, repuesto, serv_terceros, total_factura, canal_id)
        """
        cliente_id = datos[0]
        total_factura = datos[-2]

        # Contar visitas del cliente
        visitas = self.contar_visitas_cliente(cliente_id)

        # Aplicar descuento si tiene 5 o más registros
        if visitas >= 5:
            total_factura *= 0.9  # Aplicar 10% de descuento
            print(f"Descuento del 10% aplicado para cliente con ID {cliente_id}. Nuevo total: {total_factura}")

        # Insertar los datos ajustados
        query = """
        INSERT INTO consumos (cliente_id, placa, fecha_factura, 
                              servicio_propios, producto, repuesto, 
                              serv_terceros, total_factura, canal_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.db_manager.ejecutar_consulta(query, datos[:-2] + (total_factura, datos[-1]))

    def registrar_cliente_fiel(self, placa, canal_id=None):
        """
        Registra un cliente fiel si no existe.
        - Si canal_id es proporcionado, se asocia al canal.
        - Si no, el cliente se registra como fiel sin canal.
        """
        cliente_id = self.obtener_id_cliente(placa)
        if cliente_id:  # Si el cliente ya existe
            print(f"Cliente '{placa}' ya existe con ID {cliente_id}.")
            return cliente_id

        # Crear un nuevo cliente fiel
        codigo_cliente_fiel = self.generar_id_cliente_fiel()
        query = "INSERT INTO clientes (nombre, codigo_cliente, canal_id, es_fiel) VALUES (?, ?, ?, TRUE)"
        self.db_manager.ejecutar_consulta(query, (placa, codigo_cliente_fiel, canal_id))
        return self.db_manager.obtener_ultimo_id()


    def generar_id_cliente_fiel(self):
        """Genera un código único para clientes fieles."""
        numero = random.randint(1000, 9999)
        return f"B{numero}"

    def contar_visitas_cliente(self, cliente_id):
        """Cuenta el número de visitas de un cliente en la tabla de consumos."""
        query = "SELECT COUNT(*) FROM consumos WHERE cliente_id = ?"
        resultado = self.db_manager.obtener_datos(query, (cliente_id,))
        return resultado[0][0] if resultado else 0

    def obtener_id_cliente(self, nombre):
        """Obtiene el ID de un cliente por su nombre."""
        query = "SELECT id FROM clientes WHERE nombre = ?"
        resultado = self.db_manager.obtener_datos(query, (nombre,))
        return resultado[0][0] if resultado else None
    
    def obtener_id_canal(self, nombre):
        """Obtiene el ID de un canal por su nombre."""
        query = "SELECT id FROM canales WHERE nombre = ?"
        resultado = self.db_manager.obtener_datos(query, (nombre,))
        return resultado[0][0] if resultado else None
    

    def obtener_lista_clientes(self):
        """Devuelve una lista de nombres de clientes."""
        query = "SELECT nombre FROM clientes"
        return [cliente[0] for cliente in self.db_manager.obtener_datos(query)]

    def obtener_lista_canales(self):
        """Devuelve una lista de nombres de canales."""
        query = "SELECT nombre FROM canales"
        return [canal[0] for canal in self.db_manager.obtener_datos(query)]
    
    def obtener_canales(self):
        """Obtiene todos los datos de los canales desde la base de datos."""
        query = "SELECT id, nombre, tipo, cuenta_bancaria FROM canales"
        return self.db_manager.obtener_datos(query)


    def obtener_informe(self, fecha_inicio, fecha_fin):
        """Genera un informe filtrado por fechas."""
        query = """
            SELECT 
                c.id, c.placa, COALESCE(cl.nombre, 'Sin Cliente') AS cliente,
                COALESCE(cn.nombre, 'Sin Canal') AS canal, 
                c.servicio_propios, c.producto, c.repuesto, c.serv_terceros,
                c.total_factura, (c.total_factura * 0.10) AS comision, c.fecha_factura
            FROM consumos AS c
            LEFT JOIN clientes AS cl ON c.cliente_id = cl.id
            LEFT JOIN canales AS cn ON c.canal_id = cn.id
            WHERE c.fecha_factura BETWEEN ? AND ?
        """
        return self.db_manager.obtener_datos(query, (fecha_inicio, fecha_fin))
    
    
    def abrir_gestion_canales(self):
        """Abre la ventana de gestión de canales."""
        if self.gestion_canales_window is None:
            self.gestion_canales_window = GestionCanales(self)
        self.gestion_canales_window.show()
        
    def abrir_gestion_clientes(self):
        """Abre la ventana de gestión de clientes."""
        if self.gestion_clientes_window is None:
            self.gestion_clientes_window = GestionClientes(self)
        self.gestion_clientes_window.show()
        
    def abrir_consulta_consumos(self):
        """Abre la ventana de consulta de consumos."""
        if self.consulta_consumos_window is None:
            self.consulta_consumos_window = ConsultaConsumos(self)
        self.consulta_consumos_window.show()
        
    def abrir_generar_informes(self):
        """Abre la ventana de generación de informes."""
        if self.generar_informes_window is None:
            self.generar_informes_window = GenerarInformes(self)
        self.generar_informes_window.show()
        
    def obtener_clientes(self):
        """Obtiene todos los datos de los clientes desde la base de datos."""
        query = "SELECT id, nombre, codigo_cliente FROM clientes"
        return self.db_manager.obtener_datos(query)
    
    def buscar_cliente_por_nombre_o_placa(self, valor):
        """Busca un cliente por su nombre o placa en la base de datos."""
        query = "SELECT id, nombre, codigo_cliente FROM clientes WHERE nombre = ? OR codigo_cliente = ?"
        resultado = self.db_manager.obtener_datos(query, (valor, valor))
        return resultado[0] if resultado else None
    
    def crear_cliente(self, nombre, canal_id=None):
        """
        Crea un cliente general, asignando un canal si existe.
        - Si canal_id es None, el cliente será marcado como 'Cliente Fiel'.
        """
        cliente_id = self.obtener_id_cliente(nombre)
        if cliente_id:  # Verificar duplicados
            print(f"Cliente '{nombre}' ya existe con ID {cliente_id}.")
            return cliente_id

        # Insertar el cliente en la base de datos
        query = "INSERT INTO clientes (nombre, codigo_cliente, canal_id, es_fiel) VALUES (?, ?, ?, ?)"
        es_fiel = canal_id is None  # Si no hay canal, es cliente fiel
        codigo_cliente = self.generar_id_cliente_fiel()
        self.db_manager.ejecutar_consulta(query, (nombre, codigo_cliente, canal_id, es_fiel))
        return self.db_manager.obtener_ultimo_id()
    
    


    

