import openpyxl
from openpyxl.styles import Font
from datetime import datetime

class LogicaDeNegocios:
    # ...

    def exportar_ventas_a_xlsx(self):
        # Obtener la fecha actual en formato YYYY-MM-DD
        fecha_actual = datetime.now().strftime('%Y-%m-%d')

        # Crear un nuevo archivo Excel
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = fecha_actual  # Usar la fecha actual como título de la hoja

        # Agregar las ventas registradas en el día
        cursor = self.base_de_datos.cursor
        cursor.execute('SELECT producto, cantidad, precio_unitario FROM ventas WHERE fecha LIKE ?', (f'{fecha_actual}%',))
        ventas_del_dia = cursor.fetchall()

        # Agregar las ventas al archivo Excel
        sheet['A1'] = 'Producto'
        sheet['B1'] = 'Cantidad'
        sheet['C1'] = 'Precio Unitario'
        sheet['D1'] = 'Subtotal'

        total_ventas_del_dia = 0  # Inicializar el total de ventas del día

        for i, (producto, cantidad, precio_unitario) in enumerate(ventas_del_dia, 2):
            sheet[f'A{i}'] = producto
            sheet[f'B{i}'] = cantidad
            sheet[f'C{i}'] = precio_unitario
            subtotal = cantidad * precio_unitario
            sheet[f'D{i}'] = subtotal
            total_ventas_del_dia += subtotal

        # Calcular y agregar la suma total de ventas del día
        total_row = len(ventas_del_dia) + 3  # Separación de dos celdas y una fila adicional
        sheet[f'A{total_row}'] = 'Total del Día:'
        sheet[f'D{total_row}'] = total_ventas_del_dia

        # Establecer el formato de la celda para el total
        total_cell = sheet[f'D{total_row}']
        total_cell.font = Font(bold=True)

        # Guardar el archivo Excel
        archivo_xlsx = f'ventas_{fecha_actual}.xlsx'
        workbook.save(archivo_xlsx)

        print(f"Reporte de ventas del día {fecha_actual} exportado a {archivo_xlsx}")

        # Cerrar la conexión a la base de datos
        self.base_de_datos.conn.close()
