---
title: Solicitudes de devolución y procesamiento
---

Las solicitudes de devolución rastrean las devoluciones de los clientes desde su inicio hasta la finalización del reembolso—los clientes seleccionan artículos para devolver con razones, los comerciantes aprueban o rechazan las solicitudes, generan etiquetas de devolución, inspeccionan los artículos devueltos y procesan reembolsos. El flujo de trabajo avanza a través de 9 etapas de estado (pendiente → aprobado → etiqueta_enviada → en_transito → recibido → inspeccionado → completado/rechazado/anulado) con razones de devolución a nivel de artículo, notas de inspección y tarifas de reestablecimiento opcionales.

Use esta página de administración para revisar, aprobar y procesar solicitudes de devolución de clientes de manera eficiente.

## Flujo de trabajo de solicitudes de devolución

**Proceso de 9 etapas**:

### 1. Pendiente (Cliente inicia)

Cliente envía solicitud de devolución:
- Selecciona artículos del pedido
- Proporciona razón de devolución por artículo
- Notas del cliente (opcional)
- Estado: `pendiente`

### 2. Aprobado/Rechazado (Comerciante revisa)

Comerciante revisa la solicitud:
- **Aprobar**: Devolución permitida, proceder a generar etiqueta
- **Rechazar**: Devolución denegada con razón de rechazo
- Estado: `aprobado` o `rechazado`

### 3. Etiqueta enviada (Envío de devolución)

Etiqueta de devolución generada:
- Comerciante crea envío de devolución (opcional)
- Etiqueta de devolución enviada por correo electrónico al cliente
- Cliente envía los artículos de regreso
- Estado: `etiqueta_enviada`

### 4. En tránsito (Cliente envía)

Cliente envía los artículos:
- El seguimiento muestra el movimiento
- Actualización automática de estado desde la webhook del transportista
- Estado: `en_transito`

### 5. Recibido (Llega al almacén)

Artículos llegan:
- El almacén escanea el envío
- Artículos revisados
- Estado: `recibido`

### 6. Inspeccionado (Revisión de calidad)

Comerciante inspecciona los artículos:
- Registra el estado del artículo (excelente/bueno/aceptable/dañado/defectuoso)
- Añade notas de inspección
- Aplica tarifa de reestablecimiento si aplica
- Estado: `inspeccionado`

### 7. Completado (Reembolso procesado)

Reembolso emitido:
- Crea reembolso asociado
- Pago procesado
- Devolución cerrada
- Estado: `completado`

**Resultados alternativos**:
- **Anulado**: Cliente cancela antes del envío
- **Rechazado**: Comerciante deniega después de la revisión

---

## Procesamiento de solicitudes de devolución

**Paso a paso**:

**Paso 1: Revisar solicitudes pendientes**
- Navegue a Pedidos > Solicitudes de devolución
- Filtre por estado = "Pendiente"
- Haga clic en la solicitud para ver detalles

**Paso 2: Evaluar la solicitud**
- Revisar detalles del pedido
- Ver razones de devolución
- Verificar cumplimiento con la política de devolución (dentro del periodo de devolución, artículos elegibles)

**Paso 3: Aprobar o rechazar**
- Haga clic en "Aprobar" para aceptar la devolución
- O haga clic en "Rechazar" y escriba la razón de rechazo
- Guarde su decisión

**Paso 4: Generar etiqueta de devolución** (si aprobada)
- Haga clic en "Crear envío de devolución"
- Seleccione transportista/servicio
- El sistema genera la etiqueta de devolución
- Etiqueta enviada automáticamente al cliente
- Estado → `etiqueta_enviada`

**Paso 5: Monitorear tránsito**
- Las actualizaciones de seguimiento se sincronizan automáticamente desde las webhooks del transportista
- El estado avanza automáticamente a `en_transito` cuando el transportista escanea el paquete

**Paso 6: Recibir artículos**
- Cuando los artículos llegan, haga clic en "Marcar como recibido"
- Estado → `recibido`

**Paso 7: Inspeccionar artículos**
- Abra la solicitud de devolución
- Seleccione el estado del artículo desde el menú desplegable:
  - Excelente (como nuevo, reventa posible)
  - Bueno (uso mínimo, reventa posible)
  - Aceptable (uso visible, reventa posible con descuento)
  - Dañado (no reventa posible)
  - Defectuoso (defecto de fabricación)
- Añade notas de inspección
- Opcional: Aplicar tarifa de reestablecimiento (porcentaje o fijo)
- Estado → `inspeccionado`

