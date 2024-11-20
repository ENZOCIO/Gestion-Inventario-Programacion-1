## Realizado por ENZO GONZALEZ CAICEDO Y SANTIAGO JIMENEZ MARTINEZ

## Sistema de Gestión de Inventario

Este proyecto es un sistema de gestión de inventario desarrollado en Python. Incluye funcionalidades para registrar, gestionar y consultar productos, categorías, proveedores y bodegas, además de generar informes de stock. La interfaz gráfica está construida con `tkinter`


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
```

--- 

## Instrucciones de Instalacion

- **Clonar el Repositorio**

git clone https://github.com/tu_usuario/gestion-de-inventario.git
cd gestion-de-inventario

- **Crear y Activar un Entorno Virtual**

python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows

**Instalar Dependencias** 

pip install -r requirements.txt

- **Ejecutar la Aplicación**

python main.py

---

## Uso del Sistema

# Interfaz Gráfica

- Ejecuta main.py para abrir la interfaz gráfica.
- Usa las pestañas para gestionar productos, categorías, proveedores, bodegas e informes.

# Gestión con Git Bash

- Clonar el repositorio

git clone https://github.com/tu_usuario/gestion-de-inventario.git

- Crear un nuevo branch

git checkout -b feature/nombre-del-feature

- Agregar cambios

git add .
git commit -m "Descripción de los cambios"

- Subir cambios al repositorio

git push origin feature/nombre-del-feature

---


## Licencia

**Este proyecto está licenciado bajo la MIT License. Consulta el archivo LICENSE para más información.**










