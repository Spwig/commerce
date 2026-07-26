---
title: Programa de Fidelidad
---

El Programa de Fidelidad le permite recompensar a los clientes por compras y participación mediante un sistema basado en puntos. Los clientes ganan puntos, avanzan por niveles y canjean recompensas. Navegue hasta **Marketing > Programa de Fidelidad** en el menú lateral de administración.

![Panel de control de fidelidad](/static/core/admin/img/help/loyalty-program/loyalty-dashboard.webp)

## Panel de control de fidelidad

El panel de control ofrece una visión general completa de su programa de fidelidad:

### Métricas clave

- **Miembros totales** — Total de clientes inscritos
- **Miembros activos (30d)** — Miembros que ganaron o canjearon puntos en los últimos 30 días
- **Puntos pendientes** — Total de puntos no canjeados de todos los miembros
- **Tasa de canje** — Porcentaje de puntos ganados que han sido canjeados
- **Puntos ganados (30d)** — Puntos ganados en los últimos 30 días
- **Puntos canjeados (30d)** — Puntos canjeados en los últimos 30 días
- **Puntos promedio por miembro** — Saldo promedio de puntos por miembro
- **Reglas activas** — Número de reglas de ganancia actualmente activas

### Acciones rápidas

El panel de control tiene tarjetas de atajo para administrar todos los aspectos del programa:
- **Miembros** — Ver y administrar miembros de fidelidad
- **Niveles** — Configurar niveles de membresía
- **Recompensas** — Configurar el catálogo de recompensas
- **Canjeos** — Ver el historial de canjeos
- **Reglas** — Configurar cómo se ganan los puntos
- **Insignias** — Administrar insignias de logros
- **Campañas** — Ejecutar campañas de fidelidad especiales
- **Segmentos** — Crear segmentos de miembros para el targeting

### Gráficos y análisis

- **Tendencia de inscripción de miembros** — Nuevos registros de miembros con el tiempo
- **Puntos ganados vs. canjeados** — Rastrear el equilibrio del flujo de puntos
- **Distribución de niveles** — Ver cómo se distribuyen los miembros entre los niveles

## Configuración del programa

### Paso 1: Crear niveles

Los niveles definen niveles de membresía con beneficios crecientes:

1. Navegue hasta **Fidelidad > Niveles**
2. Cree niveles como Bronce, Plata, Oro, Platino
3. Para cada nivel, establezca:
   - **Nombre** — Nombre de visualización del nivel
   - **Rango** — Orden de clasificación (rango más bajo = nivel más bajo, por ejemplo, Bronce = 1, Plata = 2)
   - **Color** — Color de acento visual mostrado en las insignias de los miembros
   - **Puntos mínimos ganados** — Puntos acumulados durante la vida para calificar para este nivel
   - **Gasto mínimo** — Monto total de gasto para calificar para este nivel
   - **Pedidos mínimos** — Número de pedidos para calificar para este nivel
   - **Multiplicador de puntos** — Tasa de ganancia adicional para los miembros en este nivel (por ejemplo, 2.0 = 2 veces los puntos)

Un miembro califica para un nivel si **cualquier** uno de los tres umbrales se cumple. Puede usar solo un umbral o combinar los tres.

### Paso 2: Configurar reglas de ganancia

Las reglas definen cómo los clientes ganan puntos:

1. Navegue hasta **Fidelidad > Reglas**
2. Cree reglas usando uno de los cuatro tipos de regla:

| Tipo de regla | Descripción | Ejemplo |
|---------------|-------------|---------|
| **Gasto** | Puntos por monto gastado | 1 punto por $1 |
| **Artículo** | Puntos por artículo comprado | 50 puntos por producto en una categoría específica |
| **Acción** | Puntos por una acción específica | 200 puntos por registrarse |
| **Evento** | Puntos por un evento del calendario | Puntos de cumpleaños bonus |

3. Configure ajustes adicionales de regla:
   - **Ámbito / Filtros de ámbito** — Limitar la regla a productos, categorías o niveles de membresía específicos
   - **Monto mínimo del pedido** — Valor mínimo del carrito para que se aplique la regla
   - **Niveles permitidos** — Restringir la regla a niveles de membresía específicos
   - **Es exclusivo** — Cuando está habilitado, esta regla no puede acumularse con otras reglas
   - **Días de puntos pendientes** — Número de días antes de que los puntos ganados estén disponibles (útil para tener en cuenta los periodos de devolución)
   - **Días de vencimiento de puntos** — Número de días después de ganar antes de que los puntos expiren (dejar en blanco para no tener vencimiento)
   - **Inicio / Fin** — Restringir la regla a un rango de fechas

