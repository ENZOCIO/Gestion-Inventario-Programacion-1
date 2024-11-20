import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.proveedor import Proveedor
from app.producto import Producto

def test_proveedor_creation():
    producto1 = Producto("Manzana", "Fruta roja y jugosa", 1.5, 100, "Frutas")
    producto2 = Producto("Pera", "Fruta verde y dulce", 1.2, 75, "Frutas")
    proveedor = Proveedor("Proveedor A", "Calle 123", "123456789", [producto1, producto2])
    assert proveedor.nombre == "Proveedor A"
    assert proveedor.direccion == "Calle 123"
    assert proveedor.telefono == "123456789"
    assert proveedor.productos == [producto1, producto2]

def test_proveedor_repr():
    producto1 = Producto("Manzana", "Fruta roja y jugosa", 1.5, 100, "Frutas")
    producto2 = Producto("Pera", "Fruta verde y dulce", 1.2, 75, "Frutas")
    proveedor = Proveedor("Proveedor A", "Calle 123", "123456789", [producto1, producto2])
    assert repr(proveedor) == "Proveedor(Proveedor A, 123456789, Productos: [Manzana, Pera])"
