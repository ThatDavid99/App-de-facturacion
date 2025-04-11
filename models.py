# Importa la biblioteca MySQL y la función de conexión a la base de datos
import mysql
from db_config import get_connection

# Función para insertar una nueva factura con sus detalles
def insertar_factura(data, detalles):
   conn = get_connection()
   cursor = conn.cursor()

   try:
       # Insertar factura principal en la tabla facturas
       cursor.execute("""
           INSERT INTO facturas (numero, fecha, cliente_nombre, vendedor, estado, valor_total)
           VALUES (%s, %s, %s, %s, %s, %s)
       """, (
           data['numero'],
           data['fecha'],
           data['cliente'],
           data['vendedor'],
           data['estado'],
           0  # valor_total inicia en cero y se actualizará después
       ))
       factura_id = cursor.lastrowid  # Obtiene el ID de la factura recién insertada

       # Calcula el total sumando cada ítem de la factura
       total = 0
       for item in detalles:
           subtotal = item['cantidad'] * item['precio_unitario']
           total += subtotal
           # Inserta cada detalle de la factura
           cursor.execute("""
               INSERT INTO facturas_detalle (factura_id, articulo, cantidad, precio_unitario, subtotal)
               VALUES (%s, %s, %s, %s, %s)
           """, (
               factura_id,
               item['articulo'],
               item['cantidad'],
               item['precio_unitario'],
               subtotal
           ))

       # Actualiza el valor total en la tabla de facturas
       cursor.execute("UPDATE facturas SET valor_total = %s WHERE id = %s", (total, factura_id))
       conn.commit()  # Confirma todas las operaciones en la base de datos
       print("✅ Factura registrada correctamente.")
   except mysql.connector.Error as e:
       conn.rollback()  # Revierte cambios en caso de error
       print("Error al insertar factura:", e)
   finally:
       # Cierra las conexiones independientemente del resultado
       cursor.close()
       conn.close()

# Función para mostrar todas las facturas
def listar_facturas():
   conn = get_connection()
   cursor = conn.cursor(dictionary=True)  # Resultados como diccionarios para fácil acceso
   cursor.execute("SELECT * FROM facturas")
   for row in cursor.fetchall():
       print(row)
   cursor.close()
   conn.close()

# Función para mostrar una factura específica con todos sus detalles
def ver_factura_detallada(factura_id):
   conn = get_connection()
   cursor = conn.cursor(dictionary=True)
   # Obtiene la información principal de la factura
   cursor.execute("SELECT * FROM facturas WHERE id = %s", (factura_id,))
   factura = cursor.fetchone()
   print("Factura:", factura)

   # Obtiene los detalles/ítems de la factura
   cursor.execute("SELECT * FROM facturas_detalle WHERE factura_id = %s", (factura_id,))
   detalles = cursor.fetchall()
   print("Detalles:")
   for d in detalles:
       print(d)

   cursor.close()
   conn.close()