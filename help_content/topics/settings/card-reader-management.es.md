---
title: Gestión de lectores de tarjetas
---

La gestión de lectores de tarjetas rastrea dispositivos físicos de hardware de pago, los asigna a terminales de punto de venta (POS) y monitorea su estado operativo. Cada lector de tarjetas representa hardware real (Stripe S700, WisePOS E o P400) registrado con su proveedor de pagos. Los lectores tienen una relación uno a uno con los terminales: cada registro tiene su lector de tarjetas dedicado. Monitorea el estado del lector (en línea, fuera de línea, ocupado) en tiempo real, personaliza pantallas de inicio con tu marca y resuelve problemas de conectividad antes de que afecten la experiencia de pago del cliente.

Utiliza la gestión de lectores de tarjetas para asegurarte de que el hardware de pago esté correctamente configurado, asignado y operativo en todas las ubicaciones.

![Lista de lectores de tarjetas](/static/core/admin/img/help/card-reader-management/reader-list.webp)

## Entendiendo los lectores de tarjetas

Los lectores de tarjetas son dispositivos físicos de hardware que procesan pagos con tarjetas de crédito y débito:

**Componentes de hardware**:
- Ranura para tarjetas con chip EMV
- Antena NFC (sin contacto/pagar con un toque)
- Lector de banda magnética (heredado, raramente utilizado)
- Pantalla de visualización (muestra el monto, solicita el PIN, la firma)
- Conectividad de red (Wi-Fi o Ethernet, según el modelo)

**Integración de software**:
- Los lectores se conectan a la API de Stripe Terminal (basada en la nube, no conexión directa al dispositivo POS)
- El terminal POS solicita el pago a través de la API
- Stripe enruta la solicitud al lector registrado
- El lector procesa la tarjeta y devuelve el resultado al POS
- No se necesita conexión USB/Bluetooth entre el POS y el lector

**Un lector por terminal**:
- Cada terminal POS debe tener exactamente un lector de tarjetas asignado
- La relación uno a uno garantiza una responsabilidad clara y una solución de problemas simplificada
- Varios terminales no pueden compartir un solo lector (causa conflictos)

## Tipos de lectores de tarjetas

Spwig POS admite lectores de tarjetas Stripe Terminal:

**BBPOS WisePOS E** (`bbpos_wisepos_e`):
- Terminal todo en uno con pantalla táctil de color de 5"
- Opción de impresora integrada (recibo térmico)
- Ideal para: Pago al por menor completo, restaurantes (solicitudes de propinas en pantalla de color)
- Conectividad: Solo Wi-Fi
- Pantalla de inicio: Color completo 480×800 retrato

**Lector Stripe S700** (`stripe_s700`):
- Lector de mostrador con pantalla LCD monocromática
- Diseño compacto, resistente al agua
- Ideal para: Pago al por menor estándar, mostradores de pago compactos
- Conectividad: Wi-Fi o Ethernet
- Pantalla de inicio: Monocromática 480×800 retrato

**Verifone P400** (`verifone_p400`):
- Lector de mostrador heredado (modelo antiguo)
- Aún compatible pero no se recomienda para nuevas implementaciones
- Ideal para: Implementaciones existentes (no reemplazar hardware funcional)
- Conectividad: Wi-Fi o Ethernet
- Pantalla de inicio: Monocromática 480×800 retrato

**Compatibilidad futura**:
- Se pueden agregar modelos de lectores adicionales a medida que Stripe Terminal amplíe sus ofertas de hardware
- El menú desplegable de tipo de lector se completa automáticamente desde las capacidades del proveedor

## Flujo de trabajo de registro del lector

**Paso 1: Comprar y recibir el hardware**
- Ordene el lector desde Stripe (stripe.com/terminal) o un revendedor autorizado
- Desempaquete y encienda el lector
- Conéctelo a la red Wi-Fi (siga el proceso de configuración en pantalla del lector)

**Paso 2: Registrar en el panel de control de Stripe**
- Navegue hasta **Panel de control de Stripe > Terminal > Lectores**
- Haga clic en **Registrar nuevo lector**
- Siga el proceso de emparejamiento en pantalla (el lector muestra el código de registro)
- Asigne el lector a una ubicación de Stripe (debe coincidir con la ubicación en la configuración del proveedor de pagos)
- Anote el **ID del lector** (parece `tmr_ABC123...`)

