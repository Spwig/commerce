---
title: Rastreo de afiliados y enlaces
---

El rastreo de afiliados impulsa todo el sistema de comisiones conectando las compras de los clientes con los afiliados que los referieron. Esta guía explica cómo funcionan los enlaces de seguimiento, qué datos registra Spwig cuando los clientes hacen clic en esos enlaces y cómo el sistema de atribución basado en cookies determina qué afiliado gana cada comisión.

Entender los mecanismos de rastreo le ayuda a solucionar problemas de atribución, analizar el rendimiento de los enlaces y educar a sus afiliados sobre cómo maximizar sus conversiones.

## ¿Qué es un enlace de seguimiento?

Un enlace de seguimiento es una URL única que redirige a los clientes a su tienda mientras registra la identidad del afiliado en una cookie. Cada afiliado puede crear múltiples enlaces de seguimiento que apunten a diferentes destinos: la página de inicio, productos específicos, páginas de colecciones o páginas de aterrizaje.

Formato de ejemplo de enlace de seguimiento:
```
https://yourstore.com/affiliate/track/a2b7f8c4d1e9/
```

Este enlace redirige al destino mientras establece una cookie de seguimiento que asocia futuras compras con el afiliado que posee el código de enlace `a2b7f8c4d1e9`.

Los afiliados generan estos enlaces desde su panel de control. Copian la URL completa y la comparten en publicaciones de blog, redes sociales, correos electrónicos o cualquier canal donde lleguen a clientes potenciales.

## Componentes de los enlaces de seguimiento

Cada enlace de seguimiento contiene estos elementos:

| Componente | Ejemplo | Descripción |
|-----------|---------|-------------|
| **URL base** | `https://yourstore.com` | Dominio de su tienda |
| **Ruta de seguimiento** | `/affiliate/track/` | Punto final de seguimiento de Spwig |
| **Código de enlace** | `a2b7f8c4d1e9` | Identificador único de 12 caracteres generado automáticamente |
| **Destino** | Establecido cuando se crea el enlace | Donde el cliente aterriza después de la redirección (página de inicio, producto, etc.) |

Cuando un afiliado crea un enlace, Spwig genera automáticamente el código único de 12 caracteres. El afiliado nunca necesita crear o editar manualmente este código: simplemente eligen el destino y Spwig maneja el resto.

### Etiquetas de enlace (opcional)

Los afiliados pueden agregar una etiqueta a cada enlace para su propia organización:
- "Enlace de biografía de Instagram"
- "Descripción de YouTube"
- "Campaña de correo electrónico de Black Friday"

Las etiquetas ayudan a los afiliados a rastrear qué canales promocionales funcionan mejor. Solo son visibles para el afiliado y usted: los clientes nunca ven la etiqueta.

## ¿Cómo funciona el rastreo?

El proceso de rastreo y atribución sigue cinco pasos desde el clic hasta la comisión:

### 1. Cliente hace clic en el enlace

Un cliente potencial hace clic en el enlace de seguimiento del afiliado desde cualquier canal promocional (publicación de redes sociales, artículo de blog, boletín de noticias por correo electrónico).

### 2. Clic registrado

El punto final de seguimiento de Spwig registra los detalles del clic:
- Dirección IP
- User agent (navegador y dispositivo)
- HTTP referrer (de dónde vino el clic)
- Marca de tiempo
- Identificador de sesión

Estos datos aparecen en el **Clics** del panel de administración en **Afiliados > Clics** para análisis y detección de fraude.

### 3. Cookie establecida

El sistema de seguimiento establece una cookie en el navegador del cliente antes de redirigirlo. La cookie contiene:
- ID del afiliado (quién debe ganar la comisión)
- ID del programa (qué estructura de comisión aplica)
- Código de enlace (qué enlace específico se hizo clic)

### 4. Cliente realiza una compra

El cliente navega por su tienda y completa una compra. Esto puede ocurrir inmediatamente o días/semanas después, siempre que realice la compra dentro del período de vida útil de la cookie.

### 5. Comisión creada

En la caja de pago, Spwig verifica la cookie del afiliado. Si se encuentra y aún es válida (dentro del período de vida útil de la cookie), el sistema crea un registro de comisión con estado **Pendiente** vinculado al afiliado, programa y pedido.

## Atribución basada en cookies

La cookie de seguimiento es el mecanismo central que vincula las compras a los afiliados. Entender cómo funcionan las cookies le ayuda a establecer ventanas de atribución óptimas y solucionar problemas de seguimiento.

