---
title: Gestion de terminales POS
---

La gestión de terminales POS es la base de sus operaciones minoristas. Cada terminal representa un dispositivo físico (tableta, computadora o hardware POS dedicado) donde el personal procesa ventas. Configure terminales con asignaciones de almacén, autorizaciones de personal, integraciones de hardware y configuraciones de sincronización en línea. Supervise el estado de los terminales con un seguimiento en tiempo real del pulso del corazón y desbloquee los terminales de forma remota cuando surjan problemas. Una gestión adecuada de los terminales garantiza operaciones suaves en tienda y evita conflictos de configuración en múltiples ubicaciones.

Navegue hasta **POS > Terminales** para registrar nuevos terminales, ver el estado en línea/descargado y gestionar todas las configuraciones de los terminales.

![Lista de terminales](/static/core/admin/img/help/managing-pos-terminals/terminal-list.webp)

## Vista de la lista de terminales

La lista de terminales muestra todos los terminales registrados con información de estado clave:

**Nombre del terminal** - Etiqueta descriptiva para el terminal (ej. "Checkout 1", "Register principal", "Terminal móvil")

**UUID** - Identificador único generado automáticamente al crear (usado internamente para la identificación del dispositivo)

**Almacén** - Ubicación física asignada a este terminal (determina la disponibilidad de stock y atribución de pedidos)

**Estado en línea** - Indicador en vivo que muestra si el terminal está actualmente conectado:
- **Punto verde** - En línea (pulso recibido en los últimos 5 minutos)
- **Punto rojo** - Descargado (ningún pulso en más de 5 minutos)
- **Punto gris** - Nunca emparejado (terminal creado pero el dispositivo nunca se conectó)

**Último pulso** - Marca temporal del último ping del terminal (se actualiza cada 5 minutos cuando está en línea)

**Código de emparejamiento** - Código alfanumérico de 8 caracteres usado para el emparejamiento inicial del dispositivo (oculto después del primer uso)

**Usuarios asignados** - Cantidad de personal autorizado para usar este terminal

## Crear un nuevo terminal

Haga clic en **+ Agregar terminal** para registrar un nuevo dispositivo POS:

![Formulario de agregar terminal](/static/core/admin/img/help/managing-pos-terminals/terminal-add-form.webp)

### Configuración básica

**Nombre del terminal** - Elija un nombre descriptivo que indique:
- Ubicación física: "Register de entrada norte"
- Función: "Terminal de devoluciones"
- Secuencia: "Checkout 1", "Checkout 2", "Checkout 3"

Los nombres ayudan al personal a identificar terminales durante la asignación de turnos y la solución de problemas. Use convenciones de nomenclatura consistentes en todas las ubicaciones.

**Almacén** - **REQUERIDO** - Seleccione el almacén del cual este terminal opera:
- Determina qué stock está disponible para la venta
- Los pedidos realizados en este terminal se atribuyen a este almacén
- Las reservas de stock verifican la disponibilidad en el almacén asignado
- **No se pueden procesar ventas sin asignación de almacén**

Si tiene múltiples ubicaciones minoristas, cree un almacén separado para cada ubicación y asigne los terminales según corresponda.

**Está activo** - Conmutador para habilitar/deshabilitar el terminal sin eliminar la configuración:
- Los terminales inactivos no pueden emparejarse
- Las sesiones existentes en terminales inactivos expiran inmediatamente
- Use para deshabilitar temporalmente terminales robados o dañados

### Asignación de personal

**Usuarios asignados** - Seleccione qué miembros del personal pueden acceder a este terminal:
- Solo los usuarios asignados pueden iniciar sesión en el terminal
- Los usuarios también deben tener permisos POS en su rol de personal
- Asignar cero usuarios efectivamente bloquea el terminal
- Patrón común: Asignar a todos los empleados de la tienda a todos los terminales de la tienda

**Ejemplos de uso**:
- **Tienda general**: Asignar a todos los empleados a todos los terminales (cualquier cajero puede trabajar en cualquier caja)
- **Tienda por departamentos**: Asignar a empleados específicos de departamento a terminales de departamento
- **Multilocación**: Asignar a empleados específicos de ubicación a terminales de ubicación
- **Gerentes**: Asignar gerencia a todos los terminales para acceso de supervisión

Los usuarios sin asignación de terminal ven el error "No autorizado para este terminal" al intentar iniciar sesión.

### Configuración del hardware

El campo **Configuración del hardware** es una estructura JSON que define dispositivos periféricos:

**Impresora térmica**:
```json
{
  "printer": {
    "type": "network",
    "ip": "192.168.1.100",
    "port": 9100,
    "paper_width": 80
  }
}
```

**Lector de códigos de barras USB**:
```json
{
  "scanner": {
    "type": "usb",
    "vendor_id": "0x05e0",
    "product_id": "0x1200"
  }
}
```

**Caja registradora** (conectada a la impresora):
```json
{
  "cash_drawer": {
    "enabled": true,
    "trigger": "printer_pulse"
  }
}
```