**Paso 3: Sincronizar con Spwig (automático)**
- Spwig detecta automáticamente los lectores registrados en su ubicación de Stripe
- El trabajo en segundo plano sincroniza cada 30 minutos
- Los nuevos lectores aparecen en la lista **POS > Lectores de tarjetas** dentro de 30 minutos

**Paso 4: Asignar a terminal (manual)**
- Navegue hasta **POS > Lectores de tarjetas**
- Encuentre el lector descubierto recientemente en la lista
- Haga clic para editar
- Seleccione **Terminal** para asignar el lector
- Guarde

**Paso 5: Probar pago**
- En el terminal POS, realice una transacción de prueba
- Seleccione el método de pago con tarjeta
- El POS debe detectar el lector asignado
- Use la tarjeta de prueba de Stripe (4242 4242 4242 4242) para completar la prueba
- Verifique que el pago se complete con éxito

Si el lector no aparece durante la prueba, verifique la asignación del terminal y el estado del lector.

## Monitoreo del estado del lector

Los lectores informan su estado a la API de Stripe Terminal, que Spwig sincroniza cada 5 minutos:

**En línea** (verde) - El lector está encendido, conectado a la red y listo para aceptar pagos

**Fuera de línea** (rojo) - El lector está apagado, desconectado de la red o inalcanzable

**Ocupado** (amarillo) - El lector está procesando actualmente una transacción de pago

**Última vez visto** - Marca temporal de la última conexión del lector con la API de Stripe
- Se actualiza cada ~2 minutos cuando el lector esté en línea
- Útil para diagnosticar problemas de conectividad ("el lector se desconectó hace 3 horas" = problema de energía o red durante las horas de operación)

**Casos de uso del estado**:
- **Verificación previa a la apertura**: Verifique que todos los lectores de la tienda estén en línea antes de desbloquear las puertas
- **Solución de problemas**: "El registro 3 no acepta tarjetas" → Verifique el estado del lector → Muestra fuera de línea → Verifique la energía/red
- **Auditoría**: "¿Se procesaron pagos en el Terminal 5 ayer?" → Verifique la marca temporal de la última vez vista

## Asignación de terminal

Los lectores de tarjetas utilizan una **relación uno a uno** con los terminales:

**¿Por qué la asignación importa?**:
- Durante el pago, el POS necesita saber qué lector comunicarse
- Varios terminales compartiendo un solo lector causan conflictos (dos cajeros no pueden usar el mismo lector simultáneamente)
- Los lectores no asignados no se usarán (hardware huérfano)

**Reglas de asignación**:
- Cada terminal puede tener **exactamente uno** lector de tarjetas asignado
- Cada lector de tarjetas puede estar asignado a **exactamente uno** terminal
- Asignar un lector al Terminal A lo desasigna automáticamente del terminal anterior

**Cambio de asignaciones**:
- Edite el registro del lector
- Cambie el campo **Terminal** a un nuevo terminal
- Guarde
- El terminal anterior pierde la asignación del lector (mostrará un error "No se ha asignado ningún lector" durante el pago)

**Lectores no asignados**:
- Los lectores descubiertos recientemente comienzan no asignados
- Los lectores no asignados aparecen en la lista pero no son utilizables
- Asigne a un terminal para activarlos

## Personalización de la pantalla de inicio

Las pantallas de inicio del lector muestran la marca en la pantalla orientada al cliente cuando está inactiva:

**¿Qué es la pantalla de inicio?**
- Imagen mostrada en la pantalla del lector cuando no se está procesando un pago
- Reemplaza el logotipo predeterminado de Stripe con su marca
- Visible para los clientes mientras esperan en la caja

**Pantalla de inicio generada automáticamente vs. personalizada**:

**Generada automáticamente** (predeterminado):
- Spwig genera la pantalla de inicio desde su logotipo de tienda (si el logotipo está configurado en la configuración de la tienda)
- Tamaño automático según las especificaciones del lector (480×800 retrato)
- Monocromática para S700/P400, color para WisePOS E
- No se necesita configuración

**Pantalla de inicio personalizada** (avanzado):
- Suba su propia imagen de pantalla de inicio personalizada
- Control total sobre el diseño y la marca
- Debe cumplir con los requisitos de imagen (ver más abajo)

**Requisitos de la pantalla de inicio personalizada**:
- **Resolución**: Exactamente 480×800 píxeles (orientación retrato)
- **Formato**: PNG o JPG
- **S700/P400**: Solo monocromática (negro y blanco, sin grises)
- **WisePOS E**: Soporta color completo
- **Tamaño de archivo**: <200KB

