---
title: Modo de mantenimiento
---

El modo de mantenimiento desactiva temporalmente tu tienda en línea y muestra a los clientes un mensaje de "volveremos pronto". Tu panel de administración permanece completamente accesible durante el mantenimiento — puedes seguir trabajando mientras los clientes ven la página de mantenimiento.

Utiliza el modo de mantenimiento antes de realizar cambios que puedan causar un estado inconsistente temporal, como ejecutar una importación masiva de productos, aplicar un rediseño importante del tema o esperar a que finalice una operación de restauración.

![Interruptor del modo de mantenimiento en el panel de sistema](/static/core/admin/img/help/maintenance-mode/system-dashboard-maintenance.webp)

## Habilitar el modo de mantenimiento

1. Navega a **Gestión > Métricas del sistema**
2. Haz clic en **Panel de sistema** desde la barra de herramientas
3. En el panel **Estado de la tienda**, haz clic en **Habilitar modo de mantenimiento**
4. Opcionalmente, ingresa un **Motivo** — esto es solo para tu referencia y no se muestra a los clientes (ej. `Actualización del catálogo de productos en curso`)
5. Confirma haciendo clic en **Habilitar**

Tu tienda en línea mostrará inmediatamente la página de mantenimiento a todos los visitantes. El panel de administración no se ve afectado y puedes seguir trabajando normalmente.

## Lo que ven los clientes

Cuando el modo de mantenimiento está activo, cada página de tu tienda en línea (la tienda, páginas de productos, proceso de pago y páginas de cuenta) muestra un aviso de mantenimiento con marca. El mensaje le indica a los clientes que la tienda está temporalmente no disponible y los anima a regresar pronto.

Los clientes que estén en medio de una sesión o en el proceso de pago cuando se habilite el modo de mantenimiento también verán la página de mantenimiento en su siguiente solicitud. No se pierden pedidos en proceso — los datos aún estarán disponibles cuando deshabilites el modo de mantenimiento.

## Deshabilitar el modo de mantenimiento

1. Navega a **Gestión > Métricas del sistema**
2. Haz clic en **Panel de sistema**
3. En el panel **Estado de la tienda**, verás una notificación confirmando que el modo de mantenimiento está activo
4. Haz clic en **Deshabilitar modo de mantenimiento**
5. Confirma cuando se te lo pida

La tienda en línea vuelve a estar en línea inmediatamente. Los clientes pueden navegar y comprar como de costumbre.

## Cuando Spwig habilita automáticamente el modo de mantenimiento

Ciertoas operaciones del sistema habilitan automáticamente el modo de mantenimiento y reactivan la tienda cuando terminan:

- **Actualizaciones de la plataforma** — el proceso de actualización habilita el modo de mantenimiento antes de aplicar cambios y lo deshabilita cuando la actualización esté completa
- **Operaciones de restauración** — restaurar desde una copia de seguridad pone la tienda en modo de mantenimiento durante la duración de la restauración

Si una operación automatizada termina inesperadamente, el modo de mantenimiento podría permanecer activo. En ese caso, sigue los pasos anteriores para deshabilitarlo manualmente.

## Consejos

- Siempre avisa a tu equipo antes de habilitar el modo de mantenimiento — afecta a todos los visitantes de tu tienda en línea
- Mantén los periodos de mantenimiento lo más cortos posible; incluso unos minutos sin conexión pueden afectar la confianza de los clientes
- Usa el campo de motivo como recordatorio sobre por qué se activó el modo de mantenimiento — aparece en el registro del sistema
- Si notas que el modo de mantenimiento está activo pero no lo habilitaste tú mismo, verifica el registro del sistema para ver si alguna operación automatizada lo activó
- Planifica los periodos de mantenimiento durante horas de baja afluencia (noches o temprano por la mañana) para minimizar el impacto en las ventas