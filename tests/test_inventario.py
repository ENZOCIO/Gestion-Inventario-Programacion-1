import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))
from app.inventario import Inventario 
from app.producto import Producto
from app.categoria import Categoria
from app.proveedor import Proveedor
from app.bodega import Bodega


def test_inventario_creation():
    inventario = Inventario()
    assert len(inventario.productos) == 0
    assert len(inventario.categorias) == 0
    assert len(inventario.proveedores) == 0
    assert len(inventario.bodegas) == 0


def test_agregar_producto():
    inventario = Inventario()
    producto = Producto("Manzana", 10, 1.5, "Frutas")
    inventario.agregar_producto(producto)
    assert len(inventario.productos) == 1
    assert inventario.productos[0] == producto


def test_agregar_categoria():
    inventario = Inventario()
    categoria = Categoria("Frutas", "Frutas frescas")
    inventario.agregar_categoria(categoria)
    assert len(inventario.categorias) == 1
    assert inventario.categorias[0] == categoria


def test_agregar_proveedor():
    inventario = Inventario()
    proveedor = Proveedor("Proveedor A", [])
    inventario.agregar_proveedor(proveedor)
    assert len(inventario.proveedores) == 1
    assert inventario.proveedores[0] == proveedor


def test_agregar_bodega():
    inventario = Inventario()
    bodega = Bodega("Bodega Central", "Ciudad", 100)
    inventario.agregar_bodega(bodega)
    assert len(inventario.bodegas) == 1
    assert inventario.bodegas[0] == bodega


def test_listar_productos():
    inventario = Inventario()
    producto1 = Producto("Manzana", 10, 1.5, "Frutas")
    producto2 = Producto("Pera", 5, 1.2, "Frutas")
    inventario.agregar_producto(producto1)
    inventario.agregar_producto(producto2)
    productos = inventario.listar_productos()
    assert len(productos) == 2
    assert producto1 in productos
    assert producto2 in productos


def test_retirar_stock():
    inventario = Inventario()
    producto = Producto("Manzana", 10, 1.5, "Frutas")
    inventario.agregar_producto(producto)
    inventario.retirar_stock("Manzana", 5)
    assert producto.stock == 5


def test_retirar_stock_insuficiente():
    inventario = Inventario()
    producto = Producto("Manzana", 10, 1.5, "Frutas")
    inventario.agregar_producto(producto)
    with pytest.raises(ValueError, match="Cantidad a retirar excede el stock disponible."):
        inventario.retirar_stock("Manzana", 15)


def test_calcular_valor_total_stock():
    inventario = Inventario()
    producto1 = Producto("Manzana", 10, 1.5, "Frutas")
    producto2 = Producto("Pera", 5, 1.2, "Frutas")
    inventario.agregar_producto(producto1)
    inventario.agregar_producto(producto2)
    total_valor = inventario.calcular_valor_total_stock()
    assert total_valor == (10 * 1.5) + (5 * 1.2)


def test_agregar_producto_a_bodega():
    inventario = Inventario()
    bodega = Bodega("Bodega Central", "Ciudad", 100)
    producto = Producto("Manzana", 0, 1.5, "Frutas")
    inventario.agregar_bodega(bodega)
    inventario.agregar_producto(producto)
    inventario.agregar_producto_a_bodega("Bodega Central", producto, 50)
    assert bodega.productos["Manzana"] == 50


def test_retirar_producto_de_bodega():
    inventario = Inventario()
    bodega = Bodega("Bodega Central", "Ciudad", 100)
    producto = Producto("Manzana", 0, 1.5, "Frutas")
    inventario.agregar_bodega(bodega)
    inventario.agregar_producto(producto)
    inventario.agregar_producto_a_bodega("Bodega Central", producto, 50)
    inventario.retirar_producto_de_bodega("Bodega Central", producto, 20)
    assert bodega.productos["Manzana"] == 30


def test_agregar_producto_a_proveedor():
    inventario = Inventario()
    proveedor = Proveedor("Proveedor A", [])
    producto = Producto("Manzana", 10, 1.5, "Frutas")
    inventario.agregar_proveedor(proveedor)
    inventario.agregar_producto(producto)
    inventario.agregar_producto_a_proveedor("Proveedor A", producto)
    assert producto in proveedor.productos


def test_eliminar_producto_de_proveedor():
    inventario = Inventario()
    proveedor = Proveedor("Proveedor A", [])
    producto = Producto("Manzana", 10, 1.5, "Frutas")
    inventario.agregar_proveedor(proveedor)
    inventario.agregar_producto_a_proveedor("Proveedor A", producto)
    inventario.eliminar_producto_de_proveedor("Proveedor A", "Manzana")
    assert producto not in proveedor.productos
