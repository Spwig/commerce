---
title: POS System Overview
---

El sistema POS de Spwig transforma tu tienda en una solución de retail completa con terminales de punto de venta modernos. Implementa terminales ilimitados en ubicaciones ilimitadas con una tarifa de licencia plana de €499/año. Cada terminal es una Aplicación Web Progresiva (PWA) que funciona sin conexión, sincroniza automáticamente y se integra de forma fluida con tu inventario, datos de clientes y procesamiento de pagos. Administre todo desde el panel de administración: configuración de terminal, conciliación de turnos, personalización de recibos y integración de hardware.

Use el sistema POS cuando tenga ubicaciones de retail físicas, tiendas pop-up, ferias comerciales o cualquier entorno donde los clientes compren en persona en lugar de en línea.

![POS Dashboard](/static/core/admin/img/help/pos-system-overview/dashboard.webp)

## ¿Qué es Spwig POS?

Spwig POS es un sistema de punto de venta completamente integrado diseñado para comerciantes que venden tanto en línea como en ubicaciones físicas. A diferencia de los sistemas de punto de venta de terceros que requieren integraciones complejas, Spwig POS se construye directamente en su plataforma, asegurando una sincronización perfecta de datos en todos los canales de venta.

**Características clave**:
- **Terminales ilimitados** - Implemente tantos terminales como necesite sin costo adicional
- **Arquitectura orientada a la operación sin conexión** - Continúa procesando ventas incluso cuando se pierda la conexión a internet
- **Aplicación Web Progresiva** - Sin instalaciones en tiendas de aplicaciones; acceso mediante navegador en cualquier dispositivo (tabletas, computadoras, terminales dedicados)
- **Sincronización de inventario real** - Reservas de inventario (TTL de 15 minutos) previenen la sobreventa en canales
- **Soporte para pago dividido** - Acepte múltiples métodos de pago por transacción (efectivo + tarjeta + tarjeta de regalo)
- **Integración de hardware** - Impresoras térmicas ESC/POS, escáneres de códigos de barras, cajones de efectivo, pantallas para clientes
- **Gestión de turnos** - Conciliación de efectivo con conteos de apertura/cierre y seguimiento de discrepancias
- **Listo para múltiples ubicaciones** - Grupos de tiendas con herencia de configuraciones para gestión de franquicias y regional

## Licencia y Activación

**Tarifa plana**: €499 por año cubre terminales ilimitados en ubicaciones ilimitadas. Sin tarifas por terminal, sin tarifas por transacción, sin costos ocultos.

**Formato de licencia**: `POS-XXXX-XXXX-XXXX-XXXX` (proporcionado después de la compra)

**Activación**: Ingrese su clave de licencia en **Configuración > Licencia POS**. El sistema se valida con el servidor de licencias de Spwig y habilita todas las funciones POS inmediatamente. Las licencias incluyen un período de gracia de 14 días después de la expiración para permitir retrasos en el procesamiento de pagos.

**Lo que obtiene**:
- Registros ilimitados de terminales
- Asignaciones ilimitadas de personal
- Todas las funciones POS (turnos, gestión de efectivo, personalización de recibos, pantallas para clientes)
- Integraciones con proveedores de pago (Stripe Terminal y sistema extensible de proveedores)
- Soporte de integración de hardware
- Actualizaciones y correcciones de errores durante el período de licencia

Ninguna función POS está disponible sin una licencia válida—la interfaz de emparejamiento de terminales, la gestión de turnos y las páginas de administración POS requieren activación.

## Arquitectura del sistema

**Frontend** - Aplicación Web Progresiva de React 18:
- Primero sin conexión con caché de Service Worker (funciona sin internet)
- Sistema de construcción Vite para carga rápida
- Módulos CSS + tokens de diseño (coherentes con su tema de tienda)
- IndexedDB para persistencia de datos locales
- 10 idiomas admitidos (inglés, chino simplificado/tradicional, francés, alemán, español, portugués, japonés, ruso, árabe)

**Backend** - Integración del backend:
- 13 modelos POS (POSTerminal, POSShift, CashMovement, ReceiptTemplate, PromoSlide, etc.)
- 43+ puntos de conexión REST API para operaciones de terminal
- Sistema de reservas de inventario con gestión de TTL
- Tareas de Celery para sincronización en segundo plano
- Almacenamiento encriptado de credenciales para proveedores de pago

