---
title: Configuración de impuestos
---

Configure las reglas de impuestos para su tienda para que los impuestos correctos se apliquen automáticamente a los pedidos según la ubicación del cliente. Puede cargar configuraciones predeterminadas regionales con un solo clic o crear reglas personalizadas para cualquier país, estado, ciudad o código postal.

![Panel de impuestos](/static/core/admin/img/help/tax-configuration/tax-dashboard.webp)

## Panel de impuestos

Navegue hasta **Pedidos > Envíos > Tasa de impuestos** para abrir el panel de impuestos. La página muestra:

- **Panel de estadísticas** — cuatro tarjetas que muestran Reglas totales, Reglas activas, Países cubiertos y Tipos de impuestos en uso
- **Filtros** — buscar por nombre, país o estado, y filtrar por país, tipo de impuesto (Impuesto sobre ventas, IVA, IGV, Personalizado) o estado (Activo/Inactivo)
- **Tarjetas de reglas de impuestos** — cada tarjeta muestra la bandera del país, el nombre de la regla, la ubicación, el porcentaje de tasa, el distintivo del tipo de impuesto, el distintivo del estado, la prioridad y la cantidad de exenciones

## Carga de configuraciones predeterminadas

Haga clic en **Cargar configuraciones predeterminadas** para abrir el cuadro de diálogo de configuraciones predeterminadas. Las configuraciones predeterminadas son colecciones de tasas impositivas estándar para una región, listas para cargarse en su tienda con un solo clic.

![Cargar configuraciones predeterminadas](/static/core/admin/img/help/tax-configuration/tax-presets-modal.webp)

Las configuraciones predeterminadas se organizan por región del mundo:

| Región | Grupos de configuraciones predeterminadas |
|--------|--------------|
| **África** | IVA de África (25 tasas) |
| **Asia Pacífico** | IVA/IGV del Asia Pacífico (24 tasas), IVA de Asia Central (6 tasas) |
| **Europa** | Tasas de IVA de la UE, IVA del Reino Unido, Otros impuestos de Europa |
| **América Latina** | IVA de América Latina |
| **Medio Oriente** | IVA del Medio Oriente |
| **América del Norte** | Impuesto sobre ventas de los estados de EE. UU., IGV/HST de Canadá |
| **Oceanía** | IGV/IVA de Oceanía |

### Cómo funcionan las configuraciones predeterminadas

1. Haga clic en **Cargar** en el grupo de configuraciones predeterminadas que desee
2. El sistema crea reglas de impuestos para cada país o estado de ese grupo
3. Las reglas existentes con el mismo país, estado y tipo de impuesto se omiten automáticamente para evitar duplicados
4. Después de cargar, cada regla es completamente editable — ajuste las tasas, agregue exenciones o desactive las reglas que no necesite

Puede cargar varios grupos de configuraciones predeterminadas. Por ejemplo, cargue tanto las tasas de IVA de la UE como las del Reino Unido si vende a clientes en toda Europa.

## Crear reglas de impuestos manualmente

Haga clic en **Añadir tasa de impuesto** para crear una regla personalizada. El formulario tiene cuatro secciones:

![Formulario de tasa de impuesto](/static/core/admin/img/help/tax-configuration/tax-rate-form.webp)

### Información básica

| Campo | Descripción |
|-------|-------------|
| **Nombre** | Nombre de visualización de la regla (por ejemplo, "Impuesto sobre ventas de California") |
| **Activo** | Conmutador para habilitar o deshabilitar la regla |
| **Tipo de impuesto** | Impuesto sobre ventas, IVA, IGV o impuesto personalizado |
| **Tasa (%)** | La tasa impositiva como porcentaje (por ejemplo, ingrese 8.25 para 8.25%) |
| **Prioridad** | Los números más altos tienen prioridad cuando múltiples reglas coinciden con la misma ubicación |

### Alcance geográfico

| Campo | Descripción |
|-------|-------------|
| **País** | Código alfa-2 ISO 3166-1 (por ejemplo, US, GB, DE) |
| **Estado** | Estado o provincia (dejar en blanco para aplicar a todo el país) |
| **Ciudad** | Nombre de la ciudad (opcional, para reglas de impuesto a nivel de ciudad) |
| **Códigos postales** | Lista de códigos postales específicos (opcional, para reglas de impuesto a nivel de código postal) |

Las reglas se coinciden de lo más específico a lo menos específico. Una regla para un código postal específico tiene prioridad sobre una regla para el mismo estado, que tiene prioridad sobre una regla a nivel de país.