**Configuración de la pantalla de inicio personalizada**:
1. Edite el registro del lector de tarjetas
2. Suba la imagen a **Campo de imagen de inicio personalizada** (o seleccione desde la Biblioteca de medios)
3. Guarde
4. La pantalla de inicio se sincroniza con el lector dentro de 5 minutos

**Eliminar la pantalla de inicio personalizada**:
- Limpiar el campo **Imagen de inicio personalizada**
- Guarde
- El lector vuelve a la pantalla de inicio generada automáticamente (o al predeterminado de Stripe si no hay logotipo de tienda)

**Prueba de la pantalla de inicio**:
- Después de subir, espere 5 minutos para la sincronización
- Visite el dispositivo del lector
- Verifique que la pantalla de inicio aparezca en la pantalla inactiva
- Compruebe la calidad de la imagen, el centrado y el contraste

## Configuración de la pantalla de inicio de Stripe

Detrás de escena, Spwig gestiona la configuración de la pantalla de inicio de Stripe Terminal:

**stripe_splash_file_id** - ID interno de Stripe para el archivo de imagen de pantalla subido
- Se establece automáticamente cuando se sube la pantalla de inicio
- Se usa para hacer referencia a la pantalla en la API de Stripe

**stripe_splash_config_id** - ID interno de Stripe para la configuración de la pantalla
- Vincula el archivo de pantalla al lector
- Se gestiona automáticamente al asignar la pantalla al lector

Estos campos son de solo lectura y se gestionan automáticamente; no necesita interactuar con ellos directamente.

## Solución de problemas de problemas comunes

**Problema 1: El lector muestra fuera de línea pero está encendido**
- **Causas**: Problema de conectividad de red, contraseña de Wi-Fi cambiada, lector fuera de rango
- **Solución**: Verifique la configuración de red del lector, reconéctese a Wi-Fi, verifique que la API de Stripe esté alcanzable desde la red

**Problema 2: El POS dice "No se ha asignado ningún lector" durante el pago**
- **Causa**: El lector no está asignado al terminal o la asignación no está completa
- **Solución**: Edite el lector, asígnelo al terminal, guarde, pruebe el pago nuevamente

**Problema 3: El lector está ocupado indefinidamente (atascado en la pantalla de pago)**
- **Causa**: Transacción con tiempo de espera agotado o caída, estado del lector no restablecido
- **Solución**: Reinicie el lector (ciclo de energía), contacte al soporte de Stripe si persiste

**Problema 4: La pantalla de inicio personalizada no aparece**
- **Causas**: Imagen con resolución incorrecta, no sincronizada aún, no se cumple el requisito de monocromática (S700/P400)
- **Solución**: Verifique que la imagen sea exactamente 480×800, espere 5 minutos para la sincronización, asegúrese de que sea monocromática para lectores no de color

**Problema 5: El lector está registrado en Stripe pero no aparece en Spwig**
- **Causa**: El lector está registrado en una ubicación de Stripe diferente a la del proveedor de configuración
- **Solución**: En el panel de control de Stripe, verifique que la ubicación del lector coincida con el ID de ubicación del proveedor

## Consejos

- **Un lector por terminal** - No comparta lectores entre terminales; evita conflictos y simplifica la responsabilidad
- **Registre lectores antes de implementar en el suelo** - Complete el registro de Stripe y la asignación de Spwig antes de colocar el lector en el punto de pago
- **Pruebe pantallas de inicio en tienda** - La contraste varía según el modelo del lector y la iluminación; verifique que la pantalla se vea bien en el entorno real
- **Monitorea el estado antes de abrir** - Revise la lista de lectores cada mañana para asegurarse de que todos estén en línea antes de que abra la tienda
- **Etique el hardware físicamente** - Use un fabricante de etiquetas para marcar el lector con el nombre del terminal ("Lector del Terminal 1") para una identificación fácil durante la solución de problemas
- **Mantén los lectores en energía ininterrumpida** - Apagados durante una transacción pueden corromper el estado del lector; se recomienda un sistema de alimentación ininterrumpida (UPS)
- **Documenta los números de serie de los lectores** - Mantén un registro de los números de serie para garantizar el servicio y el soporte (se encuentran en la etiqueta del hardware del lector)
- **Actualiza el firmware del lector** - Stripe envía actualizaciones de firmware automáticamente, pero verifica periódicamente que los lectores estén en la última versión (ver panel de control de Stripe)