---
title: Crear programas de afiliados
---

Los programas de afiliados definen cómo tus socios ganan comisiones cuando refieren clientes a tu tienda. Cada programa tiene su propia estructura de comisiones, reglas de seguimiento y umbrales de pago. Puedes crear múltiples programas para servir a diferentes segmentos de afiliados — como influencers, creadores de contenido o socios de referidos en masa.

![Lista de programas](/static/core/admin/img/help/creating-affiliate-programs/programs-list.webp)

## Componentes del programa

Cada programa de afiliados consta de:

- **Nombre y descripción** — Identificar el programa y explicarlo a los afiliados
- **Estructura de comisiones** — Cuánto ganan los afiliados por venta (porcentaje o monto fijo)
- **Duración de la cookie** — Cuánto tiempo dura el seguimiento de referidos después de un clic (1-365 días)
- **Aprobación automática** — Si los nuevos afiliados se unen automáticamente o requieren revisión manual
- **Umbral mínimo de pago** — Cuánto deben ganar los afiliados antes de solicitar un pago
- **Estado** — Activo, pausado o archivado

## Tipos de comisión

Elige entre dos modelos de comisión al crear tu programa:

| Tipo | Cómo funciona | Cuándo usarlo | Cálculo de ejemplo |
|------|-------------|-------------|---------------------|
| **Porcentaje** | El afiliado gana un porcentaje del subtotal del pedido | Recompensas escalables que crecen con el valor del pedido | 10% de un pedido de $150 = $15 de comisión |
| **Monto fijo** | El afiliado gana un monto fijo por venta | Costos predecibles; ideal para productos de alto volumen y baja margen | $25 por venta independientemente del valor del pedido |

Las comisiones por **porcentaje** se escalan naturalmente — los afiliados ganan más cuando refieren clientes de alto valor. Esto alinea sus incentivos con los tuyos y es el modelo más común (normalmente 5–15%).

Las comisiones **fijas** funcionan bien para servicios, suscripciones o programas de referidos en masa donde deseas costos por venta predecibles. Son fáciles de entender y presupuestar, pero pueden subcompensar a los afiliados que atraen pedidos grandes.

## Crear un programa

Navega a **Marketing > Programas de afiliados** y haz clic en **+ Agregar programa**.

### Configuración paso a paso

1. **Nombre del programa**
   Ingresa un nombre descriptivo visible para los afiliados (por ejemplo, "Programa de socios" o "Nivel de influencer").

2. **Slug**
   Un identificador amigable para URLs, generado automáticamente a partir del nombre. Se usa en URLs y referencias internas. Puedes personalizarlo si es necesario.

3. **Descripción**
   Texto opcional que explica los beneficios y términos del programa. Los afiliados ven esto cuando revisan los programas a los que pueden unirse.

4. **Tipo de comisión**
   Selecciona **Porcentaje** o **Monto fijo**.

5. **Valor de comisión**
   - Para porcentaje: Ingresa un valor entre 0 y 100 (por ejemplo, `10` para 10%)
   - Para monto fijo: Ingresa el monto en dólares por venta (por ejemplo, `25.00` para $25)

6. **Días de duración de la cookie**
   Cuántos días dura la cookie de seguimiento (1–365). Consulta la sección siguiente para obtener orientación.

7. **Aprobación automática de afiliados**
   - **Marcado** — Los nuevos afiliados se unen automáticamente
   - **No marcado** — Revisas manualmente y apruebas cada solicitud

8. **Pago mínimo**
   El monto mínimo que un afiliado debe acumular antes de solicitar un pago (por ejemplo, `50.00` para $50).

9. **Estado**
   Establece a **Activo** para aceptar nuevos afiliados y seguir las referencias.

10. **Guardar** el programa.

## Explicación de la duración de la cookie

La duración de la cookie determina cuánto tiempo Spwig recuerda que un cliente clickeó en un enlace de referido de un afiliado.

### Cómo funciona

1. Un cliente clickea en el enlace de un afiliado
2. Spwig establece una cookie de seguimiento en el navegador del cliente
3. Si el cliente completa una compra **dentro del período de duración de la cookie**, el pedido se atribuye al afiliado
4. Si la cookie expira antes de la compra, el afiliado no gana comisión

