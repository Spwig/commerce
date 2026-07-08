---
title: POS Store Groups
---

Los grupos de tienda organizan múltiples ubicaciones minoristas con configuraciones compartidas. En lugar de configurar cada terminal individualmente, agrupe terminales por región, franquicia o tipo de ubicación y aplique configuraciones a nivel de grupo. Los grupos admiten la herencia de configuraciones: la moneda, el idioma, la zona horaria, los modelos de recibos y el contenido promocional se propagan desde el grupo a las tiendas individuales. Esto simplifica la gestión para comerciantes con múltiples ubicaciones, mientras mantiene la flexibilidad para anular configuraciones específicas de la tienda cuando sea necesario.

Use grupos de tienda cuando opere múltiples ubicaciones minoristas, franquicias o mercados regionales con requisitos operativos diferentes.

![Lista de grupos de tienda](/static/core/admin/img/help/pos-store-groups/storegroup-list.webp)

## ¿Qué son los grupos de tienda?

Los grupos de tienda son contenedores organizacionales para almacenes y terminales que comparten características comunes:

**Estrategias de agrupamiento comunes**:
- **Geográfica**: Región Norte, Región Sur, Costa Oeste, Costa Este
- **Franquicia**: Tiendas del Franquiciado A, Tiendas del Franquiciado B, Tiendas Corporativas
- **Formato**: Ubicaciones en centros comerciales, Tiendas independientes, Tiendas puntuales
- **Mercado**: Tiendas nacionales, Tiendas europeas, Tiendas del Pacífico Asiático

Los grupos no cambian la operación física de los terminales; proporcionan una capa de configuración que simplifica la gestión a gran escala.

## ¿Cuándo usar grupos de tienda

**Una ubicación** - No se necesitan grupos. Configure los terminales directamente.

**2-3 ubicaciones con configuraciones idénticas** - Los grupos son opcionales. Puede ser más fácil configurar los terminales directamente.

**4+ ubicaciones** - Se recomiendan fuertemente los grupos. La configuración centralizada ahorra tiempo.

**Operaciones multicolor** - Los grupos son esenciales. Diferentes monedas, idiomas y zonas horarias requieren anulaciones a nivel de grupo.

**Operaciones de franquicia** - Los grupos son críticos. Cada franquiciado necesita configuraciones independientes mientras se mantiene la coherencia de la marca.

## Jerarquía de herencia de configuraciones

Spwig POS utiliza una cascada de 4 niveles de configuración (prioridad más alta a más baja):

| Nivel | Prioridad | Ejemplo | Caso de uso |
|-------|----------|---------|----------|
| **Terminal** | 1 (Más alta) | El terminal 5 anula el ancho del papel a 58mm | Un solo terminal tiene hardware de impresora único |
| **Tienda** | 2 | La tienda 2 anula la moneda a GBP | Ubicación en el Reino Unido entre principalmente tiendas de EE. UU. |
| **Grupo** | 3 | El grupo europeo establece la zona horaria a CET | Coherencia regional en múltiples tiendas |
| **Sitio** | 4 (Más baja) | Valor predeterminado global: USD, inglés, UTC | Valor predeterminado para todas las configuraciones no establecidas |

**Cómo funciona**:
- El sistema verifica primero la configuración del terminal
- Si no está establecida, verifica la configuración de la tienda
- Si no está establecida, verifica la configuración del grupo
- Si no está establecida, usa los valores predeterminados del sitio

**Ejemplo**:
- Valor predeterminado del sitio: Moneda = USD, Idioma = Inglés
- Grupo "Tiendas europeas": Moneda = EUR, Idioma = no establecido
- Tienda "Tienda insignia de París": Moneda = no establecido, Idioma = Francés
- Terminal "Registro 1 de París": Moneda = no establecido, Idioma = no establecido

**Resultado para Registro 1 de París**:
- Moneda: EUR (heredado del grupo)
- Idioma: Francés (heredado de la tienda)

Esta cascada permite configuraciones generales amplias con anulaciones específicas cuando sea necesario.

## Crear un grupo de tienda

Navegue a **POS > Grupos de tienda** y haga clic en **+ Agregar grupo de tienda**:

![Formulario de agregar grupo de tienda](/static/core/admin/img/help/pos-store-groups/storegroup-add-form.webp)

### Configuración básica

**Nombre del grupo** - Etiqueta descriptiva (ej. "Tiendas de la Costa Oeste", "Franquicias Europeas", "Ubicaciones en centros comerciales")

**Código** - Identificador corto y único (ej. "WEST", "EUR", "MALL"):
- Se usa internamente para referencias
- Debe ser único en todos los grupos
- 2-10 caracteres, alfanuméricos
- Se recomienda mayúsculas para coherencia

