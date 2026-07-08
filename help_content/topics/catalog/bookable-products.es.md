---
title: Productos reservables
---

Los productos reservables permiten a los clientes reservar una fecha y hora específica cuando realizan una compra. Esto admite citas, alquileres, clases, eventos y reservas de alojamiento — todo gestionado directamente desde su administración de Spwig.

## Tipos de reserva

| Tipo | Mejor para |
|------|----------|
| **Cita** | Servicios: consultas, cortes de pelo, entrenamiento personal |
| **Alquiler** | Alquiler de equipos, vehículos, salas |
| **Clase / Taller** | Sesiones grupales con una capacidad establecida |
| **Alojamiento** | Estancias de varias noches con horarios de entrada/salida |
| **Evento** | Eventos con entrada pagada, de una sola vez o recurrentes |

## Configuración de un producto reservable

### Paso 1: Crear el producto

1. Navegue a **Productos > Todos los productos** y haga clic en **+ Añadir producto**
2. Establezca **Tipo de producto** en **Producto de reserva**
3. Complete los campos estándar del producto (nombre, descripción, precio)
4. Guarde el producto

### Paso 2: Configurar la configuración de reserva

Después de guardar, aparece una sección **Configuración de reserva** en el formulario de edición del producto. Rellene la configuración de reserva:

#### Tipo de reserva y duración

- **Tipo de reserva** — Seleccione el tipo que mejor se adapte a su servicio (Cita, Alquiler, Clase, etc.)
- **Tipo de duración** — Elija **Duración fija** para sesiones de duración establecida, o **Cliente elige la duración** para permitir que los clientes elijan cuánto tiempo necesitan
- **Duración** y **Unidad de duración** — Establezca la duración (por ejemplo, `60` minutos, `1` hora, `2` días)
- **Duración mínima/máxima** — Si los clientes pueden elegir la duración, establezca el rango permitido

#### Tiempo de buffer

El tiempo de buffer se agrega automáticamente entre reservas para permitir la preparación o limpieza:
- **Buffer antes** — Minutos reservados antes de que comience la reserva
- **Buffer después** — Minutos reservados después de que termine la reserva

Por ejemplo, una cita de masaje de 60 minutos con un buffer de 15 minutos después da 15 minutos para prepararse para el siguiente cliente.

#### Ventana de reserva anticipada

- **Notificación mínima de anticipación** — Cuánto tiempo antes debe reservar un cliente (por ejemplo, `24 horas` para que no se permitan reservas del mismo día)
- **Ventana máxima de anticipación** — Cuánto tiempo en el futuro pueden reservar los clientes (por ejemplo, `365 días`)

#### Capacidad

- **Máximo de reservas por horario** — Para clases y eventos, establezca cuántos clientes pueden reservar el mismo horario. Establezca en `1` para citas privadas.

#### Confirmación

- **Requerir confirmación manual** — Cuando está activado, las reservas no se confirman automáticamente. Debe aprobar manualmente cada reserva desde la lista de reservas. Útil cuando desee verificar a los clientes antes de confirmar.

#### Política de cancelación

- **Cancelación permitida** — Si los clientes pueden cancelar su reserva
- **Plazo de cancelación** — Cuántas horas/días antes de la reserva los clientes pueden cancelar (por ejemplo, `24 horas`)

#### Visualización del calendario

Cómo los clientes eligen su fecha y hora en la página del producto:

| Modo de visualización | Mejor para |
|-------------|----------|
| **Vista de calendario** | Uso general — calendario completo de un mes |
| **Selector de fecha** | Selección simple de una sola fecha |
| **Lista desplegable de fechas disponibles** | Productos con pocos horarios disponibles |
| **Selector de rango de fechas** | Alojamiento y alquileres de varios días |

#### Depósitos

Para requerir un depósito en el momento del pago en lugar de un pago completo:
1. Marque **Depósito habilitado**
2. Establezca **Tipo de depósito** en **Monto fijo** o **Porcentaje del total**
3. Ingrese el **Monto del depósito** (por ejemplo, `50` para $50, o `25` para 25%)

#### Configuración específica de alojamiento

Para reservas de alojamiento, aparecen campos adicionales:
- **Hora de entrada** y **Hora de salida** — Horas estándar para la propiedad
- **Ocupación estándar** — Número predeterminado de invitados incluido en la tarifa base

### Paso 3: Añadir recursos de reserva (opcional)

Los recursos son los elementos físicos o miembros del personal que se asignan a una reserva — por ejemplo, "Sala 1", "Cancha A" o "Instructor Sam".