### Elegir una duración

| Duración | Caso de uso | Escenario típico |
|----------|-------------|------------------|
| **1–7 días** | Compras impulsivas, ofertas flash | Productos de consumo masivo, ofertas limitadas |
| **30 días** | E-commerce estándar | Retail en línea general, recomendación por defecto |
| **60–90 días** | Compras consideradas | Artículos de alto costo, B2B, servicios |
| **180+ días** | Ciclos de ventas largos | Software empresarial, suscripciones, artículos de lujo |

**El estándar de la industria es 30 días.** Esto equilibra la atribución justa para los afiliados con límites prácticos de seguimiento. Las duraciones más cortas favorecen a los clientes que se convierten rápidamente; duraciones más largas dan a los clientes tiempo para investigar y regresar para completar su compra.

### Nota técnica

La duración de la cookie solo afecta la **atribución**. Las comisiones aprobadas permanecen válidas indefinidamente — la duración de la cookie solo determina si un pedido se atribuye al afiliado en primer lugar.

## Configuración de aprobación automática

La configuración de aprobación automática controla si las nuevas solicitudes de afiliados requieren revisión manual.

### Cuándo habilitar la aprobación automática

- **Programas públicos** — Deseas crecer tu base de afiliados rápidamente sin cuellos de botella
- **Productos de bajo riesgo** — El fraude o el riesgo de marca es mínimo
- **Programas de alto volumen** — Esperas muchas solicitudes y no puedes revisar cada una manualmente

### Cuándo requerir revisión manual

- **Programas por invitación** — Solo aceptas socios previamente evaluados
- **Programas premium** — Altas tasas de comisión o beneficios exclusivos
- **Productos sensibles a la marca** — Necesitas asegurarte de que los afiliados se alineen con los valores de tu marca
- **Prevención de fraude** — Deseas filtrar cuentas sospechosas

### Consideraciones de seguridad

Revisar manualmente los afiliados ayuda a prevenir:
- Esquemas de autoreferido (afiliados creando cuentas falsas para ganar comisiones)
- Violaciones de marcas (afiliados pujando por términos de tu marca en búsqueda pagada)
- Desalineación de marca (afiliados promoviendo tus productos en contextos inapropiados)

Para la mayoría de las tiendas, comenzar con **aprobación manual** es más seguro. Siempre puedes habilitar la aprobación automática más tarde una vez que hayas establecido patrones de confianza.

## Umbral mínimo de pago

El umbral mínimo de pago evita la sobrecarga administrativa de procesar muchos pagos pequeños.

### ¿Por qué establecer un mínimo?

- **Reduce las tarifas de transacción** — Los procesadores de pago cobran por transacción, por lo tanto, agrupar pagos ahorra dinero
- **Simplifica la contabilidad** — Menos eventos de pago significan menos trabajo de reconciliación
- **Estándar de la industria** — La mayoría de los programas de afiliados tienen mínimos ($25–$100)

### Umbrales típicos

| Umbral | Caso de uso |
|-----------|----------|
| **$25–$50** | Programas de alto volumen donde los afiliados alcanzan el mínimo rápidamente |
| **$50–$100** | Umbral estándar para la mayoría de los programas |
| **$100–$200** | Programas premium o pagos internacionales con altas tarifas de procesamiento |

### Equilibrando la satisfacción del afiliado

Establecer el umbral **muy alto** frustra a los afiliados que pueden esperar meses para recibir su primer pago. Establecerlo **muy bajo** crea una carga administrativa y afecta tus márgenes con tarifas.

**Recomendación:** Comienza en $50. Esto es lo suficientemente bajo para que los afiliados activos lo alcancen dentro de sus primeras pocas ventas, pero lo suficientemente alto para agrupar los pagos de manera eficiente.

### Sin máximo

No hay un límite máximo — los afiliados pueden acumular ganancias indefinidamente antes de solicitar un pago. Algunos afiliados prefieren agrupar sus solicitudes trimestral o anualmente para planificación fiscal.

## Gestión del estado del programa

Los programas pueden estar en uno de tres estados:

