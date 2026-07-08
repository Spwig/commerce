---
title: Campañas de lealtad
---

Las campañas de lealtad te permiten realizar promociones con plazo limitado y recompensas automatizadas que van más allá de tus reglas de acumulación habituales. Úselas para ofrecer doble puntos los fines de semana, recompensar a los clientes en su cumpleaños, recuperar a compradores inactivos y entregar bonificaciones dirigidas a grupos específicos de miembros.

Cada campaña define un disparador o programación, los miembros a los que se aplica y las acciones a tomar. Una vez activa, las campañas se disparan automáticamente — las configuras una vez y Spwig maneja el resto.

## Tipos de campañas

| Tipo | Cuando se dispara |
|------|------------------|
| **Basado en disparador** | Cuando ocurre un evento específico (por ejemplo, se coloca un pedido, se detecta un cumpleaños) |
| **Programado** | En un horario repetitivo (diario, semanal, mensual) |
| **Manual** | Solo cuando lo ejecutes explícitamente desde el administrador |
| **Basado en comportamiento** | Cuando un cliente coincide con un patrón de comportamiento (por ejemplo, navegar sin comprar) |

## Crear una campaña

Navega a **Promotions > Loyalty Campaigns** y haz clic en **+ Add Loyalty Campaign**.

### Paso 1: información básica

- **Nombre** — un nombre claro y descriptivo visible solo en el administrador (por ejemplo, `Birthday Bonus — 200 Points`)
- **Slug** — generado automáticamente a partir del nombre; se usa internamente
- **Descripción** — notas opcionales sobre el propósito de la campaña
- **Tipo de campaña** — seleccione el tipo de la tabla anterior

### Paso 2: disparador o programación

**Para campañas basadas en disparador**, establezca el **Evento de disparador** que activa la campaña. Los disparadores disponibles incluyen:

| Disparador | Descripción |
|-----------|------------|
| Pedido realizado | Se dispara cuando un miembro completa un pedido |
| Primer pedido | Se dispara en el primer pedido de un miembro |
| Cumpleaños del cliente | Se dispara en el cumpleaños del miembro |
| Aniversario de membresía | Se dispara cada año en el aniversario de unión del miembro |
| Carrito abandonado | Se dispara cuando un carrito se abandona sin finalizar la compra |
| Promoción de nivel | Se dispara cuando un miembro sube a un nivel más alto |
| Puntos a expirar pronto | Se dispara cuando un miembro tiene puntos a punto de expirar |
| Inactivo 90 días | Se dispara cuando un miembro no ha comprado en 90 días |
| Reseña enviada | Se dispara cuando un miembro envía una reseña de producto |
| Referido convertido | Se dispara cuando un cliente referido realiza una compra |

Puedes agregar **Condiciones de disparador** como un objeto JSON para filtrar aún más cuándo se dispara la campaña. Por ejemplo, para disparar solo pedidos superiores a $100:

```json
{
  "min_order_amount": 100
}
```

**Para campañas programadas**, establezca el **Tipo de programación** (Diario, Semanal, Mensual o Cron personalizado) y configure la hora en el campo **Configuración de programación**:

```json
{
  "hour": 9,
  "minute": 0
}
```

### Paso 3: acciones

El campo **Acciones** define qué ocurre cuando se dispara la campaña. Ingrese un arreglo JSON de objetos de acción. La acción más común es otorgar puntos bonus:

```json
[
  {
    "type": "award_points",
    "points": 200,
    "description": "Birthday bonus — thank you for being a member!"
  }
]
```

Otras acciones disponibles incluyen enviar una notificación por correo electrónico o otorgar un distintivo. Consulte la documentación de su componente proveedor para obtener la lista completa.

### Paso 4: segmentación

Controla a qué miembros se aplica la campaña usando los campos de segmentación:

