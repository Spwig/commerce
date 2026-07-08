---
title: Turnos POS y Gestión de Efectivo
---

Los turnos POS rastrean los períodos de trabajo de los cajeros y garantizan una contabilidad precisa del efectivo. Cada turno representa el tiempo de un cajero en un terminal, desde abrir el cajón con un recuento inicial de efectivo hasta cerrar el turno con un recuento final y una reconciliación. El sistema calcula automáticamente el efectivo esperado basado en las ventas en efectivo reales y lo compara con el recuento físico, destacando las discrepancias para su investigación. Los movimientos de efectivo durante los turnos (adiciones de efectivo, retiros de efectivo de bolsillo) se rastrean con razones para un historial de auditoría completo.

Navegue hasta **POS > Turnos** para ver todos los turnos, supervisar los turnos activos, revisar informes de reconciliación de efectivo y auditar la actividad histórica.

![Lista de turnos](/static/core/admin/img/help/pos-shifts-cash-management/shift-list.webp)

## Entendiendo los turnos POS

Un turno es un período de trabajo durante el cual un cajero opera un terminal. Los turnos garantizan la responsabilidad del efectivo: cada cajero es responsable del efectivo en su cajón durante su turno.

**Ciclo de vida del turno**:
1. **Apertura** - El cajero inicia el turno, cuenta el efectivo inicial y registra la cantidad
2. **Durante el turno** - Procesa ventas, acepta pagos, emite reembolsos
3. **Cierre** - El cajero cuenta el efectivo, registra la cantidad final, el sistema calcula la discrepancia
4. **Reconciliado** - El turno se finaliza y se bloquea para auditoría

**Métricas clave rastreadas**:
- **Efectivo inicial** - Cantidad de efectivo en el cajón al inicio del turno
- **Efectivo final** - Efectivo físico en el cajón al final del turno
- **Efectivo esperado** - Calculado: Efectivo inicial + ventas en efectivo - reembolsos en efectivo + movimientos de efectivo
- **Diferencia de efectivo** - Discrepancia: Efectivo final - efectivo esperado (positivo = exceso, negativo = falta)
- **Total de ventas** - Suma de todas las transacciones de venta durante el turno
- **Total de reembolsos** - Suma de todas las transacciones de reembolso durante el turno
- **Conteo de transacciones** - Número de pedidos procesados

## Vista de la lista de turnos

La lista de turnos muestra todos los turnos con información clave:

**Estado del turno**:
- **Abierto** (etiqueta verde) - Turno activo actualmente
- **Cerrado** (etiqueta gris) - Turno completado
- **Reconciliado** (etiqueta azul) - Finalizado y bloqueado para auditoría

**Terminal** - ¿En qué terminal POS estuvo el turno

**Cajero** - Miembro del personal que trabajó el turno

**Efectivo inicial** - Cantidad inicial de efectivo

**Efectivo final** - Cantidad final de efectivo (en blanco si el turno aún está abierto)

**Efectivo esperado** - Cantidad esperada calculada por el sistema basada en las transacciones

**Diferencia de efectivo** - Discrepancia (destacada en rojo si es negativa, verde si es positiva, negra si es cero)

**Duración** - Duración del turno (hora de inicio a hora de finalización)

**Total de ventas** - Ingresos generados durante el turno

Use filters to view:
- Only open shifts (monitor active terminals)
- Shifts with discrepancies (cash difference ≠ 0)
- Shifts by date range (daily reconciliation reports)
- Shifts by cashier (performance audit)

## Abrir un turno

Los cajeros abren turnos directamente desde el terminal POS (no se pueden abrir desde el administrador). El flujo de trabajo en el terminal:

1. **Personal inicia sesión** - Ingresa sus credenciales para acceder al terminal

2. **Cuenta el efectivo inicial** - Cuenta físicamente todo el efectivo en el cajón (billetes y monedas)

3. **Ingresa la cantidad inicial** - Registra la cantidad contada en la aplicación POS

4. **Comienza el turno** - El terminal está listo para procesar ventas

**Directrices para el efectivo inicial**:
- El efectivo inicial (flotante) estándar suele ser de $100-$300 según el tamaño de la tienda
- Cuenta dos veces para garantizar precisión—los errores en la apertura se propagan a las discrepancias en el cierre
- Si el cajón está vacío, el efectivo inicial es $0.00 (flotante agregado mediante movimiento de efectivo)
- Documente billetes grandes (>$50) por separado para rastrear su movimiento

![Formulario de agregar turno](/static/core/admin/img/help/pos-shifts-cash-management/shift-add-form.webp)

## Durante el turno

Mientras el turno está abierto, el sistema rastrea automáticamente:

