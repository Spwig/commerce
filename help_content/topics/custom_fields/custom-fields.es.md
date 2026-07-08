---
title: Campos personalizados
---

Los campos personalizados le permiten agregar datos adicionales a Productos, Categorías, Pedidos y Perfiles de clientes sin modificar ningún código. Úselos para almacenar información específica de su negocio, como IDs de API externos, ubicaciones de almacén, datos de cumplimiento o cualquier atributo que su tienda necesite.

## Accediendo a Campos Personalizados

Navegue hasta **Configuración > Campos Personalizados** en el menú lateral de administración.

![Página de Campos Personalizados](/static/core/admin/img/help/custom-fields/custom-fields-page.webp)

## Conceptos Clave

### Grupos de Campos

Los campos se organizan en **grupos** — colecciones lógicas que aparecen juntas como una sección. Por ejemplo, un grupo de "Información de Envío" podría contener campos para ubicación de almacén, dimensiones del paquete y clasificación de materiales peligrosos.

### Definiciones de Campo

Cada definición de campo controla:
- **Nombre**: La etiqueta mostrada en los formularios
- **Slug**: La clave legible por máquina utilizada en el almacenamiento JSON y respuestas de la API
- **Tipo de Campo**: Qué tipo de entrada se renderiza (texto, número, desplegable, etc.)
- **Validación**: Reglas como min/max, longitud máxima, expresión regular o opciones permitidas
- **Visibilidad**: Si el campo aparece en la tienda en línea

### Tipos de Campo Soportados

| Tipo | Descripción | Uso Ejemplo |
|------|-------------|-------------|
| **Texto** | Entrada de texto de una sola línea | ID de API externo, código de marca |
| **Área de texto** | Texto de múltiples líneas | Notas de manejo especial |
| **Número** | Valores enteros | Cantidad mínima de pedido |
| **Decimal** | Valores decimales | Sobrescritura de peso, dimensión personalizada |
| **Sí/No** | Conmutador de casilla de verificación | ¿Es frágil?, requiere firma |
| **Fecha** | Selector de fecha | Fecha de lanzamiento, fecha de caducidad |
| **Fecha y hora** | Selector de fecha y hora | Disponibilidad programada |
| **URL** | Dirección web | Enlace del proveedor, URL de hoja de especificaciones |
| **Email** | Dirección de correo electrónico | Contacto del fabricante |
| **Desplegable** | Lista de selección única | Tipo de material, país de origen |
| **Selección múltiple** | Lista de selección múltiple | Certificaciones, etiquetas |
| **Color** | Selector de color | Color de marca, color de etiqueta |

## Administración de Campos Personalizados

### Crear un Grupo de Campo

1. Abra **Configuración > Campos Personalizados**
2. Seleccione la pestaña del modelo (Productos, Categorías, Pedidos o Perfiles de clientes)
3. Haga clic en **Agregar Grupo**
4. Ingrese un **Nombre de Grupo** (por ejemplo, "Integraciones Externas")
5. Active opcionalmente **Mostrar en tienda en línea** si los clientes deben ver estos campos
6. Haga clic en **Guardar Grupo**

### Agregar un Campo a un Grupo

1. En la tarjeta del grupo, haga clic en **Agregar Campo**
2. Ingrese un **Nombre de Campo** — el slug se genera automáticamente
3. Elija el **Tipo de Campo**
4. Establezca opcionalmente un **Texto de Ayuda** y **Valor por Defecto**
5. Configure las opciones de validación (varía según el tipo de campo):
   - Texto: longitud máxima, patrón de expresión regular
   - Número/Decimal: valores mínimos y máximos
   - Desplegable: defina la lista de opciones
6. Establezca las opciones del campo:
   - **Requerido**: Los comerciantes deben completar este campo al guardar
   - **Mostrar en tienda en línea**: Muestra el valor en la página orientada al cliente
   - **Traducible**: Permitir que el valor se traduzca (solo texto/área de texto)
7. Haga clic en **Guardar Campo**

### Edición y Reordenación

- Haga clic en el **icono de lápiz** en cualquier grupo o campo para editarlo
- Arrastre el **manillón de agarre** para reordenar grupos o campos dentro de un grupo
- Los cambios tienen efecto inmediato en todos los formularios relevantes

### Eliminación de Grupos y Campos

