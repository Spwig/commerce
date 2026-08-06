---
title: Diseño y Temas
---

El sistema de Diseño y Temas le permite controlar la apariencia de toda su tienda — desde colores y tipografía hasta encabezados, pies de página y diseños de páginas. Navegue hasta **Configuración > Diseño y Temas** para abrir el panel de control de Diseño.

![Panel de control de diseño](/static/core/admin/img/help/design-themes/theme-dashboard.webp)

## Panel de control de Diseño

El panel le brinda una vista general del estado de diseño de su tienda:

- **Tema activo** — Muestra qué tema está aplicado actualmente, con una vista previa y botones de acceso rápido
- **Estadísticas de diseño** — Número de temas instalados, encabezados personalizados, pies de página personalizados y menús
- **Tarjetas de sección** — Vaya a Temas, Constructor de encabezados, Constructor de pies de página, Menús o Anuncios

## Temas

### Navegación entre temas

Haga clic en la tarjeta de sección **Temas** para ver todos los temas instalados. Cada tarjeta de tema muestra:
- Nombre del tema e imagen de vista previa
- Autor y versión
- Estado activo/inactivo

### Activar un tema

1. Haga clic en **Activar** en el tema que desee usar
2. El tema se aplica inmediatamente a su tienda
3. Solo puede estar activo un tema a la vez

### Personalización de tema

Cada tema admite un conjunto de **tokens de diseño** — valores configurables que controlan la apariencia visual sin editar código.

Haga clic en **Personalizar** en su tema activo para acceder al editor de tokens. Las categorías de tokens disponibles incluyen:

| Categoría | Lo que controla |
|----------|-----------------|
| **Colores** | Colores primarios, secundarios, acento, fondos, colores de texto |
| **Tipografía** | Familias de fuentes, tamaños, pesos, alturas de línea |
| **Espaciado** | Márgenes, rellenos, espacios entre elementos |
| **Bordes** | Anchos de bordes, radios, colores |
| **Sombras** | Sombras de cajas para tarjetas, botones, ventanas modales |
| **Botones** | Estilos de botones, tamaños, efectos de paso del mouse |
| **Diseño** | Anchuros de contenedores, espacios de cuadrícula, puntos de quiebre |

Los cambios se muestran en tiempo real antes de que los guarde.

## Constructor de encabezados

El constructor de encabezados le permite diseñar el encabezado de su tienda utilizando una interfaz de arrastrar y soltar.

### Crear un encabezado

1. Navegue hasta **Diseño > Constructor de encabezados**
2. Haga clic en **Crear encabezado** o edite uno existente
3. El constructor tiene tres filas: **Barra superior**, **Encabezado principal** y **Barra inferior**
4. Arrastre los widgets de la caja de herramientas a cualquier fila

### Widgets de encabezado disponibles

- **Logo** — Su logotipo de tienda con tamaño y enlace configurables
- **Menú de navegación** — Menú desplegable desde sus menús definidos
- **Barra de búsqueda** — Búsqueda de productos con resultados instantáneos
- **Icono del carrito** — Mini-carrito con etiqueta de contador de artículos
- **Icono de cuenta** — Menú desplegable de inicio de sesión/cuenta
- **Selector de idioma** — Selector de cambio de idioma para tiendas multilingües
- **Selector de moneda** — Selector de cambio de moneda para tiendas multimoneda
- **Selector de envío** — Permite a los compradores elegir su país de destino de envío, cambiando su región de ventas (y moneda, para tiendas multimoneda). Vea la guía **Disponibilidad por región** para más detalles
- **HTML personalizado** — Agregue cualquier contenido personalizado
- **Iconos de redes sociales** — Enlaces a sus perfiles en redes sociales
- **Barra de anuncio** — Mensajes promocionales y ofertas

### Configuración del encabezado

Cada plantilla de encabezado tiene configuraciones globales:
- **Encabezado fijo** — El encabezado permanece visible al desplazarse
- **Modo transparente** — Superposición en imágenes de portada
- **Punto de quiebre de móvil** — Cuándo cambiar al diseño móvil

## Constructor de pies de página

El constructor de pies de página funciona de manera similar al constructor de encabezados.

### Crear un pie de página

1. Navegue hasta **Diseño > Constructor de pies de página**
2. Haga clic en **Crear pie de página** o edite uno existente
3. El constructor admite múltiples columnas y filas
4. Arrastre los widgets a la posición deseada

### Widgets de pie de página disponibles

- **Menú de navegación** — Enlaces de navegación del pie de página
- **Registro de boletín** — Formulario de suscripción por correo electrónico
- **Iconos de redes sociales** — Enlaces a perfiles en redes sociales
- **HTML personalizado** — Contenido personalizado, sellos, certificaciones
- **Iconos de pago** — Muestra los métodos de pago aceptados
- **Copyright** — Texto de copyright dinámico con año
- **Logo** — Versión del logotipo en el pie de página

## Menús de navegación

Los menús definen los enlaces de navegación en su encabezado y pie de página.

### Crear un menú

1.

Navegue a **Diseño > Menús**
2.

Haga clic en **Añadir menú**
3.

Dale un nombre al menú (por ejemplo, "Navegación principal")
4.

Añada elementos de menú:
   - **Enlace a página** — Enlace a una página del constructor de páginas
   - **Enlace a categoría** — Enlace a una categoría de producto
   - **URL personalizada** — Cualquier URL externa o interna
   - **Desplegable** — Elementos secundarios anidados
5.

Arrastre los elementos para reordenarlos
6.

Guarde y asigne el menú a un widget de encabezado o pie de página

## Anuncios

 Cree banners promocionales que aparezcan en la parte superior de su tienda.

### Crear un anuncio

1. Navegue a **Diseño > Anuncios** (o use la tarjeta del panel de control)
2. Haga clic en **Añadir anuncio**
3. Configure:
   - **Mensaje** — El texto del anuncio (admite traducciones)
   - **Enlace** — URL opcional al hacer clic
   - **Estilo** — Color de fondo, color de texto, icono
   - **Horario** — Fechas de inicio y finalización
   - **Cerrable** — Si los clientes pueden cerrarlo
4. Guarde y active

Pueden estar activos varios anuncios simultáneamente — se rotan automáticamente.

## Consejos

- Comience con el personalizador del tema activo para adaptar los colores de su marca antes de construir encabezados y pies de página.
- Use la función **vista previa** en los constructores de encabezados y pies de página para ver los cambios antes de publicar.
- Cree encabezados separados para escritorio y móvil si necesita diseños muy diferentes.
- Mantenga la navegación simple — 5-7 elementos principales de menú es ideal para la usabilidad.
- Use anuncios para promociones con plazo de vigencia en lugar de mensajes permanentes.
- El editor de tokens del tema admite vista previa en tiempo real — experimente libremente y guarde cuando esté satisfecho.