### Estructura de la cookie

| Propiedad | Valor |
|----------|-------|
| **Nombre** | `aff_{program_id}` (por ejemplo, `aff_7` para el ID de programa 7) |
| **Valor** | JSON que contiene el ID del afiliado, código de enlace, marca de tiempo |
| **Dominio** | Dominio de su tienda |
| **Ruta** | `/` (acceso a toda la web) |
| **Duración** | Vida útil de la cookie del programa (1–365 días) |
| **HttpOnly** | `true` (evita el acceso de JavaScript para seguridad) |
| **SameSite** | `Lax` (permite el seguimiento desde referidos externos) |
| **Secure** | `true` en sitios HTTPS (recomendado) |

### Ventana de vida útil de la cookie

La vida útil de la cookie determina cuánto tiempo tienen los clientes para realizar una compra después de hacer clic en un enlace de afiliado. Esta ventana se establece por programa en **Marketing > Programas de afiliados** cuando crea o edita un programa.

Ventanas de vida útil de cookies estándar de la industria:
- **7 días**: Productos de decisión rápida (comestibles, entradas a eventos)
- **30 días**: E-commerce estándar (la configuración más común)
- **60–90 días**: Compras consideradas (muebles, electrónicos, productos B2B)
- **365 días**: Ciclos de ventas largos (bienes de lujo, servicios de alto costo)

Si un cliente hace clic en un enlace de afiliado el 1 de enero y su vida útil de la cookie es de 30 días, cualquier compra que realice hasta el 30 de enero le creditará a ese afiliado. Las compras el 31 de enero o posterior no generan comisión porque la cookie expiró.

### Modelo de atribución por último clic

Spwig utiliza **atribución por último clic**: el enlace más reciente gana. Así es como funciona:

**Escenario**: Un cliente hace clic en el enlace del afiliado A el lunes, luego en el enlace del afiliado B el miércoles y luego realiza una compra el viernes.

**Resultado**: El afiliado B gana la comisión porque su enlace fue el clic más reciente.

La cookie del último clic sobrescribe las cookies de afiliados anteriores. Este modelo es fácil de entender y evita comisiones dobles, aunque eso significa que solo un afiliado recibe crédito por pedido (el último antes de la compra).

## Registro de clics

Spwig registra cada clic en cada enlace de afiliado para proporcionar análisis tanto para usted como para el afiliado. Los datos de clic ayudan a medir el rendimiento de los enlaces, detectar fraude y optimizar estrategias promocionales.

### Datos capturados por clic

Navegue a **Afiliados > Clics** para ver todos los clics registrados. Cada entrada contiene:

| Campo | Descripción |
|-------|-------------|
| **Enlace** | ¿Qué enlace de seguimiento se hizo clic? |
| **Afiliado** | ¿Quién creó el enlace? |
| **Dirección IP** | IP del cliente (para detección de fraude) |
| **User Agent** | Información del navegador y dispositivo |
| **Referrer** | La página donde el cliente hizo clic en el enlace (por ejemplo, "https://instagram.com") |
| **ID de sesión** | Identificador único para esta sesión de navegación |
| **Marca de tiempo** | Fecha y hora exactas del clic |

### Limitación de tasa

Para prevenir el fraude de clics y el abuso de bots, Spwig limita los clics a **100 por minuto por dirección IP**. Si la misma IP supera este umbral, los clics adicionales se ignoran y no incrementan los conteos de clics.

Esta protección previene que actores maliciosos inflen estadísticas de clics sin bloquear el tráfico legítimo. Los clientes reales casi nunca superan 100 clics por minuto.

### Consideraciones de privacidad

Los datos de clic contienen direcciones IP y user agents para fines de detección de fraude. Asegúrese de que su política de privacidad revele que rastrea las referencias de afiliados y comparte datos de rendimiento anonimizados con los afiliados.

## Visualización de enlaces de afiliados

Todos los enlaces de seguimiento generados por afiliados aparecen en su panel de administración para su monitoreo y gestión.

### Accediendo a la lista de enlaces

Navegue a **Afiliados > Enlaces** para ver todos los enlaces de seguimiento de todos los afiliados y programas. La vista de lista muestra:

