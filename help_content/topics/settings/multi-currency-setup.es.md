---
title: Configuración de múltiples monedas
---

La opción de múltiples monedas permite a tus clientes navegar por los productos y completar el proceso de pago en su moneda preferida. Los precios se convierten automáticamente desde tu moneda base utilizando tipos de cambio de un proveedor conectado o tasas definidas manualmente.

## Antes de comenzar

Antes de habilitar la opción de múltiples monedas, necesitas:

1. **Un proveedor de tasas de cambio activo** - Ve a **Configuración > Pestaña de múltiples monedas > Panel de tasas de cambio** y conecta al menos un proveedor (como Open Exchange Rates, Fixer.io o ExchangeRate-API). El proveedor debe estar activo y sincronizando tasas.
2. **Al menos dos monedas** - Tu moneda base más una o más monedas adicionales que desees admitir.

## Habilitar múltiples monedas

Navega a **Configuración > Múltiples monedas** y activa **Habilitar múltiples monedas**. Una vez habilitado, configura las siguientes opciones:

| Configuración | Descripción |
|---------|-------------|
| **Modo de selección de moneda** | Cómo los clientes eligen su moneda. *Automático* detecta desde su ubicación, *Manual* les permite elegir desde un conmutador, *Ambos* combina los dos enfoques. |
| **Mostrar selector de moneda** | Muestra un selector de moneda en tu tienda en línea para que los clientes puedan cambiar la moneda manualmente. |
| **Posición del selector** | Dónde aparece el selector de moneda (encabezado, pie de página o barra lateral). |
| **Mostrar información de tipo de cambio** | Muestra una notificación a los clientes indicando que los precios son conversiones aproximadas desde tu moneda base. |
| **Habilitar formato local** | Formatea números y símbolos de moneda según la localización de cada cliente (por ejemplo, 1.234,56 para formatos europeos). |

## Modo de pago

Elige cómo funciona la opción de múltiples monedas durante el pago:

| Modo | Descripción |
|------|-------------|
| **Múltiples monedas completo** | Los clientes navegan, agregan al carrito y pagan en su moneda seleccionada. El tipo de cambio se bloquea en el momento del pago y se registra con el pedido. Este es el modo predeterminado. |
| **Solo visualización** | Los precios se muestran en la moneda del cliente para comodidad, pero el carrito y el pago siempre se procesan en tu moneda base. En el momento del pago, los clientes ven una notificación que muestra el monto aproximado convertido junto con el monto real en tu moneda base. |

**Solo visualización** es útil cuando tu proveedor de pago solo admite tu moneda base, o cuando deseas evitar por completo el riesgo de tipo de cambio. Los clientes aún ven precios localizados mientras navegan, dándoles una idea del costo en su propia moneda.

## Intervalo de sincronización de tasas de cambio

Controla con qué frecuencia tu tienda obtiene tasas recientes desde tu proveedor conectado:

| Intervalo | Descripción |
|----------|-------------|
| **En tiempo real** | Cada 15 minutos. Ideal para tiendas con ventas internacionales de alto volumen. |
| **Cada hora** | Una vez por hora. Buena combinación de frescura y uso de API. |
| **Diario** | Una vez al día. Adecuado para la mayoría de las tiendas. Este es el predeterminado. |
| **Semanal** | Una vez por semana. Para tiendas con precios estables. |
| **Mensual / Trimestral** | Actualizaciones menos frecuentes para tiendas que rara vez cambian tasas. |
| **Solo manual** | Las tasas nunca se obtienen automáticamente. Tú gestionas todas las tasas manualmente. |

El intervalo de sincronización afecta con qué frecuencia la tarea en segundo plano obtiene tasas desde tu proveedor. Entre sincronizaciones, se usan tasas almacenadas en caché. Si necesitas forzar una sincronización inmediata, usa el botón **Sincronizar ahora** en el Panel de tasas de cambio o **Sincronizar desde el proveedor** en la página de tasas de cambio manuales.

## Tasas de cambio manuales

Las tasas de cambio manuales te permiten establecer tasas de conversión exactas para pares de monedas específicos. Tienen prioridad sobre las tasas obtenidas del proveedor, dándote un control total sobre los precios.

Navega a **Tasas de cambio > Tasas de cambio manuales** para gestionarlas.

### Establecer tasas manualmente

Haz clic en **Añadir tasa** para crear una tasa para un par de monedas. Especifica la moneda base, la moneda objetivo y la tasa. Por ejemplo, establecer USD/EUR en 0,92 significa que 1 USD = 0,92 EUR.

### Sincronizar desde un proveedor

Haz clic en **Sincronizar desde el proveedor** para poblar automáticamente las tasas manuales con las últimas tasas de tu proveedor conectado.

Esto crea tasas manuales para todas las monedas admitidas, dándote un punto de partida para afinarlas.

Las tasas bloqueadas se omiten durante la sincronización, por lo que cualquier tasa que hayas ajustado manualmente no se sobrescribirá.

### Bloquear tasas

Haz clic en el icono de bloqueo de cualquier tasa para evitar que se sobrescriba durante la sincronización del proveedor. Esto es útil cuando has negociado una tasa específica o deseas mantener una tasa fija independientemente de los movimientos del mercado.

