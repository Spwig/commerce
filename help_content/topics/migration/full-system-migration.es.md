---
title: Migración completa del sistema
---

La migración completa del sistema traslada toda tu tienda -- configuraciones, productos, clientes, pedidos, archivos multimedia y todo otro dato -- de una instalación de Spwig a otra. Usa esto cuando te muevas a un nuevo servidor o configures una copia completa de tu tienda.

## Cuándo usar la migración completa

- **Reubicación del servidor**: Mover tu tienda a un nuevo proveedor de alojamiento o servidor
- **Crear una copia de entorno de pruebas**: Configurar un entorno de pruebas completo a partir de la producción
- **Recuperación ante desastres**: Restaurar una tienda completa desde una instancia de respaldo

La migración completa incluye todo lo que hace la sincronización de configuraciones, más todos los datos transaccionales (productos, clientes, pedidos, reseñas, inventario, archivos multimedia, etc.).

## ¿Qué se migra

La migración completa puede transferir todas las categorías de configuración más estas categorías de datos:

| Categoría | Descripción |
|----------|-------------|
| **Componentes instalados** | Temas, integraciones de proveedores y componentes de utilidad con sus archivos de paquete |
| **Productos, categorías y marcas** | Productos, variantes, imágenes, categorías, marcas y atributos |
| **Biblioteca de medios** | Todos los archivos multimedia y activos subidos |
| **Clientes y direcciones** | Cuentas de clientes, perfiles y direcciones |
| **Historial de pedidos** | Pedidos, elementos de pedido y registros de transacciones |
| **Reseñas de productos** | Reseñas y calificaciones de clientes |
| **Niveles de stock** | Cantidad de inventario por almacén y puntos de reorden |
| **Productos digitales y licencias** | Activos digitales, plantillas de licencias y grupos de licencias |
| **Tarjetas regalo y uso de cupones** | Saldo de tarjetas regalo y registros de uso de cupones |
| **Crédito de tienda y billeteras** | Saldo de billeteras de clientes y historial de transacciones |
| **Miembros del programa de fidelidad** | Miembros de fidelidad, puntos, transacciones y insignias |
| **Suscripciones activas** | Planes de suscripción, suscripciones activas y historial de facturación |
| **Envíos y seguimiento** | Registros de envío y eventos de seguimiento |
| **Reembolsos, devoluciones y notas de pedido** | Registros de reembolsos, solicitudes de devolución y notas |
| **Miembros de afiliados** | Cuentas de afiliados, códigos de referencia y historial de comisiones |

## Guía paso a paso

### Paso 1: Conectar a la instancia de origen

1. Navega a **Migración de datos > Sincronización Spwig a Spwig** en el menú lateral de administración
2. Haz clic en **Iniciar migración completa**
3. Conéctate a la tienda de origen (la tienda de la que estás migrando):
   - Ingresa la URL de la tienda de origen
   - Pega el token de sincronización de la tienda de origen
   - Nombra la conexión (ej. "Servidor de producción antiguo")
4. Haz clic en **Probar conexión** para verificar
5. Haz clic en **Siguiente**

> **Importante:** La migración completa siempre **extrae** datos de la tienda conectada hacia esta tienda. Ejecuta el asistente en la tienda **destino** (nueva).

### Paso 2: Elegir el alcance

Selecciona qué categorías de datos incluir en la migración. Las categorías están organizadas en grupos:

- **Configuraciones**: Configuración de la tienda, temas, proveedores, contenido
- **Datos**: Productos, clientes, pedidos, medios y otros datos transaccionales

Algunas categorías tienen dependencias (por ejemplo, los pedidos dependen de clientes y productos). Las dependencias se incluyen automáticamente cuando seleccionas una categoría.

Categorías con indicadores especiales:
- **Icono clave**: Contiene credenciales que se transfieren de forma segura
- **Icono de archivo**: Incluye archivos binarios (imágenes, medios, paquetes)
- **Icono de advertencia**: Consideraciones especiales para entornos de producción

### Paso 3: Verificaciones previas

Antes de iniciar la migración, las verificaciones previas automáticas verifican:

- **Salud de la conexión**: La tienda de origen es alcanzable y autenticada
- **Compatibilidad de versiones**: Ambas tiendas están ejecutando versiones compatibles de Spwig
- **Espacio en disco**: Hay suficiente almacenamiento disponible para archivos multimedia
- **Preparación de la base de datos**: La base de datos de destino puede recibir los datos

Si alguna verificación falla, verás instrucciones específicas sobre cómo resolver el problema antes de continuar.

### Paso 4: Progreso de la migración

La migración se ejecuta en segundo plano. Puedes navegar libremente -- el proceso continuará.

La página de progreso muestra:
- Porcentaje general con tiempo estimado restante
- Estado de finalización por categoría
- Registro de actividad en vivo con detalles de transferencia
- Estadísticas de transferencia de medios (archivos y bytes transferidos) para la categoría de medios

Para tiendas grandes con muchos productos y archivos de medios, la migración puede tomar algo de tiempo. La fase de transferencia de medios suele ser la más larga.

### Paso 5: Resultados

Después de que la migración se complete, la página de resultados muestra:

- Estadísticas resumidas (elementos migrados, omitidos, fallidos)
- Desglose por categoría con estado
- Detalles de errores para cualquier elemento fallido

## Lista de verificación después de la migración

Después de una migración exitosa, complete estos pasos en su nueva tienda:

1. **Active su licencia** en la nueva instalación
2. **Vuelva a ingresar las credenciales del proveedor de pago** que se omitieron durante la migración (las claves de prueba/sandbox no se transfieren a producción)
3. **Configure DNS** para que su dominio apunte al nuevo servidor
4. **Pruebe el flujo de pago** con un pedido de prueba
5. **Verifique que el envío de correos electrónicos** funcione correctamente
6. **Revise los archivos multimedia** y asegúrese de que las imágenes se carguen correctamente

## Rollback

Después de completar una migración completa, tiene **24 horas** para realizar un rollback. Un rollback elimina todos los datos migrados de la tienda de destino, restaurándola a su estado anterior a la migración.

Para realizar un rollback:
1. Vaya a la página de resultados o al Panel de Sincronización
2. Haga clic en **Rollback Migration** y confirme
3. Espere a que el rollback se complete

> **Advertencia:** El rollback elimina permanentemente todos los datos migrados. Cualquier cambio realizado en la tienda de destino después de la migración (nuevos pedidos, registros de clientes, etc.) también se verá afectado.

Después de 24 horas, la opción de rollback expira.

## Consejos

- **Ejecute en la tienda de destino**: El asistente de migración completa debe ejecutarse en la **nueva** tienda, extrayendo datos de la antigua
- **Migre a una instalación limpia**: Para mejores resultados, realice la migración en una instalación recién instalada de Spwig antes de ir en línea
- **Verifique el espacio en disco**: Asegúrese de que el destino tenga suficiente almacenamiento para todos los archivos multimedia
- **Mantenga el origen en funcionamiento**: No apague la tienda de origen hasta que haya verificado que todo funciona correctamente en el destino
- **Planifique la transición de DNS**: Después de verificar la migración, actualice sus registros DNS para que apunten al nuevo servidor