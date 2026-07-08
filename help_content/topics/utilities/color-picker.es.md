---
title: Selector de colores
---

El selector de colores avanzado le permite elegir colores usando varios métodos de entrada y configuraciones predeterminadas conscientes del tema. Aparece en cualquier lugar donde se utilice una propiedad de color en toda la plataforma — en el constructor de páginas, constructor de encabezados/pie de página, constructor de menús y en el administrador del catálogo. Haga clic en cualquier muestra de color o campo de entrada de color para abrir el selector.

![Selector de colores](/static/core/admin/img/help/color-picker/color-picker.webp)

## Métodos de entrada de color

El selector admite varias formas de definir un color:

| Método | Descripción | Ejemplo |
|--------|-------------|---------|
| **Hex** | Ingrese un código hex de 6 dígitos directamente | `#FF5733` |
| **RGB** | Ajuste los deslizadores de Rojo, Verde y Azul (0-255 cada uno) | `rgb(255, 87, 51)` |
| **HSL** | Establezca Matiz (0-360), Saturación (0-100%) y Brillo (0-100%) | `hsl(14, 100%, 60%)` |
| **RGBA** | RGB con un canal de transparencia alfa | `rgba(255, 87, 51, 0.8)` |
| **HSLA** | HSL con un canal de transparencia alfa | `hsla(14, 100%, 60%, 0.8)` |
| **Espectro visual** | Haga clic o arrastre en el área del espectro de colores para elegir visualmente | Selección de puntero y clic |

También puede escribir un valor directamente en el campo de texto en la parte inferior del selector.

## Selector de formato

Un menú desplegable en la parte superior del selector le permite cambiar entre los modos de salida **HEX**, **RGB**, **RGBA**, **HSL** y **HSLA**. Al cambiar de formato, el color actual se convierte automáticamente — no se pierden valores. Elija el formato que mejor se adapte a su flujo de trabajo o a los requisitos de su sistema de diseño.

## Preset de colores

Debajo del área del espectro, una fila de muestras de color de acceso rápido le permite seleccionar con un solo clic colores comunes. Estas muestras son **conscientes del tema**: se ajustan automáticamente a los colores primarios, secundarios, de énfasis y neutros del tema activo. Esto le permite mantener coherencia con su marca sin tener que memorizar códigos hex.

Para aplicar un preset, haga clic en la muestra. El selector se actualiza inmediatamente para mostrar el color seleccionado en el espectro y en los campos de entrada.

## Opacidad / Alfa

Cuando use el modo RGBA o HSLA, aparecerá un deslizador **de transparencia (alfa)** horizontal debajo del espectro. Arrástrelo para establecer la transparencia desde 0% (completamente transparente) hasta 100% (completamente opaco). El valor de opacidad también se puede editar como entrada numérica junto al deslizador para un control preciso.

Los colores semitransparentes son útiles para superposiciones, efectos de hover y elementos de diseño en capas.

## Color actual vs. nuevo

En la parte inferior del selector, dos cuadros al lado de uno otro muestran el **color actual** aplicado y el **nuevo** color seleccionado. Esta comparación le permite evaluar el cambio antes de confirmarlo. Haga clic en **Aplicar** para aceptar el nuevo color, o haga clic fuera del selector para cancelar y mantener el valor actual.

## ¿Dónde aparece?

El selector de colores es una utilidad compartida utilizada en todo el administrador:

- **Constructor de páginas** — Color del texto, color de fondo, color del borde y estados de hover en la pestaña Estilo
- **Constructor de encabezados/pie de página** — Colores del texto, fondo, icono y enlaces de los widgets
- **Constructor de menús** — Colores de los enlaces de los elementos del menú y estados de hover/activo
- **Administrador del catálogo** — Colores de los sellos de productos y colores de énfasis de las categorías

Cualquier campo que acepte un valor de color abre este mismo selector, por lo que la experiencia es coherente en todas partes.

## Consejos

- Use las muestras de colores predeterminadas de su tema para mantener la coherencia de la marca en todas las páginas y componentes.
- Cambie al modo HSL cuando necesite crear variantes más claras o más oscuras del mismo matiz — simplemente ajuste el valor de brillo.
- Copie el código hex desde el campo de texto para reutilizar exactamente el mismo color en otro campo o compartilo con un diseñador.
- Use RGBA con opacidad reducida para efectos de superposición sutiles en imágenes y secciones de hero.
- El selector recuerda los colores utilizados recientemente durante su sesión, por lo que los colores personalizados que usa con frecuencia permanecen accesibles.
- Si pega un valor de color en cualquier formato compatible en el campo de entrada de hex, el selector lo reconocerá y lo convertirá automáticamente.