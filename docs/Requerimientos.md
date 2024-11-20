# Sistema de Gestión de Inventario

## Registro de Entidades
El sistema debe permitir:
- Registrar un **producto** con los siguientes atributos:
  - Nombre
  - Descripción
  - Precio
  - Stock inicial
  - Categoría a la que pertenece
- Registrar una **categoría** con los siguientes atributos:
  - Nombre
  - Descripción
- Registrar un **proveedor** con los siguientes atributos:
  - Nombre
  - Dirección
  - Teléfono
  - Lista de productos que suministra
- Registrar una **bodega** con los siguientes atributos:
  - Nombre
  - Ubicación
  - Capacidad máxima
  - Lista de productos almacenados

## Gestión de Stock
El sistema debe permitir:
- **Agregar stock** a un producto existente, especificando la cantidad a ingresar.
- **Retirar stock** de un producto existente, especificando la cantidad a retirar.
- **Calcular el valor total del stock**, sumando el precio de cada producto por la cantidad disponible.

## Relaciones entre Entidades
El sistema debe permitir:
- **Agregar un producto** a una categoría existente.
- **Eliminar un producto** de una categoría existente.
- **Agregar un producto** a la lista de productos suministrados por un proveedor existente.
- **Eliminar un producto** de la lista de productos suministrados por un proveedor existente.
- **Agregar un producto** a la lista de productos almacenados en una bodega existente, verificando si hay espacio disponible en la bodega.
- **Retirar un producto** de la lista de productos almacenados en una bodega, verificando si la cantidad a retirar no excede el stock disponible en la bodega.
- **Consultar la disponibilidad de un producto** en una bodega específica.

## Consultas y Reportes
El sistema debe permitir:
- **Consultar información de un producto**, incluyendo:
  - Nombre
  - Descripción
  - Precio
  - Stock actual
  - Categoría a la que pertenece
  - Proveedor asociado
- **Consultar información de una categoría**, incluyendo:
  - Nombre
  - Descripción
  - Lista de productos asociados
- **Consultar información de un proveedor**, incluyendo:
  - Nombre
  - Dirección
  - Teléfono
  - Lista de productos que suministra
- **Consultar información de una bodega**, incluyendo:
  - Nombre
  - Ubicación
  - Capacidad máxima
  - Lista de productos almacenados
- **Generar informes de stock**, incluyendo:
  - Stock total
  - Stock por categoría
  - Stock por proveedor
  - Stock por bodega