**Orden de clasificación** - Controla el orden de visualización en listas de administración (los números más bajos aparecen primero):
- Use múltiplos de 10: 10, 20, 30 (permite insertar nuevos grupos entre existentes)
- Ayuda a organizar grupos lógicamente (orden geográfico, orden de tamaño, etc.)

### Anulaciones regionales

**Anulación de moneda** - Establezca una moneda a nivel de grupo diferente del valor predeterminado del sitio:
- Ejemplo: El grupo europeo usa EUR, el grupo del Pacífico Asiático usa JPY
- Todos los terminales en este grupo usan esta moneda como valor predeterminado
- Afecta la visualización de precios, la reconciliación de efectivo y los informes

**Anulación de idioma** - Establezca un idioma a nivel de grupo diferente del valor predeterminado del sitio:
- Ejemplo: Las tiendas francesas usan francés, las tiendas alemanas usan alemán
- Afecta el idioma de la interfaz de POS, el idioma de los recibos (si el modelo de recibo lo admite)
- El personal ve la interfaz de POS en este idioma al iniciar sesión en terminales del grupo

**Anulación de zona horaria** - Establezca una zona horaria a nivel de grupo diferente del valor predeterminado del sitio:
- Ejemplo: Las tiendas de la costa oeste usan America/Los_Angeles, las tiendas europeas usan Europe/Paris
- Afecta los horarios de turno, la programación de informes y la programación de diapositivas promocionales
- Asegura que los informes de turnos se alineen con las horas de negocio locales

**Cuándo anular**:
- **Moneda**: Anule siempre para ubicaciones internacionales (diferentes monedas de pago)
- **Idioma**: Anule para mercados no hablantes de inglés (contenido orientado al cliente)
- **Zona horaria**: Anule para ubicaciones >2 horas desde el valor predeterminado del sitio (horas locales precisas)

## Asociar almacenes con grupos

Después de crear un grupo, asigne almacenes a él:

1. Navegue a **Catálogo > Almacenes**
2. Edite el almacén que representa una ubicación de tienda
3. Establezca el campo **Grupo de tienda** en su grupo creado
4. Guarde

Todos los terminales asignados a este almacén ahora heredan la configuración del grupo.

**Configuración de ejemplo**:
- Cree grupo: "Tiendas europeas" (Moneda: EUR, Idioma: no establecido, Zona horaria: CET)
- Cree almacenes: "Tienda de París", "Tienda de Berlín", "Tienda de Roma"
- Asigne los 3 almacenes al grupo "Tiendas europeas"
- Cree terminales: "Registro 1 de París", "Registro 1 de Berlín", "Registro 1 de Roma"
- Cada terminal hereda la moneda EUR y la zona horaria CET del grupo
- Anule el idioma a nivel de tienda: París=Francés, Berlín=Alemán, Roma=Italiano

## Configuraciones controladas por grupos

Los grupos pueden anular estas configuraciones:

**Configuraciones operativas**:
- Moneda (afecta la visualización de precios y la reconciliación de efectivo)
- Idioma (afecta el idioma de la interfaz de POS)
- Zona horaria (afecta los horarios y la programación)

**Configuraciones de contenido** (a través de modelos con ámbito):
- Modelos de recibos (crea diseños de recibos específicos del grupo)
- Diapositivas promocionales (dirige promociones a grupos específicos)

**No controladas por grupos**:
- Configuración del hardware del terminal (configurada por terminal)
- Asignaciones de personal (configuradas por terminal)
- Niveles de stock de almacén (configurados por almacén)
- Cuentas de proveedores de pago (configuradas a nivel de sitio o por proveedor)

## Ejemplos del mundo real

### Ejemplo 1: Minorista de moda internacional

**Configuración**:
- 50 tiendas en 5 países
- Cada país tiene diferentes monedas, idiomas y requisitos fiscales

**Estructura de grupo**:
- Grupo: "Tiendas de EE. UU." (USD, inglés, America/New_York)
  - 20 almacenes (Nueva York, Los Ángeles, Chicago, etc.)
  - 60 terminales
- Grupo: "Tiendas del Reino Unido" (GBP, inglés, Europe/London)
  - 10 almacenes (Londres, Manchester, etc.)
  - 30 terminales
- Grupo: "Tiendas de la UE" (EUR, no establecido, Europe/Paris)
  - 15 almacenes (París, Berlín, Roma, etc.)
  - 45 terminales
  - Anulación de idioma a nivel de tienda (París=Francés, Berlín=Alemán, Roma=Italiano)
- Grupo: "Tiendas de Japón" (JPY, japonés, Asia/Tokyo)
  - 5 almacenes (Tokio, Osaka, etc.)
  - 15 terminales

