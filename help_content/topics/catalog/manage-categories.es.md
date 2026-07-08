---
title: Gestión de Categorías
---

Las categorías le ayudan a organizar su catálogo de productos para que los clientes puedan navegar y encontrar productos fácilmente. Vaya a **Productos > Categorías** en la barra lateral del administrador.

![Lista de categorías](/static/core/admin/img/help/manage-categories/category-list.webp)

## Lista de Categorías

La página de gestión de categorías muestra todas sus categorías como tarjetas con:

- **Imagen en miniatura** — Identificador visual de la categoría
- **Nombre y slug** — Nombre visible e identificador compatible con URLs
- **Cantidad de productos** — Número de productos asignados a esta categoría
- **Estado** — Publicada o borrador

Use las **pestañas de filtro** en la parte superior para ver rápidamente Todas, Publicadas o Borrador. La **barra de búsqueda** le permite encontrar categorías por nombre.

## Crear una Categoría

1. Haga clic en **+ Añadir Categoría** en la esquina superior derecha
2. Complete los detalles de la categoría:
   - **Nombre** — El nombre visible que verán los clientes
   - **Slug** — Se genera automáticamente a partir del nombre, se usa en las URLs
   - **Categoría principal** — Déjelo vacío para una categoría de nivel superior, o seleccione una categoría principal para crear una subcategoría
   - **Descripción** — Descripción en texto enriquecido que se muestra en la página de la categoría
3. Suba una **imagen de categoría** — se muestra en los menús de navegación y en los listados de categorías
4. Configure los **campos SEO** (meta título, descripción) en la pestaña SEO
5. Haga clic en **Guardar**

## Jerarquía de Categorías

Las categorías admiten anidación ilimitada para crear una estructura de árbol:

- **Categorías de nivel superior** — Elementos principales de navegación (ej., "Ropa", "Electrónica")
- **Subcategorías** — Anidadas bajo una categoría principal (ej., "Ropa > Hombre > Camisetas")

El desplegable de categoría principal muestra la ruta completa de la jerarquía para ayudarle a elegir el nivel correcto.

## Configuración de Categorías

### Visibilidad

- **Publicada** — La categoría aparece en la tienda y en la navegación
- **Borrador** — La categoría está oculta para los clientes pero accesible en el administrador

### Categorías Destacadas

Marque categorías como **destacadas** para resaltarlas en su página de inicio o en secciones especiales de navegación. Las categorías destacadas se pueden mostrar usando el elemento de cuadrícula de categorías del Constructor de Páginas.

### Orden de Clasificación

Controle cómo aparecen las categorías en los menús de navegación estableciendo un valor de **orden de clasificación**. Los números más bajos aparecen primero.

## Asignar Productos a Categorías

Hay dos formas de asignar productos:

1. **Desde el formulario de edición del producto** — Seleccione una categoría en el desplegable de Categoría en la pestaña de Información Básica
2. **Asignación masiva** — Seleccione varios productos de la lista de productos y use la acción masiva para asignarlos a una categoría

Cada producto puede pertenecer a una categoría principal. Use etiquetas o colecciones para agrupaciones adicionales.

## Páginas de Categoría en la Tienda

Cada categoría publicada obtiene automáticamente una página dedicada que muestra:
- Nombre y descripción de la categoría
- Imagen de banner (si está configurada)
- Cuadrícula de productos con todos los productos asignados
- Opciones de filtrado y ordenación

La URL de la página de categoría sigue el patrón: `sutienda.com/category/slug-de-categoria/`

## Consejos

- Mantenga su árbol de categorías poco profundo — 2-3 niveles de profundidad es ideal para la usabilidad de la navegación.
- Use nombres de categoría descriptivos que coincidan con lo que buscan los clientes.
- Añada imágenes de categoría para una experiencia de navegación más visual.
- Configure su estructura de categorías antes de añadir productos para mantener todo organizado.
- Use la descripción de la categoría para SEO — incluya palabras clave relevantes de forma natural.