1. En el formulario de edición del producto, vaya a la sección **Recursos de reserva**
2. Haga clic en **Añadir recurso**
3. Dado al recurso un **Nombre** y establezca su **Capacidad** (cuántas reservas puede manejar simultáneamente)
4. Opcionalmente, añada imágenes del recurso

Los recursos le permiten rastrear la disponibilidad por activo individual o miembro del personal, no solo por horario.

### Paso 4: Establecer reglas de disponibilidad

Las reglas de disponibilidad definen cuándo se pueden realizar reservas:

1. En la sección **Disponibilidad** del producto, haga clic en **Añadir regla de disponibilidad**
2. Seleccione el **Recurso** al que se aplica esta regla
3. Establezca los **Días de la semana** en los que las reservas están disponibles
4. Establezca la **Hora de inicio** y la **Hora de finalización** para la ventana disponible
5. Opcionalmente, establezca un rango de fechas (**Válido desde** / **Válido hasta**) para la disponibilidad estacional
6. Guardar

## Ver y gestionar reservas

### Lista de reservas

Navegue hasta **Catálogo > Reservas** para ver todas las reservas. Puede filtrar por:
- Estado (Pendiente de confirmación, Confirmada, Cancelada, Completada, No asistió)
- Producto
- Rango de fechas

### Estados de las reservas

| Estado | Significado |
|--------|---------|
| **Pendiente de confirmación** | En espera de aprobación manual (si se requiere confirmación) |
| **Confirmada** | La reserva está confirmada y activa |
| **Cancelada** | La reserva fue cancelada por el cliente o por usted |
| **Completada** | La fecha de la reserva ha pasado y se cumplió |
| **No asistió** | El cliente no asistió |

### Confirmar una reserva pendiente

1. Abra la reserva desde **Catálogo > Reservas**
2. Cambie el **Estado** a **Confirmada**
3. Guarde — el cliente recibe automáticamente un correo de confirmación

### Cancelar una reserva

1. Abra la reserva
2. Cambie el **Estado** a **Cancelada**
3. Ingrese un **Motivo de cancelación** (mostrado en el correo del cliente)
4. Guardar

## Gestionar la lista de espera

Cuando un horario esté completamente reservado, los clientes pueden añadirse a la lista de espera. Spwig notifica automáticamente a los clientes de la lista de espera cuando una cancelación cree un hueco.

### Ver la lista de espera

Navegue hasta **Catálogo > Lista de espera de reservas** para ver todas las entradas de la lista de espera. Cada entrada muestra:
- Nombre y correo electrónico del cliente
- El producto y la fecha deseada
- Estado: **Esperando**, **Notificado**, **Convertido en reserva** o **Caducado**

### Estados de la lista de espera

| Estado | Significado |
|--------|---------|
| **Esperando** | El cliente está en la cola, el horario aún no está disponible |
| **Notificado** | El cliente ha recibido un correo electrónico sobre un horario disponible |
| **Convertido en reserva** | El cliente tomó el horario y completó una reserva |
| **Caducado** | La fecha deseada pasó sin que un horario se hiciera disponible |

### Notificar manualmente a un cliente de la lista de espera

Si desea contactar a un cliente específico de la lista de espera antes de la notificación automática:
1. Abra la entrada de la lista de espera
2. Copie su dirección de correo electrónico y contacte directamente con él
3. Una vez que complete una reserva, el estado de su entrada en la lista de espera se actualiza a **Convertido en reserva**

## Consejos

- Active la confirmación manual para reservas de alto valor (por ejemplo, sesiones de fotografía, eventos privados) para que pueda verificar la disponibilidad y coincidir con los requisitos antes de comprometerse.
- Establezca un tiempo de buffer generoso al principio — siempre puede reducirlo una vez que entienda las necesidades reales de tiempo de entrega.
- Para clases grupales, establezca **Máximo de reservas por horario** en la capacidad de la clase y active la lista de espera para que las sesiones populares creen automáticamente una cola.
- Use el modo de selector de rango de fechas para productos de alojamiento — los clientes esperan seleccionar las fechas de llegada y salida juntas.
- Establezca un aviso mínimo de anticipación para evitar reservas de último momento si necesita tiempo de preparación (por ejemplo, un mínimo de 48 horas para pedidos de catering personalizado).
- Revise su lista de espera regularmente durante las temporadas ocupadas — el contacto manual con los clientes de la lista de espera puede llenar las cancelaciones más rápido que la notificación automática.