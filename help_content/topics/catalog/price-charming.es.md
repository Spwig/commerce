---
title: Reglas de precios atractivos
---

El precio atractivo (también llamado precios psicológicos) ajusta automáticamente los precios de tus productos para que terminen en dígitos específicos que resulten más atractivos para los clientes. Por ejemplo, en lugar de mostrar un precio de $20.00, el precio atractivo puede mostrar $19.99 — una técnica ampliamente utilizada que hace que los precios parezcan más bajos a simple vista.

Spwig aplica las reglas de precios atractivos automáticamente en toda tu tienda, por moneda, por lo que solo necesitas configurar cada regla una vez.

## Cómo funciona el precio atractivo

Cuando se calcula el precio de un producto (incluyendo después de promociones o descuentos), Spwig verifica si existe una regla activa de precios atractivos para esa moneda. Si existe, el precio se ajusta antes de mostrarse a los clientes. El ajuste se aplica a precios por encima del umbral mínimo que hayas elegido.

Puedes configurar reglas separadas para cada moneda que acepte tu tienda. Por ejemplo, podrías usar terminaciones `.99` para USD, pero redondear al múltiplo más cercano de `¥10` para JPY.

## Crear una regla de precios atractivos

1. Navega a **Catálogo > Reglas de precios atractivos**
2. Haz clic en **+ Añadir regla de precios atractivos**
3. Selecciona la **Moneda** a la que se aplica esta regla (por ejemplo, `USD`, `EUR`, `NZD`)
4. Elige un **Tipo de regla** (ver la tabla a continuación)
5. Opcionalmente, establece un **Umbral de precio mínimo** para excluir precios muy bajos
6. Marca **Aplicar a precios de venta** si también deseas que se aplique el precio atractivo cuando los artículos estén en oferta
7. Asegúrate de que **Activo** esté marcado
8. Haz clic en **Guardar**

Solo puede existir una regla por moneda. Si necesitas cambiar una regla, edita la existente.

## Tipos de reglas

| Tipo de regla | Ejemplo | Mejor para |
|---------------|---------|------------|
| **Atracción con terminación .99** | $20.50 → $19.99 | La mayoría de los productos de retail — el clásico precio psicológico |
| **Atracción con terminación .95** | $20.50 → $19.95 | Alternativa ligeramente más suave a .99 |
| **Atracción con terminación .90** | $20.50 → $19.90 | Redondeo que da sensación de redondeo pero aún está por debajo del siguiente dólar |
| **Redondear hacia abajo** | $19.50 → $19.00 | Tiendas que prefieren números enteros |
| **Redondear hacia arriba** | $19.50 → $20.00 | Redondeo ligeramente hacia arriba para una visualización limpia |
| **Redondear al múltiplo más cercano de 5** | $23.00 → $25.00 | Retail de alto tráfico y mercados |
| **Redondear al múltiplo más cercano de 10** | $23.00 → $20.00 | Artículos de mayor precio, como electrodomésticos |
| **Redondear al múltiplo más cercano de 100** | $1,234 → $1,200 | Artículos de alto valor, como muebles o electrónicos |
| **Terminación personalizada** | Cualquier — especifique a continuación | Cuando su marca utilice una terminación específica, como `.88` |

### Terminaciones personalizadas

Si elige **Terminación personalizada**, ingrese el valor de la terminación en el campo **Terminación personalizada**. Por ejemplo, ingrese `0.88` para que todos los precios terminen en `.88` (común en algunos mercados asiáticos).

## Umbral de precio mínimo

Use el campo **Umbral de precio mínimo** para omitir el ajuste de precios atractivos para artículos con precios muy bajos donde el ajuste parecería extraño. Por ejemplo, al establecer un umbral de `5.00`, los productos con un precio inferior a $5 se mostrarán con su precio calculado real sin aplicar el ajuste de precios atractivos.

Deje el valor en `0` para aplicar el ajuste de precios atractivos a todos los precios.

## Precios de venta

Por defecto, el ajuste de precios atractivos se aplica tanto a precios regulares como a precios de venta. Si desea que los precios de venta muestren sus valores calculados exactos (útil para precios promocionales limitados en el tiempo donde las cifras exactas importan), desmarque **Aplicar a precios de venta**.

## Desactivar una regla

Para detener temporalmente el ajuste de precios atractivos sin eliminar la regla, desmarque **Activo** y guarde. La regla se conserva y puede reactivarse en cualquier momento.

## Consejos

Conservar todo el formato markdown, rutas de imágenes, bloques de código y términos técnicos.

- Comienza con terminaciones en .99 si no estás seguro — es la técnica de precios psicológicos más reconocida y funciona bien en la mayoría de los tipos de productos.
- Establece un umbral mínimo si vendes artículos de bajo costo (menos de $5) para que un artículo de $3.50 no se reduzca a $2.99.
- Verifica tus precios después de habilitar una nueva regla viendo un producto en el punto de venta — los precios encantados se muestran en tiempo real.
- El Yen Japonés y monedas similares con números enteros funcionan mejor con **Redondear al múltiplo más cercano de 10** o **Redondear al múltiplo más cercano de 100**, ya que los finales decimales parecen inusuales.
- El encantamiento de precios se aplica después de todos los descuentos y promociones, por lo tanto, tus precios de venta también aparecerán encantados a menos que desactive **Aplicar a precios de venta**.
- Puedes tener tipos de reglas diferentes para diferentes monedas, lo cual es útil si vendes a múltiples mercados con convenciones de precios diferentes.