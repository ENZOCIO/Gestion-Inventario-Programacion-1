class Bodega:
    def __init__(self, nombre, ubicacion, capacidad_maxima):
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.capacidad_maxima = capacidad_maxima
        self.productos = {}  # Diccionario: {producto: cantidad}

    def espacio_disponible(self):
        # Calcula el espacio restante en la bodega
        espacio_usado = sum(self.productos.values())
        return self.capacidad_maxima - espacio_usado

    def agregar_producto(self, producto, cantidad):
        # Verifica si hay espacio disponible antes de agregar el producto
        if self.espacio_disponible() >= cantidad:
            if producto in self.productos:
                self.productos[producto] += cantidad
            else:
                self.productos[producto] = cantidad
        else:
            raise ValueError(f"No hay suficiente espacio disponible en la bodega '{self.nombre}'.")
        
    def retirar_producto(self, producto, cantidad):
        # Verifica si el producto está almacenado en la bodega
        if producto not in self.productos:
            raise ValueError(f"El producto '{producto.nombre}' no está almacenado en la bodega '{self.nombre}'.")
        # Verifica si hay suficiente cantidad para retirar
        if self.productos[producto] < cantidad:
            raise ValueError(f"No hay suficiente cantidad del producto '{producto.nombre}' en la bodega '{self.nombre}'.")
        # Realiza la operación de retiro
        self.productos[producto] -= cantidad
        # Si la cantidad del producto llega a cero, lo elimina del diccionario
        if self.productos[producto] == 0:
            del self.productos[producto]