**Seguridad**:
- Emparejamiento de terminal mediante códigos de 8 caracteres (generados en el lado del servidor, caducan después de su uso)
- Control de asignación de personal que usuarios pueden acceder a qué terminales
- Capacidad de bloqueo/desbloqueo remoto para emergencias de administración
- Credenciales encriptadas de proveedores de pago
- Autenticación basada en sesión con soporte para desbloqueo biométrico (dependiendo del navegador)

## Flujo de trabajo para comenzar

Siga estos 5 pasos para implementar su primer terminal POS:

**Paso 1: Activar la licencia POS**
- Navegue a **Configuración > Licencia POS**
- Ingrese su clave de licencia (`POS-XXXX-XXXX-XXXX-XXXX`)
- Valide la licencia (requiere conexión a internet)
- Confirme la activación

**Paso 2: Crear almacén**
- Navegue a **Catálogo > Almacenes**
- Cree un almacén que represente su ubicación de retail
- Configure la dirección y la información de contacto
- Este almacén registrará el inventario físico para ventas POS

**Paso 3: Registrar terminal**
- Navegue a **POS > Terminales**
- Haga clic en **+ Añadir Terminal**
- Establezca el nombre del terminal (ej. "Caja principal", "Cobro 1")
- Asigne el almacén del Paso 2
- Configure la configuración del hardware (impresora, escáner, cajón de efectivo)
- Guarde para generar el código de emparejamiento de 8 caracteres

**Paso 4: Asignar personal**
- En la configuración del terminal, desplácese hasta **Usuarios asignados**
- Seleccione los miembros del personal autorizados para usar este terminal
- Solo los usuarios asignados pueden iniciar sesión en el terminal
- Los usuarios deben tener permisos POS adecuados en su rol de personal

**Paso 5: Emparejar dispositivo**
- En su dispositivo de terminal (tableta/computadora), navegue a la URL `/pos/`
- Ingrese el código de emparejamiento de 8 caracteres del Paso 3
- El terminal descarga la configuración y sincroniza los datos iniciales
- Inicie sesión con las credenciales de personal asignadas
- El terminal está listo para ventas

Después de emparejar, los terminales se sincronizan automáticamente cada 5 minutos (configurable). El modo sin conexión permite continuar operando cuando no haya conexión a internet—las ventas se sincronizan automáticamente cuando se restablezca la conectividad.

## Características principales de POS

**Procesamiento de ventas**:
- Búsqueda de productos por nombre, SKU o código de barras
- Pago dividido (múltiples métodos de pago por pedido)
- Carritos guardados (guardar transacciones incompletas)
- Devoluciones y anulaciones con seguimiento de razones
- Aplicación de descuentos (cupones, tarjetas de regalo, promociones)
- Búsqueda de clientes y redención de puntos de lealtad

**Gestión de efectivo**:
- Apertura de turno con conteo de efectivo inicial
- Cierre de turno con conciliación de esperada vs real
- Movimientos de efectivo (añadidos de efectivo, retiros de efectivo con razones)
- Cálculo automático de efectivo esperado basado en ventas en efectivo
- Seguimiento y reportes de discrepancias

**Integración de hardware**:
- Impresoras de recibos térmicas ESC/POS (red o serie)
- Escáneres de códigos de barras USB
- Triggers de cajón de efectivo mediante pulso de impresora
- Pantallas para clientes (carusel promocional durante el ocio)
- Lectoras de tarjetas Stripe Terminal (S700, WisePOS E, P400)

**Capacidades sin conexión**:
- Service Worker almacena todos los activos del terminal
- IndexedDB almacena pedidos recientes (configurable: 7-30 días, 200-1000 pedidos)
- Reservas de inventario con TTL de 15 minutos previenen la sobreventa
- Cola de ventas para sincronización cuando se restablezca la conectividad
- Detección automática de reconexión

## Páginas de administración POS

Acceda a estas páginas de administración para gestionar todos los aspectos de su implementación POS:

**Panel de administración POS** (`/admin/pos/`)
- Visión general del sistema y estadísticas rápidas
- Actividad reciente de terminales
- Resumen de turnos activos
- Estado de la licencia y fecha de vencimiento

