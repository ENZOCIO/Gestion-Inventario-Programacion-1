import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))
from app.producto import Producto

def test_producto_creation():
    producto = Producto("Manzana", "Fruta roja y jugosa", 1.5, 100, "Frutas")
    assert producto.nombre == "Manzana"
    assert producto.descripcion == "Fruta roja y jugosa"
    assert producto.precio == 1.5
    assert producto.stock == 100
    assert producto.categoria == "Frutas"

def test_producto_repr():
    producto = Producto("Manzana", "Fruta roja y jugosa", 1.5, 100, "Frutas")
    assert repr(producto) == "Producto(Manzana, Frutas, 1.5, 100)"

def test_producto_equality():
    producto1 = Producto("Manzana", "Fruta roja y jugosa", 1.5, 100, "Frutas")
    producto2 = Producto("Manzana", "Fruta diferente", 2.0, 50, "Frutas")
    producto3 = Producto("Pera", "Fruta verde y dulce", 1.2, 75, "Frutas")
    assert producto1 == producto2
    assert producto1 != producto3

def test_producto_hash():
    producto1 = Producto("Manzana", "Fruta roja y jugosa", 1.5, 100, "Frutas")
    producto2 = Producto("Manzana", "Fruta diferente", 2.0, 50, "Frutas")
    producto3 = Producto("Pera", "Fruta verde y dulce", 1.2, 75, "Frutas")
    assert hash(producto1) == hash(producto2)
    assert hash(producto1) != hash(producto3)

def test_producto_update_stock():
    producto = Producto("Manzana", "Fruta roja y jugosa", 1.5, 100, "Frutas")
    producto.stock += 50
    assert producto.stock == 150
    producto.stock -= 25
    assert producto.stock == 125
