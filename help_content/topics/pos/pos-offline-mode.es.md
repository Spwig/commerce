---
title: Modo sin conexión del POS y instalación de la aplicación
---

<!-- screenshots-needed:
- url: /pos/
  filename: pos-pwa-idle.webp
  description: POS PWA en estado inactivo — vista principal de selección de inicio de sesión/terminal mostrando la marca Spwig POS
  save-to: core/static/core/admin/img/help/pos-offline-mode/
  viewport: 1440x900
  notes: Add-to-Home-Screen screenshots (iPad Safari, Android Chrome) son específicas del sistema operativo/navegador
         capturas de referencia anotadas. La sesión que captura esto debe usar la emulación del dispositivo
         o imágenes de referencia en lugar de intentar activar el prompt de instalación del navegador.
-->

El Spwig POS es una Aplicación Web Progresiva (PWA). Se ejecuta completamente en el navegador y puede instalarse en la pantalla de inicio de un dispositivo como una aplicación nativa. Debido a que la aplicación, su catálogo de productos y el historial de pedidos recientes se almacenan localmente en el dispositivo, su caja registradora sigue funcionando durante interrupciones breves de la red y conexiones lentas.

Este tema explica exactamente qué funciona cuando se pierde la conexión, cómo se reconcilian las ventas pendientes cuando vuelve, cómo instalar el POS en la pantalla de inicio de un dispositivo y cómo llegan las actualizaciones a los dispositivos instalados.

## Cómo funciona el modo sin conexión

Cuando abre el POS por primera vez en un dispositivo, el navegador descarga y almacena en caché toda la aplicación — su interfaz, imágenes y todo el código de soporte. Un componente en segundo plano llamado Service Worker gestiona este caché. Desde ese momento en adelante, la aplicación carga desde el caché local incluso si el servidor no está disponible.

Además del caché de la aplicación, el POS mantiene una base de datos local en el dispositivo (usando el almacenamiento IndexedDB integrado del navegador). Esta base de datos contiene:

- **Productos y variantes** — sincronizados desde su catálogo y actualizados cada cinco minutos mientras está en línea
- **Categorías** — sincronizadas al iniciar y actualizadas junto con los productos
- **Niveles de inventario** — sincronizados cada dos minutos mientras está en línea (usando una estrategia de red primero que recurre a los datos en caché si el servidor no responde dentro de tres segundos)
- **Registros de clientes** — hasta 1.000 clientes recientes
- **Historial de pedidos** — un número configurable de pedidos recientes del POS (por defecto: 500 pedidos en 14 días; configurado por terminal en **POS > Terminales POS**)
- **Imágenes de productos** — almacenadas localmente durante un máximo de 24 horas

Cuando el POS detecta que el dispositivo ha pasado a modo sin conexión, aparece una barra en la parte superior de la pantalla: **"Modo sin conexión - Las ventas se sincronizarán cuando se restaure la conexión."** La caja registradora continúa operando usando los datos almacenados localmente.

## Funcionalidades disponibles en modo sin conexión

| Función | Disponibilidad en modo sin conexión |
|---------|---------------------|
| Búsqueda y navegación de productos | Disponible — utiliza el catálogo almacenado localmente |
| Escaneo de códigos de barras | Disponible — los escaneos buscan productos en el caché local |
| Añadir artículos al carrito | Disponible |
| Aplicar descuentos manuales | Disponible |
| Aplicar códigos de cupón | No disponible — la verificación del saldo requiere una conexión activa |
| Pagos en efectivo | Disponible — registrados localmente y encolados para sincronización |
| Pagos con tarjeta (Entrada Manual) | Disponible — el cajero procesa en un terminal separado y introduce la referencia; registrados localmente y encolados para sincronización |
| Pagos con tarjeta (lector integrado — Terminal Stripe, etc.) | No disponible — los lectores de tarjetas integrados se comunican con la red de pagos en tiempo real |
| Pagos con tarjetas regalo | No disponible — la búsqueda de saldo requiere una conexión activa |
| Pagos divididos combinando efectivo y tarjeta manual | Disponible |
| Impresión de recibos a una impresora de red | Disponible si la impresora está en la misma red local que el dispositivo — la impresión no requiere acceso a internet, solo conectividad de red local |
| Recibos digitales (correo electrónico/SMS/WhatsApp) | No disponible — el envío requiere una conexión activa |
| Navegación por historial de pedidos | Disponible — muestra pedidos almacenados con una barra indicando que está viendo datos sin conexión |
| Devoluciones y anulaciones | No disponible — estas requieren una conexión activa |
| Consulta de puntos de lealtad del cliente | No disponible |
| Abrir y cerrar turnos | Disponible — el estado del turno se almacena localmente |