- **Código de enlace**: El identificador único de 12 caracteres
- **Afiliado**: ¿Quién creó el enlace?
- **Programa**: ¿Qué estructura de comisión aplica?
- **Etiqueta**: Descripción opcional proporcionada por el afiliado
- **Destino**: ¿A dónde redirige el enlace a los clientes?
- **Total de clics**: Cuenta de clics total desde la creación del enlace
- **Estado activo**: ¿El enlace está actualmente rastreando?

### Filtros de enlaces

Use los filtros del panel de administración para reducir la lista:
- **Por afiliado**: Ver todos los enlaces para un socio específico
- **Por programa**: Ver enlaces que promuevan una estructura de comisión específica
- **Por estado activo**: Encontrar enlaces desactivados

Este filtrado le ayuda a analizar la distribución de enlaces en su red de afiliados y a identificar los enlaces de mejor rendimiento.

## Estadísticas de enlaces

Cada enlace de seguimiento acumula métricas de rendimiento que ayudan a los afiliados a optimizar sus estrategias promocionales y a usted a identificar a sus socios de mejor rendimiento.

### Haga clic en un registro de enlace para ver estadísticas detalladas:

| Métrica | Descripción | Cálculo |
|--------|-------------|-------------|
| **Total de clics** | Todos los clics registrados desde la creación del enlace | Cuenta de registros de clics |
| **Clics (7 días)** | Indicador de actividad reciente | Clics en los últimos 7 días |
| **Conversiones** | Órdenes atribuidas a este enlace | Cuenta de comisiones desde este código de enlace |
| **Tasa de conversión** | Porcentaje de clics que resultaron en compras | (Conversiones ÷ Total de clics) × 100 |
| **Ingresos totales** | Suma de todos los valores de pedido desde este enlace | Suma de los totales de pedidos para clics convertidos |

### Usando estadísticas para optimización

**Para afiliados**: Estos números muestran qué canales promocionales funcionan mejor. Si un enlace de biografía de Instagram tiene una tasa de conversión del 5% pero un enlace de un artículo de blog tiene 15%, el afiliado debería enfocarse más en el contenido del blog.

**Para comerciantes**: Las estadísticas de enlaces revelan qué afiliados generan tráfico de calidad. Altos conteos de clics con tasas de conversión bajas sugieren que la audiencia del afiliado no es adecuada para sus productos.

## Gestión de enlaces

Puede gestionar los enlaces de afiliados desde el panel de administración para mantenimiento y solución de problemas.

### Desactivar enlaces

Para evitar que un enlace específico rastree nuevos clics mientras se conservan los datos históricos:

1. Navegue a **Afiliados > Enlaces**
2. Haga clic en el enlace que desea desactivar
3. Desmarque **Activo**
4. Haga clic en **Guardar**

Los enlaces desactivados aún redirigen a los clientes al destino, pero no establecen cookies de seguimiento ni registran clics. Esto es útil cuando un afiliado está ejecutando una campaña temporal o necesita deshabilitar un canal promocional específico.

### Editar detalles del enlace

Puede modificar:
- **Etiqueta**: Actualizar la descripción proporcionada por el afiliado
- **Destino**: Cambiar a dónde redirige el enlace (útil si mueve una página de producto)
- **Estado activo**: Habilitar o deshabilitar el seguimiento

No puede editar el código del enlace: es permanente y está vinculado a todos los datos históricos de clics y comisiones.

### Eliminar enlaces inactivos

Elimine enlaces que ya no se usen y no tengan clics ni conversiones históricas. Esto mantiene su lista de enlaces limpia sin perder datos analíticos valiosos.

**Advertencia**: Eliminar un enlace elimina todos los registros de clic asociados. Solo elimine enlaces con cero clics o cuando esté absolutamente seguro de que no necesita los datos históricos.

## Modelo de atribución

Entender la lógica de atribución de Spwig le ayuda a establecer expectativas con los afiliados y a resolver disputas sobre comisiones.

### Atribución por último clic

Como se mencionó anteriormente, Spwig utiliza atribución por último clic: si un cliente hace clic en múltiples enlaces de afiliados antes de realizar una compra, solo el afiliado más reciente gana una comisión.

**Ventajas**:
- Fácil de entender y explicar
- Evita comisiones dobles
- Recompensa a los afiliados que cierran la venta

**Desventajas**:
- Los afiliados que introdujeron al cliente no reciben crédito
- No refleja los viajes del cliente con múltiples toques
- Puede incentivar el "secuestro de enlaces" (afiliados que se dirigen a clientes de alto interés que ya fueron referidos por alguien más)

### La vida útil de la cookie determina la elegibilidad