**Paso 8: Procesar reembolso**
- Haga clic en "Crear reembolso"
- El sistema calcula el monto del reembolso:
  - Precio original del artículo
  - Menos tarifa de reestablecimiento (si se aplica)
  - Menos costo de envío (si no es reembolsable)
- Cree reembolso (vinculado a la solicitud de devolución)
- Estado → `completado`

---

## Razones de devolución a nivel de artículo

Los clientes seleccionan la razón por artículo:

**Razones comunes**:
- Artículo incorrecto recibido
- Artículo dañado/defectuoso
- Cambio de opinión/no necesario
- Artículo no coincide con la descripción
- Mejor precio encontrado
- Pedido por error
- Calidad no como esperado

**Uso de razones para**:
- Análisis (rastrear causas comunes de devolución)
- Control de calidad (identificar productos defectuosos)
- Mejora del proceso (reducir devoluciones prevenibles)

---

## Tarifas de reestablecimiento

Aplicar tarifas para compensar costos de procesamiento de devoluciones:

**Configuración**:
- **Tipo**: Porcentaje (ej. 15%) o Fijo (ej. $5)
- **Cuándo aplicar**: Devoluciones no defectuosas, artículos abiertos, pedidos especiales

**Ejemplo**:
```
Compra original: $100
Tarifa de reestablecimiento: 15%
Monto del reembolso: $85
```

**Mejores prácticas**:
- Comunique claramente la política de tarifas de reestablecimiento
- No aplicar a artículos defectuosos
- Considere eximir a clientes VIP

---

## Guías de inspección de devoluciones

Establezca criterios de inspección consistentes:

**Excelente**:
- Empaque original sin abrir
- Sin desgaste visible
- Todos los accesorios incluidos
- Reventa completa al precio completo

**Bueno**:
- Abierto pero uso mínimo
- Desgaste mínimo del empaque
- Todos los componentes presentes
- Reventa completa al precio completo

**Aceptable**:
- Uso visible/desgaste
- Empaque dañado
- Faltan accesorios no esenciales
- Reventa con descuento

**Dañado**:
- Daño físico
- Piezas faltantes
- No reventa posible
- Requerido descarte o reparación

**Defectuoso**:
- Defecto de fabricación
- Fallo funcional
- Reclamación de garantía
- Devolución al fabricante

---

## Opciones de envío de devoluciones

**Opción 1: Cliente paga envío de devolución**
- No se proporciona etiqueta de devolución
- Cliente elige su propio transportista
- Ingreso manual del número de seguimiento

**Opción 2: Comerciante proporciona etiqueta prepagada**
- Genere etiqueta de devolución a través de la cuenta del proveedor
- Costo deducido del reembolso O comerciante lo asume
- Seguimiento sincronizado automáticamente

**Opción 3: Envío de devolución gratuito**
- Comerciante asume el costo del envío de devolución
- Mejora la satisfacción del cliente
- Aumenta la tasa de devolución (considere el equilibrio)

---

## Filtros y reportes

**Filtros útiles**:
- Estado: Pendiente (requiere acción)
- Rango de fechas: Últimos 30 días
- Pedido: Búsqueda de pedido específico
- Razón: Rastrear causas de devolución

**Análisis de devoluciones**:
- Tasa de devolución por producto
- Razones de devolución más comunes
- Tiempo promedio de procesamiento (pendiente → completado)
- Ingresos por tarifas de reestablecimiento

---

## Consejos

- **Establezca una política de devolución clara** - Comunique el periodo (30 días), condiciones, tarifas
- **Procese las solicitudes de forma oportuna** - Responda a las solicitudes pendientes dentro de 24 horas
- **Revise detalladamente** - Documente el estado para evitar disputas
- **Rastree las razones de devolución** - Use los datos para mejorar productos/descripciones
- **Automatice donde sea posible** - Webhooks de transportista actualizan automáticamente el estado del tránsito
- **Comuníquese con los clientes** - Envíe actualizaciones por correo electrónico en cada cambio de estado
- **Sea justo con las tarifas de reestablecimiento** - Aplique consistentemente, exima por defectos
- **Monitorea fraudes de devolución** - Marque a clientes con demasiadas devoluciones
- **Mejore el empaque** - Reduzca devoluciones por daño
- **Actualice el inventario rápidamente** - Restablezca el inventario después de la inspección
- **Aprenda de patrones** - Devoluciones altas para productos específicos pueden indicar un problema de calidad

Recuerde: Devuelva solo el objeto JSON con los campos "title" y "content". Preserve todo el formato markdown, rutas de imágenes, bloques de código y términos técnicos exactamente como se muestran arriba.