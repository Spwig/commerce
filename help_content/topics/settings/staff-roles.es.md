---
title: Roles del personal y permisos
---

Los roles del personal le permiten controlar exactamente qué puede ver y hacer cada miembro del equipo, tanto en el panel de administración como en el terminal de punto de venta (POS). Defina roles con permisos específicos, luego asígnelos a los miembros del personal. Un usuario puede tener múltiples roles, y sus permisos efectivos son la combinación de todos los roles asignados.

![Roles del personal](/static/core/admin/img/help/staff-roles/role-list.webp)

## Cómo funciona

1. Crea **roles** que definen un conjunto de permisos (por ejemplo, "Gestor de pedidos", "Cajero")
2. Cada rol controla dos tipos de acceso: **permisos del panel de administración** y **permisos del POS**
3. **Asigna roles** a los miembros del personal desde su página de perfil
4. Los permisos efectivos de un miembro del personal son la **unión** de todos sus roles — si cualquier rol otorga acceso, el usuario lo tiene
5. Los permisos se **cachean** para el rendimiento y se refrescan automáticamente cuando cambian los roles

## Roles predefinidos

Spwig incluye 7 roles integrados que cubren las estructuras de equipo más comunes. Estos no se pueden eliminar, pero puedes crear roles personalizados para necesidades más específicas.

| Rol | Acceso | Descripción |
|------|--------|-------------|
| **Propietario de la tienda** | Admin + POS | Acceso completo a todo. Para el administrador principal de la tienda. |
| **Gerente de la tienda** | Admin + POS | Operaciones de rutina — acceso completo a productos, pedidos, clientes, marketing y búsqueda. Solo lectura para diseño, correos electrónicos, pagos y configuraciones. |
| **Editor de contenido** | Admin | Gestiona páginas, entradas de blog, diseño y medios. Solo lectura para productos. |
| **Gestor de pedidos** | Admin | Maneja pedidos, envíos, devoluciones y servicio al cliente. Solo lectura para productos. |
| **Gerente de marketing** | Admin | Gestiona promociones, cupones, afiliados, programas de fidelidad y referidos. Solo lectura para productos, clientes y medios. |
| **Cajero** | Solo POS | Personal de primer línea del POS. Puede procesar ventas y verificar saldos de tarjetas regalo. Sin descuentos, devoluciones o gestión de efectivo. |
| **Cajero senior** | Solo POS | Personal experimentado del POS. Puede procesar devoluciones, aplicar descuentos (hasta el 25%), gestionar efectivo y cerrar turnos. |

## Crear un rol personalizado

Navegue a **Configuración > Roles del personal** y haga clic en **Añadir rol**.

### Configuración general

| Configuración | Descripción |
|---------|-------------|
| **Nombre de visualización** | El nombre del rol mostrado en el panel de administración (por ejemplo, "Personal de almacén") |
| **Descripción** | Una breve explicación de para qué sirve este rol |
| **Orden de clasificación** | Controla el orden de visualización en la lista de roles |
| **Icono** | Elija entre 20 iconos para identificar visualmente el rol |
| **Color de distintivo** | Color utilizado para los distintivos de roles (Azul, Verde, Naranja, Rojo, Turquesa, Gris) |
| **Panel de administración** | Alternar si este rol otorga acceso al panel de administración |
| **Terminales de POS** | Alternar si este rol otorga acceso a los terminales de POS |

### Categorías de permisos de administrador

La pestaña de permisos de administrador organiza todas las funciones de la plataforma en 13 categorías. Para cada categoría, establece uno de los tres niveles de acceso:

- **Ninguno** — Sin acceso a esta área (los elementos del menú están ocultos)
- **Ver** — Acceso de solo lectura (puede ver los datos pero no modificarlos)
- **Completo** — Acceso completo (puede ver, crear, editar y eliminar)

![Categorías de permisos](/static/core/admin/img/help/staff-roles/permission-categories.webp)