**Ejemplo completo**:
```json
{
  "printer": {
    "type": "network",
    "ip": "192.168.1.100",
    "port": 9100,
    "paper_width": 80
  },
  "scanner": {
    "type": "usb",
    "vendor_id": "0x05e0",
    "product_id": "0x1200"
  },
  "cash_drawer": {
    "enabled": true,
    "trigger": "printer_pulse"
  }
}
```

Deje en blanco si el terminal no tiene hardware periférico (adecuado para terminales móviles o tablets sin impresora/lector).

### Configuración de caché en línea

Configure cuántos datos el terminal almacena para operaciones en línea:

**Días de sincronización de pedidos** (7-30 días, por defecto: 14):
- Número de días de pedidos recientes para almacenar localmente
- Valores más altos = más datos históricos disponibles en línea
- Valores más bajos = sincronización más rápida, menos almacenamiento utilizado
- **Recomendación**: 7 días para terminales de alto volumen, 14 días para uso normal, 30 días para operaciones de auditoría intensiva

**Límite de sincronización de pedidos** (200-1000 pedidos, por defecto: 500):
- Número máximo de pedidos para almacenar independientemente del rango de fechas
- Evita el uso excesivo de almacenamiento en terminales de alto volumen
- **Recomendación**: 200 para tablets con almacenamiento limitado, 500 para terminales estándar, 1000 para dispositivos POS dedicados

**Compromisos**:
- **Configuraciones más altas**: Mejor acceso en línea a datos históricos, sincronización inicial más lenta, más almacenamiento utilizado
- **Configuraciones más bajas**: Sincronización más rápida, menos almacenamiento, historia en línea limitada

El terminal descarga las X pedidos más recientes (dentro de Y días) en cada ciclo de sincronización. Si el terminal procesa 50 pedidos/día y sync_days es 14, se espera ~700 pedidos almacenados (puede alcanzar el límite de sincronización).

## Flujo de trabajo de emparejamiento de terminal

Después de crear un terminal, empareje el dispositivo físico:

1. **Generar código de emparejamiento** - Se crea automáticamente cuando guarda el terminal (8 caracteres alfanuméricos)

2. **Anote el código** - Se muestra en la lista de terminales y en la vista detallada (caduca después del primer emparejamiento exitoso)

3. **Navegue al dispositivo terminal** - En el dispositivo físico (tableta/computadora), abra el navegador y vaya a: `https://yourstore.com/pos/`

4. **Ingrese el código de emparejamiento** - Escriba el código de 8 caracteres cuando se le solicite

5. **El terminal descarga la configuración** - El dispositivo recibe:
   - Asignación de almacén
   - Configuración del hardware (impresora, lector, caja registradora)
   - Configuraciones de caché en línea
   - Lista de usuarios asignados
   - Sincronización inicial del catálogo de productos

6. **Aparece el prompt de inicio de sesión** - El terminal muestra la pantalla de inicio de sesión para los usuarios asignados

7. **El personal inicia sesión** - Ingrese las credenciales del usuario asignado a este terminal

8. **Se completa la sincronización inicial** - El terminal descarga:
   - Pedidos recientes (según sync_days y sync_limit)
   - Catálogo completo de productos para el almacén asignado
   - Base de datos de clientes
   - Configuraciones promocionales

9. **El terminal está listo** - Aparece la pantalla "Listo para vender" con la barra de búsqueda

10. **El código de emparejamiento se consume** - El código se elimina del administrador; genere un nuevo código si se necesita reemparejar

**Regeneración del código de emparejamiento**: Si necesita reemparejar un terminal (restablecimiento del dispositivo, caché del navegador limpiado, nuevo hardware), use la acción de administración **Regenerar código de emparejamiento**. Esto invalida el código antiguo y crea uno nuevo.

## Monitoreo del estado del terminal

### Sistema de pulso

Los terminales envían una señal de pulso al servidor cada **5 minutos** que contiene:
- UUID del terminal
- Marca temporal actual
- Cantidad de usuarios en línea
- Marca temporal de la última sincronización
- Estado del worker de servicio

**Indicador de estado en línea**:
- **Verde** - Se recibió el pulso en los últimos 5 minutos (el terminal está en línea y operativo)
- **Rojo** - No se recibió pulso en más de 5 minutos (el terminal está desconectado o offline)
- **Gris** - El terminal nunca se emparejó (nunca se recibió un pulso)

**Casos de uso**:
- **Apertura diaria**: Verificar que todos los terminales estén en línea antes de abrir la tienda
- **Solución de problemas**: Identificar qué terminales están experimentando problemas de conectividad
- **Auditoría**: Verificar que los terminales estén activos durante las horas de operación

### Marca temporal del último pulso

Muestra la fecha y hora exacta del último pulso. Use esto para:
- Determinar cuánto tiempo ha estado un terminal fuera de línea
- Identificar patrones (por ejemplo, el terminal se desconecta cada noche al cerrar)
- Verificar la frecuencia de sincronización (debería actualizarse cada ~5 minutos cuando esté en línea)

