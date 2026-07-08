---
title: "Paquetes de Productos"
---

Los paquetes de productos te permiten vender conjuntos preensamblados de productos a un precio de paquete. Esto es perfecto para sets de regalo, kits de inicio o cualquier combinacion de productos que desees ofrecer juntos con un descuento.

![Bundle components admin](/static/core/admin/img/help/product-bundles/bundle-components.webp)

## Estrategias de Precios

Elige como se calcula el precio del paquete:

| Estrategia | Descripcion |
|------------|-------------|
| **Precio Fijo** | Establece un precio unico para todo el paquete, sin importar los precios de los componentes. |
| **Descuento Porcentual** | Calcula automaticamente el precio como un porcentaje de descuento sobre los precios combinados de los componentes. |
| **Suma de Componentes** | El precio del paquete es igual al total de todos los precios de los componentes (util para mostrar agrupaciones sin descuento). |

## Creacion de un Paquete

### Paso 1: Crear el Producto

1. Navega a **Productos > Todos los Productos** y haz clic en **+ Agregar Producto**
2. Establece el **Tipo de Producto** como **Paquete de Productos**
3. Completa el nombre del paquete, la descripcion y las imagenes
4. Guarda el producto

### Paso 2: Agregar Componentes

Cambia a la pestana **Articulos del Paquete** para agregar productos a tu paquete:

1. Haz clic en **+ Agregar Componente**
2. Busca y selecciona un producto del menu desplegable
3. Establece la **Cantidad** para cada componente (ej., 2x mascarillas faciales en un set de cuidado de la piel)
4. Establece el **Orden** para controlar el orden de visualizacion
5. Opcionalmente marca un componente como **Opcional** (los clientes pueden excluirlo)
6. Si el componente es un producto variable, elige entre:
   - Una **variante fija** — todos los clientes reciben la misma variante
   - **Permitir seleccion de variante** — los clientes eligen su variante preferida al pagar

El resumen en la parte inferior muestra el conteo de **Componentes Totales** y el **Valor del Paquete** (suma de los precios de los componentes).

### Paso 3: Configurar Precios

Cambia a la pestana **Precios**:

1. Selecciona tu **Estrategia de Precios del Paquete**
2. Para **Precio Fijo** — ingresa el precio del paquete directamente
3. Para **Descuento Porcentual** — establece el porcentaje de descuento (ej., 15% de descuento)
4. Para **Suma de Componentes** — el precio se calcula automaticamente

## Que se Puede Incluir en un Paquete

| Tipo de Producto | Puede ser Componente? |
|-----------------|----------------------|
| Producto Simple | Si |
| Producto Variable | Si (variante fija o eleccion del cliente) |
| Producto Digital | Si |
| Producto Personalizable | No |
| Producto Configurable | No |
| Paquete de Productos | No (los paquetes no pueden anidarse) |
| Tarjeta de Regalo | No |

## Gestion de Inventario

El inventario del paquete se gestiona a traves de sus componentes:

- **Todos los componentes deben estar en stock** para que el paquete se pueda comprar
- Cuando se ordena un paquete, el stock se deduce de cada producto componente individualmente
- Si algun componente se queda sin stock, el paquete deja de estar disponible
- Los niveles de stock de los componentes se verifican en tiempo real durante el proceso de pago

## Componentes Opcionales

Marca un componente como **Opcional** para permitir que los clientes personalicen su paquete:

- Los componentes opcionales se incluyen por defecto pero los clientes pueden eliminarlos
- El precio del paquete se ajusta en consecuencia cuando se excluyen componentes opcionales
- Al menos un componente debe ser no opcional (obligatorio)

## Experiencia del Cliente

Cuando un cliente ve un paquete en tu tienda:

1. **Lista de Componentes** — Todos los productos incluidos se muestran con imagenes y cantidades
2. **Ahorro del Paquete** — Se muestra el descuento en comparacion con comprar los articulos individualmente
3. **Seleccion de Variante** — Para componentes con seleccion de variante habilitada, los clientes eligen su opcion preferida
4. **Articulos Opcionales** — Los clientes pueden activar o desactivar componentes opcionales
5. **Agregar al Carrito Unico** — Todo el paquete se agrega como un solo articulo

## Consejos

- Usa la estrategia de Descuento Porcentual para la mayor flexibilidad de precios — se ajusta automaticamente cuando cambian los precios de los componentes.
- Muestra el monto de ahorro de manera prominente en la descripcion del producto para incentivar la compra de paquetes.
- Limita los paquetes a 3-5 componentes para la mejor experiencia del cliente. Demasiados articulos pueden resultar abrumadores.
- Usa componentes opcionales para ofrecer una version "basica" y "premium" del mismo paquete.
- Verifica regularmente que todos los productos componentes sigan activos y en stock.