**Gestión de terminales** (`/admin/pos_app/posterminal/`)
- Registre y configure terminales
- Asigne personal y almacenes
- Supervise el estado en línea/ sin conexión (seguimiento de latido)
- Desbloqueo remoto de terminales
- [Más información: Gestión de terminales POS](managing-pos-terminals)

**Gestión de turnos** (`/admin/pos_app/posshift/`)
- Ver todos los turnos (abiertos, cerrados, históricos)
- Revisar informes de conciliación de efectivo
- Seguimiento de movimientos de efectivo y discrepancias
- Auditoría de actividad de turnos
- [Más información: Turnos POS y gestión de efectivo](pos-shifts-cash-management)

**Grupos de tienda** (`/admin/pos_app/storegroup/`)
- Organice terminales por ubicación/ región
- Configure configuraciones de nivel de grupo (moneda, idioma, zona horaria)
- Implemente jerarquía de herencia de configuraciones
- [Más información: Grupos de tienda POS](pos-store-groups)

**Plantillas de recibos** (`/admin/pos_app/receipttemplate/`)
- Personalice recibos impresas (ancho de papel, logotipo, encabezado/pie de página)
- Configure campos de cumplimiento (ID de impuesto, registro comercial)
- Añada códigos QR para promociones
- Alcance las plantillas a tiendas o grupos específicos
- [Más información: Personalización de plantillas de recibos](receipt-template-customization)

**Diapositivas promocionales** (`/admin/pos_app/promoslide/`)
- Cree contenido de carusel para pantallas de clientes
- Destine diapositivas a tiendas o grupos específicos
- Programar promociones estacionales
- [Más información: Diapositivas promocionales para pantallas de clientes](customer-display-promo-slides)

**Proveedores de pago** (`/admin/pos_app/posterminalprovider/`)
- Configure la integración de Stripe Terminal
- Administre credenciales de proveedores de pago
- Supervise el estado de conexión
- [Más información: Proveedores de terminales de pago](payment-terminal-providers)

**Lectores de tarjetas** (`/admin/pos_app/posterminalreader/`)
- Registre lectores de tarjetas físicos
- Asigne lectores a terminales
- Personalice pantallas de inicio (branding de pantalla para clientes)
- Supervise el estado del lector (en línea, sin conexión, ocupado)
- [Más información: Gestión de lectores de tarjetas](card-reader-management)

## Implementación en múltiples ubicaciones

Para comerciantes con múltiples ubicaciones de retail, Spwig POS admite la herencia de configuraciones jerárquicas:

**Jerarquía de configuración** (de mayor prioridad a menor):
1. Configuración específica del terminal (sobrescribe todo)
2. Configuración específica de la tienda (sobrescribe grupo y sitio)
3. Configuración de grupo (sobrescribe configuraciones predeterminadas del sitio)
4. Configuraciones predeterminadas del sitio (caída para todo)

Configure configuraciones compartidas en el nivel de grupo (ej. moneda regional, idioma) y sobrescriba según sea necesario para tiendas o terminales específicos. Consulte [Grupos de tienda POS](pos-store-groups) para obtener orientación detallada sobre la configuración.

## Consejos

- **Empiece con un terminal** - Pruebe la configuración POS y el flujo de trabajo con un solo terminal antes de implementar a toda la flota
- **Asigne almacén antes de emparejar** - Los terminales no pueden procesar ventas sin una asignación de almacén
- **Configure plantillas de recibos temprano** - Los campos de cumplimiento (IDs de impuesto) varían por región; configure antes de ir en línea
- **Pruebe el modo sin conexión** - Desconecte internet y verifique que las ventas continúen; confirme la sincronización cuando se reconecte
- **Use grupos de tienda para múltiples ubicaciones** - Simplifica la gestión de configuración para implementaciones de franquicia o regionales
- **Supervise el estado del latido** - Los terminales pingen al servidor cada 5 minutos; los terminales sin conexión aparecen en el panel de administración
- **Configure límites de sincronización para el rendimiento** - Los terminales con conexiones lentas se benefician de configuraciones de sync_days/sync_limit más bajas
- **Haga copia de seguridad de la configuración del hardware** - Documente IPs de impresoras, configuraciones de escáneres, configuración de cajón de efectivo para recuperación ante desastres

Recuerde: preserve all markdown formatting, image paths, code blocks, and technical terms exactly as shown in the preservation rules.