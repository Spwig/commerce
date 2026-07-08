---
title: Compartir en redes sociales
---

Los botones de compartir en redes sociales permiten a los clientes compartir tus productos, entradas de blog y páginas directamente desde tu tienda en línea. Tú controlas qué plataformas se muestran, cómo lucen los botones, dónde se colocan y si se rastrea y cuenta la actividad de compartir.

## Configuración de compartir en redes sociales

Todo el comportamiento de compartir en redes sociales se controla desde una sola página de configuración. Navega a **Marketing > Configuración de Compartir en Redes Sociales** (la página se redirige automáticamente al formulario de configuración — solo hay un registro de configuración).

### Ubicación: dónde aparecen los botones

La sección **Ubicación** controla qué tipos de contenido muestran automáticamente los botones de compartir.

| Configuración | Descripción |
|---------|-------------|
| **Habilitar en Productos** | Mostrar botones de compartir en las páginas de detalles del producto |
| **Habilitar en Categorías** | Mostrar botones de compartir en las páginas de listado de categorías |
| **Habilitar en Entradas de Blog** | Mostrar botones de compartir en las páginas de entradas de blog |
| **Habilitar en Páginas Personalizadas** | Mostrar botones de compartir en páginas personalizadas de la tienda |

Marque los tipos de contenido donde desee que aparezcan los botones. Puede habilitar cualquier combinación — por ejemplo, solo productos y entradas de blog.

**Ubicación de los botones** controla dónde en la página se muestran los botones:

| Opción | Descripción |
|--------|-------------|
| **Debajo del contenido** (por defecto) | Se muestra después del contenido principal |
| **Arriba del contenido** | Se muestra antes del contenido principal |
| **Barra lateral** | Se muestra en la barra lateral de la página |
| **Flotante (fijo)** | Se mantiene en el lado de la ventana de visualización a medida que el visitante desplaza la página |

### Apariencia: cómo lucen los botones

La sección **Apariencia** controla qué plataformas se muestran y cómo se estilan los botones.

**Plataformas habilitadas** — deje vacío para mostrar todas las plataformas compatibles, o ingrese un arreglo JSON para restringir qué plataformas se muestran:

```json
["facebook", "twitter", "pinterest", "whatsapp", "email"]
```

Claves de plataforma compatibles: `facebook`, `twitter`, `linkedin`, `pinterest`, `whatsapp`, `telegram`, `email`

**Estilo del botón**:

| Estilo | Descripción |
|-------|-------------|
| **Solo ícono** (por defecto) | Muestra solo el ícono de la plataforma |
| **Ícono + Etiqueta** | Muestra el ícono y el nombre de la plataforma |
| **Solo etiqueta** | Muestra solo el nombre de la plataforma como texto |

**Tamaño del botón** — elija **Pequeño**, **Mediano** (por defecto) o **Grande** para que coincida con el diseño de su tienda en línea.

**Dirección de disposición** — organice los botones **Horizontalmente** (por defecto, uno al lado del otro) o **Verticalmente** (apilados).

**Mostrar título** — cuando está activado, aparece un encabezado "Compartir" encima del grupo de botones.

**Visibilidad en dispositivos móviles** controla la visualización de los botones en pantallas pequeñas:

| Opción | Descripción |
|--------|-------------|
| **Siempre mostrar** (por defecto) | Los botones son visibles en todos los dispositivos |
| **Ocultar en dispositivos móviles** | Los botones se ocultan en dispositivos móviles |
| **Solo en dispositivos móviles** | Los botones se muestran solo en dispositivos móviles |

### Configuración de seguimiento

**Mostrar conteo de compartidos** — cuando está activado, aparece un distintivo de conteo en cada botón que muestra cuántas veces esa plataforma ha sido compartida. Los conteos se actualizan en tiempo real a medida que se registran los compartidos.

**Seguir compartidos** — cuando está activado, cada clic de compartir se registra en el análisis de compartir. Desactivar esto detiene el registro de nuevos datos, pero no elimina los datos existentes. El seguimiento también otorga insignias de lealtad a los clientes que comparten (si el programa de lealtad está activo).