**Ventas en efectivo** - Cualquier transacción donde el cliente pague con efectivo físico (agrega al efectivo esperado)

**Reembolsos en efectivo** - Cualquier reembolso emitido en efectivo (resta del efectivo esperado)

**Ventas con tarjeta** - Transacciones con tarjetas de crédito/débito (no afectan el efectivo)

**Pago combinado** - Pago parcial en efectivo + parcial en tarjeta (solo la parte en efectivo afecta el efectivo esperado)

**Tarjetas regalo y vales** - Métodos de pago no en efectivo (no afectan el efectivo)

Los cajeros continúan procesando ventas normalmente. El sistema mantiene un cálculo en curso de efectivo esperado detrás de escena.

## Movimientos de efectivo

Los movimientos de efectivo son ajustes al cajón durante un turno:

**Adiciones de flotante** - Agregar efectivo al cajón:
- Razón: "Agregando cambio para billetes grandes"
- Cantidad: +$100.00
- El efectivo esperado aumenta en $100.00

**Retiros de efectivo de bolsillo** - Retirar efectivo para gastos:
- Razón: "Compra de suministros de oficina"
- Cantidad: -$25.00
- El efectivo esperado disminuye en $25.00

**Depósitos bancarios** - Retirar efectivo excesivo por seguridad:
- Razón: "Depósito seguro - más de $500 en el cajón"
- Cantidad: -$300.00
- El efectivo esperado disminuye en $300.00

**Registros de movimientos de efectivo en el terminal**:
1. Toque **Menú** > **Movimiento de efectivo**
2. Seleccione el tipo: Agregar o Quitar
3. Ingrese la cantidad
4. Ingrese la razón (requerida para el historial de auditoría)
5. Confirme

Todos los movimientos de efectivo aparecen en el informe de detalles del turno con marcas de tiempo, cantidades y razones.

## Cerrar un turno

Cuando un cajero termina su período de trabajo, cierra el turno:

1. **Toque Cerrar turno** - En el menú del terminal

2. **Procese las transacciones restantes** - Complete cualquier carrito de compras en espera o ventas pendientes

3. **Cuenta el efectivo final** - Cuenta físicamente todo el efectivo en el cajón
   - Cuenta los billetes por denominación ($100s, $50s, $20s, $10s, $5s, $1s)
   - Cuenta las monedas por tipo (cuartos, décimos, níquel, centavos)
   - Total = cantidad final de efectivo

4. **Ingrese la cantidad final** - Registra el total contado

5. **El sistema calcula la discrepancia**:
   - Efectivo esperado = Efectivo inicial + ventas en efectivo - reembolsos en efectivo + movimientos de efectivo
   - Diferencia de efectivo = Efectivo final - efectivo esperado
   - Ejemplo: Efectivo final $485.00 - Efectivo esperado $480.00 = +$5.00 exceso

6. **Revise la discrepancia** - El terminal muestra la diferencia:
   - **Exacto ($0.00)** - Reconciliación perfecta
   - **Exceso pequeño (+$1 a +$5)** - Redondeo aceptable o propina del cliente
   - **Falta pequeña (-$1 a -$5)** - Error menor de conteo, aceptable
   - **Discrepancia grande (>$5)** - Reconteo requerido

7. **Reconteo si es necesario** - Si la discrepancia es grande (>$10), el cajero debe recontar el efectivo final antes de finalizar

8. **Finalizar el turno** - Confirme la cantidad final, el estado del turno cambia a "Cerrado"

9. **Imprima el informe del turno** - El terminal imprime un recibo de reconciliación de efectivo para los registros del cajero

![Detalles del turno](/static/core/admin/img/help/pos-shifts-cash-management/shift-detail.webp)

## Fórmula de reconciliación de efectivo

El sistema calcula el efectivo esperado usando esta fórmula:

```
Efectivo esperado = Efectivo inicial
                + Ventas en efectivo
                - Reembolsos en efectivo
                + Adiciones de efectivo (movimientos)
                - Retiros de efectivo (movimientos)
```

**Ejemplo**:
- Efectivo inicial: $200.00
- Ventas en efectivo: $450.00 (de 15 transacciones)
- Reembolsos en efectivo: -$30.00 (1 devolución)
- Adición de efectivo: +$100.00 (efectivo agregado durante el turno)
- Retiro de efectivo: -$50.00 (retiro de efectivo de bolsillo)
- **Efectivo esperado: $200 + $450 - $30 + $100 - $50 = $670.00**

Si el cajero cuenta $675.00 al cerrar:
- Diferencia de efectivo: $675.00 - $670.00 = **+$5.00 exceso**

