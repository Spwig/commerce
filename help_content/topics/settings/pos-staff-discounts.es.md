---
title: Descuentos del personal y seguridad del terminal
---

Las configuraciones de descuentos del personal del POS le permiten controlar cuánto descuento puede aplicar cada miembro del personal en el punto de venta. Los eventos de bloqueo del terminal proporcionan un registro de auditoría de cada vez que un terminal se bloqueó o desbloqueó, lo que le ayuda a rastrear quién accedió al terminal y si ocurrieron intentos de inicio de sesión fallidos.

## Límites de descuentos del personal

Cada miembro del personal que utiliza el POS puede tener permisos de descuento individuales. Por defecto, el personal puede aplicar un descuento máximo del 10% a los artículos o al carrito completo. Puede aumentar o disminuir este límite por persona, o designar al personal como administradores que puedan aprobar descuentos que excedan los límites estándar.

### Configuración del límite de descuento de un miembro del personal

1. Navegue a **POS > Descuentos del Personal**
2. Haga clic en **+ Agregar Descuento del Personal del POS** o haga clic en un miembro del personal existente para editar
3. Seleccione el **Miembro del Personal** de la lista
4. Establezca los límites de descuento:

| Campo | Descripción |
|-------|-------------|
| **Máximo de Descuento %** | Porcentaje máximo de descuento que esta persona puede aplicar (por ejemplo, `10` para 10%) |
| **Máximo de Monto de Descuento** | Monto fijo máximo por transacción (deje en blanco para no tener un límite fijo) |
| **Puede Aplicar Descuentos por Artículo** | Permitir descuentos en elementos individuales |
| **Puede Aplicar Descuentos al Carrito** | Permitir descuentos en el total del carrito |
| **Requiere Razón** | Cuando está marcado, el miembro del personal debe escribir una razón antes de aplicar cualquier descuento |

5. Haga clic en **Guardar**

### Cómo funcionan los límites de descuento en el POS

Cuando un cajero intenta aplicar un descuento:
- Si el descuento está dentro de su límite, se aplica inmediatamente
- Si el descuento excede su límite, el terminal solicita **aprobación del administrador**
- Un administrador ingresa su PIN para autorizar la sobrescripción, y el descuento se aplica

Este flujo de trabajo evita descuentos de alto valor no autorizados, mientras permite flexibilidad cuando se justifiquen descuentos reales.

## Roles de administrador

El personal con la bandera **Es Administrador** puede aprobar descuentos que excedan los límites de otros miembros del personal. Los administradores se identifican en el terminal mediante un PIN que ingresan cuando se solicita una aprobación.

### Configuración de un administrador

1. Abra el registro de descuentos de un miembro del personal
2. Marque **Es Administrador**
3. Ingrese un **PIN de Administrador** (4-6 dígitos) — este se almacena de forma segura en forma de hash cuando se guarda
4. Haga clic en **Guardar**

El PIN del administrador es independiente del PIN del cajero utilizado para bloquear/desbloquear el terminal. Un administrador puede tener tanto un PIN de administrador (para aprobaciones de descuentos) como un PIN de cajero (para acceso al terminal).

### Seguridad del PIN del administrador

Cuando ingresa un PIN en el formulario de administración y lo guarda, Spwig lo hashea automáticamente — el PIN en texto plano nunca se almacena. El campo del PIN en texto plano se borra después de guardar, lo cual es un comportamiento esperado.

## PIN del cajero y acceso con tarjeta

Cada miembro del personal también puede tener un **PIN del Cajero** para bloquear y desbloquear el terminal:

- **PIN del Cajero** — PIN de 4 a 6 dígitos utilizado para desbloquear el terminal después de que se bloquea automáticamente o se bloquea manualmente
- **Identificador de Tarjeta** — Una tarjeta registrada (tarjeta de swiping o NFC) también puede usarse para desbloquear el terminal

