---
title: Gestión de traducciones de la interfaz de usuario
---

La página de traducciones de la interfaz de usuario le permite personalizar cómo aparecen las cadenas de la interfaz del frontend—botones, etiquetas, mensajes de error y otras cadenas de texto de la interfaz—en cada idioma. A diferencia de las traducciones de contenido de productos o páginas, estas son los elementos de interfaz fijos que ven los clientes en toda su tienda. Personalícelas para que coincidan con la voz de su marca o mejore la claridad para su audiencia específica.

Esta página muestra todas las cadenas de interfaz traducibles y le permite anular las traducciones predeterminadas proporcionadas por Spwig.

## Entendiendo las traducciones de la interfaz de usuario

Las traducciones de la interfaz de usuario son las cadenas de texto que componen la interfaz de su tienda:

**Ejemplos de cadenas de interfaz de usuario**:
- Botones: "Añadir al carrito", "Pagar", "Buscar"
- Etiquetas: "Precio", "Cantidad", "Dirección de envío"
- Mensajes: "Artículo añadido al carrito", "Pedido confirmado", "Dirección de correo electrónico no válida"
- Navegación: "Inicio", "Tienda", "Contáctenos"
- Campos de formulario: "Correo electrónico", "Contraseña", "Nombre"

Spwig incluye traducciones predeterminadas para aproximadamente 300 cadenas de interfaz en todos los idiomas compatibles. La página de traducciones de la interfaz de usuario le permite anular cualquier una de estas predeterminadas con sus propias traducciones personalizadas.

## ¿Por qué personalizar las traducciones de la interfaz de usuario?

**Voz de la marca**: Cambie "Añadir al carrito" por "Comprar ahora" o "Consigue el tuyo" para que coincida con la personalidad de su marca

**Variaciones regionales**: Ajuste las traducciones para mercados específicos (inglés británico vs. inglesa americana, español europeo vs. español latinoamericano)

**Claridad**: Si la traducción predeterminada no tiene sentido para sus productos o audiencia, reemplácela con un texto más claro

**Términos específicos de la industria**: Use el terminología que sus clientes esperan (por ejemplo, "Agendar cita" en lugar de "Añadir al carrito" para tiendas basadas en servicios)

## Buscando cadenas

Use la caja de búsqueda para encontrar cadenas específicas de la interfaz de usuario:

**Buscar por texto en inglés**: Escriba "add to cart" para encontrar las traducciones de ese botón

**Buscar por traducción**: Escriba texto en cualquier idioma para encontrar traducciones coincidentes

**Buscar por clave**: Si conoce la clave de traducción (por ejemplo, `cart.add_item`), busque directamente por ella

La página se actualiza instantáneamente mientras escribe, mostrando solo las cadenas coincidentes.

## Viendo detalles de traducción

Cada cadena de interfaz de usuario muestra:

**Texto en inglés de origen** - La versión en inglés predeterminada (su punto de referencia)

**Clave de traducción** - El identificador interno usado en el código (por ejemplo, `cart.add_to_cart`)

**Columnas de idioma** - Traducción actual para cada idioma activo

**Estado de anulación** - Si ha personalizado la traducción (destacado si se ha anulado)

## Creando anulaciones de traducción

Para personalizar la traducción de una cadena de interfaz de usuario:

1. **Encuentre la cadena** usando la búsqueda (por ejemplo, busque "add to cart")
2. **Haga clic en la celda de idioma** que desee personalizar
3. **Introduzca su traducción personalizada** en el editor emergente
4. **Guarde** - Su anulación entra en vigor de inmediato

La traducción predeterminada original se mantiene - está creando una anulación que tiene prioridad.

## Revertir a las predeterminadas

Para eliminar una anulación personalizada y restaurar la traducción predeterminada:

1. **Haga clic en la traducción anulada** (estas están resaltadas)
2. **Haga clic en "Revertir a la predeterminada"** en el editor
3. **Confirme** - La traducción predeterminada se restaura de inmediato

Puede revertir anulaciones de idioma individuales sin afectar sus anulaciones en otros idiomas.

## Filtros por estado de anulación

Use el menú desplegable de filtro para ver:

**Todas las cadenas** - Cada cadena de interfaz en el sistema (~300 en total)

**Solo anuladas** - Cadenas donde ha creado traducciones personalizadas

**Solo predeterminadas** - Cadenas que aún usan las traducciones predeterminadas de Spwig

Esto le ayuda a revisar qué cadenas ha personalizado y a identificar lagunas.

## Ejemplos comunes de personalización

| Traducción predeterminada en inglés | Anulación personalizada | Caso de uso |
|----------------|----------------|----------|
| Add to Cart | Buy Now | Llamada a la acción más directa |
| Checkout | Secure Checkout | Destacar la seguridad |
| Search | Find Products | Más específico para el comercio electrónico |
| Contact Us | Get in Touch | Tono más amigable |
| Subscribe | Join Our Newsletter | Propuesta de valor más clara |

## Validación de traducciones

Al introducir traducciones personalizadas, valide que:

**La longitud se ajuste al espacio de la interfaz** - Las traducciones pueden ser más largas o más cortas que el inglés (las palabras en alemán suelen ser más largas, por ejemplo)

**Mantenga el significado** - No cambie la funcionalidad en la traducción (un botón "Cancelar" no debería decir "Eliminar")

**Terminología consistente** - Use la misma traducción para términos repetidos en toda la interfaz

**Formalidad adecuada** - Ajuste el tono a su mercado objetivo (formal vs. informal)

## Consistencia en múltiples idiomas

Al personalizar una cadena para múltiples idiomas:

1. **Empiece con su idioma predeterminado** - Establezca la base
2. **Personalice otros idiomas** para coincidir con la misma intención
3. **Pruebe en cada idioma** para verificar el diseño y el significado
4. **Use hablantes nativos** cuando sea posible para revisar personalizaciones en idiomas no ingleses

Las personalizaciones inconsistentes en varios idiomas crean una experiencia de cliente confusa.

## Exportación e importación en masa

Para personalizaciones extensas, considere usar el flujo de trabajo de exportación/importación:

1. **Exportar** las traducciones actuales como JSON o CSV
2. **Edite en una hoja de cálculo** o editor de texto (más fácil para cambios en masa)
3. **Importar** las traducciones actualizadas de vuelta al sistema

Este flujo de trabajo está disponible a través de la página de Trabajos de traducción para gestionar proyectos de traducción a gran escala.

## Consejos

- **Busque antes de personalizar** - Asegúrese de que esté editando la cadena correcta; algunas cadenas similares sirven para propósitos diferentes
- **Pruebe en el frontend después de guardar** - Verifique que su traducción personalizada aparezca correctamente en la interfaz real
- **Mantenga las traducciones concisas** - Lo más breve posible es generalmente mejor para botones y etiquetas
- **Documente sus anulaciones** - Mantenga notas sobre por qué personalizó cadenas específicas para referencia futura
- **Use terminología consistente** - Si personaliza "Carrito" en "Cesta", hágalo de forma consistente en todas las cadenas relacionadas
- **Considere los diseños para móviles** - Las traducciones largas pueden envolverse o truncarse en pantallas pequeñas
- **Revise después de las actualizaciones de idioma** - Cuando Spwig agregue nuevas traducciones predeterminadas, revise y personalice para mantener la consistencia

Recuerde: Mantenga todo el formato de markdown, rutas de imágenes, bloques de código y términos técnicos exactamente como se muestran en las reglas de preservación.