**Beneficios**:
- Una configuración de grupo aplica a todas las tiendas en cada mercado
- Modelos de recibos con ámbito en grupos (formato de IVA para la UE, impuesto de ventas para EE. UU.)
- Diapositivas promocionales dirigidas por región (EE. UU.: Venta del Día de la Memoria, UE: Venta de las Vacaciones de Verano)

### Ejemplo 2: Cadena de cafeterías

**Configuración**:
- 30 ubicaciones, todas en el mismo país, pero diferentes formatos

**Estructura de grupo**:
- Grupo: "Ubicaciones en centros comerciales" (no establecido, no establecido, no establecido)
  - 10 tiendas en centros comerciales
  - Diapositivas promocionales con horarios extendidos (abiertas hasta las 9 p.m.)
  - Modelo de recibo con código QR de validación de estacionamiento en centros comerciales
- Grupo: "Tiendas independientes" (no establecido, no establecido, no establecido)
  - 15 tiendas en la calle
  - Diapositivas promocionales con horarios estándar
  - Modelo de recibo estándar
- Grupo: "Ubicaciones en aeropuertos" (no establecido, no establecido, no establecido)
  - 5 tiendas en aeropuertos
  - Diapositivas promocionales de 24 horas
  - Modelo de recibo con integración de código QR de información de vuelo

**Beneficios**:
- Contenido promocional diferente para diferentes formatos
- Personalización del recibo según la ubicación
- Gestión simplificada (actualice un grupo en lugar de actualizar 10 tiendas individuales)

### Ejemplo 3: Operación de franquicia

**Configuración**:
- 100 tiendas, 20 diferentes franquiciados

**Estructura de grupo**:
- Grupo: "Franquiciado A" (no establecido, no establecido, no establecido)
  - 10 tiendas operadas por Franquiciado A
  - Información de contacto del Franquiciado A en recibos (a través de un modelo de recibo de grupo)
  - Contenido promocional del Franquiciado A (eventos locales, ofertas)
- Grupo: "Franquiciado B" (no establecido, no establecido, no establecido)
  - 8 tiendas operadas por Franquiciado B
  - Información de contacto del Franquiciado B en recibos
  - Contenido promocional del Franquiciado B
- (Repetir para todos los franquiciados)
- Grupo: "Tiendas corporativas" (no establecido, no establecido, no establecido)
  - 5 tiendas propiedad corporativa
  - Marca corporativa y promociones

**Beneficios**:
- Cada franquiciado gestiona sus propias configuraciones de grupo
- Coherencia de marca mantenida a través de valores predeterminados del sitio
- Independencia del franquiciado a través de anulaciones de grupo

## Administrar configuraciones de grupo

**Cambiar configuraciones de grupo** afecta a todos los terminales de ese grupo:
- Cambio de moneda: Todos los terminales del grupo cambian a la nueva moneda en la próxima sincronización
- Cambio de idioma: Todos los terminales del grupo cambian al nuevo idioma en la próxima sincronización
- Cambio de zona horaria: Todos los terminales del grupo recalculan los horarios en la próxima sincronización

**Consideraciones del impacto**:
- Pruebe los cambios en un solo terminal antes de aplicarlos a todo el grupo
- Notifique a los empleados sobre los cambios próximos (por ejemplo, cambio de idioma)
- Programar cambios durante horas de menor demanda para minimizar interrupciones

**Eliminar un grupo**:
- Reasigne todos los almacenes a otro grupo o quite la asignación del grupo
- Los terminales pierden las configuraciones del grupo y caen de vuelta a los valores predeterminados del sitio
- No se puede eliminar un grupo mientras los almacenes aún estén asignados

## Consejos

- **Use códigos significativos** - "WEST" es más claro que "GRP1" al revisar configuraciones
- **Planifique la jerarquía antes de crear grupos** - Piense en su estructura organizacional primero; reestructurar más tarde es tedioso
- **Pruebe las configuraciones del grupo con un solo terminal** - Antes de asignar 50 almacenes a un grupo, pruebe las configuraciones del grupo con un solo terminal
- **Anule con moderación a nivel de tienda** - Demasiadas anulaciones a nivel de tienda anulan el propósito de los grupos
- **Documente el propósito del grupo** - Anote en el nombre del grupo lo que hace que este grupo sea único (geografía, formato, franquiciado)
- **Use el orden de clasificación estratégicamente** - Ordene los grupos por importancia (Tiendas corporativas primero) o geografía (de oeste a este) para una navegación más fácil
- **Mantenga un número razonable de grupos** - 20+ grupos sugiere una segmentación excesiva; considere consolidar
- **Las anulaciones de moneda son permanentes** - Cambiar la moneda de un grupo durante la operación complica la contabilidad; planifique cuidadosamente

Recuerde: preserve todos los formatos de markdown, rutas de imágenes, bloques de código y términos técnicos exactamente como se muestran en las reglas de preservación.