Para configurar un PIN del cajero, ingréselo en el campo **PIN del Cajero** y guárdelo. Al igual que el PIN del administrador, se hashea automáticamente al guardar.

## Eventos de bloqueo del terminal

Cada vez que un terminal se bloquea o se desbloquea, Spwig registra un evento de bloqueo del terminal. Esto crea un registro de auditoría de seguridad completo.

### Ver eventos de bloqueo

Navegue a **POS > Eventos de Bloqueo del Terminal** para ver el historial completo. Puede filtrar eventos por:
- Terminal
- Tipo de evento
- Rango de fechas

### Tipos de eventos

| Evento | Significado |
|-------|---------|
| **Bloqueo Manual** | Un miembro del personal bloqueó deliberadamente el terminal |
| **Bloqueo Automático (Tiempo de Inactividad)** | El terminal se bloqueó automáticamente debido a la inactividad |
| **Desbloqueo por Cajero** | El cajero se autenticó y desbloqueó el terminal |
| **Desbloqueo por Gerente** | Un gerente usó sus credenciales para desbloquear |
| **Desbloqueo por Tarjeta** | El terminal se desbloqueó usando una tarjeta registrada |
| **Desbloqueo por Biométrico** | El terminal se desbloqueó usando huella dactilar o reconocimiento facial |
| **Intento de Desbloqueo Fallido** | Se realizó un intento de desbloqueo con credenciales incorrectas |
| **Bloqueo (3+ fallidos)** | El terminal se bloqueó después de varios intentos fallidos |

### Qué contienen los registros de eventos de bloqueo

Cada evento registra:
- El **Terminal** involucrado
- El **Tipo de Evento**
- Quién realizó la acción (**Realizado por**) y quién estaba conectado cuando ocurrió el bloqueo (**Bloqueado por**)
- Si se usó un **Sobrescritura por Gerente**
- El **Método de Desbloqueo** (PIN, tarjeta o biométrico)
- **Intentos fallidos** antes de este evento (útil para detectar patrones de fuerza bruta)
- El **Total del Carrito** y la cantidad de artículos en el momento del evento
- La dirección IP de la solicitud

### Investigando una preocupación de seguridad

Si sospechas de acceso no autorizado a un terminal:

1. Navega a **POS > Eventos de Bloqueo del Terminal**
2. Filtra por el terminal en cuestión
3. Busca eventos del tipo **Intento de Desbloqueo Fallido** o **Bloqueo** — estos indican intentos repetidos de acceso fallido
4. Revisa el campo **Realizado por** en los desbloqueos exitosos para ver quién obtuvo acceso
5. Cruza la información con los registros de turnos (**POS > Turnos**) para verificar el cajero que debía estar de turno

## Consejos

- Establece límites de descuento basados en el nivel de experiencia del personal — el personal nuevo podría comenzar en 5%, el personal experimentado en 10-15%, y los gerentes pueden aprobar cualquier porcentaje más alto.
- Habilita **Requiere Razón** para cualquier personal con límites de descuento más altos. Tener una razón en los registros ayuda a analizar patrones de descuento e identificar cualquier uso indebido.
- Revisa los eventos de bloqueo del terminal semanalmente si tu tienda tiene múltiples empleados o alta rotación de personal — los patrones de acceso irregulares son más fáciles de detectar antes de convertirse en un problema.
- Si un miembro del personal deja la empresa, elimina inmediatamente su PIN de cajero y su identificador de tarjeta para prevenir el acceso al terminal.
- Usa el evento de bloqueo para identificar terminales que puedan necesitar ajustar su tiempo de bloqueo automático — si los clientes activan con frecuencia bloqueos accidentales, el tiempo de inactividad podría estar configurado demasiado corto.
- Los PINs de gerentes deben cambiarse periódicamente. Actualízalos en el registro de descuentos del personal — el nuevo PIN se almacena en forma hasheada al guardar.