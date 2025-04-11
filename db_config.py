# Importa la biblioteca necesaria para conectar con MySQL
import mysql.connector

# Función para obtener la conexión a la base de datos 
def get_connection(database='facturas'):
   return mysql.connector.connect(
       host='localhost',       # Servidor local
       user='root',            # Usuario de la base de datos
       password='root',        # Contraseña del usuario
       database=database       # Nombre de la base de datos (por defecto 'facturas')
   )

"""Esta función se utiliza para crear la base de datos si no existe 
(me arrojaba error así que tuve que hacerlo de esta manera)"""

def get_server_connection():
   return mysql.connector.connect(
       host='localhost',       # Servidor local
       user='root',            # Usuario de la base de datos
       password='root'         # Contraseña del usuario
   )