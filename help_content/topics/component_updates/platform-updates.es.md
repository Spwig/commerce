---
title: Actualizaciones de la plataforma
---

Su instalación de Spwig está construida a partir de una colección de componentes — temas, widgets, integraciones, elementos del constructor de páginas y conexiones de proveedores — cada uno con su propia versión que puede actualizarse de forma independiente. El Registro de Componentes le ofrece una vista central de todo lo instalado, muestra qué componentes tienen actualizaciones pendientes y le permite instalar o revertir actualizaciones en cualquier momento.

![Vista general del Registro de Componentes](/static/core/admin/img/help/platform-updates/component-registry-overview.webp)

## Entendiendo el registro de componentes

Navegue hasta **Panel de control del sistema > Actualizaciones de componentes** para ver cada componente instalado en su tienda. Cada fila muestra:

- **Nombre** — el nombre de visualización del componente
- **Tipo** — qué tipo de componente es (tema, widget, integración, etc.)
- **Versión actual** — la versión que actualmente está en ejecución en su tienda
- **Estado de actualización** — si hay una actualización disponible
- **Canal** — qué canal de actualización sigue el componente
- **Actualización automática** — si las actualizaciones se instalan automáticamente
- **Bloqueado** — si el componente está congelado en su versión actual

El panel en la parte superior de la página muestra conteos resumidos: total de componentes instalados, cuántos tienen actualizaciones disponibles y cuántos están actualizados.

### Tipos de componentes

| Tipo | Qué es |
|------|------------|
| Tema | El diseño visual de su tienda |
| Widget | Bloques reutilizables del constructor de páginas |
| Elemento del constructor de páginas | Elementos personalizados para el constructor de páginas |
| Utilidad del constructor de páginas | Herramientas y utilidades del editor |
| Plantilla de encabezado/pie de página | Diseños de encabezado y pie de página |
| Proveedor de envío | Integraciones con transportistas (FedEx, UPS, etc.) |
| Proveedor de correo electrónico | Servicios de entrega de correo electrónico |
| Proveedor de pago | Integraciones con pasarelas de pago |
| Proveedor de tasas de cambio | Fuentes de datos de tasas de cambio de moneda |
| Proveedor de traducción | Servicios de traducción con inteligencia artificial |
| Paquete de idioma | Archivos de traducción de la interfaz |

## Canales de actualización

Cada componente sigue un canal de actualización que controla qué lanzamientos recibe. Puede asignar cada componente a un canal diferente según el nivel de riesgo que esté dispuesto a asumir.

| Canal | Descripción | Mejor para |
|---------|-------------|----------|
| **Estable** | Lanzamientos listos para producción, completamente probados | Todos los componentes en tiendas en producción |
| **Beta** | Construcciones previas al lanzamiento para probar nuevas funciones antes de que se estabilicen | Componentes no críticos que desee previsualizar |
| **Desarrollo** | Funciones más recientes, pueden ser inestables | Solo entornos de prueba |
| **Seguridad** | Solo parches de seguridad críticos, entregados con la máxima prioridad | Componentes donde la estabilidad es fundamental |

Para cambiar el canal de un componente, haga clic en su nombre para abrir la vista de detalles, luego seleccione un nuevo valor en el campo **Canal de actualización** y guárdelo.

## Verificar actualizaciones

Spwig verifica actualizaciones automáticamente a intervalos configurados en la configuración del servidor de actualizaciones (por defecto: cada 24 horas). Para verificar inmediatamente:

1. Navegue hasta **Panel de control del sistema > Actualizaciones de componentes**
2. Haga clic en el botón **Verificar actualizaciones** en la parte superior de la página
3. El sistema contacta al servidor de actualizaciones de Spwig y actualiza el estado de actualización de todos los componentes
4. Los componentes con actualizaciones disponibles se resaltan, y el recuento de **Actualizaciones disponibles** se actualiza

También puede desencadenar una verificación de actualización para componentes individuales usando la acción **Verificar actualizaciones** del menú de acciones de la lista.

## Instalando actualizaciones

### Actualizando un solo componente

1. Navegue hasta **Panel de control del sistema > Actualizaciones de componentes**
2. Encuentre el componente que desea actualizar — los componentes con actualizaciones disponibles muestran un indicador de actualización junto a su versión
3. Haga clic en el botón **Instalar actualización** en la fila de ese componente
4. Confirme la actualización cuando se le solicite
5. La actualización se descarga, verifica y se instala — un indicador de progreso muestra cada etapa
6. Una vez completado, el **Versión actual** del componente se actualiza al nuevo número de versión

### Actualizando múltiples componentes

1.

Seleccione las casillas junto a los componentes que desea actualizar
2.



Elige **Instalar actualizaciones** desde el menú desplegable **Acción**
3.

Haz clic en **Ir** para continuar
4.

Las actualizaciones se instalan en orden de dependencia — los componentes en los que otros dependen se actualizan primero

### ¿Qué ocurre durante una actualización

El proceso de actualización pasa por través de estas etapas:

1. **Comprobación** — confirma que la actualización está disponible y que tu licencia es válida
2. **Descarga** — recupera el paquete desde el servidor de actualizaciones de Spwig
3. **Verificación** — comprueba la integridad del paquete contra un checksum SHA-256
4. **Extracción** — desempaqueta los nuevos archivos
5. **Implementación** — activa la nueva versión
6. **Comprobación de salud** — verifica que el componente funcione correctamente después de la actualización

Si alguna etapa falla, el sistema intenta automáticamente restaurar la versión anterior.

## Actualizaciones a nivel de plataforma

