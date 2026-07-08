---
title: Restricciones de cupón
---

Las restricciones de cupón controlan quién puede usar un cupón, cuándo y con qué frecuencia. Configure estas opciones al crear o editar un cupón en **Marketing > Cupones**.

![Reglas de restricción](/static/core/admin/img/help/voucher-restrictions/restriction-rules.webp)

## Límites de uso

Establezca límites globales y por cliente en la sección **Límites de uso** del formulario del cupón.

- **Máximo de usos total** — El número máximo de veces que este cupón puede canjearse entre todos los clientes. Deje vacío para ilimitado.
- **Máximo de usos por cliente** — Cuántas veces un solo cliente puede usar este cupón. Establezca en 1 para la mayoría de las campañas.

| Patrón | Máximo total | Por cliente | Caso de uso |
|---------|-----------|--------------|----------|
| Campaña limitada | 100 | 1 | "Primeros 100 clientes" escasez |
| Código compartido ilimitado | (vacío) | 1 | Código de marketing continuo |
| Uso múltiple ilimitado | (vacío) | (vacío) | Descuento interno/para personal |
| Códigos únicos de uso único | 1 | 1 | Códigos generados en masa para campañas |

## Valor mínimo del pedido

El campo **Valor mínimo del pedido** protege sus márgenes al requerir un total de carrito antes de que se aplique el cupón. Por ejemplo, "$10 de descuento en pedidos superiores a $50" asegura que nunca descuente un pedido pequeño hasta un punto no rentable.

| Descuento | Valor mínimo sugerido | Proporción |
|----------|-------------------|-------|
| $5 de descuento | $30+ | ~6:1 |
| $10 de descuento | $50+ | ~5:1 |
| $20 de descuento | $100+ | ~5:1 |
| 15% de descuento | $40+ | Depende del catálogo |

## Límite de descuento (Monto máximo de descuento)

El campo **Monto máximo de descuento** en **Configuración del descuento** limita cuánto puede deducir un cupón de porcentaje. Esto solo se aplica a cupones de tipo porcentaje y evita descuentos descontrolados en carritos de alto valor.

Ejemplo: "20% de descuento, máximo $50 de descuento"
- Carrito de $200 = $40 de descuento (20%)
- Carrito de $300 = $50 de descuento (limitado)
- Carrito de $1,000 = aún $50 de descuento (limitado)

Agregue un límite de descuento en cualquier cupón de porcentaje que comparta públicamente.

## Reglas de combinación

El conjunto de campos **Restricciones y reglas** (haga clic para expandir) contiene casillas de verificación que controlan cómo interactúan los cupones con otros descuentos.

| Configuración | Qué hace | Cuándo habilitar |
|---------|--------------|----------------|
| **Excluir artículos en oferta** | El cupón salta los productos ya en oferta | La mayoría de las campañas — protege los márgenes de oferta |
| **No se puede combinar con otros cupones** | Solo un cupón por pedido | Valor predeterminado para la mayoría de los cupones |
| **No se puede combinar con artículos en oferta** | Bloquea el cupón si el carrito tiene CUALQUIER artículo en oferta | Campañas estrictas donde el cupón reemplaza el precio de oferta |
| **Solo para clientes nuevos** | Solo clientes con cero pedidos anteriores | Campañas de bienvenida/adquisición |

## Restricciones de cliente

Para un objetivo simple, marque **Solo para clientes nuevos** en el conjunto de campos **Restricciones y reglas**.

Para un objetivo avanzado, use la tabla **Restricciones del cupón** en la parte inferior del formulario. Haga clic en **+ Agregar otra restricción del cupón** para agregar filas. Cada restricción tiene tres campos:

- **Tipo** — Categoría de restricción (menú desplegable)
- **Valor** — Valor coincidente (separado por comas o JSON)
- **Es inclusivo** — Marcado = el cliente debe coincidir; no marcado = el cliente no debe coincidir

| Tipo | Valor | Inclusivo | Efecto |
|------|-------|-----------|--------|
| user_email_domain | @company.com | Sí | Solo empleados de la empresa pueden usarlo |
| shipping_country | US,CA | Sí | Solo clientes de EE. UU. y Canadá |
| shipping_country | RU | No | Todos EXCEPTO Rusia |
| day_of_week | monday,tuesday | Sí | Solo válido en lunes y martes |
| payment_method | stripe | Sí | Solo para pagos con Stripe |

Combine varias filas para restricciones en capas. Todos los límites inclusivos deben coincidir, y ningún límite exclusivo puede coincidir, para que se aplique el cupón.

## Estrategias de vencimiento

Controle cuándo vence un cupón usando los campos de fecha y validez.

- **Fecha de finalización** — Fecha de corte estricta (por ejemplo, 31 de diciembre de 2026).

El cupón deja de funcionar a medianoche.
- **Días válidos** — Validez móvil desde la creación o primer uso del cupón.

Sobrescribe la fecha de finalización cuando se establece.


Útil para códigos de bienvenida: "válido durante 30 días a partir de su recepción".

| Estrategia | Fecha de finalización | Días válidos | Caso de uso |
|----------|----------|------------|----------|
| Plazo fijo | Establecido | (vacío) | Campañas estacionales, eventos |
| Ventana deslizante | (vacío) | 30 | Códigos de bienvenida, cupones de recompensa |
| Sin vencimiento | (vacío) | (vacío) | Códigos continuos, descuentos para el personal |

## Prevención del abuso

Siga esta lista de verificación para mantener sus cupones seguros:

- Siempre establezca **Máximo de usos por cliente** en 1, a menos que haya una razón específica para no hacerlo.
- Establezca **Valor mínimo del pedido** en todos los cupones de monto fijo.
- Agregue un **Monto máximo de descuento** en los cupones de porcentaje públicos.
- Use códigos difíciles de adivinar para cupones de alto valor — evite códigos obvios como "DISCOUNT50".
- Monitorea el análisis de uso en cada tarjeta de cupón en el panel de control.
- Desactive inmediatamente un cupón si observa patrones inusuales de redención.
- Para campañas de alto valor, use códigos únicos generados en masa en lugar de un solo código compartido.

## Consejos

- Comience con restricciones e afloje los límites si la redención es demasiado baja — es más fácil relajar las reglas que ajustarlas después de que los códigos estén en circulación.
- Pruebe cada cupón con un checkout real antes de distribuirlo a los clientes.
- Revise regularmente el panel de análisis de cupones para detectar problemas a tiempo.
- Combine varias restricciones para una protección en capas — por ejemplo, límite por cliente + valor mínimo del pedido + límite de descuento + excluir artículos en oferta.