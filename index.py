import tkinter as tk
from tkinter import ttk
from recursos.base_de_datos import *
from recursos.logica_de_negocio import *
from tkinter import messagebox

class MenuPrincipalUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Don Justo")
        self.logica = LogicaDeNegocios()
        root.geometry("1200x650")

        # Inicialmente, ocultar la ventana principal
        self.ocultar_ventana_principal()

        # Crear una función que muestra la ventana de inicio de sesión o registro
        self.mostrar_ventana_inicio_sesion_o_registro()

    def ocultar_ventana_principal(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def mostrar_ventana_inicio_sesion_o_registro(self):
        # Crear elementos para el inicio de sesión y registro
        self.usuario_label = tk.Label(self.root, text="Usuario:")
        self.usuario_label.pack()
        self.usuario_entry = tk.Entry(self.root)
        self.usuario_entry.pack()

        self.contrasena_label = tk.Label(self.root, text="Contraseña:")
        self.contrasena_label.pack()
        self.contrasena_entry = tk.Entry(self.root, show="*")
        self.contrasena_entry.pack()

        self.registrar_button = tk.Button(self.root, text="Registrar", command=self.registrar_usuario)
        self.registrar_button.pack()

        self.iniciar_sesion_button = tk.Button(self.root, text="Iniciar Sesión", command=self.iniciar_sesion)
        self.iniciar_sesion_button.pack()

    def mostrar_ventana_principal(self):
        # Borra los elementos de la ventana actual
        self.ocultar_ventana_principal()

        # Crear un Frame principal para la ventana de opciones
        frame = tk.Frame(self.root)
        frame.pack(side="left", fill="y")

        # Crear botones para cada opción del menú
        self.btn_registrar_venta = tk.Button(frame, text="Registrar una Venta", command=self.registrar_venta)
        self.btn_ver_reporte_ventas = tk.Button(frame, text="Ver Reporte de Ventas", command=self.mostrar_reporte_ventas)
        self.btn_registrar_compra = tk.Button(frame, text="Registrar una Compra", command=self.registrar_compra)
        self.btn_ver_reporte_compras = tk.Button(frame, text="Ver Reporte de Compras", command=self.ver_reporte_compras)
        self.btn_ver_reporte_compras_almacen = tk.Button(frame, text="Ver Reporte de Compras para el Almacén", command=self.ver_reporte_compras_almacen)
        self.btn_ver_almacen = tk.Button(frame, text="Ver Almacén", command=self.mostrar_almacen)
        self.btn_limpiar_tablas = tk.Button(frame, text="Limpiar Contenido de Tablas", command=self.logica.limpiar_contenido_tablas)
        self.btn_modificar_precio = tk.Button(frame, text="Modificar Precio de un Producto", command=self.modificar_precio_producto)  

        # Utilizar el sistema de geometría grid para distribuir los botones
        self.btn_registrar_venta.grid(row=0, column=0, sticky="nsew")
        self.btn_ver_reporte_ventas.grid(row=1, column=0, sticky="nsew")
        self.btn_registrar_compra.grid(row=2, column=0, sticky="nsew")
        self.btn_ver_reporte_compras.grid(row=3, column=0, sticky="nsew")
        self.btn_ver_reporte_compras_almacen.grid(row=4, column=0, sticky="nsew")
        self.btn_ver_almacen.grid(row=5, column=0, sticky="nsew")
        self.btn_limpiar_tablas.grid(row=6, column=0, sticky="nsew")
        self.btn_modificar_precio.grid(row=7, column=0, sticky="nsew")

        # Configurar el peso de las filas para que sean proporcionales
        for i in range(8):
            frame.grid_rowconfigure(i, weight=1)

        # Inicializar variables para la sección de reporte de ventas
        self.section_reporte_ventas = None
        self.tabla_ventas = None
        self.campo_busqueda = None

        # Inicializar variables para la sección de ver almacen
        self.section_ver_almacen = None
        self.tabla_almacen = None  
        
        # Inicializar variables para la sección de registro de compra
        self.section_registrar_compra = None
        
        # Inicializar variables para la sección de ver el reporte de compras
        self.section_reporte_compras = None
        self.tabla_compras = None
        
        # Inicializar variables para la sección de ver el balance de compras
        self.tabla_compras_almacen = None
        self.section_reporte_compras_almacen = None
        
        # Inicializar variables para la sección de actualizacion de precios
        self.nuevo_precio_entry = None
        self.section_modificar_precio_producto = None
        
        # Inicializar variables para la sección de registrar venta
        self.section_registrar_venta = None

    def registrar_usuario(self):
        usuario = self.usuario_entry.get()
        contrasena = self.contrasena_entry.get()

        if not usuario or not contrasena:
            messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")
            return

        # Verificar si el usuario ya existe
        usuario_existente = self.logica.base_de_datos.autenticar_usuario(usuario, contrasena)
        if usuario_existente:
            messagebox.showwarning("Advertencia", "El usuario ya existe. Por favor, inicie sesión en su lugar.")
            return

        # Registrar al usuario en la base de datos
        self.logica.base_de_datos.registrar_usuario(usuario, contrasena)
        messagebox.showinfo("Éxito", "Usuario registrado correctamente.")

    def iniciar_sesion(self):
        usuario = self.usuario_entry.get()
        contrasena = self.contrasena_entry.get()

        if not usuario or not contrasena:
            messagebox.showwarning("Advertia", "Por favorenc, complete todos los campos.")
            return

        # Autenticar al usuario
        usuario_autenticado = self.logica.base_de_datos.autenticar_usuario(usuario, contrasena)
        if usuario_autenticado:
            messagebox.showinfo("Éxito", "Inicio de sesión exitoso.")
            # Realizar acciones adicionales después del inicio de sesión
            self.mostrar_ventana_principal()
        else:
            messagebox.showwarning("Advertencia", "Inicio de sesión fallido. Verifique sus credenciales.")           
        
    def mostrar_reporte_ventas(self):
        # Limpiar la ventana principal antes de mostrar el reporte de ventas
        self.limpiar_ventana()

        # Crear una sección para el reporte de ventas
        self.section_reporte_ventas = tk.Frame(self.root)
        self.section_reporte_ventas.pack(side="left", fill="both", expand=True)

        # Crear una etiqueta y un campo de entrada para buscar por ID
        etiqueta_busqueda = tk.Label(self.section_reporte_ventas, text="Buscar por ID de Venta:")
        etiqueta_busqueda.grid(row=0, column=0)
        self.campo_busqueda = tk.Entry(self.section_reporte_ventas)
        self.campo_busqueda.grid(row=0, column=1)

        # Crear una tabla para mostrar el reporte de ventas
        self.tabla_ventas = ttk.Treeview(self.section_reporte_ventas, columns=("ID", "Producto", "Cantidad", "Unidad", "Precio", "Fecha"), height=20, show="headings")
        self.tabla_ventas.heading("ID", text="ID")
        self.tabla_ventas.heading("Producto", text="Producto")
        self.tabla_ventas.heading("Cantidad", text="Cantidad")
        self.tabla_ventas.heading("Unidad", text="Unidad")
        self.tabla_ventas.heading("Precio", text="Precio")
        self.tabla_ventas.heading("Fecha", text="Fecha")
        self.tabla_ventas.grid(row=1, column=0, columnspan=2)


        # Configurar el ancho de las columnas
        self.tabla_ventas.column("#1", width=100)  # Ancho de la columna ID
        self.tabla_ventas.column("#2", width=200)  # Ancho de la columna Producto
        self.tabla_ventas.column("#3", width=100)  # Ancho de la columna Cantidad
        self.tabla_ventas.column("#4", width=100)  # Ancho de la columna Unidad
        self.tabla_ventas.column("#5", width=100)  # Ancho de la columna Precio
        self.tabla_ventas.column("#6", width=150)  # Ancho de la columna Fecha

        def buscar_venta():
            # Obtener el ID de búsqueda
            id_busqueda = self.campo_busqueda.get()
            # Implementa la búsqueda de la venta por ID (debes ajustarlo a tus datos)
            venta_encontrada = self.logica.buscar_venta_por_id(id_busqueda)  # Reemplaza con tu lógica
            # Limpia la tabla
            for item in self.tabla_ventas.get_children():
                self.tabla_ventas.delete(item)
            # Llena la tabla con la venta encontrada
            if venta_encontrada:
                self.tabla_ventas.insert("", "end", values=venta_encontrada)

        def mostrar_ventas_completas():
            # Implementa la obtención de todas las ventas completas
            ventas_completas = self.logica.obtener_todas_las_ventas()
            # Limpia la tabla
            for item in self.tabla_ventas.get_children():
                self.tabla_ventas.delete(item)
            # Llena la tabla con todas las ventas
            for venta in ventas_completas:
                self.tabla_ventas.insert("", "end", values=venta)

        # Botón para buscar
        btn_buscar = tk.Button(self.section_reporte_ventas, text="Buscar", command=buscar_venta)
        btn_buscar.grid(row=0, column=2)

        # Botón para mostrar todas las ventas
        btn_mostrar_todas = tk.Button(self.section_reporte_ventas, text="Mostrar Todas las Ventas", command=mostrar_ventas_completas)
        btn_mostrar_todas.grid(row=1, column=2)
 
    def registrar_venta(self):
        # Limpiar la ventana principal antes de mostrar la sección de "Registrar Venta"
        self.limpiar_ventana()

        # Crear una sección para "Registrar Venta"
        self.section_registrar_venta = tk.Frame(self.root)
        self.section_registrar_venta.pack(side="left", fill="both", expand=True)

        # Implementar la lógica para registrar ventas y mostrar la suma total de los artículos seleccionados antes de confirmar la venta

        # Crear una tabla (Treeview) para mostrar los productos disponibles en el almacén
        tabla_almacen = ttk.Treeview(self.section_registrar_venta, columns=("ID", "Producto", "Cantidad", "Unidad", "Proveedor", "Precio Unitario"), height=20, show="headings")
        tabla_almacen.heading("ID", text="ID")
        tabla_almacen.heading("Producto", text="Producto")
        tabla_almacen.heading("Cantidad", text="Cantidad")
        tabla_almacen.heading("Unidad", text="Unidad")
        tabla_almacen.heading("Proveedor", text="Proveedor")
        tabla_almacen.heading("Precio Unitario", text="Precio Unitario")
        tabla_almacen.grid(row=0, column=0)

        # Configurar el ancho de las columnas
        tabla_almacen.column("ID", width=100)
        tabla_almacen.column("Producto", width=200)
        tabla_almacen.column("Cantidad", width=100)
        tabla_almacen.column("Unidad", width=100)
        tabla_almacen.column("Proveedor", width=150)
        tabla_almacen.column("Precio Unitario", width=150)

        # Llenar la tabla con los datos de productos disponibles (debes ajustar esto según tu lógica)
        productos_disponibles = self.logica.obtener_productos_disponibles()
        for producto in productos_disponibles:
            tabla_almacen.insert("", "end", values=producto)

        # Crear etiquetas y campos de entrada para la venta
        etiqueta_producto = tk.Label(self.section_registrar_venta, text="Producto:")
        etiqueta_producto.grid(row=1, column=0)
        campo_producto = tk.Entry(self.section_registrar_venta)
        campo_producto.grid(row=1, column=1)

        etiqueta_cantidad = tk.Label(self.section_registrar_venta, text="Cantidad:")
        etiqueta_cantidad.grid(row=2, column=0)
        campo_cantidad = tk.Entry(self.section_registrar_venta)
        campo_cantidad.grid(row=2, column=1)

        etiqueta_precio_unitario = tk.Label(self.section_registrar_venta, text="Precio Unitario:")
        etiqueta_precio_unitario.grid(row=3, column=0)
        campo_precio_unitario = tk.Entry(self.section_registrar_venta)
        campo_precio_unitario.grid(row=3, column=1)

        etiqueta_unidad = tk.Label(self.section_registrar_venta, text="Unidad:")
        etiqueta_unidad.grid(row=4, column=0)
        campo_unidad = tk.Entry(self.section_registrar_venta)
        campo_unidad.grid(row=4, column=1)

        etiqueta_proveedor = tk.Label(self.section_registrar_venta, text="Proveedor:")
        etiqueta_proveedor.grid(row=5, column=0)
        campo_proveedor = tk.Entry(self.section_registrar_venta)
        campo_proveedor.grid(row=5, column=1)

        etiqueta_suma_total = tk.Label(self.section_registrar_venta, text="Suma Total:")
        etiqueta_suma_total.grid(row=6, column=0)
        suma_total_var = tk.StringVar()
        suma_total_label = tk.Label(self.section_registrar_venta, textvariable=suma_total_var)
        suma_total_label.grid(row=6, column=1)

        # Variable para almacenar el producto seleccionado
        producto_seleccionado = None

        # Función para manejar la selección de un producto en la tabla
        def seleccionar_producto(event):
            nonlocal producto_seleccionado
            item = tabla_almacen.item(tabla_almacen.selection())
            producto = item['values']
            producto_seleccionado = producto

            # Llenar los campos de la venta con los atributos del producto seleccionado
            if producto_seleccionado:
                campo_producto.delete(0, "end")
                campo_producto.insert(0, producto_seleccionado[1])  # Nombre del producto
                campo_precio_unitario.delete(0, "end")
                campo_precio_unitario.insert(0, producto_seleccionado[5])  # Precio Unitario
                campo_unidad.delete(0, "end")
                campo_unidad.insert(0, producto_seleccionado[3])  # Unidad
                campo_proveedor.delete(0, "end")
                campo_proveedor.insert(0, producto_seleccionado[4])  # Proveedor

        # Asignar la función de selección al evento de clic en la tabla
        tabla_almacen.bind("<ButtonRelease-1>", seleccionar_producto)

        # Lista para almacenar las ventas
        ventas_realizadas = []

        # Función para calcular la suma total de los artículos seleccionados
        def calcular_suma_total():
            total = 0
            for venta in ventas_realizadas:
                total += venta["subtotal"]
            suma_total_var.set(f"S/.{total:.2f}")

        # Crear un botón para agregar la venta
        def agregar_producto_a_venta():
            if producto_seleccionado is not None:
                cantidad = int(campo_cantidad.get())
                precio_unitario = float(campo_precio_unitario.get())
                unidad = campo_unidad.get()
                proveedor = campo_proveedor.get()

                subtotal = cantidad * precio_unitario

                # Generar un ID único para el producto en la venta
                producto_id = len(ventas_realizadas) + 1  # Puedes ajustar la generación de IDs según tus necesidades

                venta = {
                    "producto_id": producto_id,
                    "producto": producto_seleccionado[1],
                    "cantidad": cantidad,
                    "precio_unitario": precio_unitario,
                    "unidad": unidad,
                    "proveedor": proveedor,
                    "subtotal": subtotal
                }

                ventas_realizadas.append(venta)
                calcular_suma_total()

        def registrar():
            if producto_seleccionado is not None:
                producto = producto_seleccionado[1]
                cantidad = int(campo_cantidad.get())
                precio_unitario = float(campo_precio_unitario.get())
                unidad = campo_unidad.get()
                proveedor = campo_proveedor.get()

                # Implementa la lógica para registrar la venta en tu objeto de lógica de negocios
                venta_registrada = self.logica.confirmar_venta(producto, cantidad, precio_unitario, unidad, proveedor)

                if venta_registrada:
                    messagebox.showinfo("Éxito", "Venta registrada correctamente.")
                    self.logica.exportar_ventas_a_xlsx()  # Llamada a la función exportar_ventas_a_xlsx
                else:
                    messagebox.showerror("Error", "No se pudo registrar la venta. Verifica los datos.")

        boton_agregar = tk.Button(self.section_registrar_venta, text="Agregar Venta", command=agregar_producto_a_venta)
        boton_agregar.grid(row=7, column=0, columnspan=2)

        boton_registrar = tk.Button(self.section_registrar_venta, text="Registrar Venta", command=registrar)
        boton_registrar.grid(row=8, column=0, columnspan=2)

        # Crear un botón para cerrar la pestaña de "Registrar Venta"
        boton_cerrar_ventana = tk.Button(self.section_registrar_venta, text="Cerrar Ventana", command=self.cerrar_ventana_registrar_venta)
        boton_cerrar_ventana.grid(row=10, column=0, columnspan=2)
        
    def cerrar_ventana_registrar_venta(self):
        self.section_registrar_venta.destroy()  # Cierra la pestaña de "Registrar Venta"

    def mostrar_almacen(self):
        # Limpiar la ventana principal antes de mostrar la sección de "Ver Almacén"
        self.limpiar_ventana()

        # Crear una sección para "Ver Almacén"
        self.section_ver_almacen = tk.Frame(self.root)
        self.section_ver_almacen.pack(side="left", fill="both", expand=True)

        # Implementa aquí la lógica para mostrar el almacén. Puedes agregar etiquetas, tablas o cualquier widget que necesites.
        # Crear una tabla (Treeview) para mostrar el contenido del almacén
        self.tabla_almacen = ttk.Treeview(self.section_ver_almacen, columns=("ID", "Producto", "Cantidad", "Unidad", "Precio Unitario", "Proveedor"), height=20, show="headings")
        self.tabla_almacen.heading("ID", text="ID")
        self.tabla_almacen.heading("Producto", text="Producto")
        self.tabla_almacen.heading("Cantidad", text="Cantidad")
        self.tabla_almacen.heading("Unidad", text="Unidad")
        self.tabla_almacen.heading("Precio Unitario", text="Precio Unitario")
        self.tabla_almacen.heading("Proveedor", text="Proveedor")
        self.tabla_almacen.grid(row=0, column=0)

        # Configurar el ancho de las columnas
        self.tabla_almacen.column("ID", width=200)
        self.tabla_almacen.column("Producto", width=100)
        self.tabla_almacen.column("Cantidad", width=100)
        self.tabla_almacen.column("Unidad", width=200)
        self.tabla_almacen.column("Precio Unitario", width=150)
        self.tabla_almacen.column("Proveedor", width=150)

        # Obtener datos del almacén (debes ajustar esto según tu lógica)
        datos_almacen = self.logica.obtener_datos_almacen()

        # Llenar la tabla con los datos del almacén
        for producto in datos_almacen:
            self.tabla_almacen.insert("", "end", values=producto)

        # Botón para cerrar la sección de "Ver Almacén"
        btn_cerrar = tk.Button(self.section_ver_almacen, text="Cerrar", command=self.cerrar_seccion_ver_almacen)
        btn_cerrar.grid(row=1, column=0)
        
    def cerrar_seccion_ver_almacen(self):
        # Cerrar la sección de "Ver Almacén" y limpiar la ventana
        if self.section_ver_almacen:
            self.section_ver_almacen.destroy()             
        if self.tabla_almacen:
            self.tabla_almacen = None
      #  if self.campo_busqueda:
          #  self.campo_busqueda = None
          
    def limpiar_ventana(self):
        # Limpiar la ventana principal antes de mostrar una nueva sección
        if self.section_reporte_ventas:
            self.section_reporte_ventas.destroy()
        if self.tabla_ventas:
            self.tabla_ventas = None
        if self.campo_busqueda:
            self.campo_busqueda = None

        # Limpiar la sección de "Registrar Compra" si está abierta
        if self.section_registrar_compra:
            self.section_registrar_compra.destroy()
            self.section_registrar_compra = None

        # Limpiar la sección de "Ver Almacén" si está abierta
        if self.section_ver_almacen:
            self.section_ver_almacen.destroy()
            self.section_ver_almacen = None

        # Limpiar la sección de "Reporte de Compras" si está abierta
        if self.section_reporte_compras:
            self.section_reporte_compras.destroy()
            self.section_reporte_compras = None
            self.tabla_compras = None
            
        # Limpiar la sección de "Reporte de Compras de Almacen" si está abierta    
        if self.section_reporte_compras_almacen:
            self.section_reporte_compras_almacen.destroy()
            self.section_reporte_compras_almacen = None
            self.tabla_compras_almacen = None  
            
        if self.section_modificar_precio_producto:
            self.section_modificar_precio_producto.destroy()
            self.section_modificar_precio_producto
            self.nuevo_precio_entry = None
            
        if self.section_registrar_venta:
            self.section_registrar_venta.destroy()
            self.section_registrar_venta = None      
               
    def registrar_compra(self):
        # Limpia la ventana principal antes de mostrar el registro de compra
        self.limpiar_ventana()

        # Crea un marco (frame) para la sección de registro de compra
        self.section_registrar_compra = tk.Frame(self.root)
        self.section_registrar_compra.pack(side="right", fill="both", expand=True)

        self.proveedor_label = tk.Label(self.section_registrar_compra, text="Proveedor:")
        self.proveedor_label.grid(row=0, column=0)
        self.proveedor_entry = tk.Entry(self.section_registrar_compra)
        self.proveedor_entry.grid(row=0, column=1)

        self.producto_label = tk.Label(self.section_registrar_compra, text="Producto:")
        self.producto_label.grid(row=1, column=0)
        self.producto_entry = tk.Entry(self.section_registrar_compra)
        self.producto_entry.grid(row=1, column=1)

        self.cantidad_label = tk.Label(self.section_registrar_compra, text="Cantidad:")
        self.cantidad_label.grid(row=2, column=0)
        self.cantidad_entry = tk.Entry(self.section_registrar_compra)
        self.cantidad_entry.grid(row=2, column=1)

        self.precio_label = tk.Label(self.section_registrar_compra, text="Precio Unitario:")
        self.precio_label.grid(row=3, column=0)
        self.precio_entry = tk.Entry(self.section_registrar_compra)
        self.precio_entry.grid(row=3, column=1)

        self.unidad_label = tk.Label(self.section_registrar_compra, text="Unidad:")
        self.unidad_label.grid(row=4, column=0)
        self.unidad_entry = tk.Entry(self.section_registrar_compra)
        self.unidad_entry.grid(row=4, column=1)

        def guardar_compra():
            proveedor = self.proveedor_entry.get()
            producto = self.producto_entry.get()
            cantidad = self.cantidad_entry.get()
            precio = self.precio_entry.get()
            unidad = self.unidad_entry.get()

            try:
                cantidad = int(cantidad)
                precio = float(precio)

                if proveedor and producto and cantidad > 0 and precio > 0 and unidad:
                    # Llama a la función 'guardar_compra' de la lógica de negocios
                    self.logica.guardar_compra(proveedor, producto, cantidad, precio, unidad)
                    messagebox.showinfo("Éxito", "Compra registrada correctamente.")
                    
                    self.logica.exportar_compras_a_xlsx()
                    
                else:
                    messagebox.showwarning("Advertencia", "Por favor, complete todos los campos correctamente.")
            except ValueError:
                messagebox.showwarning("Advertencia", "Cantidad y precio deben ser números válidos.")

        guardar_button = tk.Button(self.section_registrar_compra, text="Guardar Compra", command=guardar_compra)
        guardar_button.grid(row=5, column=0, columnspan=2)

        def cerrar_registro_compra():
            # Cerrar la sección de registro de compra y limpiar la ventana
            if self.section_registrar_compra:
                self.section_registrar_compra.destroy()
                self.limpiar_ventana()
    
        cerrar_button = tk.Button(self.section_registrar_compra, text="Cerrar", command=cerrar_registro_compra)
        cerrar_button.grid(row=6, column=0, columnspan=2)
     
    def ver_reporte_compras(self):
        # Limpiar la ventana principal antes de mostrar el reporte de compras
        self.limpiar_ventana()

        # Crear una sección para el reporte de compras
        self.section_reporte_compras = tk.Frame(self.root)
        self.section_reporte_compras.pack(side="left", fill="both", expand=True)

        # Crear una tabla para mostrar el reporte de compras
        self.tabla_compras = ttk.Treeview(self.section_reporte_compras, columns=("ID", "Proveedor", "Producto", "Cantidad", "Precio", "Unidad", "Fecha"), height=20, show="headings")
        self.tabla_compras.heading("ID", text="ID")
        self.tabla_compras.heading("Proveedor", text="Proveedor")
        self.tabla_compras.heading("Producto", text="Producto")
        self.tabla_compras.heading("Cantidad", text="Cantidad")
        self.tabla_compras.heading("Precio", text="Precio")
        self.tabla_compras.heading("Unidad", text="Unidad")
        self.tabla_compras.heading("Fecha", text="Fecha")
        self.tabla_compras.grid(row=0, column=0, columnspan=2)

        # Configurar el ancho de las columnas
        self.tabla_compras.column("#1", width=100)  # Ancho de la columna ID
        self.tabla_compras.column("#2", width=200)  # Ancho de la columna Proveedor
        self.tabla_compras.column("#3", width=200)  # Ancho de la columna Producto
        self.tabla_compras.column("#4", width=100)  # Ancho de la columna Cantidad
        self.tabla_compras.column("#5", width=100)  # Ancho de la columna Precio
        self.tabla_compras.column("#6", width=100)  # Ancho de la columna Unidad
        self.tabla_compras.column("#7", width=130)  # Ancho de la columna Fecha

        # Obtener los datos de compras desde la lógica de negocios
        compras = self.logica.ver_reporte_compras()

        # Llenar la tabla con los datos de compras
        for compra in compras:
            self.tabla_compras.insert("", "end", values=compra)

        # Botón para cerrar la sección de "Reporte de Compras"
        btn_cerrar = tk.Button(self.section_reporte_compras, text="Cerrar", command=self.cerrar_seccion_reporte_compras)
        btn_cerrar.grid(row=1, column=0)
    
    def cerrar_seccion_reporte_compras(self):
        # Cerrar la sección de "Reporte de Compras" y limpiar la ventana
        if self.section_reporte_compras:
            self.section_reporte_compras.destroy()
            self.tabla_compras = None
            self.section_reporte_compras = None

    def ver_reporte_compras_almacen(self):
        # Limpia la ventana principal antes de mostrar el reporte de compras para el almacén
        self.limpiar_ventana()

        # Crear una sección para el reporte de compras para el almacén
        self.section_reporte_compras_almacen = tk.Frame(self.root)
        self.section_reporte_compras_almacen.pack(side="left", fill="both", expand=True)

        # Crear una tabla para mostrar el reporte de compras para el almacén
        self.tabla_compras_almacen = ttk.Treeview(self.section_reporte_compras_almacen, columns=("Producto", "Unidad", "Precio Unitario", "Cantidad Total", "Costo Total"), height=20, show="headings")
        self.tabla_compras_almacen.heading("Producto", text="Producto")
        self.tabla_compras_almacen.heading("Unidad", text="Unidad")
        self.tabla_compras_almacen.heading("Precio Unitario", text="Precio Unitario")
        self.tabla_compras_almacen.heading("Cantidad Total", text="Cantidad Total")
        self.tabla_compras_almacen.heading("Costo Total", text="Costo Total")
        self.tabla_compras_almacen.grid(row=0, column=0, columnspan=2)

        # Configurar el ancho de las columnas
        self.tabla_compras_almacen.column("#1", width=200)  # Ancho de la columna Producto
        self.tabla_compras_almacen.column("#2", width=100)  # Ancho de la columna Unidad
        self.tabla_compras_almacen.column("#3", width=150)  # Ancho de la columna Precio Unitario
        self.tabla_compras_almacen.column("#4", width=150)  # Ancho de la columna Cantidad Total
        self.tabla_compras_almacen.column("#5", width=150)  # Ancho de la columna Costo Total

        # Obtener los datos del reporte de compras para el almacén desde la lógica de negocios
        compras_almacen = self.logica.ver_reporte_compras_almacen()

        # Llenar la tabla con los datos del reporte de compras para el almacén
        for compra in compras_almacen:
            self.tabla_compras_almacen.insert("", "end", values=compra)

        # Calcular la suma total de los costos
        suma_total_costos = sum(float(compra[4]) for compra in compras_almacen)

        # Agregar la suma total de los costos debajo de la tabla
        suma_total_label = tk.Label(self.section_reporte_compras_almacen, text=f"Suma Total de Costos: S/. {suma_total_costos}", font=("bold", 12))
        suma_total_label.grid(row=2, column=0, columnspan=2)
        
        # Botón para cerrar la sección de "Reporte de Compras para el Almacén"
        btn_cerrar = tk.Button(self.section_reporte_compras_almacen, text="Cerrar", command=self.cerrar_seccion_reporte_compras_almacen)
        btn_cerrar.grid(row=3, column=1)

    def cerrar_seccion_reporte_compras_almacen(self):
        # Cerrar la sección de "Reporte de Compras para el Almacén" y limpiar la ventana
        if self.section_reporte_compras_almacen:
            self.section_reporte_compras_almacen.destroy()
            self.tabla_compras_almacen = None
            self.section_reporte_compras_almacen = None

    def modificar_precio_producto(self):
        # Limpia la ventana principal antes de mostrar la sección de modificar precio del producto
        self.limpiar_ventana()

        # Crear una sección para modificar el precio del producto
        self.section_modificar_precio_producto = tk.Frame(self.root)
        self.section_modificar_precio_producto.pack(side="left", fill="both", expand=True)

        # Obtener la lista de productos disponibles en el almacén junto con sus atributos
        productos_disponibles = self.logica.obtener_productos_disponibles()

        if not productos_disponibles:
            mensaje_label = tk.Label(self.section_modificar_precio_producto, text="No hay productos disponibles en el almacén.")
            mensaje_label.grid(row=0, column=0)
        else:
            mensaje_label = tk.Label(self.section_modificar_precio_producto, text="Productos disponibles:")
            mensaje_label.grid(row=0, column=0)

            # Crear una tabla para mostrar los productos disponibles
            tabla_productos = ttk.Treeview(self.section_modificar_precio_producto, columns=("ID", "Producto", "Cantidad", "Unidad", "Proveedor", "Precio Unitario"), height=10, show="headings")
            tabla_productos.heading("ID", text="ID")
            tabla_productos.heading("Producto", text="Producto")
            tabla_productos.heading("Cantidad", text="Cantidad")
            tabla_productos.heading("Unidad", text="Unidad")
            tabla_productos.heading("Proveedor", text="Proveedor")
            tabla_productos.heading("Precio Unitario", text="Precio Unitario")
            tabla_productos.grid(row=1, column=0, columnspan=2)

            # Configurar el ancho de las columnas daskldjaslkj
            tabla_productos.column("#1", width=100)  # Ancho de la columna ID
            tabla_productos.column("#2", width=200)  # Ancho de la columna Producto
            tabla_productos.column("#3", width=100)  # Ancho de la columna Cantidad
            tabla_productos.column("#4", width=100)  # Ancho de la columna Unidad
            tabla_productos.column("#5", width=200)  # Ancho de la columna Proveedor
            tabla_productos.column("#6", width=150)  # Ancho de la columna Precio Unitario

            # Llenar la tabla con los datos de productos disponibles
            for producto in productos_disponibles:
                tabla_productos.insert("", "end", values=producto)

            # Etiqueta y campo de entrada para el nuevo precio
            nuevo_precio_label = tk.Label(self.section_modificar_precio_producto, text="Nuevo Precio Unitario:")
            nuevo_precio_label.grid(row=2, column=0)
            self.nuevo_precio_entry = tk.Entry(self.section_modificar_precio_producto)
            self.nuevo_precio_entry.grid(row=2, column=1)

            def actualizar_precio():
                # Obtener el ID del producto seleccionado
                seleccion = tabla_productos.selection()
                if seleccion:
                    id_producto = tabla_productos.item(seleccion, "values")[0]
                    nuevo_precio = self.nuevo_precio_entry.get()

                    if nuevo_precio:
                        try:
                            nuevo_precio = float(nuevo_precio)
                            # Llama a la función para actualizar el precio en la lógica de negocios
                            success = self.logica.actualizar_precio_producto(id_producto, nuevo_precio)
                            if success:
                                messagebox.showinfo("Éxito", f"Precio del producto con ID '{id_producto}' actualizado correctamente.")
                            else:
                                messagebox.showwarning("Advertencia", "El pproducto no fue encontrado en la base de datos.")
                        except ValueError:
                            messagebox.showwarning("Advertencia", "Por favor, ingrese un valor válido para el precio.")
                    else:
                        messagebox.showwarning("Advertencia", "Por favor, ingrese un valor válido para el precio.")
                else:
                    messagebox.showwarning("Advertencia", "Por favor, seleccione un producto para actualizar el precio.")

            # Botón para actualizar el precio
            actualizar_precio_button = tk.Button(self.section_modificar_precio_producto, text="Actualizar Precio", command=actualizar_precio)
            actualizar_precio_button.grid(row=3, column=0, columnspan=2)

            # Botón para cerrar la sección de "Modificar Precio del Producto"
            btn_cerrar = tk.Button(self.section_modificar_precio_producto, text="Cerrar", command=self.cerrar_seccion_modificar_precio_producto)
            btn_cerrar.grid(row=4, column=0, columnspan=2)

    def cerrar_seccion_modificar_precio_producto(self):
        # Cerrar la sección de "Modificar Precio del Producto" y limpiar la ventana
        if self.section_modificar_precio_producto:
            self.section_modificar_precio_producto.destroy()
            self.nuevo_precio_entry = None
            self.section_modificar_precio_producto = None

if __name__ == "__main__":
    root = tk.Tk()
    app = MenuPrincipalUI(root)
    root.mainloop()