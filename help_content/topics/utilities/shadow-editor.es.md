---
title: Editor de sombras
---

El editor de sombras te permite agregar profundidad y dimensión a los elementos con sombras de caja y sombras de texto configurables. Las sombras crean una jerarquía visual, llaman la atención sobre elementos importantes y dan a tu tienda en línea una sensación pulida y moderna. Abre la **pestaña de Estilo** de cualquier elemento y busca el grupo **Efectos** para acceder al editor de sombras.

![Editor de sombras](/static/core/admin/img/help/shadow-editor/shadow-editor.webp)

## Tipos de sombras

El editor ofrece dos pestañas en la parte superior:

- **Sombra de caja** — Agrega una sombra alrededor del recuadro delimitador completo del elemento. Úsala para tarjetas, botones, contenedores, imágenes y secciones.
- **Sombra de texto** — Agrega una sombra detrás de los caracteres de texto únicamente. Úsala para títulos o texto superpuesto en imágenes para mejorar la legibilidad.

Cada pestaña tiene su propia configuración independiente. Puedes aplicar tanto una sombra de caja como una sombra de texto al mismo elemento si es necesario.

## Propiedades de sombras

Cada capa de sombra se define mediante las siguientes propiedades:

| Propiedad | Descripción | Rango |
|----------|-------------|-------|
| **Desplazamiento X** | Distancia horizontal de la sombra respecto al elemento | -50px a 50px |
| **Desplazamiento Y** | Distancia vertical de la sombra respecto al elemento | -50px a 50px |
| **Radio de desenfoque** | Cuán suave o difusa aparece el borde de la sombra. Valores más altos producen sombras más suaves. | 0px a 100px |
| **Radio de expansión** | Expande o contrae el tamaño de la sombra en relación con el elemento (solo sombra de caja) | -50px a 50px |
| **Color** | El color de la sombra, configurable con soporte completo de opacidad mediante el selector de color | Cualquier color con alfa |
| **Inserción** | Conmutador para renderizar la sombra dentro del elemento en lugar de fuera (solo sombra de caja) | Encendido / Apagado |

Ajusta los valores usando los deslizadores o escribe números precisos directamente en los campos de entrada.

## Múltiples sombras

Puedes apilar múltiples capas de sombra en un solo elemento para crear efectos de profundidad complejos y realistas:

- Haz clic en el botón **+** para agregar una nueva capa de sombra
- Cada capa aparece como una fila en la lista de sombras con sus propios controles
- Arrastra las capas para reordenarlas — las sombras se renderizan en el orden de la lista, con la primera capa en la parte superior
- Activa el **icono de ojo** en cualquier capa para ocultarla temporalmente sin eliminar la configuración
- Haz clic en el **icono de basura** para eliminar una capa

Combinar una sombra oscura y estrecha con una sombra amplia y suave crea un efecto natural de "elevación" que imita la profundidad física.

## Preset de sombras

Los presets de aplicación rápida te permiten agregar estilos de sombra comunes con un solo clic:

| Preset | Descripción |
|--------|-------------|
| **Pequeño** | Sombra sutil y cercana para una leve elevación (tarjetas, entradas) |
| **Mediano** | Profundidad moderada para elementos interactivos (botones, menús desplegables) |
| **Grande** | Sombra destacada para elementos flotantes (modales, ventanas emergentes) |
| **Suave** | Gran desenfoque con baja opacidad para un brillo suave y difuso |
| **Duro** | Mínimo desenfoque con mayor opacidad para un borde definido y claro |
| **Inserción** | Sombra interna para un aspecto presionado o hundido |

Después de aplicar un preset, puedes ajustar propiedades individuales para afinar el resultado.

## Vista actual vs. nueva

En la parte inferior del editor, dos cuadros de comparación muestran la **sombra actual** (como se guardó) y la **sombra nueva** (tus cambios pendientes). Esta vista de lado a lado facilita evaluar la diferencia antes de comprometerse. Haz clic en **Aplicar** para aceptar, o haz clic fuera para descartar tus cambios.

## ¿Dónde aparece?

El editor de sombras está disponible en los siguientes lugares:

- **Constructor de páginas** — Pestaña de Estilo, grupo de Efectos en secciones, contenedores, columnas y elementos individuales
- **Constructor de encabezado/pie de página** — Configuración de sombras a nivel de widget para elementos como logotipos, barras de búsqueda y elementos de navegación

Cualquier elemento que admita el grupo de estilo Efectos mostrará los controles del editor de sombras.

## Consejos

- Usa sombras sutiles (presets Pequeño o Suave) para la mayoría de los elementos — sombras pesadas pueden hacer que el diseño se sienta desordenado.
- Combina una sombra cercana y oscura con una sombra lejana y clara para el efecto de elevación más natural.
- Las sombras internas funcionan bien en campos de entrada y contenedores para crear un efecto de panel hundido.
- Las sombras de texto deben ser mínimas — un desplazamiento de 1px con un ligero desenfoque mejora la legibilidad en fondos de imagen sin parecer anticuado.
- Prueba tus sombras contra fondos claros y oscuros si tu tema admite un conmutador de modo oscuro.

Recuerda: Preserva todo el formato markdown, rutas de imágenes, bloques de código y términos técnicos exactamente como se muestran en las reglas de preservación.