## Ventas pendientes y sincronización cuando vuelve la conexión

Las ventas en modo sin conexión no se pierden.


Cuando el registro no puede alcanzar al servidor, cada venta completada se escribe en una cola local (el almacén `pendingTransactions` en la base de datos local del dispositivo).

La venta incluye todos los elementos del carrito, cantidades, precios, método de pago y la hora en que se completó.

Cuando se restaura el acceso a internet, el POS hace lo siguiente automáticamente:

1. Detecta la reconexión mediante el evento `online` del navegador
2. Muestra un banner: **"Sincronizando N transacción(es) pendiente(s)..."**
3. Envía las ventas en cola al backend en orden, usando un horario de reintento con retroceso exponencial si el primer intento falla (hasta 10 reintentos dentro de una ventana máxima de cinco minutos por intento)
4. Marca cada venta como sincronizada una vez que el backend confirme que se realizó

**Protección contra ventas duplicadas** — cada venta en cola se le asigna un ID local único antes de salir del dispositivo. El backend verifica este ID antes de crear un pedido. Si se envía la misma venta dos veces (por ejemplo, porque un reintento se solapó con un primer intento exitoso), el backend ignora la duplicada. Nunca terminarás con ventas contadas dos veces.

**Detección de conflictos** — en casos raros, el backend puede marcar una venta en cola como conflicto (por ejemplo, si un producto fue eliminado en el servidor mientras el dispositivo estaba desconectado). Las ventas conflictivas aparecen en **POS > Configuración > Transacciones pendientes** para que las revise y las resuelva manualmente.

**Ajustes de inventario** fuera de línea se manejan de la misma manera: los cambios de inventario realizados mientras se está desconectado se colocan en cola y se reproducen cuando se restablece la conexión. Las cifras de inventario locales en el dispositivo se actualizan inmediatamente para que el cajero vea un recuento exacto (estimado).

## Instalación del POS en la pantalla de inicio del dispositivo

Instalar el POS en la pantalla de inicio le da una experiencia en pantalla completa sin barra de direcciones del navegador, un icono de acceso directo en el dispositivo y tiempos de inicio más rápidos.

### iPad (Safari)

1. Abra Safari y navegue hasta la URL del POS de su tienda: `https://yourstore.com/pos/`
2. Inicie sesión y complete el emparejamiento inicial si es un nuevo dispositivo.
3. Toque el botón **Compartir** (el cuadrado con una flecha hacia arriba) en la barra de herramientas de Safari.
4. Desplácese hacia abajo en la hoja de compartir y toque **Añadir a pantalla de inicio**.
5. Edite el nombre si lo desea (por defecto es "Spwig POS") y toque **Añadir**.

El icono del POS ahora aparece en la pantalla de inicio de su iPad. Al tocarlo, abre la aplicación en pantalla completa sin la barra de navegador de Safari.

> **Nota:** Se requiere Safari en el iPad para la opción Añadir a pantalla de inicio. Los navegadores de terceros en iOS (Chrome, Firefox) no admiten la instalación de PWA hasta mediados de 2025.

### Android (Chrome)

