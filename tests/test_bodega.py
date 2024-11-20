import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.bodega import Bodega  
def test_bodega_creation():
    bodega = Bodega("Central", "City Center", 100)
    assert bodega.nombre == "Central"
    assert bodega.ubicacion == "City Center"
    assert bodega.capacidad_maxima == 100
    assert bodega.espacio_disponible() == 100
    assert bodega.productos == {}

def test_agregar_producto():
    bodega = Bodega("Central", "City Center", 100)
    bodega.agregar_producto("Manzanas", 30)
    assert bodega.productos["Manzanas"] == 30
    assert bodega.espacio_disponible() == 70

    bodega.agregar_producto("Manzanas", 20)
    assert bodega.productos["Manzanas"] == 50
    assert bodega.espacio_disponible() == 50

    bodega.agregar_producto("Peras", 20)
    assert bodega.productos["Peras"] == 20
    assert bodega.espacio_disponible() == 30

    with pytest.raises(ValueError, match="No hay suficiente espacio disponible"):
        bodega.agregar_producto("Naranjas", 50)

def test_retirar_producto():
    bodega = Bodega("Central", "City Center", 100)
    bodega.agregar_producto("Manzanas", 50)

    bodega.retirar_producto("Manzanas", 20)
    assert bodega.productos["Manzanas"] == 30
    assert bodega.espacio_disponible() == 70

    bodega.retirar_producto("Manzanas", 30)
    assert "Manzanas" not in bodega.productos
    assert bodega.espacio_disponible() == 100

    with pytest.raises(ValueError, match="no está almacenado en la bodega"):
        bodega.retirar_producto("Peras", 10)
        
    bodega.agregar_producto("Manzanas", 40)
    with pytest.raises(ValueError, match="No hay suficiente cantidad del producto"):
        bodega.retirar_producto("Manzanas", 50)

def test_espacio_disponible():
    bodega = Bodega("Central", "City Center", 200)
    assert bodega.espacio_disponible() == 200
    bodega.agregar_producto("Manzanas", 50)
    assert bodega.espacio_disponible() == 150
    bodega.agregar_producto("Peras", 70)
    assert bodega.espacio_disponible() == 80
    bodega.retirar_producto("Peras", 20)
    assert bodega.espacio_disponible() == 100
