---
title: Proveedores de Terminal de Pago
---

Los proveedores de terminal de pago permiten la aceptación de tarjetas de crédito y débito en tus terminales de punto de venta (POS). Stripe Terminal es el proveedor principal admitido, ofreciendo lectores de tarjetas modernos (S700, WisePOS E, P400), tarifas competitivas de procesamiento y una integración sin problemas. Configure cuentas de proveedores con credenciales de API, supervise el estado de conexión en tiempo real y administre múltiples proveedores si opera en diferentes regiones. El sistema de proveedores es extensible: se pueden integrar procesadores de pago adicionales a través del marco de proveedores si Stripe Terminal no opera en su mercado.

Use proveedores de pago para aceptar pagos con tarjetas de forma segura, rastrear el estado del procesamiento de pagos y gestionar la asignación de lectores en los terminales.

![Lista de Proveedores de Pago](/static/core/admin/img/help/payment-terminal-providers/provider-list.webp)

## Visión General de los Proveedores de Pago

Los proveedores de pago son servicios de terceros que procesan pagos con tarjetas en nombre de su negocio:

**Responsabilidades del Proveedor**:
- Autorizar transacciones con tarjetas en tiempo real
- Comunicarse con lectores físicos de tarjetas
- Manejar la seguridad de los pagos (cumplimiento PCI, encriptación)
- Transferir fondos a su cuenta bancaria (liquidación)
- Proporcionar informes de transacciones y gestión de disputas

**Rol de Spwig**:
- Enrutar solicitudes de pago al proveedor configurado
- Almacenar credenciales encriptadas del proveedor
- Supervisar el estado de la conexión
- Asociar lectores con terminales
- Registrar los resultados de los pagos en los pedidos

## Stripe Terminal (Proveedor Principal)

Stripe Terminal es el proveedor de pago recomendado para la mayoría de los comerciantes:

**Características**:
- Lectores de tarjetas de chip EMV modernos
- Soporte de pagos sin contacto (NFC) (Apple Pay, Google Pay, tarjetas de pago por toque)
- Gestión integrada de disputas
- Autorización en tiempo real
- API amigable para desarrolladores
- Disponible en 40+ países

**Precios** (a partir de 2024, verifique las tarifas actuales):
- Tarifas por transacción: 2,7% + $0,05 por transacción presencial (EE. UU.)
- Sin tarifas mensuales, sin tarifas de configuración, sin tarifas de cumplimiento PCI
- Hardware de lector de tarjetas: compra única ($59-$299 según el modelo)

**Regiones admitidas**:
- Estados Unidos, Canadá, Reino Unido, Unión Europea, Australia, Singapur y más
- Verifique la disponibilidad de Stripe: https://stripe.com/terminal

**Lectores admitidos**:
- BBPOS WisePOS E (terminal Android todo en uno)
- Stripe Reader S700 (lector de mostrador)
- Verifone P400 (lector legado, aún admitido)

## Configuración de Stripe Terminal

**Paso 1: Crear cuenta de Stripe**
- Regístrese en stripe.com
- Complete la verificación empresarial (cuenta bancaria, ID fiscal)
- Active los pagos

**Paso 2: Habilitar Stripe Terminal**
- En el panel de Stripe, vaya a **Productos > Terminal**
- Haga clic en **Comenzar**
- Acepte los términos de servicio de Terminal

**Paso 3: Crear ubicación**
- Stripe Terminal requiere una "Ubicación" que represente su sitio de venta físico
- Vaya a **Terminal > Ubicaciones**
- Haga clic en **Crear Ubicación**
- Ingrese la dirección de la tienda y los detalles
- Guarde el ID de ubicación (parece `tml_1ABC123...`)

**Paso 4: Generar clave de API**
- Vaya a **Desarrolladores > Claves de API**
- Localice su **Clave secreta** (comienza con `sk_live_...` para producción, `sk_test_...` para pruebas)
- Copie la clave secreta (no la comparta públicamente)

**Paso 5: Configurar en Spwig**
- Vaya a **POS > Proveedores de Pago**
- Haga clic en **+ Agregar Proveedor de Pago**
- Seleccione **Proveedor**: "Stripe Terminal"
- Ingrese **Clave secreta de API** (de Paso 4)
- Ingrese **ID de ubicación** (de Paso 3)
- Guarde

**Paso 6: Probar conexión**
- Después de guardar, el estado del proveedor debe cambiar a "Conectado" (verde)
- Si el estado muestra "Error" (rojo), verifique la clave de API y el ID de ubicación
- Revise el mensaje de error en la vista de detalles del proveedor