| Estado | Descripción | Comportamiento |
|--------|-------------|----------|
| **Activo** | El programa está en ejecución | Acepta nuevos afiliados, sigue referidos, calcula comisiones |
| **Pausado** | Deshabilitado temporalmente | Los afiliados existentes permanecen pero no hay nuevos registros; las cookies de referidos existentes aún funcionan |
| **Archivado** | Cerrado permanentemente | Sin nuevos afiliados, sin nuevos referidos seguidos; los datos históricos se preservan para informes |

### Cuándo pausar un programa

- Estás revisando tasas de comisión o términos
- Estás sobrecostando los pagos a afiliados este trimestre
- Estás probando una nueva estructura de programa y deseas evitar que nuevos afiliados se unan al antiguo

Los programas pausados aún honran las cookies de seguimiento existentes y las comisiones pendientes — solo estás evitando que nuevos afiliados se unan.

### Cuándo archivar un programa

- Has reemplazado el programa con una nueva estructura
- El programa tenía un límite de tiempo (por ejemplo, campaña estacional)
- Estás consolidando múltiples programas en uno

Los programas archivados permanecen en la base de datos para informes históricos, pero se eliminan de las vistas de gestión activa.

## Ejemplos de programas

### Ejemplo 1: Programa de influencer (porcentaje)

| Campo | Valor |
|-------|-------|
| Nombre | Programa de influencer |
| Tipo de comisión | Porcentaje |
| Valor de comisión | 10 |
| Días de duración de la cookie | 30 |
| Aprobación automática | No marcado (revisión manual) |
| Umbral mínimo de pago | 50.00 |
| Estado | Activo |

**Caso de uso:** Reclutar influencers de redes sociales y creadores de contenido. La comisión del 10% se escala con el valor del pedido, recompensando a los afiliados que atraen clientes de alto gasto. La aprobación manual asegura que evalúes la audiencia y alineación de marca de cada influencer.

### Ejemplo 2: Programa de referidos en masa (monto fijo)

| Campo | Valor |
|-------|-------|
| Nombre | Programa de socios de referidos |
| Tipo de comisión | Monto fijo |
| Valor de comisión | 25.00 |
| Días de duración de la cookie | 7 |
| Aprobación automática | Marcado |
| Umbral mínimo de pago | 100.00 |
| Estado | Activo |

**Caso de uso:** Asociarse con sitios de ofertas, agregadores de cupones y redes de referidos que generan alto volumen. La comisión fija de $25 mantiene los costos predecibles, y la corta duración de la cookie (7 días) se enfoca en convertidores rápidos. Se habilita la aprobación automática ya que estos socios suelen autogestionarse.

### Ejemplo 3: Socio premium (alto porcentaje)

| Campo | Valor |
|-------|-------|
| Nombre | Nivel de socio premium |
| Tipo de comisión | Porcentaje |
| Valor de comisión | 15 |
| Días de duración de la cookie | 90 |
| Aprobación automática | No marcado |
| Umbral mínimo de pago | 200.00 |
| Estado | Activo |

**Caso de uso:** Programa exclusivo para afiliados de alto rendimiento o socios estratégicos. Mayor comisión (15%) recompensa su tráfico de calidad, y la duración de la cookie de 90 días acomoda ciclos de consideración más largos. Aprobación manual solo — este es un nivel por invitación.

## Consejos

- Comienza con una **comisión por porcentaje** (5–15%) para la mayoría de los programas — es más fácil explicársela a los afiliados y se escala naturalmente con el valor del pedido.
- Usa **30 días de duración de la cookie** como punto de partida — es el estándar de la industria y equilibra la atribución justa con límites prácticos de seguimiento.
- Habilita **aprobación manual** inicialmente para evaluar a los afiliados, luego cambia a aprobación automática una vez que hayas establecido patrones de confianza y controles contra el fraude.
- Establece tu **umbral mínimo de pago** en $50–$100 para equilibrar la satisfacción del afiliado (no demasiado alto para alcanzar) con la eficiencia administrativa (no demasiados pagos pequeños).
- Crea **programas separados** para diferentes segmentos de afiliados (influencers, sitios de contenido, agregadores de ofertas) para que puedas seguir el rendimiento y ajustar las comisiones de forma independiente.
- Monitorea regularmente el **tablero de análisis** para identificar a los afiliados de alto rendimiento y ajustar las tasas de comisión para retener a los socios principales.