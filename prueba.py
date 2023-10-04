import sqlite3
from datetime import datetime

# ... (Código de inicialización de la base de datos y las funciones de exportación a XLSX) ...

# Función para registrar una compra y actualizar el almacen y el archivo XLSX
def registrar_compra():
    proveedor = input("Ingrese el nombre del proveedor: ")
    producto = input("Ingrese el nombre del producto comprado: ")
    cantidad = int(input("Ingrese la cantidad comprada: "))
    precio = float(input("Ingrese el precio unitario: "))
    fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect('ventas.db')
    cursor = conn.cursor()

    # Registrar la compra en la tabla 'compras'
    cursor.execute('''
        INSERT INTO compras (proveedor, producto, cantidad, precio, fecha)
        VALUES (?, ?, ?, ?, ?)
    ''', (proveedor, producto, cantidad, precio, fecha))

    # Verificar si el producto existe en el almacen
    cursor.execute('SELECT id_producto, cantidad FROM almacen WHERE producto = ?', (producto,))
    almacen_info = cursor.fetchone()

    if almacen_info:
        # Si el producto existe en el almacen, actualizar la cantidad
        id_producto = almacen_info[0]
        nueva_cantidad = almacen_info[1] + cantidad
        cursor.execute('''
            UPDATE almacen
            SET cantidad = ?
            WHERE id_producto = ?
        ''', (nueva_cantidad, id_producto))
    else:
        # Si el producto no existe en el almacen, SQLite generará un ID único automáticamente
        cursor.execute('''
            INSERT INTO almacen (producto, cantidad)
            VALUES (?, ?)
        ''', (producto, cantidad))

    conn.commit()
    conn.close()

    # Exportar los datos actualizados del almacen y las compras a los archivos XLSX
    exportar_almacen_a_xlsx()
    exportar_compras_a_xlsx()

    print("Compra registrada correctamente.")

# ... (Resto del código, incluyendo la función del menú principal) ...

if __name__ == '__main__':
    crear_tabla_almacen()
    inicializar_base_de_datos()
    menu_principal()



# Función para ver el contenido del almacen
def ver_almacen():
    conn = sqlite3.connect('ventas.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id_producto, producto, cantidad, proveedor FROM almacen')
    filas = cursor.fetchall()

    if not filas:
        print("El almacen está vacío.")
    else:
        print("Contenido del Almacen:")
        print("{:<15} {:<25} {:<10} {:<15}".format("ID Producto", "Producto", "Cantidad", "Proveedor"))
        for fila in filas:
            print("{:<15} {:<25} {:<10} {:<15}".format(fila[0], fila[1], fila[2], fila[3]))

    conn.close()

# ... (Resto del código, incluyendo la función del menú principal) ...

if __name__ == '__main__':
    crear_tabla_almacen()
    inicializar_base_de_datos()
    menu_principal()