| Categoría | Qué controla |
|----------|-----------------|
| **Catálogo de productos** | Productos, categorías, marcas, atributos, stock, almacenes, activos digitales |
| **Pedidos y cumplimiento** | Pedidos, reembolsos, devoluciones, envíos, configuración de envío |
| **Clientes** | Perfiles de clientes, segmentos, análisis |
| **Contenido y páginas** | Páginas, entradas de blog, anuncios, formularios |
| **Diseño y tema** | Temas, plantillas de encabezado/pie de página, menús, tokens de diseño, CSS personalizado |
| **Marketing y promociones** | Promociones, cupones, afiliados, programas de fidelidad, referidos, feeds de productos |
| **Biblioteca de medios** | Imágenes, videos, carpetas, etiquetas |
| **Sistema de correo electrónico** | Cuentas de correo electrónico, plantillas, cola de entrega |
| **Pagos y facturación** | Proveedores de pago, transacciones, webhooks, suscripciones, tasas de cambio |
| **Búsqueda** | Configuración de búsqueda, sinónimos, redirecciones, análisis |
| **Configuración de la tienda** | Configuración del sitio, geolocalización, mapeos de países, reglas de negocio |
| **Gestión de POS** | Terminales de POS, turnos, movimientos de efectivo, plantillas de recibos |
| **Usuarios y roles** | Cuentas de usuarios del personal, roles, tokens de API |

Cuando un usuario tiene múltiples roles, el **nivel de acceso más alto** gana. Por ejemplo, si el Rol A otorga "Ver" a Productos y el Rol B otorga "Completo", el usuario obtiene acceso "Completo".

### Banderas de permisos de POS

Si el rol otorga acceso al POS, la pestaña de permisos del POS le permite ajustar exactamente qué puede hacer un operador de POS. Estos son independientes de los permisos de administrador y se verifican en el terminal de POS.

![Permisos de POS](/static/core/admin/img/help/staff-roles/pos-permissions.webp)

| Grupo | Permiso | Descripción |
|-------|-----------|-------------|
| **General** | Acceso al POS | Puede usar el sistema de POS en general |
| **Ventas y descuentos** | Descuentos manuales | Puede aplicar descuentos manuales en elementos de línea o a nivel de carrito |
| | Porcentaje máximo de descuento | El porcentaje máximo de descuento permitido (0–100) |
| | Sobrescritura de precios | Puede sobrescribir los precios de los productos en el mostrador |
| **Reembolsos y anulaciones** | Procesar reembolsos | Puede procesar reembolsos en pedidos de POS |
| | Anular pedidos | Puede anular pedidos de POS del turno actual |
| **Tarjetas regalo** | Emitir tarjetas regalo | Puede emitir nuevas tarjetas regalo en el mostrador |
| | Verificar el saldo de tarjetas regalo | Puede consultar los saldos de tarjetas regalo |
| **Gestión de efectivo** | Gestión de efectivo | Puede realizar operaciones de entrada y salida de efectivo |
| | Abrir caja registradora | Puede abrir la caja registradora sin una venta |
| | Cerrar turnos | Puede cerrar turnos y realizar la reconciliación de efectivo |
| **Informes** | Ver informes de POS | Puede ver informes de turnos y resúmenes de ventas |
| **Inventario** | Ajustes de inventario | Puede ajustar los niveles de inventario (recibir, dañar, recuentar, devolver) |

Para los permisos booleanos, si **cualquier** rol del usuario lo habilita, el usuario lo tiene. Para el Porcentaje máximo de descuento, el **valor más alto** entre todos los roles se aplica.

## Gestionar miembros del personal

Navegue a **Configuración > Gestión del personal** para ver y gestionar su equipo.

### Lista de personal

La lista de personal muestra a todos los usuarios con acceso al personal. Para cada miembro, puede ver:
- **Nombre y correo electrónico**
- **Roles asignados** (mostrados como distintivos de color)
- **Tipo de acceso** — Solo administrador, Solo POS o Ambos
- **Estado de 2FA** — Si se ha habilitado la autenticación de dos factores
- **Estado activo/inactivo**

