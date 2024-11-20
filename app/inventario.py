from producto import Producto
from categoria import Categoria
from proveedor import Proveedor
from bodega import Bodega


class Inventario:
    def __init__(self):
        self.productos = []
        self.categorias = []
        self.proveedores = []
        self.bodegas = []

    def agregar_producto(self, producto):
        if not isinstance(producto, Producto):
            raise ValueError("El objeto no es una instancia de la clase Producto")
        self.productos.append(producto)
        print(f"Producto agregado: {producto.nombre}")
        print(f"Productos en inventario: {[p.nombre for p in self.productos]}")



    def agregar_categoria(self, categoria):
        if not isinstance(categoria, Categoria):
            raise ValueError("El objeto no es una instancia de la clase Categoria")
        self.categorias.append(categoria)

    def agregar_proveedor(self, proveedor):
        if not isinstance(proveedor, Proveedor):
            raise ValueError("El objeto no es una instancia de la clase Proveedor")
        self.proveedores.append(proveedor)

    def agregar_bodega(self, bodega):
        if not isinstance(bodega, Bodega):
            raise ValueError("El objeto no es una instancia de la clase Bodega")
        self.bodegas.append(bodega)

    def listar_categorias(self):
        return self.categorias

    def listar_productos(self):
        print("Lista de productos en el inventario:", [p.nombre for p in self.productos])
        return self.productos



    def listar_proveedores(self):
        return self.proveedores

    def listar_bodegas(self):
        return self.bodegas

    def __repr__(self):
        return f"Inventario({len(self.productos)} productos, {len(self.categorias)} categorias, {len(self.proveedores)} proveedores, {len(self.bodegas)} bodegas)"

    def retirar_stock(self, nombre_producto, cantidad):
        for producto in self.productos:
            if producto.nombre == nombre_producto:
                if producto.stock >= cantidad:
                    producto.stock -= cantidad
                    return True
            else:
                raise ValueError("Cantidad a retirar excede el stock disponible.")
        return False  # Si el producto no se encuentra
    
    def agregar_stock(self, nombre_producto, cantidad):
        for producto in self.productos:
            if producto.nombre == nombre_producto:
                producto.stock += cantidad  # Actualizar el stock
                return True
        return False  # Si el producto no se encuentra

    
    def calcular_valor_total_stock(self):
        # Calcula el valor total del stock sumando precio * stock para cada producto
        total = sum(producto.precio * producto.stock for producto in self.productos)
        return total
    
    def eliminar_producto_de_categoria(self, nombre_producto, nombre_categoria):
        for producto in self.productos:
            if producto.nombre == nombre_producto and producto.categoria == nombre_categoria:
                self.productos.remove(producto)
                return True
        return False  # Si no se encuentra el producto o la categoría
    
    def agregar_producto_a_proveedor(self, nombre_proveedor, producto):
        # Buscar proveedor
        proveedor = next((p for p in self.proveedores if p.nombre == nombre_proveedor), None)
        if not proveedor:
            raise ValueError(f"El proveedor '{nombre_proveedor}' no existe.")

        # Verificar si el producto ya está en la lista
        if producto in proveedor.productos:
            raise ValueError(f"El producto '{producto.nombre}' ya está asociado al proveedor '{nombre_proveedor}'.")

        # Agregar el producto
        proveedor.productos.append(producto)
        print(f"Producto '{producto.nombre}' agregado al proveedor '{nombre_proveedor}'.")
        return True

    
    def eliminar_producto_de_proveedor(self, nombre_proveedor, nombre_producto):
        for proveedor in self.proveedores:
            if proveedor.nombre == nombre_proveedor:
                producto_a_eliminar = next((p for p in proveedor.productos if p.nombre == nombre_producto), None)
                if producto_a_eliminar:
                    proveedor.productos.remove(producto_a_eliminar)  # Eliminar el producto de la lista
                    return True
                else:
                      raise ValueError(f"El producto '{nombre_producto}' no está en la lista de productos suministrados por '{nombre_proveedor}'.")
            return False  # Si no se encuentra el proveedor
        
    def agregar_producto_a_bodega(self, nombre_bodega, producto, cantidad):
            # Busca la bodega por su nombre
            bodega = next((b for b in self.bodegas if b.nombre == nombre_bodega), None)
            if not bodega:
                raise ValueError(f"La bodega '{nombre_bodega}' no existe.")

            # Intenta agregar el producto a la bodega
            bodega.agregar_producto(producto, cantidad)
    
    def retirar_producto_de_bodega(self, nombre_bodega, producto, cantidad):
        # Buscar la bodega por su nombre
        bodega = next((b for b in self.bodegas if b.nombre == nombre_bodega), None)
        if not bodega:
            raise ValueError(f"La bodega '{nombre_bodega}' no existe.")

        # Llamar al método retirar_producto de la bodega
        bodega.retirar_producto(producto, cantidad)

    




