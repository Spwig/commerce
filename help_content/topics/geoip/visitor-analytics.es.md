---
title: Analítica de visitantes
---

La analítica de visitantes te da una visión clara de cómo los clientes se mueven por tu tienda. Puedes ver qué páginas atraen más visitas, cómo se comporta el tráfico general con el tiempo, qué dispositivos usan tus clientes y cómo se comparan los visitantes nuevos frente a los que ya han estado antes — todo sin necesidad de herramientas de analítica externas.

## Visión general de las pantallas de analítica

Tu tienda registra la actividad de los visitantes automáticamente una vez que el sistema GeoIP está activo. Los datos se organizan en tres vistas, cada una ofreciendo un nivel diferente de detalle.

### Resumen del tráfico diario

Navega a **Clientes > Estadísticas de tráfico diario** para ver el tráfico general de tu tienda por día. Cada fila representa un día del calendario y muestra:

| Columna | Qué te indica |
|--------|-------------------|
| **Fecha** | El día en que se registró el tráfico |
| **Total de vistas** | Todas las vistas de páginas, incluyendo bots |
| **Visitantes únicos** | Visitantes distintos (por sesión) |
| **Vistas de bots** | Vistas de crawlers y herramientas automatizadas |
| **Visitantes nuevos** | Sesiones sin historial previo |
| **Visitantes recurrentes** | Sesiones de visitantes vistos anteriormente |
| **Vistas de escritorio** | Vistas desde navegadores de escritorio |
| **Vistas móviles** | Vistas desde dispositivos móviles |
| **Vistas de tabletas** | Vistas desde dispositivos de tableta |

Utiliza la navegación de jerarquía de fechas en la parte superior de la lista para saltar rápidamente a un mes o año específico. Los totales se actualizan una vez al día mediante un proceso en segundo plano automatizado, por lo que las cifras del día actual aparecerán al día siguiente por la mañana.

### Estadísticas por página

Navega a **Clientes > Estadísticas de páginas diarias** para ver el tráfico desglosado por página individual. Cada fila muestra una ruta de URL en un día, por lo que puedes comparar el rendimiento de páginas específicas con el tiempo.

| Columna | Qué te indica |
|--------|-------------------|
| **Fecha** | El día al que aplican estas estadísticas |
| **Ruta de URL** | La ruta de página normalizada (por ejemplo, `/products/blue-widget`) |
| **Vistas** | Total de vistas de esa página ese día |
| **Visitantes únicos** | Visitantes distintos que vieron esa página |
| **Vistas de bots** | Vistas de bots en esa página |
| **Entradas** | Cuántas sesiones comenzaron en esta página (fue su página de inicio) |

Utiliza el cuadro de búsqueda **Ruta de URL** para encontrar estadísticas de una página específica. Por ejemplo, busca `/products/` para ver todo el tráfico de páginas de productos, o busca un slug específico de producto para enfocarte en un artículo concreto.

### Eventos de vistas de páginas individuales

Navega a **Clientes > Vistas de páginas** para obtener un registro crudo de cada navegación de página rastreada. Este es un registro de solo lectura — no puedes agregar ni editar entradas. Úsalo para investigar sesiones específicas o para verificar que el rastreo se esté registrando correctamente.

Cada registro muestra:
- **Ruta de URL** — la página que se visitó
- **Sesión** — un identificador corto para la sesión del visitante
- **Fuente** — si la visita vino del frontend sin cabeza o de la tienda en línea estándar
- **Es bot** — si el visitante se identificó como tráfico automatizado
- **Es página de entrada** — si esta fue la primera página en su sesión
- **Marca de tiempo** — la hora exacta de la visita

Puedes filtrar por **Es bot**, **Fuente** y **Es página de entrada** usando los filtros del panel lateral, y navegar por fecha usando la jerarquía de fechas en la parte superior.

## Analizar tendencias del tráfico

El resumen del tráfico diario es tu mejor herramienta para detectar tendencias. Busca patrones como:

- **Picos de tráfico** después de realizar una promoción o enviar un correo electrónico de marketing
- **Crecimiento gradual** a lo largo de semanas y meses a medida que tu tienda gana visibilidad orgánica
- **Patrones de fin de semana frente a días laborables** para entender cuándo tus clientes están más activos
- **División entre móvil y escritorio** para decidir si priorizar cambios en el diseño optimizado para móviles

Las columnas **Visitantes nuevos** y **Visitantes recurrentes** juntas te indican cuán bien estás manteniendo a tus clientes. Una tienda saludable suele ver una mezcla de ambos — una alta proporción de visitantes nuevos sugiere una fuerte adquisición, mientras que una mayor proporción de visitantes recurrentes sugiere que se está construyendo la lealtad del cliente.

La vista de estadísticas por página, ordenada por vistas en orden descendente (el valor predeterminado), muestra inmediatamente cuáles páginas generan más tráfico en un día determinado.

Busca:

- **Páginas con alta entrada y baja vista** — páginas que atraen visitantes desde búsquedas o anuncios, pero pueden no mantener su atención
- **Páginas con alta vista y muchos visitantes únicos** — páginas populares de destino que vale la pena mantener actualizadas
- **Páginas de productos con un aumento en el recuento de vistas** — productos que pueden estar ganando visibilidad en búsquedas

### Ejemplo: encontrar el tráfico de un producto

Para comprobar cuánto tráfico recibió tu producto más vendido la semana pasada:

1. Navega a **Customers > Daily Page Stats**
2. Usa la jerarquía de fechas para seleccionar la semana relevante
3. En el cuadro de búsqueda, ingresa el slug de la URL del producto (por ejemplo, `/blue-widget`)
4. Revisa **Views**, **Unique Visitors** y **Entries** durante los días mostrados

## Datos de ubicación de los visitantes

Navega a **Customers > Visitor Locations** para ver una vista a nivel de sesión de dónde se encuentran ubicados tus visitantes. Cada registro representa una sesión de un visitante e incluye:

- País y ciudad (resueltos automáticamente por el sistema GeoIP)
- Tipo de dispositivo (escritorio, móvil, tableta)
- Preferencias de moneda y idioma seleccionadas por el visitante
- Atribución de campaña UTM (fuente, medio, nombre de la campaña)
- Banderas de tráfico de bots y administradores

Puedes filtrar visitantes por país, tipo de dispositivo, fuente UTM y si eran bots o personal de administración. Usa el filtro **Is Bot** establecido en falso para enfocarte en el tráfico real de clientes, y el filtro **Is Admin Traffic** para excluir tus propias sesiones de prueba del análisis.

## Consejos

- Las vistas de bots se rastrean por separado y se excluyen automáticamente del recuento de visitantes únicos — tus cifras de tráfico reflejan la actividad real de los clientes
- La columna **Entries** en las estadísticas por página te indica qué páginas actúan como la puerta de entrada de tu tienda desde búsquedas y anuncios; optimizar esas páginas tiene el mayor impacto
- Filtra las ubicaciones de los visitantes por **UTM Source** para medir cuánto tráfico está enviando un canal de marketing específico (por ejemplo, una newsletter por correo electrónico o un anuncio de Google)
- Las estadísticas diarias se agrupan durante la noche — si necesitas revisar el tráfico del mismo día, usa directamente el registro de vistas de página
- La descomposición de dispositivos en la resumen diario te ayuda a priorizar el trabajo de diseño; si más de la mitad de tus visitas son móviles, asegúrate de que tus páginas de productos y el proceso de pago se vean bien en pantallas pequeñas