- **Target All Members** — marcado por defecto; la campaña se aplica a cada miembro activo de lealtad
- **Target Segment** — restringe la campaña a miembros de un segmento específico (ver [Segments](#managing-member-segments) a continuación)
- **Target Tiers** — restringe la campaña a miembros de niveles específicos de lealtad

### Paso 5: límites y tiempos de enfriamiento

- **Max Triggers Per Member** — cuántas veces el mismo miembro puede beneficiarse de esta campaña. Establezca en `1` para bonos de un solo uso como un regalo de cumpleaños. Deje en blanco para ilimitado.
- **Cooldown Days** — días mínimos entre disparadores de campaña para el mismo miembro. Por ejemplo, establezca en `365` para evitar que una campaña de cumpleaños se dispare más de una vez al año.

### Paso 6: fechas de la campaña

Establezca **Start Date** y **End Date** para hacer la campaña con plazo limitado. Deje ambos en blanco para una campaña continua.

Las campañas pueden estar en uno de estos estados:

| Estado | Descripción |
|--------|-------------|
| **Borrador** | Creado pero aún no activo; es seguro configurarlo y probarlo |
| **Activo** | En ejecución y se activará cuando se cumplan las condiciones |
| **Pausado** | Detenido temporalmente sin perder la configuración |
| **Finalizado** | Fuera de su fecha de finalización; ya no se activa |
| **Archivado** | Oculto de la lista activa pero conservado para registros |

Después de completar todos los campos, haga clic en **Guardar**. Luego cambie el estado a **Activo** para iniciar la campaña.

## Ejemplos prácticos

### Ejemplo: doble puntos en fin de semana

**Escenario:** Otorgar 2x puntos en todas las compras realizadas durante un fin de semana específico.

| Campo | Valor |
|-------|-------|
| Nombre | `Doble Puntos Fin de Semana — Marzo` |
| Tipo de Campaña | Basado en Triggers |
| Evento de Trigger | Pedido Realizado |
| Acciones | `["{\"type\": \"award_points_multiplier\", \"multiplier\": 2.0}"]` |
| Fecha de Inicio | Tarde del viernes |
| Fecha de Fin | Medianoche del domingo |
| Target All Members | Marcado |

### Ejemplo: bono de cumpleaños

**Escenario:** Dar a cada miembro de lealtad 200 puntos adicionales en su cumpleaños.

| Campo | Valor |
|-------|-------|
| Nombre | `Bono de Cumpleaños` |
| Tipo de Campaña | Basado en Triggers |
| Evento de Trigger | Cumpleaños del Cliente |
| Acciones | `["{\"type\": \"award_points\", \"points\": 200, \"description\": \"Feliz cumpleaños desde parte de nosotros\"}"]` |
| Máximo de Triggers por Miembro | 1 |
| Días de Enfriamiento | 365 |
| Target All Members | Marcado |

### Ejemplo: campaña de recuperación de clientes

**Escenario:** Enviar 100 puntos adicionales a los miembros que no han comprado en 90 días.

| Campo | Valor |
|-------|-------|
| Nombre | `Bono de Recuperación de 90 Días` |
| Tipo de Campaña | Basado en Triggers |
| Evento de Trigger | Inactivo 90 Días |
| Acciones | `["{\"type\": \"award_points\", \"points\": 100, \"description\": \"Nos extrañan — aquí tienes algunos puntos adicionales\"}"]` |
| Máximo de Triggers por Miembro | 1 |
| Días de Enfriamiento | 180 |
| Target All Members | Marcado |

## Gestionar segmentos de miembros

Los segmentos le permiten dirigir campañas a grupos específicos de miembros de lealtad. Navegue hasta **Promociones > Segmentos de Lealtad** para gestionarlos.

### Tipos de segmento

| Tipo | Descripción |
|------|-------------|
| **Basado en Reglas** | Miembros determinados por reglas (por ejemplo, miembros con más de 1,000 puntos) |
| **Cálculo Dinámico** | Miembros calculados en demanda desde criterios en tiempo real |
| **Asignación Manual** | Los miembros se agregan al segmento manualmente |

### Crear un segmento

1. Navegue hasta **Promociones > Segmentos de Lealtad** y haga clic en **+ Agregar Segmento de Lealtad**
2. Complete:
   - **Nombre** — nombre descriptivo (por ejemplo, `Clientes de Alto Valor`, `Miembros de Nivel Plata`)
   - **Slug** — generado automáticamente
   - **Tipo de Criterio** — cómo se determina la membresía
   - **Configuración de Criterio** — objeto JSON que define las reglas de membresía
3. Haga clic en **Guardar**

#### Ejemplo: segmento para miembros con 500+ puntos

```json
{
  "min_available_points": 500
}
```

#### Ejemplo: segmento solo para miembros de nivel oro

```json
{
  "tier_slugs": ["gold"]
}
```

La columna **Cuenta de Miembros** en la lista de segmentos muestra cuántos miembros coinciden actualmente. Haga clic en un segmento y use la acción **Recalcular Cuenta de Miembros** para recalcularla si sus datos han cambiado.

## Seguimiento del rendimiento de la campaña

### Historial de ejecución de campañas

Navegue hasta **Promociones > Ejecuciones de Campaña** para ver un registro de cada vez que una campaña se haya activado para cualquier miembro. Cada registro de ejecución muestra qué campaña se ejecutó, para qué miembro se ejecutó y el resultado.

### Revisión del alcance de una campaña

Abra cualquier registro de campaña para ver la cuenta de **Veces Activado** y cuándo se activó la campaña por última vez. Esto le da una vista rápida de cuántos miembros han beneficiado de la campaña.

## Consejos

Conservar todo el formato de markdown, rutas de imágenes, bloques de código y términos técnicos.

- Cree campañas en estado **Borrador** primero para que pueda revisar todas las configuraciones antes de que se activen
- Use **Máximo de disparadores por miembro** en todas las campañas de bonificación única (cumpleaños, primer compra, registro) para evitar que los clientes obtengan el bono más de una vez
- Combine un **Segmento objetivo** con una campaña basada en disparadores para realizar promociones exclusivas de nivel — por ejemplo, doble puntos en compras solo para miembros de Oro y Platino
- Establezca un valor de **Días de enfriamiento** en campañas de recuperación para que los miembros no sean bombardeados si realizan una compra pequeña y luego se vuelven inactivos poco tiempo después
- La lista de campañas es su mejor herramienta para mantener un control sobre qué promociones están activas actualmente — reviértala antes de lanzar nuevas ofertas para asegurarse de que las campañas no se acumulen sin querer
- Archive las campañas finalizadas en lugar de eliminarlas para tener un registro histórico de qué promociones realizó y cuándo