- Haga clic en el **icono de basura** en un grupo o campo para eliminarlo
- Las eliminaciones son **eliminaciones suaves** — los datos se conservan en la base de datos pero se ocultan de los formularios
- Esto protege los datos existentes de pérdida accidental

## Uso de Campos Personalizados en Formularios

Una vez que defina campos personalizados para un modelo, una **pestaña de Campos Personalizados** aparece automáticamente en el formulario de edición correspondiente.

### Productos y Categorías

1. Abra cualquier producto o categoría para edición
2. Haga clic en la **pestaña de Campos Personalizados**
3. Rellene los campos según sea necesario
4. Haga clic en **Guardar** — los valores se almacenan junto con el registro

### Pedidos

Los valores de campos personalizados para pedidos se muestran como una **sección de solo lectura** en la página de detalles del pedido. Los campos personalizados de pedidos se establecen normalmente a través de la API o en el momento del pago.

### Perfiles de Clientes

1. Abra un perfil de cliente
2. Haga clic en la **pestaña de Campos Personalizados**
3. Rellene los campos y guarde

## Acceso a la API

### Listando Definiciones de Campo

Recuperar todas las definiciones de campos personalizados para un modelo:

```
GET /api/custom-fields/definitions/?model=product&app=catalog
```

**Respuesta:**
```json
[
  {
    "id": 1,
    "name": "External API ID",
    "slug": "external_api_id",
    "field_type": "text",
    "is_required": false,
    "group": { "name": "External Integrations" }
  }
]
```

### Leyendo Valores de Campos Personalizados

Los valores de campos personalizados se incluyen en el objeto JSON `custom_fields` en las respuestas de la API del modelo:

```json
{
  "id": 42,
  "name": "Blue Widget",
  "custom_fields": {
    "external_api_id": "API-12345",
    "is_fragile": true
  }
}
```

### Escribir Valores de Campos Personalizados

Incluya `custom_fields` al crear o actualizar un registro a través de la API:

```json
{
  "custom_fields": {
    "external_api_id": "API-67890",
    "warehouse_location": "WH-A3"
  }
}
```

Los valores se validan contra las definiciones de campo. Los valores inválidos devuelven un error `400` con detalles.

### Consultar por Campos Personalizados

Los campos personalizados están indexados para consultas rápidas en la base de datos. Filtre registros usando filtros de consulta de base de datos:

```
GET /api/products/?custom_fields__warehouse_location=WH-A3
```

## Visualización en la Tienda en Línea

### Para Desarrolladores de Temas

Use la etiqueta de plantilla `render_custom_fields` para mostrar campos personalizados en la tienda en línea:

```python
{% load custom_fields_tags %}

{# Renderizar todos los campos visibles en la tienda en línea #}
{% render_custom_fields product %}

{# Obtener un valor de campo específico #}
{% get_custom_field product "warehouse_location" as location %}
<p>Envío desde: {{ location }}</p>
```

Solo los campos con **Mostrar en tienda en línea** habilitado a nivel de grupo y campo se renderizarán.

## Buenas Prácticas

- **Use nombres descriptivos** — los nombres de los campos aparecen en los formularios y en la tienda en línea
- **Establezca texto de ayuda** — guíe a los comerciantes sobre qué ingresar en cada campo
- **Agrupe campos relacionados** — mantenga los formularios organizados y intuitivos
- **Use valores por defecto** — establezca valores razonables para reducir la entrada de datos
- **Sea selectivo con la visibilidad en la tienda en línea** — solo muestre los campos que sean significativos para los clientes
- **Use slugs en integraciones** — los slugs son identificadores estables; los nombres de campos pueden cambiar

## Solución de Problemas

**Pestaña de Campos Personalizados no apareciendo:**
- Verifique que al menos un grupo de campos activo exista para ese modelo
- Revise que la clase de administración incluya el `CustomFieldsAdminMixin`
- Limpie la caché y recargue la página

**Valores de campo no guardándose:**
- Asegúrese de que los campos obligatorios estén completos
- Revise las reglas de validación (mínimo/máximo, patrones de expresión regular, opciones permitidas)
- Verifique que el campo esté activo y no eliminado suavemente

**API devolviendo custom_fields vacíos:**
- Confirme que el modelo tenga el `CustomFieldsMixin`
- Revise que existan definiciones de campo para el tipo de contenido correcto
- Asegúrese de que el serializador incluya `CustomFieldsSerializerMixin`

## Temas Relacionados

- [Adding Products](#)
- [Store Settings](#)