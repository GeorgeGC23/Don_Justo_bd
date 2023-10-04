import sqlite3

# ... (Código de inicialización de la base de datos y las funciones de exportación a XLSX) ...

# Función para registrar un producto en el almacen con ID único generado por SQLite
def registrar_producto_almacen():
    producto = input("Ingrese el nombre del producto a agregar al almacen: ")
    cantidad = int(input("Ingrese la cantidad inicial en el almacen: "))

    conn = sqlite3.connect('ventas.db')
    cursor = conn.cursor()

    # Insertar el producto en el almacen con un ID autoincremental
    cursor.execute('''
        INSERT INTO almacen (producto, cantidad)
        VALUES (?, ?)
    ''', (producto, cantidad))

    conn.commit()
    conn.close()

    # Consultar el ID generado automáticamente para el producto
    conn = sqlite3.connect('ventas.db')
    cursor = conn.cursor()
    cursor.execute('SELECT last_insert_rowid()')
    last_id = cursor.fetchone()[0]
    conn.close()

    # Construir el ID personalizado
    nuevo_id = f'DJ001P00{last_id:03d}'

    # Actualizar el registro del producto en el almacen con el nuevo ID
    conn = sqlite3.connect('ventas.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE almacen SET id_producto = ? WHERE rowid = ?', (nuevo_id, last_id))
    conn.commit()
    conn.close()

    print(f"Producto '{producto}' registrado en el almacen con ID personalizado: {nuevo_id}.")

# ... (Resto del código, incluyendo la función del menú principal) ...

if __name__ == '__main__':
    crear_tabla_almacen()
    inicializar_base_de_datos()
    menu_principal()
