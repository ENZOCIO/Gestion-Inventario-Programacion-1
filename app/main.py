import tkinter as tk
from tkinter import ttk, messagebox
from inventario import Inventario
from producto import Producto
from categoria import Categoria
from bodega import Bodega
from proveedor import Proveedor


class InventarioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Inventario")

        # Crear el inventario
        self.inventario = Inventario()

        # Crear la interfaz
        self.create_widgets()
    
    def create_informes_widgets(self):
        frame = self.informes_frame

        # Botones para generar diferentes informes
        ttk.Button(frame, text="Informe de Stock Total", command=self.informe_stock_total).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ttk.Button(frame, text="Informe de Stock por Categoría", command=self.informe_stock_categoria).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        ttk.Button(frame, text="Informe de Stock por Proveedor", command=self.informe_stock_proveedor).grid(row=2, column=0, padx=10, pady=5, sticky="w")
        ttk.Button(frame, text="Informe de Stock por Bodega", command=self.informe_stock_bodega).grid(row=3, column=0, padx=10, pady=5, sticky="w")

        # Área para mostrar los resultados del informe
        self.informe_resultado_text = tk.Text(frame, wrap="word", height=20, width=80, state="disabled")
        self.informe_resultado_text.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

        frame.rowconfigure(4, weight=1)
        frame.columnconfigure(0, weight=1)

    
    def informe_stock_total(self):
        total_stock = sum(producto.stock for producto in self.inventario.listar_productos())
        self.mostrar_informe(f"Stock Total: {total_stock}")
    
    def informe_stock_categoria(self):
        categorias = {}
        for producto in self.inventario.listar_productos():
            if producto.categoria not in categorias:
                categorias[producto.categoria] = 0
            categorias[producto.categoria] += producto.stock

        informe = "Stock por Categoría:\n"
        for categoria, stock in categorias.items():
            informe += f"- {categoria}: {stock}\n"

        self.mostrar_informe(informe)
    
    def informe_stock_proveedor(self):
        proveedores = {}

        # Recorrer todos los proveedores
        for proveedor in self.inventario.listar_proveedores():
            if proveedor.nombre not in proveedores:
                proveedores[proveedor.nombre] = 0  # Inicializar el stock del proveedor

            # Sumar el stock de cada producto suministrado por el proveedor
            for producto in proveedor.productos:
                proveedores[proveedor.nombre] += producto.stock

        # Crear el informe
        informe = "Stock por Proveedor:\n"
        for proveedor, stock in proveedores.items():
            informe += f"- {proveedor}: {stock}\n"

        self.mostrar_informe(informe)


    def informe_stock_bodega(self):
        bodegas = {}

        # Recorrer todas las bodegas registradas
        for bodega in self.inventario.listar_bodegas():
            # Inicializar el stock de la bodega
            if bodega.nombre not in bodegas:
                bodegas[bodega.nombre] = 0
        
            # Sumar el stock de cada producto almacenado en la bodega
            for producto, cantidad in bodega.productos.items():
                bodegas[bodega.nombre] += cantidad

        # Crear el informe
        informe = "Stock por Bodega:\n"
        for bodega, stock in bodegas.items():
            informe += f"- {bodega}: {stock}\n"

        self.mostrar_informe(informe)



    def mostrar_informe(self, informe):
        self.informe_resultado_text.config(state="normal")  # Habilitar edición temporalmente
        self.informe_resultado_text.delete("1.0", tk.END)   # Limpiar el contenido previo
        self.informe_resultado_text.insert(tk.END, informe) # Insertar el informe
        self.informe_resultado_text.config(state="disabled")  # Deshabilitar edición nuevamente






    
    def retirar_producto_de_bodega(self):
        nombre_bodega = self.bodega_retirar_combobox.get()
        nombre_producto = self.producto_retirar_combobox.get()
        cantidad_str = self.cantidad_retirar_entry.get()

        if not (nombre_bodega and nombre_producto and cantidad_str):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            cantidad = int(cantidad_str)
            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor que cero.")
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero positivo.")
            return

        producto = next((p for p in self.inventario.listar_productos() if p.nombre == nombre_producto), None)
        if not producto:
            messagebox.showerror("Error", f"El producto '{nombre_producto}' no existe en el inventario.")
            return

        try:
            self.inventario.retirar_producto_de_bodega(nombre_bodega, producto, cantidad)
            producto.stock += cantidad  # Devuelve el stock al inventario principal
            self.actualizar_tabla_bodegas()  # Llama al método para actualizar la tabla de bodegas
            self.actualizar_tabla_productos()  # Actualiza la tabla de productos
            self.actualizar_listas_productos()  # Sincroniza los combobox
            messagebox.showinfo("Éxito", f"Se retiraron {cantidad} unidades del producto '{nombre_producto}' de la bodega '{nombre_bodega}'.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))


    
    def agregar_producto_a_bodega(self):
        nombre_bodega = self.bodega_combobox.get()
        nombre_producto = self.producto_bodega_combobox.get()
        cantidad_str = self.cantidad_bodega_entry.get()

        if not (nombre_bodega and nombre_producto and cantidad_str):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            cantidad = int(cantidad_str)
            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor que cero.")
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero positivo.")
            return

        # Buscar el producto en el inventario
        producto = next((p for p in self.inventario.listar_productos() if p.nombre == nombre_producto), None)
        if not producto:
            messagebox.showerror("Error", f"El producto '{nombre_producto}' no existe en el inventario.")
            return

        # Verificar que haya suficiente stock del producto
        if producto.stock < cantidad:
            messagebox.showerror("Error", f"No hay suficiente stock del producto '{nombre_producto}' en el inventario.")
            return

        # Intentar agregar el producto a la bodega
        try:
            self.inventario.agregar_producto_a_bodega(nombre_bodega, producto, cantidad)
            producto.stock -= cantidad  # Reducir el stock en el inventario principal
            self.actualizar_tabla_bodegas()
            self.actualizar_tabla_productos()
            messagebox.showinfo("Éxito", f"Se agregó {cantidad} unidades del producto '{nombre_producto}' a la bodega '{nombre_bodega}'.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))



    
    def actualizar_proveedores_combobox(self):
        # Obtener todos los proveedores registrados
        proveedores = self.inventario.listar_proveedores()
        nombres_proveedores = [proveedor.nombre for proveedor in proveedores]

        # Actualizar combobox
        self.proveedor_producto_combobox['values'] = nombres_proveedores
        self.proveedor_eliminar_combobox['values'] = nombres_proveedores

        # Seleccionar el primer proveedor si hay datos
        if nombres_proveedores:
            self.proveedor_producto_combobox.set(nombres_proveedores[0])
            self.proveedor_eliminar_combobox.set(nombres_proveedores[0])
        else:
            self.proveedor_producto_combobox.set("")
            self.proveedor_eliminar_combobox.set("")

        self.proveedor_producto_combobox.update()
        self.proveedor_eliminar_combobox.update()


    
    def actualizar_productos_de_proveedor(self, nombre_proveedor):
        # Buscar el proveedor seleccionado
        proveedor = next((p for p in self.inventario.listar_proveedores() if p.nombre == nombre_proveedor), None)

        # Si el proveedor existe, actualiza el combobox con sus productos
        if proveedor:
            productos_del_proveedor = [producto.nombre for producto in proveedor.productos]
            print(f"Productos asociados al proveedor '{nombre_proveedor}':", productos_del_proveedor)
            self.producto_eliminar_combobox['values'] = productos_del_proveedor

            # Seleccionar el primer producto, si hay productos disponibles
            if productos_del_proveedor:
                self.producto_eliminar_combobox.set(productos_del_proveedor[0])
            else:
                self.producto_eliminar_combobox.set("")
        else:
            # Si el proveedor no existe, limpia el combobox
            self.producto_eliminar_combobox['values'] = []
            self.producto_eliminar_combobox.set("")

        self.producto_eliminar_combobox.update()


    
    def on_proveedor_seleccionado(self, event):
        # Obtener el proveedor seleccionado
        nombre_proveedor = self.proveedor_eliminar_combobox.get()
        self.actualizar_productos_de_proveedor(nombre_proveedor)  

    
    
    def eliminar_producto_de_proveedor(self):
    # Obtener datos del formulario
        nombre_proveedor = self.proveedor_eliminar_combobox.get()
        nombre_producto = self.producto_eliminar_combobox.get()

        # Validar campos obligatorios
        if not (nombre_proveedor and nombre_producto):
            messagebox.showerror("Error", "Debe seleccionar un proveedor y un producto.")
            return

        # Intentar eliminar el producto del proveedor
        try:
            if self.inventario.eliminar_producto_de_proveedor(nombre_proveedor, nombre_producto):
                self.actualizar_tabla_proveedores()  # Actualizar la tabla de proveedores
                messagebox.showinfo("Éxito", f"El producto '{nombre_producto}' fue eliminado del proveedor '{nombre_proveedor}'.")
            else:
                messagebox.showerror("Error", f"No se encontró el proveedor '{nombre_proveedor}'.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

            self.actualizar_productos_de_proveedor(nombre_proveedor)  # <- Aquí
            self.actualizar_tabla_proveedores() 
    
    def actualizar_tabla_proveedores(self):
        # Obtener todos los proveedores registrados
        proveedores = self.inventario.listar_proveedores()

        # Limpiar la tabla
        for row in self.proveedores_tree.get_children():
            self.proveedores_tree.delete(row)

        # Rellenar la tabla con los proveedores registrados
        for proveedor in proveedores:
            productos_texto = ", ".join([p.nombre for p in proveedor.productos])
            self.proveedores_tree.insert("", "end", values=(proveedor.nombre, proveedor.direccion, proveedor.telefono, productos_texto))

        # Actualizar el combobox de proveedores
        nombres_proveedores = [proveedor.nombre for proveedor in proveedores]
        self.proveedor_eliminar_combobox['values'] = nombres_proveedores

        # Actualizar los productos suministrados para el proveedor seleccionado
        if nombres_proveedores:
            # Seleccionar el primer proveedor por defecto y actualizar sus productos
            self.proveedor_eliminar_combobox.current(0)
            self.actualizar_productos_de_proveedor(nombres_proveedores[0])
        else:
            # Si no hay proveedores, limpiar el combobox de productos
            self.producto_eliminar_combobox['values'] = []
        
        self.actualizar_proveedores_combobox()




    
    def agregar_producto_a_proveedor(self):
        nombre_proveedor = self.proveedor_producto_combobox.get()
        nombre_producto = self.producto_agregar_combobox.get()

        # Validar campos obligatorios
        if not (nombre_proveedor and nombre_producto):
            messagebox.showerror("Error", "Debe seleccionar un proveedor y un producto.")
            return

        # Buscar el producto en el inventario
        producto = next((p for p in self.inventario.listar_productos() if p.nombre == nombre_producto), None)
        if not producto:
            messagebox.showerror("Error", f"El producto '{nombre_producto}' no existe en el inventario.")
            return

        # Intentar agregar el producto al proveedor
        try:
            self.inventario.agregar_producto_a_proveedor(nombre_proveedor, producto)
            messagebox.showinfo("Éxito", f"El producto '{nombre_producto}' fue agregado al proveedor '{nombre_proveedor}'.")
            self.actualizar_tabla_proveedores()  # Actualizar la interfaz
        except ValueError as e:
            messagebox.showerror("Error", str(e))

            self.actualizar_productos_de_proveedor(nombre_proveedor)  # <- Aquí
            self.actualizar_tabla_proveedores()

    
    def actualizar_tabla_bodegas(self):
        # Limpiar la tabla de bodegas
        for row in self.bodegas_tree.get_children():
            self.bodegas_tree.delete(row)

        # Rellenar la tabla con las bodegas registradas
        for bodega in self.inventario.listar_bodegas():
            productos_texto = ", ".join([f"{producto.nombre} ({cantidad})" for producto, cantidad in bodega.productos.items()])
            self.bodegas_tree.insert("", "end", values=(bodega.nombre, bodega.ubicacion, bodega.capacidad_maxima, productos_texto))

        # Actualizar los combobox de bodegas
        nombres_bodegas = [bodega.nombre for bodega in self.inventario.listar_bodegas()]
        self.bodega_combobox['values'] = nombres_bodegas
        self.bodega_retirar_combobox['values'] = nombres_bodegas
    

    def actualizar_productos_a_agregar(self):
        # Obtener los productos registrados en el inventario
        productos = self.inventario.listar_productos()
        productos_nombres = [producto.nombre for producto in productos]

        # Depuración: Verificar los productos disponibles
        print("Productos disponibles para agregar:", productos_nombres)

        # Actualizar el combobox "Producto a agregar"
        self.producto_agregar_combobox['values'] = productos_nombres

        # Seleccionar el primer producto, si hay productos disponibles
        if productos_nombres:
            self.producto_agregar_combobox.set(productos_nombres[0])
        else:
            self.producto_agregar_combobox.set("")
        self.producto_agregar_combobox.update()





    
    def eliminar_producto_de_categoria(self):
        # Obtener datos del formulario
        nombre_producto = self.producto_eliminar_entry.get()
        nombre_categoria = self.categoria_eliminar_combobox.get()

        # Validar campos obligatorios
        if not (nombre_producto and nombre_categoria):
            messagebox.showerror("Error", "Debe especificar un producto y una categoría.")
            return

        # Intentar eliminar el producto de la categoría
        if self.inventario.eliminar_producto_de_categoria(nombre_producto, nombre_categoria):
            # Actualizar la interfaz
            self.actualizar_listas_productos()
            self.actualizar_tabla_productos()
            messagebox.showinfo("Éxito", f"Producto '{nombre_producto}' eliminado de la categoría '{nombre_categoria}'.")
        else:
            messagebox.showerror("Error", f"No se encontró el producto '{nombre_producto}' en la categoría '{nombre_categoria}'.")

    
    def calcular_valor_total_stock(self):
        # Calcular el valor total usando el método del inventario
        total = self.inventario.calcular_valor_total_stock()

        # Mostrar el resultado en un mensaje emergente
        messagebox.showinfo("Valor Total del Stock", f"El valor total del stock es: ${total:.2f}")

    def actualizar_tabla_productos(self):
        # Limpiar la tabla de productos
        for row in self.productos_tree.get_children():
            self.productos_tree.delete(row)

        # Obtener los productos registrados en el inventario
        productos = self.inventario.listar_productos()

        # Rellenar la tabla con los productos registrados
        for producto in productos:
            self.productos_tree.insert("", "end", values=(producto.nombre, producto.descripcion, f"${producto.precio:.2f}", producto.stock, producto.categoria))

    # Actualizar los combobox relacionados con productos
        nombres_productos = [producto.nombre for producto in productos]
        self.producto_bodega_combobox['values'] = nombres_productos
        self.producto_retirar_combobox['values'] = nombres_productos
        self.producto_stock_combobox['values'] = nombres_productos
        self.producto_eliminar_combobox['values'] = nombres_productos


    def retirar_stock(self):
        producto_nombre = self.producto_retirar_combobox.get()
        cantidad_str = self.cantidad_retirar_entry.get()

        if not (producto_nombre and cantidad_str):
            messagebox.showerror("Error", "Debe seleccionar un producto y especificar una cantidad.")
            return

        try:
            cantidad = int(cantidad_str)
            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor que cero.")
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero positivo.")
            return

        # Retirar el stock del producto
        try:
            if self.inventario.retirar_stock(producto_nombre, cantidad):
                self.cantidad_retirar_entry.delete(0, tk.END)
                self.actualizar_tabla_productos()  # Actualizar la tabla
                messagebox.showinfo("Éxito", f"Se retiraron {cantidad} unidades del producto {producto_nombre}.")
            else:
                messagebox.showerror("Error", "El producto no se encontró.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))


    
    def agregar_stock(self):
        producto_nombre = self.producto_stock_combobox.get()
        cantidad_str = self.cantidad_stock_entry.get()

        if not (producto_nombre and cantidad_str):
            messagebox.showerror("Error", "Debe seleccionar un producto y especificar una cantidad.")
            return

        try:
            cantidad = int(cantidad_str)
            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor que cero.")
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero positivo.")
            return

        # Agregar el stock al producto
        if self.inventario.agregar_stock(producto_nombre, cantidad):
            self.cantidad_stock_entry.delete(0, tk.END)
            self.actualizar_tabla_productos()  # Actualizar la tabla
            messagebox.showinfo("Éxito", f"Se agregó {cantidad} unidades al producto {producto_nombre}.")
        else:
            messagebox.showerror("Error", "El producto no se encontró.")


    
    def actualizar_listas_productos(self):
        # Obtener todos los productos registrados
        productos = self.inventario.listar_productos()
        productos_nombres = [producto.nombre for producto in productos]

        # Depuración: Verificar datos
        print("Productos registrados en el inventario:", productos_nombres)

        # Limpiar combobox y listbox
        self.producto_retirar_combobox['values'] = []
        self.producto_stock_combobox['values'] = []
        self.producto_bodega_combobox['values'] = []
        self.productos_suministrados_listbox.delete(0, tk.END)

        # Actualizar los combobox y listbox
        self.producto_retirar_combobox['values'] = productos_nombres
        self.producto_stock_combobox['values'] = productos_nombres
        self.producto_bodega_combobox['values'] = productos_nombres

        for producto in productos:
            self.productos_suministrados_listbox.insert(tk.END, producto.nombre)

        # Seleccionar un valor por defecto si hay productos disponibles
        if productos_nombres:
            self.producto_retirar_combobox.set(productos_nombres[0])
            self.producto_stock_combobox.set(productos_nombres[0])
            self.producto_bodega_combobox.set(productos_nombres[0])
        else:
            # Si no hay productos, limpiar selección
            self.producto_retirar_combobox.set("")
            self.producto_stock_combobox.set("")
            self.producto_bodega_combobox.set("")

        # Forzar actualización de los widgets
        self.producto_retirar_combobox.update()
        self.producto_stock_combobox.update()
        self.producto_bodega_combobox.update()

        self.root.update_idletasks()






    def create_widgets(self):
        # Pestañas para manejar productos, categorías y proveedores
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")

        self.productos_frame = ttk.Frame(self.notebook)
        self.categorias_frame = ttk.Frame(self.notebook)
        self.proveedores_frame = ttk.Frame(self.notebook)
        self.informes_frame = ttk.Frame(self.notebook)  # Nueva pestaña de Informe

        self.notebook.add(self.productos_frame, text="Productos")
        self.notebook.add(self.categorias_frame, text="Categorías")
        self.notebook.add(self.proveedores_frame, text="Proveedores")
        self.notebook.add(self.informes_frame, text="Informes")
        self.create_informes_widgets()

        # Interfaz para productos
        self.create_productos_widgets()

        # Interfaz para categorías
        self.create_categorias_widgets()

        # Interfaz para proveedores
        self.create_proveedores_widgets()

        # Interfaz para bodega
        self.bodegas_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.bodegas_frame, text="Bodegas")
        self.create_bodegas_widgets()


    def create_productos_widgets(self):
        frame = self.productos_frame

        # Campos para registrar productos
        ttk.Label(frame, text="Nombre:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.nombre_producto_entry = ttk.Entry(frame)
        self.nombre_producto_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(frame, text="Descripción:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.descripcion_producto_entry = ttk.Entry(frame)
        self.descripcion_producto_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(frame, text="Precio:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.precio_producto_entry = ttk.Entry(frame)
        self.precio_producto_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(frame, text="Stock Inicial:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.stock_producto_entry = ttk.Entry(frame)
        self.stock_producto_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(frame, text="Categoría:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.categoria_producto_combobox = ttk.Combobox(frame, state="readonly")
        self.categoria_producto_combobox.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

        ttk.Button(frame, text="Registrar Producto", command=self.registrar_producto).grid(row=5, column=0, columnspan=2, pady=10)

        # Campos para agregar stock
        ttk.Label(frame, text="Producto:").grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.producto_stock_combobox = ttk.Combobox(frame, state="readonly")
        self.producto_stock_combobox.grid(row=6, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(frame, text="Cantidad a agregar:").grid(row=7, column=0, padx=10, pady=5, sticky="w")
        self.cantidad_stock_entry = ttk.Entry(frame)
        self.cantidad_stock_entry.grid(row=7, column=1, padx=10, pady=5, sticky="ew")

        ttk.Button(frame, text="Agregar Stock", command=self.agregar_stock).grid(row=8, column=0, columnspan=2, pady=10)

        # Campos para retirar stock
        ttk.Label(frame, text="Producto:").grid(row=9, column=0, padx=10, pady=5, sticky="w")
        self.producto_retirar_combobox = ttk.Combobox(frame, state="readonly")
        self.producto_retirar_combobox.grid(row=9, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(frame, text="Cantidad a retirar:").grid(row=10, column=0, padx=10, pady=5, sticky="w")
        self.cantidad_retirar_entry = ttk.Entry(frame)
        self.cantidad_retirar_entry.grid(row=10, column=1, padx=10, pady=5, sticky="ew")

        ttk.Button(frame, text="Retirar Stock", command=self.retirar_stock).grid(row=11, column=0, columnspan=2, pady=10)

        # Botón para calcular el valor total del stock
        ttk.Button(frame, text="Calcular Valor Total del Stock", command=self.calcular_valor_total_stock).grid(row=12, column=0, columnspan=2, pady=10)

        # Tabla para mostrar productos registrados
        self.productos_tree = ttk.Treeview(frame, columns=("Nombre", "Descripción", "Precio", "Stock", "Categoría"), show="headings")
        self.productos_tree.heading("Nombre", text="Nombre")
        self.productos_tree.heading("Descripción", text="Descripción")
        self.productos_tree.heading("Precio", text="Precio")
        self.productos_tree.heading("Stock", text="Stock")
        self.productos_tree.heading("Categoría", text="Categoría")
        self.productos_tree.grid(row=13, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(13, weight=1)


    def create_categorias_widgets(self):
        frame = self.categorias_frame

        # Sección: Crear Categorías
        crear_frame = ttk.LabelFrame(frame, text="Crear Categoría")
        crear_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        ttk.Label(crear_frame, text="Nombre de la Categoría:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.nombre_categoria_entry = ttk.Entry(crear_frame)
        self.nombre_categoria_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(crear_frame, text="Descripción:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.descripcion_categoria_entry = ttk.Entry(crear_frame)
        self.descripcion_categoria_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        ttk.Button(crear_frame, text="Registrar Categoría", command=self.registrar_categoria).grid(row=2, column=0, columnspan=2, pady=10)

        crear_frame.columnconfigure(1, weight=1)

        # Sección: Eliminar Producto de Categoría
        eliminar_frame = ttk.LabelFrame(frame, text="Eliminar Producto de Categoría")
        eliminar_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        ttk.Label(eliminar_frame, text="Producto a eliminar:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.producto_eliminar_entry = ttk.Entry(eliminar_frame)
        self.producto_eliminar_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(eliminar_frame, text="Categoría:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.categoria_eliminar_combobox = ttk.Combobox(eliminar_frame, state="readonly")
        self.categoria_eliminar_combobox.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        ttk.Button(eliminar_frame, text="Eliminar Producto de Categoría", command=self.eliminar_producto_de_categoria).grid(row=2, column=0, columnspan=2, pady=10)

        eliminar_frame.columnconfigure(1, weight=1)

        # Tabla: Mostrar Categorías
        self.categorias_tree = ttk.Treeview(frame, columns=("Nombre", "Descripción"), show="headings")
        self.categorias_tree.heading("Nombre", text="Nombre")
        self.categorias_tree.heading("Descripción", text="Descripción")
        self.categorias_tree.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(2, weight=1)



    def create_proveedores_widgets(self):
        frame = self.proveedores_frame

        # Sección: Registrar un nuevo proveedor
        registrar_frame = ttk.LabelFrame(frame, text="Registrar Proveedor")
        registrar_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        ttk.Label(registrar_frame, text="Nombre del Proveedor:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.nombre_proveedor_entry = ttk.Entry(registrar_frame)
        self.nombre_proveedor_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(registrar_frame, text="Dirección:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.direccion_proveedor_entry = ttk.Entry(registrar_frame)
        self.direccion_proveedor_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(registrar_frame, text="Teléfono:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.telefono_proveedor_entry = ttk.Entry(registrar_frame)
        self.telefono_proveedor_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(registrar_frame, text="Productos Suministrados:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.productos_suministrados_listbox = tk.Listbox(registrar_frame, selectmode="multiple")
        self.productos_suministrados_listbox.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        ttk.Button(registrar_frame, text="Registrar Proveedor", command=self.registrar_proveedor).grid(row=4, column=0, columnspan=2, pady=10)

        registrar_frame.columnconfigure(1, weight=1)

        # Sección: Agregar Producto a Proveedor
        agregar_frame = ttk.LabelFrame(frame, text="Agregar Producto a Proveedor")
        agregar_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        ttk.Label(agregar_frame, text="Proveedor:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.proveedor_producto_combobox = ttk.Combobox(agregar_frame, state="readonly")
        self.proveedor_producto_combobox.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(agregar_frame, text="Producto a agregar:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.producto_agregar_combobox = ttk.Combobox(agregar_frame, state="readonly")
        self.producto_agregar_combobox.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        ttk.Button(agregar_frame, text="Agregar Producto a Proveedor", command=self.agregar_producto_a_proveedor).grid(row=2, column=0, columnspan=2, pady=10)

        agregar_frame.columnconfigure(1, weight=1)

        # Sección: Eliminar Producto de Proveedor
        eliminar_frame = ttk.LabelFrame(frame, text="Eliminar Producto de Proveedor")
        eliminar_frame.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")

        ttk.Label(eliminar_frame, text="Proveedor:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.proveedor_eliminar_combobox = ttk.Combobox(eliminar_frame, state="readonly")
        self.proveedor_eliminar_combobox.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        self.proveedor_eliminar_combobox.bind("<<ComboboxSelected>>", self.on_proveedor_seleccionado)

        ttk.Label(eliminar_frame, text="Producto a eliminar:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.producto_eliminar_combobox = ttk.Combobox(eliminar_frame, state="readonly")
        self.producto_eliminar_combobox.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        ttk.Button(eliminar_frame, text="Eliminar Producto de Proveedor", command=self.eliminar_producto_de_proveedor).grid(row=2, column=0, columnspan=2, pady=10)

        eliminar_frame.columnconfigure(1, weight=1)

        # Tabla para mostrar proveedores registrados
        self.proveedores_tree = ttk.Treeview(frame, columns=("Nombre", "Dirección", "Teléfono", "Productos"), show="headings")
        self.proveedores_tree.heading("Nombre", text="Nombre")
        self.proveedores_tree.heading("Dirección", text="Dirección")
        self.proveedores_tree.heading("Teléfono", text="Teléfono")
        self.proveedores_tree.heading("Productos", text="Productos")
        self.proveedores_tree.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(3, weight=1)

        self.actualizar_productos_a_agregar()  
        self.proveedor_producto_combobox.bind("<<ComboboxSelected>>", self.on_proveedor_seleccionado)



    def registrar_proveedor(self):
        # Obtener datos del formulario
        nombre = self.nombre_proveedor_entry.get()
        direccion = self.direccion_proveedor_entry.get()
        telefono = self.telefono_proveedor_entry.get()
        seleccionados = self.productos_suministrados_listbox.curselection()

        # Validar campos obligatorios
        if not (nombre and direccion and telefono):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        # Validar que haya productos seleccionados
        if not seleccionados:
            messagebox.showerror("Error", "Debe seleccionar al menos un producto.")
            return

        # Obtener los productos seleccionados
        productos_seleccionados = []
        for i in seleccionados:
            producto = self.inventario.listar_productos()[i]
            productos_seleccionados.append(producto)

        # Crear y agregar el proveedor al inventario
        proveedor = Proveedor(nombre, direccion, telefono, productos_seleccionados)
        self.inventario.agregar_proveedor(proveedor)

        # Insertar el proveedor en la tabla
        productos_texto = ", ".join([p.nombre for p in productos_seleccionados])
        self.proveedores_tree.insert("", "end", values=(nombre, direccion, telefono, productos_texto))

        # Limpiar los campos del formulario
        self.nombre_proveedor_entry.delete(0, tk.END)
        self.direccion_proveedor_entry.delete(0, tk.END)
        self.telefono_proveedor_entry.delete(0, tk.END)
        self.productos_suministrados_listbox.selection_clear(0, tk.END)

        messagebox.showinfo("Éxito", "Proveedor registrado exitosamente.")

        self.actualizar_proveedores_combobox()



    def registrar_producto(self):
        nombre = self.nombre_producto_entry.get()
        descripcion = self.descripcion_producto_entry.get()
        precio = self.precio_producto_entry.get()
        stock = self.stock_producto_entry.get()
        categoria = self.categoria_producto_combobox.get()

        if not (nombre and descripcion and precio and stock and categoria):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            precio = float(precio)
            stock = int(stock)
            if precio <= 0 or stock < 0:
                raise ValueError("El precio debe ser mayor que cero y el stock no puede ser negativo.")
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número decimal y el stock un entero positivo.")
            return

        producto = Producto(nombre, descripcion, precio, stock, categoria)
        self.inventario.agregar_producto(producto)
         # Depuración
        print("Producto registrado:", producto.nombre)
        print("Productos en inventario:", [p.nombre for p in self.inventario.listar_productos()])

        self.actualizar_tabla_productos()

        # Depuración: Verificar los productos en el inventario
        print([p.nombre for p in self.inventario.listar_productos()])

        self.actualizar_tabla_productos()
        self.actualizar_listas_productos()
        self.actualizar_productos_a_agregar()  
        self.root.update_idletasks()


        # Limpiar los campos
        self.nombre_producto_entry.delete(0, tk.END)
        self.descripcion_producto_entry.delete(0, tk.END)
        self.precio_producto_entry.delete(0, tk.END)
        self.stock_producto_entry.delete(0, tk.END)
        self.categoria_producto_combobox.set("")

        messagebox.showinfo("Éxito", "Producto registrado exitosamente.")

    def registrar_categoria(self):
        nombre = self.nombre_categoria_entry.get()
        descripcion = self.descripcion_categoria_entry.get()

        if not (nombre and descripcion):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        categoria = Categoria(nombre, descripcion)
        self.inventario.agregar_categoria(categoria)

        self.categorias_tree.insert("", "end", values=(nombre, descripcion))

        # Actualizar las categorías en el combobox de productos
        self.categoria_producto_combobox['values'] = [cat.nombre for cat in self.inventario.listar_categorias()]

        self.nombre_categoria_entry.delete(0, tk.END)
        self.descripcion_categoria_entry.delete(0, tk.END)

        messagebox.showinfo("Éxito", "Categoría registrada exitosamente.")

        self.actualizar_listas_productos()

    
    def registrar_bodega(self):
        nombre = self.nombre_bodega_entry.get()
        ubicacion = self.ubicacion_bodega_entry.get()
        capacidad = self.capacidad_bodega_entry.get()

        if not (nombre and ubicacion and capacidad):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            capacidad = int(capacidad)
            if capacidad <= 0:
                raise ValueError("La capacidad debe ser mayor que cero.")
        except ValueError:
            messagebox.showerror("Error", "La capacidad debe ser un número entero positivo.")
            return

        # Crear la nueva bodega
        bodega = Bodega(nombre, ubicacion, capacidad)
        self.inventario.agregar_bodega(bodega)

        # Actualizar la tabla y los combobox
        self.actualizar_tabla_bodegas()

        # Limpiar los campos
        self.nombre_bodega_entry.delete(0, tk.END)
        self.ubicacion_bodega_entry.delete(0, tk.END)
        self.capacidad_bodega_entry.delete(0, tk.END)

        messagebox.showinfo("Éxito", f"Bodega '{nombre}' registrada exitosamente.")


    
    def create_bodegas_widgets(self):
        frame = self.bodegas_frame

        # Campos para registrar una nueva bodega
        ttk.Label(frame, text="Nombre de la Bodega:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.nombre_bodega_entry = ttk.Entry(frame)
        self.nombre_bodega_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(frame, text="Ubicación:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.ubicacion_bodega_entry = ttk.Entry(frame)
        self.ubicacion_bodega_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(frame, text="Capacidad Máxima:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.capacidad_bodega_entry = ttk.Entry(frame)
        self.capacidad_bodega_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        ttk.Button(frame, text="Registrar Bodega", command=self.registrar_bodega).grid(row=3, column=0, columnspan=2, pady=10)

        # Campos para agregar un producto a una bodega existente
        ttk.Label(frame, text="Bodega:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.bodega_combobox = ttk.Combobox(frame, state="readonly")
        self.bodega_combobox.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(frame, text="Producto:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.producto_bodega_combobox = ttk.Combobox(frame, state="readonly")
        self.producto_bodega_combobox.grid(row=5, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(frame, text="Cantidad:").grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.cantidad_bodega_entry = ttk.Entry(frame)
        self.cantidad_bodega_entry.grid(row=6, column=1, padx=10, pady=5, sticky="ew")

        ttk.Button(frame, text="Agregar Producto a Bodega", command=self.agregar_producto_a_bodega).grid(row=7, column=0, columnspan=2, pady=10)

        # Campos para retirar un producto de una bodega existente
        ttk.Label(frame, text="Bodega:").grid(row=9, column=0, padx=10, pady=5, sticky="w")
        self.bodega_retirar_combobox = ttk.Combobox(frame, state="readonly")
        self.bodega_retirar_combobox.grid(row=9, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(frame, text="Producto:").grid(row=10, column=0, padx=10, pady=5, sticky="w")
        self.producto_retirar_combobox = ttk.Combobox(frame, state="readonly")
        self.producto_retirar_combobox.grid(row=10, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(frame, text="Cantidad a retirar:").grid(row=11, column=0, padx=10, pady=5, sticky="w")
        self.cantidad_retirar_entry = ttk.Entry(frame)
        self.cantidad_retirar_entry.grid(row=11, column=1, padx=10, pady=5, sticky="ew")

        ttk.Button(frame, text="Retirar Producto de Bodega", command=self.retirar_producto_de_bodega).grid(row=12, column=0, columnspan=2, pady=10)

        # Tabla para mostrar bodegas registradas
        self.bodegas_tree = ttk.Treeview(frame, columns=("Nombre", "Ubicación", "Capacidad Máxima", "Productos"), show="headings")
        self.bodegas_tree.heading("Nombre", text="Nombre")
        self.bodegas_tree.heading("Ubicación", text="Ubicación")
        self.bodegas_tree.heading("Capacidad Máxima", text="Capacidad Máxima")
        self.bodegas_tree.heading("Productos", text="Productos")
        self.bodegas_tree.grid(row=13, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(13, weight=1)



# Inicialización
root = tk.Tk()
app = InventarioApp(root)
root.mainloop()

