# producto.py
class Producto:
    def __init__(self, nombre, descripcion, precio, stock, categoria):
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock
        self.categoria = categoria
    
    def __hash__(self):
        # Usa el nombre del producto como base para el hash
        return hash(self.nombre)

    def __eq__(self, other):
        # Compara los productos basándose en su nombre
        if isinstance(other, Producto):
            return self.nombre == other.nombre
        return False

    def __repr__(self):
        return f"Producto({self.nombre}, {self.categoria}, {self.precio}, {self.stock})"