1. Abra Chrome y navegue hasta la URL del POS de su tienda: `https://yourstore.com/pos/`
2. Inicie sesión y complete el emparejamiento si es necesario.
3. Toque el **menú de tres puntos** (arriba a la derecha) y toque **Instalar app** (o **Añadir a pantalla de inicio** en versiones antiguas de Chrome).
4. Confirme toque **Instalar**.

El icono del POS aparece en la pantalla de inicio y en el cajón de aplicaciones. Al iniciar desde el icono, abre la aplicación en modo independiente.

### Escritorio (Chrome o Edge)

1. Navegue hasta la URL del POS de su tienda en Chrome o Edge.
2. Busque el **icono de instalación** en la barra de direcciones del navegador (un monitor de computadora con una flecha hacia abajo, o un icono de "+" según la versión).
3. Alternativamente, abra el **menú de tres puntos** y elija **Instalar Spwig POS** (Chrome) o **Apps > Instalar este sitio como aplicación** (Edge).
4. Confirme la instalación.

El POS se abre como una ventana independiente sin pestañas del navegador ni la barra de direcciones. Aparece en la lista de aplicaciones del sistema y puede fijarse en la barra de tareas.

## Cómo se actualiza la aplicación

El POS gestiona sus propias actualizaciones a través del Service Worker. No es necesario que visite una tienda de aplicaciones ni que descargue nada manualmente.

**Ciclo de actualización:**

1.

Cada vez que abre el POS (o la pestaña se vuelve activa después de estar en segundo plano), el Service Worker verifica el servidor en busca de una nueva versión.
2.

Si hay una nueva versión disponible, el Service Worker la descarga en segundo plano mientras continúa trabajando — su sesión actual no se interrumpe.
3.

La actualización se aplica la próxima vez que abra el POS.

Si la app ya está abierta y hay una sincronización pendiente, el POS espera a que la cola se vacíe antes de indicar que una recarga está lista, para evitar interrumpir un turno activo con ventas no sincronizadas.

**¿Qué significa "recargar" cuando hay ventas pendientes** — si ves un aviso para recargar una actualización y tienes ventas sin conexión pendientes, cierra el turno actual de forma limpia (o espera hasta que el banner de sincronización se quite) antes de recargar. Recargar mientras hay ventas en cola no las elimina — permanecen en la base de datos local — pero es más seguro sincronizar primero para confirmar que se recibieron.

**Verificar la versión instalada** — abre el POS, toca el **icono de menú** (tres líneas horizontales) y ve a **Configuración**. La versión actual del build se muestra en la parte inferior del panel de configuración.

## Almacenamiento y limpieza de la instalación

El POS almacena varios tipos de datos localmente:

| Qué | Tamaño típico |
|------|-------------|
| Capa de la app (HTML, CSS, JS, iconos) | ~3–5 MB |
| Catálogo de productos (texto y metadatos) | 1–10 MB según el tamaño del catálogo |
| Imágenes de productos (caché) | 5–50 MB según el tamaño del catálogo |
| Historial de pedidos | 1–5 MB (500 pedidos) |
| Registros de clientes | 1–3 MB (1,000 clientes) |
| Cola de transacciones pendientes | Mínimo; se limpia al sincronizar |

**Si el dispositivo tiene poca memoria de almacenamiento** — los navegadores aplican presión al almacenamiento en caché cuando el dispositivo está lleno. El POS establece sus cachés como persistentes donde el navegador lo permite, pero en dispositivos muy llenos, el navegador puede eliminar primero las imágenes de productos. Si las imágenes dejan de cargar, el POS las recacheará en la próxima sincronización. Las ventas sincronizadas y la capa de la app no se ven afectadas.

**Restablecer la instalación** — si el POS se comporta de forma inesperada (atascado en una versión antigua, catálogo que no se actualiza, sincronización permanentemente atascada), puedes realizar un restablecimiento limpio:

