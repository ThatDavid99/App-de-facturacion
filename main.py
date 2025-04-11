from models import insertar_factura, listar_facturas, ver_factura_detallada
from validators import validar_factura
from database import crear_base_de_datos, crear_tablas

def main():
    crear_base_de_datos()
    crear_tablas()
    while True:
        print("\n--- Menú ---")
        print("1. Crear nueva factura")
        print("2. Listar facturas")
        print("3. Ver factura detallada")
        print("4. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            data = {
                "numero": input("Número de factura: "),
                "fecha": input("Fecha (YYYY-MM-DD): "),
                "cliente": input("Nombre del cliente: "),
                "vendedor": input("Nombre del vendedor: "),
                "estado": input("Estado (1 = activa, 0 = inactiva): ") == "1"
            }

            detalles = []
            while True:
                articulo = input("Artículo (vacío para terminar): ")
                if not articulo:
                    break
                cantidad = int(input("Cantidad: "))
                precio = float(input("Precio unitario: "))
                detalles.append({
                    "articulo": articulo,
                    "cantidad": cantidad,
                    "precio_unitario": precio
                })

            errores = validar_factura(data, detalles)
            if errores:
                print("\n Errores de validación:")
                for err in errores:
                    print("-", err)
            else:
                insertar_factura(data, detalles)

        elif opcion == "2":
            listar_facturas()

        elif opcion == "3":
            id_factura = int(input("ID de la factura: "))
            ver_factura_detallada(id_factura)

        elif opcion == "4":
            break

        else:
            print(" Opción inválida")

if __name__ == "__main__":
    main()
