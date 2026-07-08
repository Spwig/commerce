---
title: Programa de Referidos
---

El programa de referidos permite que tus clientes existentes compartan un enlace de referido único con sus amigos y familiares. Cuando un amigo referido realiza su primera compra calificada, tanto el referidor como el nuevo cliente pueden recibir una recompensa — impulsando la adquisición de nuevos clientes a través del boca a boca.

## Cómo funciona el programa de referidos

1. Un cliente comparte su enlace de referido único (o código) con un amigo.
2. El amigo hace clic en el enlace y se rastrea mediante una cookie durante un máximo de 30 días (configurable).
3. El amigo se registra y realiza su primera orden calificada.
4. El sistema crea un registro de atribución de referido y ejecuta verificaciones de fraude y elegibilidad.
5. Si la atribución se aprueba, se otorgan recompensas a ambas partes.

Tu tienda tiene una única configuración del programa de referidos. Navega a **Marketing > Programa de Referidos** para configurarlo.

## Configuración del programa de referidos

### Estado del programa

El programa tiene tres estados:

- **Borrador** — El programa se está configurando pero aún no está en vivo. Los enlaces de referidos están inactivos.
- **Activo** — El programa está en vivo. Los clientes pueden compartir enlaces y ganar recompensas.
- **Pausado** — El programa se ha detenido temporalmente. Las atribuciones existentes aún se procesan, pero no se rastrean nuevas referencias.

Establece el **Estado** en **Activo** cuando estés listo para lanzarlo. Puedes pausarlo en cualquier momento.

### Configuración de recompensas

Define las recompensas que se otorgan cuando una referencia se convierte. El programa admite **recompensas de ambos lados** — lo que significa que puedes recompensar tanto al referidor (el cliente que compartió el enlace) como al referido (el nuevo cliente que lo usó).

Configura recompensas para cada destinatario en el campo **Configuración de Recompensas**. Los tipos de recompensas disponibles son:

| Tipo de Recompensa | Descripción |
|-------------------|-------------|
| **Crédito en la tienda** | Añade crédito al monedero del cliente, utilizable en futuras compras |
| **Código de cupón** | Genera un código de descuento único |
| **Descuento porcentaje** | Emite un descuento porcentual para usar en el checkout |
| **Beneficio exclusivo** | Un beneficio personalizado (por ejemplo, regalo gratuito, acceso prioritario) — descrito en el campo de descripción de la recompensa |

**Ejemplo de configuración** — $10 de crédito en la tienda para el referidor y $10 de descuento para el nuevo cliente:

```json
{
  "referrer": {"kind": "credit", "amount": 10},
  "referee": {"kind": "discount", "amount": 10},
  "double_sided": true
}
```

Establece "double_sided": false si solo deseas recompensar al referidor.

### Reglas de elegibilidad

Las reglas de elegibilidad determinan qué referencias califican para recompensas. Configúralas en el campo **Reglas de Elegibilidad**:

| Regla | Qué hace |
|-------|----------|
| `new_customer_only` | Si `true`, el amigo referido debe ser un cliente nuevo (sin pedidos anteriores) |
| `min_order_value` | El monto mínimo del pedido (en la moneda de tu tienda) que debe gastar el amigo referido |
| `exclude_discounts` | Si `true`, los pedidos donde el cliente referido usó un cupón no califican |
| `exclude_staff` | Si `true`, las cuentas de personal no pueden ser referidores ni referidos |

**Ejemplo** — solo nuevos clientes, mínimo $40 de pedido, personal excluido:

```json
{
  "new_customer_only": true,
  "min_order_value": 40.0,
  "exclude_discounts": false,
  "exclude_staff": true
}
```

### Configuración de tiempo

El campo **Configuración de Tiempo** controla cuándo se otorgan las recompensas después de un pedido calificado:

| Configuración | Qué hace |
|---------------|----------|
| `issue_on` | Cuándo otorgar la recompensa: `signup` (inmediatamente al registrarse), `first_purchase` (inmediatamente después del pedido) o `post_refund` (después de que expire el período de devolución) |
| `refund_window_days` | Cuántos días esperar antes de otorgar recompensas al usar `post_refund` (por defecto: 14 días) |

Usar `post_refund` es el enfoque más cauteloso — espera hasta que el período de devolución haya terminado antes de otorgar recompensas, reduciendo el riesgo de otorgar recompensas a pedidos que se devuelvan posteriormente.

### Límites y tope

Evita que un solo referidor gane recompensas ilimitadas estableciendo límites en el campo **Límites y tope**:

| Configuración | Qué hace |
|---------|--------------|
| `monthly_per_referrer` | Número máximo de referidos exitosos recompensados por mes, por referidor |
| `lifetime_per_referrer` | Número total máximo de referidos exitosos recompensados en toda la vida, por referidor |
| `max_reward_per_order` | Valor máximo de recompensa (en la moneda de su tienda) otorgado por una sola conversión de referido |

**Ejemplo** — 20 referidos por mes, 200 en toda la vida, $50 máximo de recompensa por conversión:

```json
{
  "monthly_per_referrer": 20,
  "lifetime_per_referrer": 200,
  "max_reward_per_order": 50
}
```

### Configuración de seguimiento

Configure cómo se rastrean los enlaces de referidos en el campo **Configuración de seguimiento**:

| Configuración | Qué hace |
|---------|--------------|
| `cookie_ttl_days` | Cuántos días permanece activa la cookie de seguimiento de referidos después de que un amigo haga clic en el enlace (por defecto: 30) |
| `attribution` | Método de atribución — actualmente `last_touch` (el clic más reciente en el enlace de referido se atribuye) |