Use los filtros para restringir por rol, tipo de acceso o estado de 2FA.

### Asignar roles al personal

1. Haga clic en un miembro del personal para abrir su perfil
2. En la sección **Roles**, verá tarjetas para cada rol disponible
3. Haga clic en el interruptor de cualquier tarjeta de rol para asignarla o quitarla
4. Los cambios tienen efecto inmediato — no se necesita un botón de guardar
5. El resumen de **Permisos efectivos** a continuación muestra el resultado combinado de todos los roles asignados

### Añadir un nuevo miembro del personal

1. Navegue a **Configuración > Gestión del personal** y haga clic en **Añadir miembro del personal**
2. Ingrese el correo electrónico, nombre y apellido del usuario
3. Establezca una contraseña temporal
4. Asigne uno o más roles
5. El usuario ahora puede iniciar sesión con el acceso que proporcionan sus roles

## Clonar roles

Para crear un nuevo rol basado en uno existente:

1. Abra el rol que desea copiar
2. Haga clic en **Clonar rol** en la parte inferior de la página
3. Se crea un nuevo rol con todos los mismos permisos
4. Rénamealo y ajusta los permisos según sea necesario
5. Guarda el nuevo rol

Esto es útil cuando necesitas un rol similar a uno existente con pequeñas diferencias — por ejemplo, un "Gerente junior" basado en "Gerente de tienda" pero con menos permisos.

## Cómo se aplican los permisos

### Panel de administración

- **Visibilidad del menú** — Las secciones del menú lateral se ocultan para las categorías donde el usuario tiene acceso "Ninguno"
- **Acceso a páginas** — Intentar visitar una página restringida muestra un error de permiso
- **Restricciones de acción** — Con acceso "Ver", los botones de edición y eliminación se ocultan y las acciones de guardar se bloquean
- **Bypass de superusuario** — Las cuentas de superusuario siempre tienen acceso completo, independientemente de las asignaciones de roles

### Terminal de POS

- **Puerta de inicio de sesión** — Solo los usuarios con al menos un rol que tenga "Terminales de POS" habilitado pueden iniciar sesión en el POS
- **Conmutadores de características** — Los botones y acciones de POS (reembolso, descuento, anulación, etc.) se muestran o ocultan según los permisos de POS combinados del usuario
- **Límite de descuento** — El Porcentaje máximo de descuento impone un límite estricto sobre cuán grande puede ser el descuento que un operador de POS aplica
- **Cumplimiento de API** — Todos los permisos de POS se verifican en la capa de API del servidor, no solo en la interfaz de usuario

## Consejos

- **Empiece con roles predefinidos** — Los 7 roles integrados cubren la mayoría de las estructuras de equipo. Cree roles personalizados solo cuando necesite un control de acceso más específico.
- **Use la función de clonar** — Cuando necesite un rol similar a uno existente, clónelo y haga ajustes en lugar de construirlo desde cero.
- **Asigne múltiples roles cuando sea necesario** — Un miembro del personal que maneje tanto pedidos como marketing puede asignársele tanto el rol de "Gestor de pedidos" como el de "Gestor de marketing". Los permisos se combinan automáticamente.
- **Separe el acceso de administrador y POS** — Los cajeros generalmente no necesitan acceso de administrador, y el personal de oficina no necesita acceso a POS. Use los interruptores de acceso para mantener las cosas limpias.
- **Establezca límites de descuento para el personal de POS** — El Porcentaje máximo de descuento impide que los cajeros apliquen descuentos excesivos. Establezca en 0 para no permitir descuentos, o un límite razonable como 10–25% para el personal senior.
- **Revise los roles periódicamente** — A medida que su equipo crece, revise las asignaciones de roles para asegurarse de que el personal tenga el acceso mínimo necesario para su trabajo. Quite los roles cuando las personas cambien de posición.
- **Habilite 2FA para roles sensibles** — El personal con acceso a pagos, configuraciones o gestión de usuarios debe tener la autenticación de dos factores habilitada para la seguridad.