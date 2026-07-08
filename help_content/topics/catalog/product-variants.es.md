---
title: Variantes de Producto
---

Las variantes de producto le permiten ofrecer un solo producto en múltiples opciones — como diferentes tallas, colores o materiales — cada una con su propio SKU, precio y nivel de stock. Navegue a cualquier **Producto Variable** y haga clic en la pestaña **Variaciones**.

![Variantes de producto](/static/core/admin/img/help/product-variants/product-variants.webp)

## Comprender las Variantes

Un **Producto Variable** es un tipo de producto que admite múltiples variaciones. Por ejemplo, una camiseta puede estar disponible en:
- **Colores**: Azul, Rojo, Verde
- **Tallas**: S, M, L, XL

Cada combinación (ej., "Azul / Grande") se convierte en una variante separada con su propio inventario y precio.

## Configurar un Producto Variable

### Paso 1: Establecer el Tipo de Producto

1. Abra el formulario de edición del producto (o cree un nuevo producto)
2. En la pestaña **Información Básica**, establezca **Tipo de Producto** como **Producto Variable**
3. Guarde el producto

### Paso 2: Definir Atributos

Los atributos son las opciones que diferencian sus variantes (ej., Talla, Color).

1. Vaya a la pestaña **Variaciones**
2. En la sección **Atributos del Producto**, haga clic en **+ Añadir Atributo** para asignar un atributo existente, o **Crear Nuevo** para definir uno nuevo
3. Para cada atributo, especifique los valores disponibles (ej., Pequeño, Mediano, Grande)

### Paso 3: Crear Variantes

1. En la sección **Variantes del Producto**, haga clic en **+ Añadir Nueva Variante**
2. Configure cada variante:
   - **Nombre** — Etiqueta descriptiva (ej., "Azul", "Grande / Rojo")
   - **SKU** — Código único de unidad de mantenimiento de stock
   - **Precio** — Precio específico de la variante (puede diferir del producto base)
   - **Stock** — Nivel de inventario actual
3. Repita para cada variante que necesite

## Gestionar Variantes

### Detalles de la Variante

Cada tarjeta de variante muestra:
- **Nombre** y **SKU** — Información de identificación
- **Precio** — Precio de venta actual
- **Nivel de stock** — Cantidad disponible con indicador de estado (En Stock / Stock Bajo / Agotado)

Haga clic en una tarjeta de variante para expandir y editar todos sus detalles.

### Configuración Específica de la Variante

Cada variante puede tener su propia configuración:

| Configuración | Descripción |
|---------------|-------------|
| **Precio** | Anular el precio del producto base |
| **Precio de comparación** | Mostrar un precio de oferta con tachado |
| **SKU** | Identificador único para inventario |
| **Nivel de Stock** | Seguimiento de inventario independiente |
| **Peso** | Para cálculos de envío |
| **Imagen** | Imagen de producto específica de la variante |

### Editar una Variante

1. Haga clic en el **icono de edición** en la tarjeta de la variante
2. Modifique los campos deseados
3. Haga clic en **Guardar** para actualizar

### Eliminar una Variante

1. Haga clic en el **icono de eliminar** en la tarjeta de la variante
2. Confirme la eliminación

**Nota:** Eliminar una variante borra su registro de inventario. Esta acción no se puede deshacer.

## Atributos

### ¿Qué Son los Atributos?

Los atributos son definiciones de opciones reutilizables. Una vez que crea un atributo como "Talla" con los valores "S, M, L, XL", puede asignarlo a cualquier producto variable.

### Crear Atributos

1. En la pestaña Variaciones, haga clic en **Crear Nuevo** en la sección Atributos del Producto
2. Introduzca el nombre del atributo (ej., "Color")
3. Añada valores (ej., "Rojo", "Azul", "Verde")
4. Guarde el atributo

### Asignar Atributos

Los atributos se pueden asignar a múltiples productos. El mismo atributo "Talla" se puede usar en Camisetas, Pantalones y Zapatos.

## Visualización en la Tienda

En la tienda, los productos variables muestran:
- Selectores de opciones (desplegables o muestras) para cada atributo
- Actualizaciones automáticas de precio cuando se selecciona una variante
- Disponibilidad de stock por variante
- Imágenes específicas de la variante

## Consejos

- Use nombres de atributos consistentes en todos los productos para una experiencia de compra uniforme.
- Configure todos los atributos antes de crear variantes para agilizar el proceso.
- Suba imágenes específicas de cada variante para que los clientes puedan ver exactamente lo que están pidiendo.
- Mantenga los SKU sistemáticos (ej., "CAMISETA-AZUL-G") para facilitar la gestión del inventario.
- Use el precio de comparación en las variantes para realizar ofertas específicas por talla o color.