![Formulario de Agregar Proveedor de Pago](/static/core/admin/img/help/payment-terminal-providers/provider-add-form.webp)

## Campos de Configuración del Proveedor

**Clave del Proveedor** - Seleccione el procesador de pago:
- **stripe_terminal** - Stripe Terminal (recomendado)
- **manual** - Entrada de pago manual (solo para pruebas, sin procesamiento real)
- Pueden aparecer proveedores adicionales si se instalan a través del sistema de componentes

**Credenciales (Encriptadas)** - Estructura JSON que contiene las credenciales de API:
- Encriptadas automáticamente antes del almacenamiento
- Nunca visibles en texto plano después de guardar
- Estructura de ejemplo (Stripe Terminal):
```json
{
  "api_key": "sk_live_ABC123...",
  "location_id": "tml_1ABC123..."
}
```

**Configuración del Proveedor** - Configuración adicional (específica del proveedor):
- Descripción de la factura (aparece en el estado de cuenta de la tarjeta de crédito del cliente)
- Captura automática (capturar inmediatamente los pagos autorizados en lugar de captura manual)
- Sobrescritura de moneda (si la cuenta del proveedor usa una moneda diferente que la tienda)

**Estado de Conexión** - Indicador de estado en tiempo real:
- **Conectado** (verde) - El proveedor es alcanzable y configurado correctamente
- **Error** (rojo) - La conexión falló o las credenciales son inválidas
- **Desconocido** (gris) - No se ha probado aún (inmediatamente después de la creación)

**Última Prueba** - Marca temporal de la prueba de conexión más reciente
- Se actualiza automáticamente cuando se procesan transacciones
- Inicie la prueba manualmente mediante la acción de administración **Probar Conexión**

## Monitoreo del Estado de Conexión

El sistema monitorea la conectividad del proveedor para alertarle sobre problemas antes de que los clientes intenten pagos:

**Pruebas Automáticas**:
- Cada transacción de pago desencadena una prueba de conexión (por necesidad)
- Un trabajo en segundo plano prueba la conexión cada 6 horas (monitoreo preventivo)

**Significados del Estado**:

**Conectado** - La API del proveedor es alcanzable, las credenciales son válidas, lista para procesar pagos

**Error** - Causas comunes:
- Clave de API inválida (revocada, caducada o incorrecta)
- ID de ubicación inválido (ubicación eliminada en Stripe, ID incorrecto introducido)
- Problemas de conectividad de red (firewall bloqueando la API de Stripe)
- Fallo en el servicio de Stripe (raro)

**Desconocido** - El proveedor nunca se ha probado aún (cuenta nueva pendiente de primera transacción)

**Resolviendo el estado de error**:
1. Revise el mensaje de error en la vista de detalles del proveedor (explica el problema específico)
2. Verifique que la clave de API aún sea válida en el panel de Stripe
3. Verifique que el ID de ubicación aún exista en el panel de Stripe
4. Pruebe la conexión manualmente mediante la acción de administración **Probar Conexión**
5. Actualice las credenciales si es necesario

![Detalles del Proveedor de Pago](/static/core/admin/img/help/payment-terminal-providers/provider-detail.webp)

## Comparación de Lectores de Tarjetas Admitidos

Stripe Terminal ofrece múltiples opciones de hardware de lectores:

| Modelo | Tipo | Métodos de Pago | Pantalla | Mejor Para | Precio |
|-------|------|-----------------|---------|----------|-------|
| **WisePOS E** | Todo en uno | Chip EMV, NFC, deslizar | Pantalla táctil de color de 5" | Punto de venta de retail completo | ~$299 |
| **S700** | De mostrador | Chip EMV, NFC, deslizar | Pantalla LCD monocromática | Pago estándar de retail | ~$249 |
| **P400** | De mostrador | Chip EMV, NFC, deslizar | Pantalla LCD monocromática | Implementaciones legadas | ~$299 |

**Ventajas de WisePOS E**:
- Basado en Android (ejecuta aplicaciones, puede mostrar contenido personalizado)
- Pantalla táctil de color (mejor experiencia de usuario para solicitudes de propinas, captura de firma)
- Impresora de recibos integrada (opcional)
- Velocidad de transacción más rápida

**Ventajas de S700**:
- Costo más bajo que WisePOS E
- Huella compacta
- Diseño resistente a salpicaduras