## Informes y auditoría de turnos

Los informes de turnos proporcionan información de reconciliación detallada:

**Sección de resumen**:
- Efectivo inicial y final
- Cálculo del efectivo esperado
- Diferencia de efectivo (exceso/falta)
- Total de ventas y reembolsos
- Conteo de transacciones
- Duración del turno

**Detalles de transacción**:
- Todas las ventas durante el turno (IDs de pedidos, cantidades, métodos de pago)
- Todos los reembolsos emitidos
- Marca de tiempo de cada transacción

**Registro de movimientos de efectivo**:
- Todas las adiciones y retiros
- Razones proporcionadas
- Marcas de tiempo

**Casos de uso**:
- **Reconciliación diaria** - Revisar todos los turnos al final del día laboral
- **Rendimiento del cajero** - Identificar patrones de discrepancias por miembro del personal
- **Detección de robo** - Falta grande y consistente puede indicar robo
- **Necesidades de capacitación** - Discrepancias frecuentes pequeñas sugieren problemas de precisión en el conteo
- **Historial de auditoría** - Registro completo para propósitos contables y fiscales

## Gestión de efectivo con múltiples terminales

Para tiendas con múltiples terminales que ejecutan turnos concurrentes:

**Cajones separados**: Cada terminal tiene su propio cajón de efectivo—los turnos son independientes. El cajero A en el Terminal 1 y el cajero B en el Terminal 2 ejecutan turnos separados con reconciliación separada.

**Cajón compartido**: Algunas tiendas comparten un solo cajón de efectivo entre múltiples terminales (no se recomienda). Si lo hace:
- Solo un turno puede estar abierto por cajón compartido en un momento dado
- Los cajeros deben cerrar el turno al pasarle el cajón al siguiente cajero
- Los movimientos de efectivo rastrean todas las adiciones/retiros durante las transferencias
- Las discrepancias son más difíciles de atribuir a cajeros específicos

**Mejor práctica**: Un cajón de efectivo por terminal, un turno por cajero por sesión. Esto garantiza una responsabilidad clara y una reconciliación simplificada.

## Manejo de discrepancias

Cuando el efectivo cerrado no coincide con el efectivo esperado:

**Discrepancias pequeñas (<$5)**:
- Aceptables debido a redondeo, errores de conteo o propinas del cliente
- Documente en notas del turno
- No se necesita ninguna acción adicional a menos que aparezca un patrón

**Discrepancias medianas ($5-$20)**:
- Reconteo de efectivo antes de finalizar el turno
- Revise el registro de transacciones en busca de errores (cambio incorrecto dado, transacción anulada no procesada)
- Documente las circunstancias en las notas del turno
- Se recomienda una revisión por parte del gerente

**Discrepancias grandes (>$20)**:
- Reconteo obligatorio
- Se requiere aprobación del gerente para cerrar el turno
- Revise todas las transacciones y movimientos de efectivo
- Investigue posibles causas (robo, toque de cajón, efectivo inicial incorrecto)
- Puede requerir acción disciplinaria según las circunstancias

**Faltas consistentes**:
- Patrón de discrepancias negativas del mismo cajero = problema de capacitación o robo
- Implemente supervisión adicional (revisión aleatoria del gerente durante el turno)
- Revise los procedimientos de capacitación en POS
- Considere actualizaciones en las políticas de manejo de efectivo

## Consejos

- **Cuenta el efectivo inicial dos veces** - Los errores en la apertura se propagan a las discrepancias en el cierre; la precisión al inicio evita problemas al final
- **Registra los movimientos de efectivo inmediatamente** - No espere hasta el cierre para documentar adiciones de flotante o retiros de efectivo de bolsillo
- **Siempre proporciona razones para los movimientos** - "Agregado $100" es inútil para auditoría; "Agregado $100 para cambio (pocos billetes de $5)" es útil
- **Recontea si la discrepancia es >$10** - No finalices el turno con una discrepancia grande sin recontar
- **Imprime informes de turnos diariamente** - Adjunta a la documentación de reconciliación diaria para contabilidad
- **Revisa patrones, no discrepancias individuales** - Una falta de -$3.00 está bien; cinco faltas consecutivas de -$3.00 es un problema
- **Cierra los turnos al final del día** - No dejes los turnos abiertos toda la noche; las discrepancias son más fáciles de investigar cuando son recientes
- **Capacita a los cajeros en el conteo por denominación** - La mayoría de los errores provienen del conteo incorrecto de billetes (pensar que un $5 es un $10)
- **Usa envolturas para monedas** - Las monedas pre-empacadas reducen errores de conteo y aceleran la reconciliación