Solo las compras dentro de la ventana de vida útil de la cookie generan comisiones. Si la cookie expira antes del pago, no se crea ninguna comisión incluso si el cliente vuelve a través de un marcador.

**Ejemplo**: Vida útil de la cookie de 30 días
- Cliente hace clic en el enlace el 1 de enero → Cookie establecida, expira el 31 de enero
- Cliente compra el 25 de enero → Comisión creada
- Cliente compra el 5 de febrero → Sin comisión (cookie expirada)

### Seguimiento de sesión

Además de la cookie, Spwig rastrea el ID de sesión para cada clic. Esto permite la atribución de múltiples visitas dentro de la misma sesión, incluso si las cookies se bloquean o eliminan.

Si un cliente hace clic en un enlace, navega por su tienda, lo que desencadena múltiples cargas de página y luego realiza una compra — todo en la misma sesión — el afiliado recibe crédito incluso sin una cookie persistente.

## Solución de problemas

Problemas de seguimiento comunes y cómo resolverlos:

### Enlace no rastreando clics

**Síntomas**: El recuento de clics permanece en cero a pesar de que los afiliados reportan haber compartido el enlace.

**Causas y soluciones**:
1. **El enlace está desactivado**: Verifique el estado **Activo** en la página de detalles del enlace
2. **El programa está inactivo**: Navegue a **Afiliados > Programas** y verifique que el estado del programa sea **Activo**
3. **La cuenta del afiliado está desactivada**: Verifique el estado de la cuenta del afiliado en **Afiliados > Afiliados**
4. **Limitación de tasa**: Verifique si la misma IP está generando clics excesivos (tráfico de bots)

### Tasa de conversión baja

**Síntomas**: Altos recuentos de clics pero muy pocos pedidos atribuidos.

**Causas y soluciones**:
1. **Vida útil de la cookie demasiado corta**: Aumente la vida útil del programa si sus productos requieren investigación y consideración
2. **Calidad de la página de destino**: Revise la página de aterrizaje — ¿es amigable con móviles? ¿Carga rápidamente? ¿El producto está en stock?
3. **Incongruencia de audiencia**: La audiencia del afiliado puede no ser la adecuada para sus productos
4. **Navegadores bloqueando cookies**: Algunas herramientas de privacidad bloquean cookies de terceros, aunque Spwig utiliza cookies de primeras partes que son menos propensas a bloquearse

### Registros de clic duplicados

**Síntomas**: El mismo cliente genera múltiples registros de clic en rápida sucesión.

**Causa**: Este es un comportamiento normal. Cada carga de página del enlace de seguimiento crea un registro de clic. Si un cliente hace clic, la página carga lentamente y hace clic nuevamente, verá múltiples registros.

**Solución**: No se requiere ninguna acción. El limitador de tasa previene el abuso (100 clics/minuto/IP), y los clics duplicados del mismo sesión no afectan la atribución — solo se establece una cookie.

## Consejos

- **Pruebe el rastreo antes del lanzamiento** — Cree una cuenta de afiliado de prueba, genere un enlace de seguimiento, haga clic en él en un navegador incógnito y complete una compra de prueba. Verifique que la comisión aparezca con la atribución correcta del afiliado.
- **Eduque a los afiliados sobre la vida útil de la cookie** — Asegúrese de que los afiliados entiendan que solo ganan comisiones por compras dentro del período de la cookie. Esto les ayuda a establecer expectativas realistas y enfocarse en el tráfico de alto interés.
- **Monitorea patrones de clic para detectar fraude** — Cuentas de clics inusualmente altas desde una sola IP o clics sin cadena de usuario agent pueden indicar tráfico de bots. Revise cuidadosamente a estos afiliados antes de aprobar las comisiones.
- **Use etiquetas de enlaces consistentemente** — Incentive a los afiliados a etiquetar sus enlaces por canal (Instagram, Blog, Correo electrónico) para que puedan ambos analizar qué canales promocionales generan las mejores conversiones.
- **Considere vidas útiles de cookies más largas para productos de alto costo** — Si su valor promedio de pedido es alto y los clientes suelen investigar antes de comprar, extienda la vida útil de la cookie a 60–90 días para capturar esas conversiones retrasadas.
- **Revise los datos de referidos para obtener información sobre canales** — El campo de referido muestra de dónde provienen los clics. Si ve muchos clics desde "instagram.com" o "youtube.com", sabe qué plataformas sociales usan sus afiliados con más efectividad.