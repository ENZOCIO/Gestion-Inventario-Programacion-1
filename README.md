## Realizado por ENZO GONZALEZ CAICEDO Y SANTIAGO JIMENEZ MARTINEZ

## Sistema de Gestión de Inventario

Este proyecto es un sistema de gestión de inventario desarrollado en Python. Incluye funcionalidades para registrar, gestionar y consultar productos, categorías, proveedores y bodegas, además de generar informes de stock. La interfaz gráfica está construida con `tkinter`.



---

## Características Principales

- Registro de Entidades:
  - **Productos**: Nombre, descripción, precio, stock inicial y categoría.
  - **Categorías**: Nombre y descripción.
  - **Proveedores**: Nombre, dirección, teléfono y lista de productos suministrados.
  - **Bodegas**: Nombre, ubicación, capacidad máxima y lista de productos almacenados.
- Gestión de Stock:
  - Agregar y retirar stock de productos.
  - Calcular el valor total del inventario.
- Relaciones entre Entidades:
  - Asociar y eliminar productos de categorías, proveedores y bodegas.
  - Validar espacio disponible en bodegas y cantidad disponible de stock.
- Consultas e Informes:
  - Generar informes sobre stock total, por categoría, proveedor o bodega.
  - Consultar información detallada de cualquier entidad.

---

## Requisitos del Sistema

- **Python 3.8+**
- Módulos requeridos:
  - `tkinter`
  - `graphviz` (opcional, para diagramas UML)

Instala las dependencias con:
```bash
pip install -r requirements.txt

GestionDeInventario/
├── app/
│   ├── bodega.py         # Clase Bodega
│   ├── categoria.py      # Clase Categoria
│   ├── inventario.py     # Clase Inventario
│   ├── producto.py       # Clase Producto
│   ├── proveedor.py      # Clase Proveedor
├── tests/                # Tests unitarios con pytest
├── main.py               # Aplicación gráfica con tkinter
├── README.md             # Documentación del proyecto
└── requirements.txt      # Dependencias del proyecto


# Instrucciones de Instalacion

    - **Clonar el Repositorio**

    git clone https://github.com/tu_usuario/gestion-de-inventario.git
    cd gestion-de-inventario



