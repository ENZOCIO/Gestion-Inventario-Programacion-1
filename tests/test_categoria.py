import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  
from app.categoria import Categoria  # Replace with the correct import path if necessary

def test_categoria_creation():
    # Test creation of a Categoria instance
    categoria = Categoria("Frutas", "Productos frescos y naturales")
    assert categoria.nombre == "Frutas"
    assert categoria.descripcion == "Productos frescos y naturales"

def test_categoria_repr():
    # Test the __repr__ method
    categoria = Categoria("Lácteos", "Productos derivados de la leche")
    assert repr(categoria) == "Categoria(Lácteos, Productos derivados de la leche)"