Además de componentes individuales, Spwig puede recibir actualizaciones a nivel de plataforma que actualizan el motor de tienda principal. Estas actualizaciones pasan por un proceso más detallado que incluye migraciones de base de datos y un breve periodo de mantenimiento.

Navega a **Panel de control del sistema > Actualizaciones de la plataforma** para ver y gestionar las actualizaciones a nivel de plataforma por separado de los componentes individuales.

### Revisar lo nuevo antes de instalar

Haz clic en **Buscar actualizaciones** para ver si hay una nueva versión de la plataforma disponible. Cuando se encuentra una, la tarjeta **Actualización disponible** muestra el cambio de versión (por ejemplo, `v1.7.0 → v1.7.1`), el **Tamaño del paquete**, **Tiempo estimado**, y el **Canal** de actualización — y una vista previa de **Lo nuevo** para que puedas ver qué cambió antes de decidir instalar:

- Una línea de resumen que describe la versión
- Una lista con viñetas de los principales cambios en esa versión (hasta cinco, con una nota si hay más)

Si la actualización cambia tu esquema de base de datos, aparece un aviso **Requiere migración de base de datos** con un tiempo estimado. Las actualizaciones de seguridad muestran un distintivo **Actualización de seguridad** que recomienda que las instales de inmediato. Lee la vista previa de **Lo nuevo** antes de instalar — es la forma más rápida de ver si una versión requiere alguna atención adicional, como pasos indicados después de completar la actualización.

El historial de actualizaciones de la plataforma se muestra más abajo en la página. Cada entrada muestra la transición de versión (por ejemplo, `v1.3.2 → v1.3.3`), el estado y la duración del proceso de actualización.

Las actualizaciones de seguridad se marcan por separado y, si **Instalar automáticamente actualizaciones de seguridad** está habilitado en la configuración de tu servidor de actualizaciones, se instalan automáticamente sin necesidad de acción manual.

## Ver el historial de versiones

Para ver todas las versiones anteriormente instaladas de un componente:

1. Haz clic en el nombre del componente para abrir su vista de detalles
2. Desplázate hasta la sección **Versiones del componente** en la parte inferior de la página
3. Cada entrada de versión muestra el número de versión, cuándo se instaló, el método de instalación y su estado de salud

El sistema mantiene disponibles las tres últimas versiones instaladas para realizar un rollback. Las versiones más antiguas se eliminan automáticamente.

## Realizar un rollback de un componente

Si una actualización causa problemas, puedes volver a una versión anterior:

1. Abre la vista de detalles del componente
2. Desplázate hasta la sección **Rollback**
3. Selecciona la versión que deseas restaurar
4. Haz clic en **Volver a esta versión**

Solo las versiones marcadas como **Rollback disponible** pueden restaurarse. El registro del rollback indica quién inició el rollback y cuándo.

## Bloquear componentes

Bloquear un componente impide que se instalen actualizaciones, incluidas las automáticas. Esto es útil cuando tienes personalizaciones o integraciones que dependen de una versión específica.

1. Abre la vista de detalles del componente
2. Marca la casilla **Bloqueado** en la sección **Bloqueo y congelamiento**
3. Ingresa un motivo en **Razón de bloqueo** para que tu equipo entienda por qué está congelado
4. Guarda el registro

Los componentes bloqueados se muestran con un indicador de bloqueo en la lista del registro. Para desbloquear, desmarca **Bloqueado** y guarda.

## Leer los registros de actualización

El registro de actualización registra cada operación de instalación, actualización, rollback y comprobación de salud:

1.

Abre la vista de detalles de un componente
2.

Los **Registros de actualización** son visibles en línea en la parte inferior de la página
3.



Cada entrada muestra: la acción realizada, las horas de inicio y fin, las versiones antigua y nueva, si fue automática o manual, y cualquier mensaje de error si la operación falló

Las entradas de registro con un estado **Fallido** incluyen el mensaje de error completo para ayudar en la solución de problemas.

## Habilitar actualizaciones automáticas

Puedes permitir que Spwig instale actualizaciones automáticamente cuando estén disponibles:

1. Abre la vista de detalles del componente
2. Marca **Actualización Automática** en la sección **Versión y Estado de Actualización**
3. Guarda el registro

Con la actualización automática habilitada, el sistema instalará las actualizaciones durante el próximo ciclo de verificación programado. Las actualizaciones de seguridad siguen la configuración global **Instalar automáticamente actualizaciones de seguridad**, independientemente de la configuración individual del componente.

## Consejos

- Siempre actualiza en el canal **Estable** para temas y proveedores de pago — estos son los componentes más orientados al cliente y la estabilidad es lo más importante
- Bloquea un componente antes de realizar modificaciones personalizadas en él, y registra claramente la razón para que los miembros del equipo futuros sepan que no deben actualizarlo
- Revisa las **Notas de Lanzamiento** en la entrada de versión del componente antes de instalar un salto de versión importante — los cambios rotos se indican allí
- Antes de instalar una actualización de la plataforma, lee la vista previa de **¿Qué es nuevo?** en la página **Actualizaciones de la Plataforma** — para ver las notas de lanzamiento completas, incluyendo cualquier paso adicional que puedas necesitar, continúa en la página **Actualización del Sistema**
- Después de una actualización, navega hasta la sección afectada de tu tienda para confirmar que todo se ve y funciona como se espera antes de declarar la actualización completa
- Si la actualización automática está habilitada en un componente, supervisa periódicamente los **Registros de Actualización** para asegurarte de que las actualizaciones automáticas se completen con éxito