1. **Desinstalar la app** — en móvil, presiona y mantén el icono del POS y elige **Eliminar** o **Desinstalar**. En escritorio, haz clic derecho en la barra de título de la ventana de la app y elige **Desinstalar**.
2. Abre directamente la URL del POS en el navegador y vuelve a iniciar sesión.
3. El dispositivo se le pedirá el código de emparejamiento de 8 caracteres del terminal nuevamente. Puedes encontrar o regenerar este código en el administrador en **POS > Terminales POS** — abre el terminal y haz clic en **Regenerar código de emparejamiento**.
4. Un emparejamiento recién generado fuerza una sincronización completa de todos los datos en caché.

> **Después de restablecer**: cualquier venta sin conexión que estuviera en cola pero no se sincronizó antes del restablecimiento se perderá, ya que la base de datos local se limpia. Asegúrate siempre de restaurar la conexión y que el banner de sincronización se quite antes de restablecer una instalación.

## Solución de problemas

### El POS está atascado en una versión antigua

El Service Worker puede no haber activado aún la nueva versión. Intente cerrar todas las pestañas del navegador que tengan el POS abierto, luego reabrirlo. Si el problema persiste, restablezca la instalación como se describe anteriormente.

### El banner "Sin conexión" no se quita

Verifique que el dispositivo tenga acceso a internet fuera del POS (intente cargar otro sitio). Si el dispositivo está en línea pero el banner persiste:

- El servidor del POS puede estar temporalmente inaccesible — espere un minuto y el POS intentará automáticamente de nuevo.
- Si está en una red que requiere una página de inicio de sesión (portal cautivo), abra una nueva pestaña del navegador, complete el inicio de sesión y luego regrese al POS.

### Un producto está ausente en el POS pero existe en el administrador

El POS sincroniza productos cada cinco minutos mientras está en línea. Si agregó un producto en el administrador hace muy poco, toque el **icono de menú** y vaya a **Configuración > Sincronizar ahora** para desencadenar una sincronización inmediata. Si el producto aún no aparece, confirme que esté marcado como **Activo** y que no esté excluido de la disponibilidad en el POS en la configuración del producto.

### Las transacciones pendientes están atascadas en el estado "Conflicto"

Vaya a **POS > Configuración** (dentro de la app del POS en sí) y revise el panel de **Transacciones Pendientes**.

Las transacciones en conflicto suelen ser causadas por un producto o precio que cambió entre el momento en que se realizó la venta sin conexión y cuando se sincronizó.


Puedes ver los detalles de la venta y, si la venta se recibió correctamente, marcarla como revisada.

## Consejos

- Ejecuta el POS en un dispositivo dedicado que permanezca conectado a tu red Wi-Fi local. Los breves cortes de conexión a Wi-Fi se manejan automáticamente, pero un dispositivo que esté desconectado durante períodos prolongados necesitará más tiempo para re-sincronizarse cuando se reconecte.
- Los intervalos de sincronización son por dispositivo. Si tienes múltiples terminales, cada uno se sincroniza de forma independiente. Una venta en un terminal aparecerá inmediatamente en el administrador al sincronizar, pero el caché de pedidos local del otro terminal solo se actualiza en su propio ciclo de sincronización.
- Antes de una interrupción planificada de internet (por ejemplo, al mudarse a un evento sin Wi-Fi), abre el POS mientras aún estés conectado para que el catálogo y los datos de inventario estén completamente actualizados. Las ventas en efectivo se colarán de forma confiable; simplemente evita los pagos integrados con tarjeta hasta que estés de vuelta en línea.
- Si solo necesitas ventas en efectivo en un evento, el método de pago con tarjeta manual (el cajero procesa en un terminal independiente y ingresa una referencia) también funciona sin conexión para transacciones con tarjeta.
- Mantén el dispositivo enchufado durante un turno prolongado — la base de datos local y el proceso de sincronización no afectan significativamente la batería en comparación con la pantalla, pero un dispositivo cargado siempre es más seguro para el comercio.