### Reglas de aplicación

| Campo | Descripción |
|-------|-------------|
| **Aplicar a envíos** | Cuando se marca, este impuesto también se aplica a los costos de envío |
| **Impuesto compuesto** | Cuando se marca, este impuesto se calcula sobre otros impuestos (la cantidad base más impuestos aplicados anteriormente) |

### Exenciones de productos

| Campo | Descripción |
|-------|-------------|
| **Tipos de productos exentos** | Tipos de productos exentos de este impuesto (por ejemplo, digitales, servicios) |
| **Categorías exentas** | Categorías de productos específicas exentas de este impuesto |

## Tipos de impuestos

| Tipo | Usado para | Ejemplos |
|------|----------|---------|
| **Impuesto sobre ventas** | EE. UU., Canadá | Impuestos sobre ventas estatales y provinciales |
| **IVA** | Europa, Reino Unido, gran parte de Asia y África | Impuesto sobre el valor agregado |
| **IGV** | Australia, Nueva Zelanda, India, Singapur | Impuesto al consumo de bienes y servicios |
| **Impuesto personalizado** | Casos especiales | Recargos locales, impuestos ambientales, impuestos a lujo |

## Cómo funciona el cálculo de impuestos

Cuando un cliente llega al proceso de pago, el sistema calcula automáticamente los impuestos según su dirección de envío:

1. **Coincidencia geográfica** — encuentra todas las reglas activas que coinciden con el país del cliente, luego se estrecha por estado, ciudad y código postal
2. **Puntuación de especificidad** — las reglas más específicas (código postal > ciudad > estado > país) se clasifican más alto
3. **Orden de prioridad** — dentro del mismo nivel de especificidad, las reglas con mayor prioridad tienen prioridad
4. **Exenciones de productos** — los productos exentos se excluyen de cada regla aplicable
5. **Impuestos no compuestos** — se calculan primero en el precio base de cada artículo
6. **Impuestos compuestos** — se calculan en el precio base más todos los impuestos no compuestos ya aplicados
7. **Impuesto de envío** — si una regla tiene "Aplicar a envíos" habilitado, el costo de envío se incluye en el monto gravable

El desglose de impuestos se almacena con el pedido para que pueda ver exactamente qué reglas se aplicaron y cuánto aportó cada una.

## Configuraciones comunes

### Tienda de la UE

1. Haga clic en **Cargar configuraciones predeterminadas** y cargue el grupo **Tasas de IVA de la UE**
2. Esto crea reglas de IVA para todos los estados miembros de la UE con sus tasas estándar actuales
3. Opcionalmente, cargue **IVA del Reino Unido** si también vende a clientes del Reino Unido

### Tienda de EE. UU.

1. Haga clic en **Cargar configuraciones predeterminadas** y cargue el grupo **Impuesto sobre ventas de los estados de EE. UU.**
2. Esto crea reglas de impuesto sobre ventas para todos los estados de EE. UU. que recaudan impuesto sobre ventas
3. Para impuestos a nivel de ciudad, agregue manualmente reglas con el campo de ciudad rellenado y una prioridad más alta

### Tienda de múltiples regiones

1. Cargue varios grupos de configuraciones predeterminadas para cada mercado en el que venda
2. El sistema aplica el impuesto correcto según la ubicación de cada cliente
3. Ajuste las reglas individuales según sea necesario para sus requisitos empresariales específicos

## Consejos

- **Comience con configuraciones predeterminadas** — cargue los grupos de configuraciones predeterminadas para sus mercados objetivo, luego personalice las tasas individuales en lugar de crear cada regla desde cero.
- **Use la prioridad con sabiduría** — establezca valores de prioridad más altos para las reglas locales más específicas para que correctamente sobrescriban las reglas regionales más amplias.
- **Revise cuidadosamente el impuesto compuesto** — el impuesto compuesto es raro. La mayoría de las jurisdicciones usan impuestos simples (no compuestos). Solo habilite el impuesto compuesto cuando sus regulaciones locales específicamente requieran el cálculo de impuesto sobre impuesto.
- **Mantenga las reglas activas/inactivas** — en lugar de eliminar reglas de impuesto para cambios estacionales o temporales, active/desactive las reglas según sea necesario.
- **Pruebe antes de lanzar** — después de configurar sus reglas de impuesto, coloque un pedido de prueba desde diferentes direcciones para verificar que los impuestos correctos se estén aplicando.