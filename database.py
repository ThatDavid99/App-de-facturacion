# Importa las funciones de conexión del módulo db_config
from db_config import get_connection
from db_config import get_server_connection, get_connection

# Función para crear la base de datos facturas
def crear_base_de_datos():
   try:
       # Obtiene conexión al servidor MySQL (sin base de datos específica)
       conn = get_server_connection()
       cursor = conn.cursor()
       # Crea la base de datos si no existe
       cursor.execute("CREATE DATABASE IF NOT EXISTS facturas")
       print("Base de datos 'facturas' creada (o ya existía).")
   except Exception as e:
       # Maneja cualquier error durante la creación
       print("Error al crear la base de datos:", e)
   finally:
       # Cierra las conexiones independientemente del resultado
       cursor.close()
       conn.close()

# Función para crear las tablas necesarias en la base de datos
def crear_tablas():
   # Obtiene conexión a la base de datos facturas
   conn = get_connection()
   cursor = conn.cursor()

   try:
       # Crea la tabla de facturas si no existe
       cursor.execute("""
           CREATE TABLE IF NOT EXISTS facturas (
               id INT AUTO_INCREMENT PRIMARY KEY,
               numero VARCHAR(50) UNIQUE NOT NULL,
               fecha DATE NOT NULL,
               cliente_nombre VARCHAR(100) NOT NULL,
               vendedor VARCHAR(100) NOT NULL,
               estado BOOLEAN NOT NULL,
               valor_total FLOAT DEFAULT 0
           );
       """)

       # Crea la tabla de detalles de factura si no existe
       cursor.execute("""
           CREATE TABLE IF NOT EXISTS facturas_detalle (
               id INT AUTO_INCREMENT PRIMARY KEY,
               factura_id INT,
               articulo VARCHAR(100) NOT NULL,
               cantidad INT NOT NULL CHECK (cantidad > 0),
               precio_unitario FLOAT NOT NULL CHECK (precio_unitario >= 0),
               subtotal FLOAT NOT NULL,
               FOREIGN KEY (factura_id) REFERENCES facturas(id) ON DELETE CASCADE
           );
       """)

       # Confirma los cambios en la base de datos
       conn.commit()
       print("Tablas creadas (o ya existían).")
   except Exception as e:
       # Maneja cualquier error durante la creación de tablas
       print("Error al crear las tablas:", e)
   finally:
       # Cierra las conexiones independientemente del resultado
       cursor.close()
       conn.close()