- Las **tasas bloqueadas** muestran un distintivo de bloqueo y se excluyen de la sincronización automática.
- Las **tasas desbloqueadas** pueden actualizarse cuando hagas clic en Sincronizar desde el Proveedor.

### Comparación de proveedores

Cada tasa manual muestra la tasa actual del proveedor junto a ella, con una diferencia en porcentaje. Esto te ayuda a ver a simple vista cómo se comparan tus tasas manuales con las tasas del mercado:

- Un porcentaje **verde** significa que tu tasa es más alta que la tasa del proveedor.
- Un porcentaje **rojo** significa que tu tasa es más baja que la tasa del proveedor.

## Markup de tasas de cambio

Puedes agregar un porcentaje de markup a las tasas de cambio para cubrir los cargos por conversión de moneda y protegerte contra fluctuaciones de tasas entre el momento en que un cliente coloca un pedido y cuando recibes el pago.

Por ejemplo, un markup del 2% en una tasa de cambio de 1.18 USD/EUR la ajustaría aproximadamente a 1.20 USD/EUR. Este pequeño margen ayuda a asegurar que no pierdas dinero en conversiones de moneda.

## Estrategia de selección de tasas

Cuando tengas varios proveedores de tasas de cambio conectados, puedes elegir cómo se seleccionan las tasas:

- **Proveedor principal** - Siempre usa las tasas de tu proveedor principal designado. Esto garantiza un precio consistente en toda tu tienda. Si el proveedor principal no tiene datos para un par de monedas, se recurre a la última tasa disponible de cualquier proveedor.
- **Última disponible** - Usa la tasa más recientemente sincronizada de cualquier proveedor activo. Esto te da los datos más recientes, pero las tasas pueden variar ligeramente entre proveedores.

Para la mayoría de las tiendas, el **Proveedor principal** es la opción recomendada, ya que proporciona el precio más predecible.

## Monedas admitidas

Usa el administrador de monedas de arrastrar y soltar para elegir qué monedas admite tu tienda:

1. **Monedas disponibles** (columna izquierda) muestra todas las monedas que puedes habilitar.
2. **Monedas activas** (columna derecha) muestra las monedas actualmente habilitadas en tu tienda.
3. Arrastra monedas entre columnas para habilitar o deshabilitarlas.
4. Arrastra dentro de la columna Activa para reordenar cómo aparecen las monedas en el conmutador.
5. Haz clic en **Guardar configuración de monedas** para aplicar tus cambios.

Tu moneda base siempre está activa y no puede eliminarse.

## Cómo se resuelven las tasas de cambio

Cuando se necesita convertir un precio, el sistema verifica las tasas en este orden:

1. **Tasa de cambio manual** - Si existe una tasa manual activa para el par de monedas, siempre se usará primero.
2. **Tasa del proveedor** - Si no existe una tasa manual, se usará la última tasa de tu proveedor conectado.

Esto significa que puedes usar proveedores para la mayoría de las monedas y sobrescribir pares específicos con tasas manuales donde necesitas un control preciso.

## Importante: Esta configuración es permanente

Una vez que se habilita el multi-monedas y los clientes realizan pedidos en monedas extranjeras, esta configuración **no se puede deshabilitar**. Esto se debe a que:

- Los pedidos almacenan permanentemente la moneda elegida por el cliente y la tasa de cambio utilizada en el momento del pedido.
- Los informes financieros y los cálculos de reembolsos dependen de estos datos históricos de moneda.
- Deshabilitar el multi-monedas dejaría los pedidos existentes en un estado inconsistente.

Si no se han realizado pedidos en monedas extranjeras, aún puedes deshabilitar el multi-monedas.

## Consejos

Mantén todo el formato de markdown, rutas de imágenes, bloques de código y términos técnicos.

- **Prueba con un pedido pequeño primero** - Realiza un pedido de prueba en una moneda extranjera para verificar el flujo de pago y asegurarte de que se apliquen correctamente las tasas de cambio.
- **Monitorea las tasas de cambio regularmente** - Revisa periódicamente el Panel de tasas de cambio para asegurarte de que tu proveedor esté sincronizando las tasas y que estas parezcan razonables.
- **Considera un margen adicional para monedas volátiles** - Si ofreces monedas con alta volatilidad, un margen ligeramente más alto (2-3%) puede proteger tus márgenes.
- **Comienza con monedas principales** - Empieza con monedas ampliamente utilizadas (EUR, GBP, JPY, CAD, AUD) y expande según la demanda de los clientes.
- **Revisa la compatibilidad con los proveedores de pago** - No todos los proveedores de pago admiten todas las monedas.

Verifica la documentación de tu proveedor de pago para confirmar qué monedas procesan.
- **Usa el modo Solo visualización si no estás seguro** - Si no estás seguro de si tu proveedor de pago maneja el pago en múltiples monedas, comienza con el modo Solo visualización.

Puedes cambiar más tarde al modo Multi-moneda completo.
- **Bloquea las tasas antes de los períodos promocionales** - Si estás realizando una venta, bloquea tus tasas de cambio con anticipación para asegurar precios consistentes durante toda la promoción.