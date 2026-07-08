---
title: Códigos de Cupón
---

Los códigos de cupón le permiten crear códigos de descuento, cupones y tarjetas regalo que los clientes ingresan en el momento del pago para recibir un descuento. Navegue hasta **Marketing > Cupones** en el menú lateral de administración.

![Lista de cupones](/static/core/admin/img/help/voucher-codes/voucher-list.webp)

## Panel de Cupones

La página de cupones muestra una vista general con:

- **Tarjetas de Estadísticas** — Cuentas de cupones activos, inactivos, redimidos y totales
- **Filtros** — Buscar por código o nombre, filtrar por Tipo, Estado y Alcance
- **Tarjetas de Cupones** — Cada cupón se muestra con detalles de uso y estado

## Crear un Cupón

1. Haga clic en **+ Agregar Cupón** en la parte superior derecha
2. Llene los detalles del cupón:
   - **Código** — El código que los clientes ingresan en el momento del pago (ej. "SAVE20", "FREESHIP")
   - **Nombre/Descripción** — Descripción interna para su referencia
   - **Tipo de Descuento** — Elija cómo se aplica el descuento
   - **Valor del Descuento** — La cantidad o porcentaje de descuento
3. Configure las reglas de uso:
   - **Límite de Uso** — Máximo total de redimidos (0 = ilimitado)
   - **Límite por Cliente** — Máximo de usos por cliente
   - **Valor Mínimo del Pedido** — Valor mínimo del carrito requerido
4. Establezca el **alcance**:
   - **Todo el Carrito** — El descuento se aplica al pedido completo
   - **Productos Específicos** — Solo se aplica a artículos seleccionados
   - **Categorías Específicas** — Solo se aplica a artículos en categorías seleccionadas
5. Opcionalmente establezca la fecha de vencimiento:
   - **Fecha de Vencimiento** — Cuando el cupón deja de funcionar
6. Haga clic en **Guardar**

## Tipos de Cupón

| Tipo | Descripción | Ejemplo |
|------|-------------|---------|
| **Monto Fijo** | Deduce un monto fijo en dólares | $20 de descuento en el pedido |
| **Porcentaje** | Deduce un porcentaje del total | 15% de descuento en el pedido |
| **Envío Gratis** | Elimina los cargos de envío | Envío gratis en cualquier pedido |

## Administrar Cupones

### Tarjetas de Cupones

Cada tarjeta de cupón muestra:
- **Código** — El código del cupón en negrita
- **Descripción** — Qué hace el cupón
- **Etiqueta de Estado** — Activo o Inactivo
- **Detalles del Descuento** — Tipo y valor (ej. "$ 20.00" o "15.00%")
- **Alcance** — Si se aplica a todo el carrito o a artículos específicos
- **Contador de Uso** — Cuántas veces se ha redimido el cupón
- **Fecha de Creación** — Cuando se creó el cupón
- **Vencimiento** — Fecha de vencimiento o "Sin vencimiento"

### Acciones de Cupón

Cada tarjeta tiene botones de acción:
- **Editar** — Modificar la configuración del cupón
- **Ver Historial** — Ver el historial de redimidos
- **Eliminar** — Eliminar el cupón

### Filtros de Cupones

Use la barra de filtro para encontrar cupones específicos:
- **Buscar** — Buscar por código, nombre o descripción
- **Tipo** — Monto Fijo, Porcentaje o Envío Gratis
- **Estado** — Activo o Inactivo
- **Alcance** — Todo el Carrito o productos específicos

## Generación Masiva de Cupones

Para campañas grandes, puede generar cupones en masa:
1. El sistema genera automáticamente códigos únicos (ej. "COUPONX1600406498")
2. Establezca parámetros comunes para todos los cupones generados
3. Distribuya los códigos por correo electrónico, redes sociales o impresión

## Experiencia del Cliente

Cuando un cliente tiene un código de cupón:
1. Ellos proceden al **pago**
2. Ingresan el código en el campo de **código de descuento**
3. El descuento se aplica inmediatamente si el cupón es válido
4. La resumen del pedido se actualiza para mostrar el descuento

Si un cupón es inválido (vencido, límite de uso alcanzado, valor mínimo no alcanzado), el cliente ve un mensaje de error claro.

## Consejos

- Use códigos memorables para campañas de marketing (ej. "SUMMER20" en lugar de cadenas aleatorias).
- Establezca límites por cliente para prevenir el abuso de descuentos valiosos.
- Use valores mínimos de pedido para mantener la rentabilidad (ej. "$10 de descuento en pedidos superiores a $50").
- Monitorea el contador de redimidos en el panel para seguir la efectividad de la campaña.
- Crea cupones con vencimiento limitado para generar urgencia (ej. "Válido solo este fin de semana").
- Usa el estado Activo/Inactivo para pausar cupones sin eliminarlos.
