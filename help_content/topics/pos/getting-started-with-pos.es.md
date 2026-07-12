---
title: '# Comenzando con POS'
---

Spwig POS convierte cualquier tableta o navegador en un cajero completo en tienda — conectado a tu catálogo de productos, inventario y historial de pedidos. Esta lista de verificación te guía desde una instalación reciente hasta realizar tu primera venta. Cada paso enlaza a un tema dedicado si deseas los detalles completos.

![Panel de POS](/static/core/admin/img/help/pos/getting-started-dashboard.webp)

## Paso 1: Habilitar POS para una ubicación de tienda

Los terminales de POS están vinculados a una ubicación física de tienda. En Spwig, las ubicaciones de tienda son almacenes marcados como ubicaciones de venta al por menor.

1. Navega a **Catálogo > Almacenes** en tu barra lateral de administración.
2. Abre el almacén que deseas usar como tienda, o crea uno nuevo.
3. Marca el interruptor **Ubicación de venta al por menor** y ingresa un **nombre de visualización de POS** (por ejemplo, "Tienda de la Calle Alta"). Este nombre aparece en los recibos y en el selector de terminales.
4. Guarda el almacén.

Si tienes múltiples tiendas o deseas agruparlas para informes regionales, crea primero un **Grupo de Tiendas** en **POS > Grupos de Tiendas**, luego asigna cada almacén a ese grupo. Los grupos de tiendas te permiten establecer una moneda compartida, zona horaria y plantilla de recibo que todas las ubicaciones del grupo heredan.

## Paso 2: Crear o verificar al menos una cuenta de personal con acceso a POS

Tu personal inicia sesión en el POS usando las mismas credenciales que usa para el administrador de Spwig. Cualquier cuenta de personal con estado **Activo** y al menos el permiso `pos_admin` puede acceder al POS.

Para verificar o conceder acceso, ve a **Configuración > Gestión de Personal**, abre la cuenta del miembro del personal y confirma que tenga el rol de POS adecuado asignado. No se necesita una cuenta de POS separada.

## Paso 3: Registrar tu primer terminal de POS

Un terminal representa un solo cajero o dispositivo. Lo registras en el administrador, luego vinculas un dispositivo físico a él usando un código de emparejamiento único.

1. Navega a **POS > Terminales de POS** y haz clic en **+ Añadir Terminal de POS**.
2. Dale al terminal un nombre (por ejemplo, "Cajero Frontal") y asígnalo a la ubicación de tienda que habilitaste en el Paso 1.
3. Guarda el terminal. Spwig genera un **código de emparejamiento de 8 caracteres** — lo verás en la página de detalles del terminal.
4. En el dispositivo que deseas usar como cajero, abre un navegador y ve a `/pos/`.
5. Ingresa el código de emparejamiento cuando se te lo pida. El dispositivo ahora está vinculado a este terminal.

El código de emparejamiento es de uso único. Si necesitas reemparejar un dispositivo, abre el terminal en el administrador y haz clic en **Regenerar código de emparejamiento**.

Para opciones de configuración de hardware (impresora de recibos, escáner de códigos de barras, caja registradora), consulta [Configuración del Terminal de POS](pos-terminal-setup).

## Paso 4: Configurar un proveedor de pago

El proveedor de pago conecta tus lectores de tarjetas a una red de pago como Stripe Terminal o Square. Usa el asistente de configuración de 5 pasos para ingresar tus credenciales.

1. Navega a **POS > Proveedores de Pago** y haz clic en **Configurar proveedor**.
2. El asistente se abre en `/admin/pos/terminal-provider/wizard/step1/`.

![Asistente del Proveedor de Pago](/static/core/admin/img/help/pos/getting-started-provider-wizard-step1.webp)

3. Selecciona tu proveedor (por ejemplo, **Stripe Terminal**) y sigue las instrucciones en pantalla a través de los cinco pasos: seleccionar proveedor → instrucciones de configuración → ingresar credenciales → probar conexión → configurar ubicación.
4. Un distintivo verde **Conectado** confirma que la integración está activa.

Si solo necesitas efectivo y entrada manual de tarjetas, selecciona **Manual** como proveedor — no se requieren credenciales.

Para ver los campos de credenciales detallados para cada proveedor compatible, consulta [Configuración del proveedor de pago POS](pos-payment-provider-setup).

## Paso 5: Asociar un lector de tarjetas