Haga clic en **Guardar** en la parte inferior del formulario para aplicar sus cambios. Las configuraciones tienen efecto inmediatamente.

## Ver actividad de compartir

### Eventos de compartir individuales

Navegue a **Marketing > Compartidos en Redes Sociales** para ver un registro de cada evento de compartir registrado. Cada entrada muestra:

- **Plataforma** — qué red social se usó (mostrada como un distintivo con color)
- **Contenido compartido** — el tipo y nombre del contenido compartido (por ejemplo, `producto: Blue Widget`)
- **Usuario** — el cliente que compartió, o "Anónimo" para visitantes que no estaban conectados
- **Tipo de dispositivo** — escritorio, móvil o tableta
- **Compartido en** — la fecha y hora del compartir

El registro de compartir es de solo lectura — las entradas se crean automáticamente cuando los clientes hagan clic en los botones de compartir.

Utilice los filtros **Plataforma** y **Tipo de dispositivo** para explorar patrones de compartición, y la jerarquía de fechas para analizar períodos de tiempo específicos.

### Cuentas de compartición por contenido

Navegue hasta **Marketing > Cuentas de compartimiento** para ver totales de compartimientos agrupados por elemento de contenido y plataforma. Esta vista le permite identificar fácilmente sus productos y publicaciones más compartidos.

Cada entrada muestra:
- **Contenido** — el tipo y nombre del elemento (por ejemplo, `producto: Blue Widget`)
- **Plataforma** — la red social
- **Cuenta de compartimiento** — total de compartimientos registrados en esa plataforma
- **Última actualización** — cuándo se recalculó la cuenta por última vez

La lista está ordenada por cuenta de compartimiento descendente, por lo que su contenido más viral aparece en la parte superior. Las cuentas de compartimiento se actualizan automáticamente siempre que se registre un nuevo evento de compartimiento — no es necesario actualizarlas manualmente.

## Entender cómo se rastrean los compartimientos

Cuando un cliente hace clic en un botón de compartir, Spwig registra:

1. En qué plataforma compartieron
2. Qué contenido se compartió (producto, entrada de blog, página, etc.)
3. Si estaban conectados (si es así, el compartimiento se vincula a su cuenta para la integración de lealtad)
4. El tipo de dispositivo
5. La URL que se compartió

La cuenta de compartimiento para esa plataforma y elemento de contenido se incrementa automáticamente. Si **Mostrar cuentas de compartimiento** está habilitado, la cuenta actualizada aparece en el botón la próxima vez que se cargue la página.

## Integración de lealtad

Si su programa de lealtad está activo y **Seguir compartimientos** está habilitado, los clientes conectados ganan insignias de lealtad cuando comparten contenido. La insignia de compartir en redes sociales forma parte de las reglas basadas en acciones del programa de lealtad.

Para configurar recompensas de puntos por compartir, navegue hasta **Clientes > Reglas de lealtad** y busque reglas con el tipo **Basado en acciones** y el tipo de acción **Compartimiento social**.

## Consejos

- Active primero el compartir en productos y entradas de blog — estos son los tipos de contenido más propensos a ser compartidos de forma orgánica
- Pinterest es especialmente valioso para categorías de productos visuales como moda, decoración para el hogar y comida — priorícelo en la lista `enabled_platforms` para esas tiendas
- El compartir en WhatsApp impulsa fuertes conversiones desde referidos calientes, especialmente en dispositivos móviles; considere usar el modo de visualización **Solo móvil** para WhatsApp, manteniendo otras plataformas visibles en todos los dispositivos
- Si nota que las cuentas de compartimiento están infladas, revise si el tráfico de prueba (de sesiones de administrador) se contó antes de que la bandera **Es tráfico de administrador** funcionara correctamente — puede restablecer las cuentas eliminando entradas del análisis de compartimientos
- Revise la lista de Cuentas de compartimiento mensualmente para identificar sus productos más compartidos y destacarlos más prominentemente en su página principal o en correos electrónicos de marketing