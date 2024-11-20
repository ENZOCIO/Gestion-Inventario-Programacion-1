class Proveedor:
    def __init__(self, nombre, direccion, telefono, productos):
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.productos = productos  # Lista de productos

    def __repr__(self):
        productos_nombres = ", ".join([p.nombre for p in self.productos])
        return f"Proveedor({self.nombre}, {self.telefono}, Productos: [{productos_nombres}])"