Con un proveedor de pago conectado, puedes asociar un lector de tarjetas físico a uno de tus terminales usando el asistente de 3 pasos para el lector.

1. Navega a **POS > Lectors de tarjetas** y haz clic en **Añadir lector**.
2. El asistente para el lector comienza en `/admin/pos/reader/wizard/step1/`.
3. Selecciona tu proveedor, luego elige **Registrar nuevo dispositivo** (introduce el código mostrado en la pantalla del lector) o **Descubrir existente** (Spwig recupera lectores ya registrados con el proveedor).
4. En el último paso, asigna el lector al terminal que creaste en el Paso 3.

Cada terminal admite un lector de tarjetas asignado. Puedes reasignar lectores en cualquier momento desde la lista de Lectors de tarjetas.

## Paso 6: Diseña tu recibo (opcional para el primer día)

Spwig crea una plantilla de recibo predeterminada automáticamente. Puedes comenzar a vender inmediatamente sin tocarla — la predeterminada imprime el nombre de tu tienda, la dirección, la venta detallada, el método de pago y un pie de página "¡Gracias por su compra!".

Cuando estés listo para personalizar, ve a **POS > Plantillas de recibo**. Las opciones incluyen tu logotipo, número de identificación fiscal, promoción con código QR, política de devolución y ancho de papel (58mm o 80mm para impresoras térmicas). Puedes crear plantillas separadas por tienda o por grupo de tiendas.

## Paso 7: Abre tu primer turno

Los turnos rastrean quién procesó las ventas y cuánto efectivo debería estar en la caja. Los cajeros abren y cierran turnos directamente en el POS.

1. En el dispositivo emparejado, ve a `/pos/` e inicia sesión con tus credenciales de personal.
2. Selecciona el terminal y la ubicación de la tienda.
3. Spwig te pide que **cuentes el efectivo inicial** — introduce la cantidad de efectivo ya en la caja (introduce `0` si la caja está vacía).
4. Toca **Abrir turno**. La caja ahora está lista para vender.

Para una explicación completa de los turnos, movimientos de efectivo y reportes de conciliación, consulta [Gestión de turnos POS](pos-shifts).

## Paso 8: Realiza tu primera venta

Una vez que un turno esté abierto, vender es sencillo:

1. Busca productos por nombre, escanea un código de barras o navega por categorías para agregar artículos al carrito.
2. Aplica un descuento o un código de cupón si es necesario.
3. Toca **Cobrar** para comenzar el pago. Elige el método de pago (efectivo, tarjeta mediante lector o pago dividido).
4. Para pagos con tarjeta, el lector le pide al cliente que toque o inserte su tarjeta.
5. El recibo se imprime automáticamente (o se muestra una opción de recibo digital). La orden se guarda en tu historial de pedidos en tiempo real.

## Paso 9: Cierra el turno al final del día

Cerrar un turno bloquea la caja y genera un resumen de conciliación.

1. Desde el menú POS, toca **Cerrar turno**.
2. Cuenta el efectivo en la caja y introduce el total cuando se te lo pida.
3. Spwig calcula el efectivo esperado basado en el efectivo inicial, ventas en efectivo y cualquier movimiento de efectivo durante el turno, y te muestra la diferencia.
4. Confirma para cerrar. El informe del turno se guarda y es visible en **POS > Turnos** en tu administración.

Registra cualquier efectivo retirado o añadido a la caja durante el día como **movimientos de efectivo** (a través del menú de turno) en lugar de ajustar el conteo final — esto mantiene tu conciliación precisa.

## Consejos

- Completa los Pasos 1 a 5 antes de tu primer día de operaciones.

Los Pasos 6 a 9 se pueden realizar el día de operaciones.
- Usa una contraseña de personal fuerte pero memorable — el personal de POS introduce sus credenciales en la caja, por lo que contraseñas demasiado complejas los ralentizan.
- Si el lector de tarjetas no aparece en línea, haz clic en **Sincronizar lectores** en la página de Lectors de tarjetas para recuperar el estado más reciente de tu proveedor.
- Prueba el flujo completo (abrir turno → venta → recibo → cerrar turno) con una transacción de prueba de $0.01 antes de tu período de operaciones ocupado.
- El POS funciona sin conexión para ventas en efectivo básicas.

Los pagos con terminal de tarjeta requieren una conexión a internet para autorizar.
- Puedes tener múltiples terminales en una ubicación de tienda — añade un nuevo registro de terminal en el administrador y párquelo a un dispositivo diferente.