### Paso 3: Configurar recompensas

Las recompensas son lo que los clientes pueden canjear por sus puntos:

1. Navegue hasta **Fidelidad > Recompensas**
2. Cree recompensas como:
   - **Cupón de $5 de descuento** — 500 puntos
   - **Envío gratis** — 300 puntos
   - **10% de descuento** — 1000 puntos

> **No se pueden canjear actualmente los códigos de descuento.** Una recompensa con **Tipo de Recompensa** establecido en **Código de Descuento** — como el cupón de $5 de descuento o el ejemplo del 10% de descuento anterior — actualmente no puede canjearse.

El miembro ve un error claro y sus puntos se devuelven automáticamente a su saldo, por lo que nada se pierde, pero la recompensa aún no es utilizable.

Este es un arreglo deliberado: antes, el canje reportaba éxito mientras silenciosamente deducía puntos y no entregaba nada.

Si los miembros mencionan que un canje "no funciona", se refiere a esto — no es un nuevo problema.

Las recompensas de descuento volverán a funcionar en una versión futura.

Esto no afecta las recompensas de Envío Gratis, Producto Gratis o Experiencia/Privilegio.

### Paso 4: Crear insignias (opcional)

Las insignias reconocen logros de los clientes:

1. Navegue a **Loyalty > Badges**
2. Cree insignias para hitos:
   - **Primera compra** — Otorgada después de la primera orden
   - **Gran gasto** — Otorgada después de gastar $500+
   - **Cliente leal** — Otorgada después de 10 órdenes

Las insignias pueden incluir premios de puntos adicionales al ser otorgadas.

## Gestionar miembros

### Lista de miembros

Ver todos los miembros de lealtad con:
- Nivel y estado actual
- Saldo de puntos
- Fecha de inscripción
- Actividad reciente

### Principales generadores de puntos

El tablero destaca a sus miembros más activos con una tabla de clasificación que muestra el rango, nombre, nivel y puntos generados en el período.

### Transacciones recientes

Un registro de transacciones muestra toda la actividad reciente de puntos. Los tipos de transacción incluyen:

| Tipo | Significado |
|------|---------|
| **Earn** | Puntos acreditados por una compra calificada o regla |
| **Redeem** | Puntos gastados en una recompensa |
| **Bonus** | Puntos adicionales de una insignia, campaña o premio manual |
| **Adjustment** | Corrección manual de puntos realizada por un miembro del personal |
| **Revoke** | Puntos eliminados (por ejemplo, después de la cancelación de una orden) |
| **Expire** | Puntos que han superado su fecha de vencimiento |

### Ajustes manuales de puntos

Puede agregar o deducir puntos manualmente para cualquier miembro:

1. Abra la página de detalles del miembro
2. Haga clic en **Adjust Points**
3. Ingrese la cantidad de puntos (positiva para agregar, negativa para deducir)
4. Ingrese la razón del ajuste
5. Haga clic en **Save**

El ajuste se registra como una transacción y es visible en el historial de transacciones del miembro.

## Campañas

Las campañas de lealtad le permiten realizar promociones especiales:
- **Doble puntos los fines de semana** — Aumente temporalmente las tasas de generación de puntos
- **Eventos de puntos adicionales** — Otorgue puntos extra por acciones específicas
- **Promociones de ascenso de nivel** — Reduzca el umbral para el avance de nivel

## Consejos

- Comience con reglas simples de generación de puntos (1 punto por cada $1 gastado) y amplíe con el tiempo.
- Establezca umbrales de recompensa alcanzables para mantener a los miembros comprometidos — si las recompensas parecen inalcanzables, los miembros pierden interés.
- Use insignias para gamificar la experiencia y fomentar comportamientos específicos.
- Monitorea la Tasa de Canje — un programa saludable tiene una tasa de canje del 10-30%.
- Lanza campañas durante períodos lentos para aumentar la participación.
- Use el gráfico de Puntos Generados vs. Canjeados para asegurarse de que su programa sea sostenible.