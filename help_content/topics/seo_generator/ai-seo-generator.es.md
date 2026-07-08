---
title: Generador de SEO con IA
---

El Generador de SEO con IA escribe automáticamente títulos meta, descripciones meta y otro contenido de SEO para tus productos utilizando un proveedor de IA. En lugar de escribir manualmente el contenido de SEO para cada producto, puedes generar contenido preciso y optimizado en masa con una sola acción.

Tu tienda viene con un generador de SEO integrado que funciona de inmediato. También puedes instalar componentes adicionales de proveedores de IA desde el mercado de componentes de Spwig para acceder a modelos de lenguaje más potentes.

## Cómo funciona el generador de SEO

El generador de SEO lee el nombre, la descripción, la categoría y los atributos de tu producto, y luego utiliza el proveedor de IA configurado para escribir contenido de SEO adaptado a ese producto. El contenido generado se guarda directamente en los campos de SEO del producto.

Puedes generar contenido de SEO para productos individuales desde la página de edición del producto, o ejecutar una generación en masa en varios productos desde la lista de productos.

## Configuración de un proveedor de SEO

### Usando el proveedor integrado

Tu tienda incluye un proveedor de SEO integrado que genera contenido de SEO de forma determinista a partir de tus datos de producto — no se requieren claves de API externas. Se establece automáticamente como el proveedor principal en nuevas instalaciones.

Para verificar que esté activo:

1. Navega a **Marketing > Proveedores de SEO**
2. Verifica que el proveedor integrado aparezca con un distintivo **PRINCIPAL** y un estado **ACTIVO**
3. Si no se muestran proveedores, haz clic en **+ Agregar cuenta de proveedor de SEO** y establece **Clave del proveedor** en `deterministic`

### Conectar un componente de proveedor de IA

Para contenido de SEO más rico y contextual, puedes instalar un componente de proveedor de IA (como un proveedor basado en OpenAI o Claude) desde el mercado de componentes de Spwig.

1. Instala el componente del proveedor a través del sistema de actualización de componentes (pide a tu administrador de tienda)
2. Navega a **Marketing > Proveedores de SEO**
3. Haz clic en **+ Agregar cuenta de proveedor de SEO**
4. Llena el formulario:

**Sección de información del proveedor:**
- **Sitio** — selecciona tu tienda
- **Componente del proveedor** — elige el componente de proveedor de IA instalado
- **Clave del proveedor** — deja en blanco cuando uses un proveedor basado en componente
- **Nombre de la cuenta** — un nombre descriptivo, como `Proveedor de SEO de OpenAI`

**Sección de configuración:**
- **Activo** — marca para habilitar este proveedor
- **Principal** — marca para usar este como el proveedor predeterminado para toda la generación de SEO
- **Prioridad** — los números más bajos se prueban primero en la cadena de respaldo
- **Configuración** — configuraciones específicas del proveedor como un objeto JSON (por ejemplo, nombre del modelo, tono, idioma)

5. Haz clic en **Guardar**

Solo se puede establecer un proveedor como principal. Si marcas un nuevo proveedor como principal, el anterior se degrada automáticamente.

### Cadena de respaldo de proveedores

Si tu proveedor principal falla (por ejemplo, debido a un corte de API), tu tienda se pasa automáticamente al siguiente proveedor activo en orden de prioridad. Esto asegura que la generación de SEO continúe funcionando incluso si un proveedor está temporalmente inactivo.

## Generando contenido de SEO para un producto

### Producto individual

1. Navega a **Productos > Productos** y abre cualquier producto
2. Desplázate hasta la sección **SEO** del formulario del producto
3. Haz clic en el botón **Generar SEO**
4. El proveedor de IA genera un título meta y una descripción meta basados en los detalles del producto
5. Revisa el contenido generado y edita si es necesario
6. Haz clic en **Guardar** para aplicar los cambios

### Generación en masa

Para generar o actualizar el contenido de SEO para múltiples productos a la vez:

1. Navega a **Productos > Productos**
2. Selecciona los productos que deseas actualizar usando sus casillas de verificación, o selecciona todos
3. Abre el menú desplegable **Acción**
4. Elige **Generar contenido de SEO** (o nombre de acción similar — verifica el menú desplegable para la etiqueta exacta)
5. Haz clic en **Ir**

Spwig encola las tareas de generación y las procesa en segundo plano. Refresca la lista de productos después de un minuto o dos para ver los campos de SEO actualizados.

## Revisando la cobertura de SEO

El generador de SEO rastrea qué productos ya tienen contenido de SEO. Para identificar productos que aún necesitan SEO:

1.

Navega a **Productos > Productos**
2.


Utilice el filtro **Estado SEO** (si está disponible) para mostrar productos con títulos meta o descripciones faltantes
3.

Seleccione esos productos y ejecute la acción de generación por lotes

## Configuración del proveedor

El campo **Configuración** en una cuenta de proveedor de SEO acepta un objeto JSON con configuración específica del proveedor. Opciones comunes incluyen:

```json
{
  "language": "en",
  "tone": "professional",
  "max_title_length": 60,
  "max_description_length": 160
}
```

Estas configuraciones varían según el componente del proveedor. Consulte la documentación del proveedor para obtener la lista completa de opciones disponibles.

## Administrar múltiples proveedores

Si tiene configuradas más de una cuenta de proveedor de SEO, la lista de proveedores muestra su estado a primera vista:

- **Etiqueta PRIMARIO** — este proveedor se usa por defecto para toda la generación de SEO
- **Etiqueta ACTIVO** — el proveedor está habilitado
- **Etiqueta INACTIVO** — el proveedor está deshabilitado y no se usará

Para cambiar qué proveedor es el primario, abra la cuenta del proveedor que desea promover, marque la casilla **Es primario** y guarde. El sistema asegura automáticamente que solo un proveedor tenga la bandera primaria en cualquier momento.

## Consejos

- Genere contenido SEO para nuevos productos inmediatamente después de crearlos — solo toma segundos y da a los motores de búsqueda algo útil para indexar de inmediato
- Revise las descripciones meta generadas por IA antes de publicar si sus productos tienen nombres poco comunes o técnicos; el generador funciona mejor con nombres de productos claros y descriptivos
- Establezca "max_title_length": 60 y "max_description_length": 160 en la configuración del proveedor para mantener el contenido generado dentro de los límites de caracteres recomendados por Google
- Ejecute la generación de SEO por lotes después de importar un catálogo de productos grande para rellenar rápidamente todos los campos de SEO
- Si actualiza significativamente la descripción de un producto, regenere su contenido SEO para mantener las etiquetas meta alineadas con el nuevo texto
- El proveedor determinista integrado es un buen punto de partida; actualice a un componente impulsado por IA una vez que su catálogo esté configurado y desee contenido SEO más rico y con un sonido más natural