**P400** (modelo antiguo):
- Aún admitido pero no recomendado para nuevas implementaciones
- Procesamiento de tarjetas de chip más lento que S700/WisePOS E

Todos los lectores se conectan al POS de Spwig a través de la API de Stripe Terminal (no se requiere conexión directa USB/Bluetooth al dispositivo POS).

## Consideraciones de Seguridad

**Encriptación de Credenciales**:
- Todas las credenciales del proveedor se encriptan en reposo en la base de datos
- La encriptación utiliza la clave secreta de la aplicación (definida en la configuración de la aplicación)
- Las credenciales nunca aparecen en registros o mensajes de error

**Permisos de Clave de API**:
- Use **claves de API restringidas** en producción (limite los permisos solo al Terminal)
- No use claves secretas no restringidas (acceso más amplio de lo necesario = riesgo de seguridad)
- En el panel de Stripe, cree una clave restringida con solo **permisos de Terminal**

**Cumplimiento PCI**:
- Stripe Terminal maneja el cumplimiento PCI (los datos de la tarjeta nunca tocan los servidores de Spwig)
- Los números de tarjetas se procesan completamente en el hardware del lector → servidores de Stripe → redes de tarjetas
- Spwig solo almacena los resultados del pago (aprobado/rechazado), nunca los detalles de la tarjeta

**Rotación de Claves**:
- Gire claves de API anualmente como práctica de seguridad recomendada
- Al girar, actualice las credenciales en la configuración del proveedor
- Las claves antiguas pueden revocarse en el panel de Stripe después de confirmar que la nueva clave funciona

## Múltiples Proveedores

Algunos comerciantes necesitan múltiples cuentas de proveedor:

**Operaciones con múltiples monedas**:
- Tiendas en EE. UU. usan cuenta de Stripe EE. UU. (procesa USD)
- Tiendas en Europa usan cuenta de Stripe UE (procesa EUR)
- Configure un proveedor separado por moneda

**Proveedores de respaldo**:
- Proveedor principal (Stripe Terminal)
- Proveedor de respaldo (entrada manual) cuando los lectores fallen
- El cajero selecciona el proveedor al iniciar el pago

**Pruebas vs. Producción**:
- Proveedor de prueba con clave de API `sk_test_...`
- Proveedor de producción con clave de API `sk_live_...`
- Cambie de proveedores después de la fase de pruebas

## Solución de Problemas de Issues Comunes

**Issue 1: El estado muestra "Error" con el mensaje "Clave de API inválida"**
- **Causa**: Clave de API revocada o copiada incorrectamente
- **Solución**: Genere una nueva clave de API en el panel de Stripe, actualice las credenciales del proveedor, pruebe la conexión

**Issue 2: Lector no detectado durante el pago**
- **Causa**: Lector no registrado a la ubicación del proveedor
- **Solución**: En el panel de Stripe, verifique que el lector esté registrado a la misma ID de ubicación usada en la configuración del proveedor

**Issue 3: Pagos rechazados a pesar de tarjeta válida**
- **Causa**: Cuenta de Stripe no completamente activada (verificación pendiente)
- **Solución**: Complete la verificación empresarial en el panel de Stripe (cuenta bancaria, ID fiscal)

**Issue 4: El estado de conexión muestra "Desconocido" y nunca se actualiza**
- **Causa**: Proveedor nunca probado (no se han intentado transacciones)
- **Solución**: Use la acción de administración **Probar Conexión** para desencadenar manualmente la prueba de conectividad

## Consejos

- **Modo de prueba antes de producción** - Use claves de API de prueba de Stripe (`sk_test_...`) para la configuración inicial y pruebas
- **Un proveedor por moneda** - No intente procesar EUR con una cuenta de Stripe basada en USD; cree proveedores separados
- **Monitoree el estado de conexión semanalmente** - El monitoreo proactivo previene fallos de pago en la caja
- **Restrinja los permisos de la clave de API** - Limite las claves de API de Stripe solo a permisos de Terminal (principio de privilegio mínimo)
- **Documente los IDs de ubicación** - Mantenga un registro de qué ubicación de Stripe corresponde a qué tienda física
- **Pruebe la asignación del lector** - Después de la configuración del proveedor, pruebe el pago con un lector de tarjetas real para verificar el flujo de extremo a extremo
- **Mantenga la información de contacto de Stripe actualizada** - Asegúrese de que la información de contacto empresarial en Stripe coincida con la actual (importante para disputas, cumplimiento)