## Función de desbloqueo remoto

Cuando un terminal se vuelve inresponsive o se atasca en una pantalla (crash de software, problemas de tiempo de sesión, congelamiento del navegador), use la acción de administración **Desbloqueo remoto**:

**Cómo funciona**:
1. Seleccione el terminal problemático en la lista de administración
2. Elija **Desbloqueo remoto** desde el menú de acciones de administración
3. Confirme la acción
4. El servidor envía una señal de desbloqueo a través de la respuesta del pulso
5. El terminal recibe la señal en el siguiente ciclo de pulso (<5 min)
6. El terminal fuerza el cierre de sesión del usuario actual y vuelve a la pantalla de inicio de sesión

**Cuándo usarlo**:
- El terminal se congela en la pantalla de transacción
- El personal no puede cerrar sesión (el botón de cierre de sesión no responde)
- La sesión aparece activa pero el terminal es inresponsive
- El navegador se ha caído pero la cookie de sesión persiste

**Importante**: El desbloqueo remoto **no reinicia** el dispositivo o el navegador, solo fuerza el cierre de sesión y el borrado de la sesión. Si el terminal está completamente congelado, el personal puede necesitar reiniciar manualmente el navegador o el dispositivo.

## Edición de la configuración del terminal

Haga clic en un terminal en la lista para editar su configuración:

![Formulario de edición de terminal](/static/core/admin/img/help/managing-pos-terminals/terminal-edit-form.webp)

**Es seguro cambiar mientras el terminal está en línea**:
- Nombre del terminal
- Usuarios asignados
- Configuración del hardware (toma efecto después de que el terminal reinicie la aplicación)
- Configuraciones de caché en línea (toman efecto en la siguiente sincronización)

**Requiere reemparejamiento**:
- Asignación de almacén (cambiar almacén requiere reemparejamiento para sincronizar el nuevo inventario)

**No se puede cambiar**:
- UUID (identificador inmutable)

Los cambios en la mayoría de las configuraciones se aplican en el siguiente ciclo de pulso/sincronización. Los cambios en la configuración del hardware requieren que el personal cierre y vuelva a abrir la aplicación POS (o refresque el navegador).

## Solución de problemas de problemas comunes

**El terminal muestra "No autorizado" al iniciar sesión**:
- Verifique que el usuario esté en la **lista de usuarios asignados** para este terminal
- Verifique que el usuario tenga permisos POS en **Personal y permisos > Roles**
- Verifique que el terminal esté marcado como **Está activo**

**El terminal no se empareja (código inválido)**:
- Los códigos de emparejamiento caducan después del primer uso, regenere si es necesario
- Los códigos son sensibles a mayúsculas y minúsculas, verifique la capitalización
- Verifique que el terminal esté marcado como **Está activo**

**El terminal muestra "Offline" (punto rojo)**:
- Verifique que el dispositivo tenga conectividad a internet
- Verifique que el terminal esté realmente en ejecución (navegador abierto a la URL /pos/)
- Asegúrese de que el firewall no esté bloqueando las solicitudes de pulso
- Espere 5 minutos para el siguiente ciclo de pulso

**El terminal es lento para sincronizar**:
- Reduzca **Días de sincronización de pedidos** de 30 a 7
- Reduzca **Límite de sincronización de pedidos** de 1000 a 200
- Verifique la velocidad de la red en la ubicación del terminal
- Verifique que el servidor no esté bajo carga pesada

**La impresora no funciona**:
- Verifique la IP y el puerto de la impresora en **Configuración del hardware**
- Pruebe la conectividad de la impresora desde el dispositivo del terminal (ping a la dirección IP)
- Verifique que la impresora sea compatible con ESC/POS
- Verifique que la impresora esté encendida y en línea

## Consejos

- **La convención de nombres importa** - Use nombres consistentes (ubicación + número) para simplificar la gestión a gran escala
- **Siempre asigne almacén antes de emparejar** - Los terminales no pueden procesar ventas sin asignación de almacén
- **Pruebe la configuración del hardware antes de implementar** - Imprima un recibo de prueba para verificar la integración de la impresora/caja registradora
- **Monitorea el pulso diariamente** - Establezca una rutina para verificar que todos los terminales estén en línea al abrir la tienda
- **Reduce los límites de sincronización para terminales móviles** - Tablets y teléfonos benefician de sync_days: 7, sync_limit: 200
- **Usa el desbloqueo remoto con moderación** - El cierre de sesión forzado interrumpe transacciones activas; confirme que el terminal esté realmente atascado primero
- **Documenta los códigos de emparejamiento** - Anote el código antes de implementar el terminal en el piso de venta (en caso de que la configuración tome más tiempo del esperado)
- **Asigna a gerentes a todos los terminales** - Asegura que los supervisores puedan acceder a cualquier caja para anular, reembolsos y solución de problemas