### Política de fraude

El sistema de detección de fraude califica automáticamente cada atribución de referido por riesgo antes de aprobarla. Configure la política en el campo **Política de fraude**:

| Configuración | Qué hace |
|---------|--------------|
| `policy` | Estrictitud general: `strict`, `balanced` o `lenient` |
| `auto_reject_threshold` | Puntaje de riesgo (0–100) por encima del cual las atribuciones se rechazan automáticamente (por defecto: 80) |
| `auto_approve_threshold` | Puntaje de riesgo por debajo del cual las atribuciones se aprueban automáticamente (por defecto: 30) |
| `check_ip` | Si `true`, verifica si el referidor y el referido comparten la misma dirección IP |
| `check_device` | Si `true`, verifica si hay huellas de dispositivos compartidas entre el referidor y el referido |
| `check_velocity` | Si `true`, monitorea velocidades anormalmente altas de referidos desde una sola fuente |
| `velocity_window_hours` | El período de tiempo (en horas) para la verificación de velocidad |
| `max_referrals_per_window` | Número máximo de referidos permitidos desde una sola fuente dentro del período de velocidad |

Las atribuciones con un puntaje de riesgo entre los umbrales de rechazo automático y aprobación automática entran en un estado **Pendiente** y requieren revisión manual.

### Términos y condiciones

Ingrese cualquier término y condición legal para el programa en el campo **Términos y condiciones**. Este texto se muestra a los clientes cuando ven el programa de referidos. Se admite el formato Markdown.

## Ver atribuciones de referidos

Navegue hasta **Marketing > Atribuciones de Referidos** para ver todos los casos de referidos — la conexión entre un referidor y un cliente referido.

![Lista de atribuciones de referidos](/static/core/admin/img/help/referral-program/attribution-list.webp)

Cada atribución muestra al referidor, al cliente referido, el primer pedido que realizaron, el estado actual y el puntaje de riesgo.

### Estados de atribución

| Estado | Qué significa |
|--------|---------------|
| **Pendiente** | En espera de revisión — el puntaje de riesgo está en el rango de revisión manual |
| **Aprobado** | Referido válido — las recompensas se han otorgado o se otorgarán |
| **Rechazado** | El referido no calificó o fue marcado como fraudulento |
| **Caducado** | El referido no se convirtió dentro del período de seguimiento |

### Aprobar o rechazar atribuciones manualmente

Para atribuciones en estado **Pendiente**, puede aprobarlas o rechazarlas manualmente abriendo el registro de atribución y usando los botones de acción. Al rechazar, elija un **Motivo de rechazo**:

- Referido propio
- No es un nuevo cliente
- Valor del pedido inferior al mínimo
- Correo electrónico temporal
- Límite excedido
- Riesgo de fraude
- Pedido reembolsado o cancelado
- Rechazo manual

También puede agregar **Notas de rechazo** para su propio registro.

### Filtros por nivel de riesgo

Use el filtro **Nivel de riesgo** en el panel lateral para enfocarse en atribuciones de alto riesgo que necesitan revisión:

- Bajo riesgo (puntaje 0–30) — Aprobado automáticamente
- Riesgo medio (puntaje 31–70) — Revisión manual
- Alto riesgo (puntaje 71–89) — Revisión manual, trate con precaución
- Muy alto riesgo (puntaje 90+) — Rechazado automáticamente

## Ver recompensas emitidas

Navegue hasta **Marketing > Recompensas Emitidas** para ver todas las recompensas que se han emitido como resultado de atribuciones aprobadas.

Cada entrada de recompensa muestra al cliente, si es el referidor o el referido, el tipo y monto de la recompensa, y el estado actual de canje.

### Estados de recompensa

| Estado | Qué significa |
|--------|---------------|
| **Pendiente** | La recompensa ha sido creada pero aún no se ha entregado al cliente |
| **Emitida** | La recompensa está activa y disponible para que el cliente la use |
| **Canjeadas** | El cliente ha utilizado la recompensa |
| **Caducada** | La recompensa pasó su fecha de vencimiento sin haberse utilizado |
| **Revocada** | La recompensa fue cancelada manualmente (por ejemplo, si el pedido original fue reembolsado después de que se emitió la recompensa) |

### Revocar una recompensa

Si una recompensa necesita ser cancelada — por ejemplo, el pedido calificable fue devuelto — abra el registro de la recompensa y use la acción **Revocar**. Agregue una nota explicando por qué se revocó para sus registros.

## Consejos

- Comience con la configuración de horario `post_refund`. Esperar a que expire el período de devolución antes de emitir recompensas evita recompensar pedidos que al final se devuelvan.
- La política de fraude `balanced` es una buena opción predeterminada para la mayoría de las tiendas. Cambie a `strict` si nota un pico inusual de referidos provenientes de un número pequeño de cuentas.
- Establezca límites mensuales y de toda la vida realistas. Si el valor de su recompensa es alto, un límite de 10–20 por mes por referidor es razonable para prevenir el abuso.
- Revise las atribuciones **Pendientes** semanalmente. Dejar que permanezcan sin revisión durante demasiado tiempo puede frustrar a los referidores legítimos que esperan su recompensa.
- Use el filtro **Nivel de Riesgo** para priorizar su cola de revisión manual — comience con las atribuciones de muy alto riesgo antes de pasar a las de riesgo medio.
- Mantenga sus Condiciones y Términos cortos y en lenguaje sencillo. Los clientes son más propensos a participar cuando entienden claramente las reglas.