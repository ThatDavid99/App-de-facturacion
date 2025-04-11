# Importa la función de conexión a la base de datos
from db_config import get_connection

# Función para verificar si un número de factura ya existe en la base de datos
def factura_numero_unico(numero):
   conn = get_connection()
   cursor = conn.cursor()
   # Consulta para contar facturas con el mismo número
   cursor.execute("SELECT COUNT(*) FROM facturas WHERE numero = %s", (numero,))
   result = cursor.fetchone()[0]  # Obtiene la cantidad de coincidencias
   cursor.close()
   conn.close()
   return result == 0  # Retorna True si no existe ninguna factura con ese número

# Función para validar los datos de una factura antes de insertarla
def validar_factura(data, detalles):
   errores = []  # Lista para almacenar mensajes de error

   # Validación de campos obligatorios en los datos principales
   if not data['numero']:
       errores.append("El número de factura es obligatorio.")
   elif not factura_numero_unico(data['numero']):
       errores.append("El número de factura ya existe.")

   if not data['fecha']:
       errores.append("La fecha es obligatoria.")

   if not data['cliente']:
       errores.append("El nombre del cliente es obligatorio.")

   if not data['vendedor']:
       errores.append("El nombre del vendedor es obligatorio.")

   if data['estado'] not in [True, False]:
       errores.append("Estado inválido.")

   # Validación de los detalles/ítems de la factura
   if not detalles or not isinstance(detalles, list):
       errores.append("Debe haber al menos un ítem en el detalle.")

   # Revisa cada ítem del detalle
   for idx, item in enumerate(detalles):
       if not item['articulo']:
           errores.append(f"Ítem {idx+1}: El nombre del artículo es obligatorio.")
       if item['cantidad'] <= 0:
           errores.append(f"Ítem {idx+1}: La cantidad debe ser mayor que 0.")
       if item['precio_unitario'] < 0:
           errores.append(f"Ítem {idx+1}: El precio unitario no puede ser negativo.")

   return errores  # Retorna la lista de errores encontrados