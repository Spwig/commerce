---
title: Campos del constructor de formularios y validación
---

Los campos de formulario son los bloques de construcción de tus formularios—cada campo recopila un fragmento de datos de los usuarios. El constructor de formularios ofrece 22 tipos de campos que van desde entradas de texto simples hasta escalas de calificación avanzadas y selectores de productos. Configure cada campo con etiquetas, reglas de validación, texto de ayuda y lógica condicional para crear formularios dinámicos que se adapten según las respuestas del usuario. Los campos pueden ser obligatorios u opcionales, validados con patrones de expresión regular y estilizados con clases CSS personalizadas.

Use esta guía para comprender todos los tipos de campos disponibles, cuándo usar cada uno y cómo configurar la validación y la lógica condicional.

## Configuración básica de campos

Cada campo comparte estos ajustes comunes:

**Identidad**:
- **Nombre del campo** - Nombre de máquina para el almacenamiento de datos (sin espacios, use guiones bajos: `email_address`)
- **Tipo de campo** - Determina el comportamiento de entrada y la representación
- **Asignación de paso** - ¿A qué paso pertenece este campo (solo para formularios de múltiples pasos)?

**Visualización**:
- **Etiqueta** - Pregunta o indicación mostrada a los usuarios (ejemplo: "¿Cuál es su dirección de correo electrónico?")
- **Texto de marcador de posición** - Texto de ayuda dentro de la entrada (ejemplo: "you@example.com")
- **Texto de ayuda** - Guía adicional debajo del campo (ejemplo: "Nunca compartiremos su correo electrónico")
- **Valor predeterminado** - Valor prellenado (los usuarios pueden cambiarlo)

**Diseño**:
- **Ancho** - Ancho completo (100%), medio (50%) o un tercio (33%) del ancho del formulario
- **Clase CSS** - Clases adicionales de estilo para un diseño personalizado
- **Orden** - Posición dentro del paso (arrastre para reordenar)

**Validación**:
- **Obligatorio** - Cambiar el estado obligatorio (aparece un asterisco rojo en la etiqueta)
- **Longitud mínima/máxima** - Límites de caracteres (campos de texto)
- **Valor mínimo/máximo** - Límites numéricos (campos de número)
- **Patrón de validación** - Expresión regular personalizada para validación compleja
- **Mensaje de error** - Texto personalizado mostrado cuando falla la validación

## Campos de entrada de texto

**Texto de una línea** (`text`):
- Entrada de texto básica para respuestas cortas
- Validación: longitud mínima/máxima, patrón de expresión regular
- Caso de uso: Nombres, direcciones, códigos de producto, respuestas cortas
- Ejemplo: "Nombre completo", "Dirección de calle", "Nombre de la empresa"

**Texto de múltiples líneas** (`textarea`):
- Área de texto expandible para contenido más largo (3-10 filas)
- Validación: longitud mínima/máxima
- Caso de uso: Comentarios, retroalimentación, descripciones detalladas, mensajes
- Ejemplo: "Cuéntanos sobre su experiencia", "Notas adicionales"

**Dirección de correo electrónico** (`email`):
- Validación específica para correo electrónico (requiere @ y dominio)
- Teclados móviles muestran el botón @ de forma destacada
- Caso de uso: Correo de contacto, suscripciones a boletines, creación de cuenta
- Ejemplo: "Dirección de correo electrónico", "Correo de trabajo"

**Número de teléfono** (`phone`):
- Formatea automáticamente números de teléfono
- Teclados móviles muestran disposición numérica
- Validación: patrón configurable (formatos internacionales admitidos)
- Caso de uso: Teléfono de contacto, contacto de emergencia, programación de citas
- Ejemplo: "Número de teléfono", "Teléfono móvil", "Número de contacto"

**Número** (`number`):
- Entrada numérica con controles de incremento/decremento
- Validación: valor mínimo/máximo, incremento de paso
- Devuelve un número (no cadena) en las respuestas
- Caso de uso: Cantidades, edades, años de experiencia, montos de presupuesto
- Ejemplo: "¿Cuántos empleados tiene?", "Su edad", "Años en el negocio"

**URL** (`url`):
- Validación de URL (requiere http:// o https://)
- Teclados móviles muestran el botón .com
- Caso de uso: Sitio web, perfil de LinkedIn, enlace a portafolio
- Ejemplo: "Sitio web de la empresa", "URL del portafolio"

## Campos de selección

**Selector de desplazamiento** (`select`):
- Selección de una opción de un menú desplegable
- Configuración: matriz de {valor, etiqueta} opciones
- Soporta selección predeterminada
- Caso de uso: Categorías, estados/países, selección de estado
- Ejemplo: "Seleccione su país", "Departamento", "¿Cómo se enteró de nosotros?"
- Mejor para: 5+ opciones (menos opciones use radio en su lugar)

**Botones de opción** (`radio`):
- Elección única de opciones visibles (todas las opciones mostradas)
- Configuración: matriz de {valor, etiqueta} opciones
- Mejor experiencia de usuario que select para 2-4 opciones
- Caso de uso: Preguntas de sí/no, género, preferencias con pocas opciones
- Ejemplo: "¿Recomendaría nuestro servicio?", "Método de contacto preferido"

**Casilla de verificación** (`checkbox`):
- Casilla de verificación de un solo estado (encendido/apagado)
- Devuelve verdadero/falso en las respuestas
- Caso de uso: Aceptación de términos, acuerdos, preferencia única
- Ejemplo: "Acepto los términos y condiciones", "Suscribirse al boletín"

**Grupo de casillas de verificación** (`checkbox_group`):
- Selección múltiple de opciones (los usuarios pueden seleccionar 0, 1 o muchas)
- Configuración: matriz de {valor, etiqueta} opciones
- Devuelve matriz de valores seleccionados
- Caso de uso: Preferencias de múltiple selección, intereses, características necesarias
- Ejemplo: "¿Qué temas le interesan?", "Seleccione todas las que se aplican"

## Campos de calificación

**Calificación con estrellas** (`rating_stars`):
- Escala visual de calificación con estrellas (normalmente 1-5 estrellas)
- Configuración:
  - `max_stars`: 3-10 estrellas (por defecto: 5)
  - `allow_half`: verdadero/falso para calificaciones con medio estrella
  - `icon`: fa-star (por defecto) o fa-heart
  - `color`: código de color hexadecimal (por defecto: #FFD700 oro)
- Caso de uso: Calificaciones de productos, calidad del servicio, puntuaciones de satisfacción
- Ejemplo: "Califique su experiencia", "¿Cómo fue nuestro servicio?"

**Escala Likert** (`rating_likert`):
- Escala de calificación de enunciados: de "muy en desacuerdo" a "muy de acuerdo"
- Configuración:
  - `scale_type`: 5_point (1-5) o 7_point (1-7)
  - `labels`: personalizar el texto de los extremos (izquierda: "Muy en desacuerdo", derecha: "Muy de acuerdo")
- Devuelve valor numérico (1-5 o 1-7)
- Caso de uso: Enunciados de encuesta, escalas de acuerdo, medición de sentimiento
- Ejemplo: "El producto cumple con mis necesidades", "El servicio al cliente fue útil"

**Puntaje Net Promoter (NPS)** (`rating_nps`):
- Escala de 0-10: "No muy probable" a "Muy probable"
- Configuración:
  - `low_label`: texto del extremo izquierdo (por defecto: "No muy probable")
  - `high_label`: texto del extremo derecho (por defecto: "Muy probable")
- Devuelve valor de 0-10 (0-6 = detractores, 7-8 = pasivos, 9-10 = promotores)
- Caso de uso: Encuestas NPS, probabilidad de recomendación, medición de lealtad
- Ejemplo: "¿Qué tan probable es que recomiende nuestro servicio a un amigo?"

## Campos avanzados

**Carga de archivos** (`file`):
- Carga de un solo archivo o múltiples archivos
- Configuración:
  - `max_size_mb`: límite de tamaño de archivo por archivo (por defecto: 5MB)
  - `allowed_types`: matriz de extensiones (ejemplo: ["pdf", "doc", "docx", "jpg", "png"])
  - `max_files`: número máximo de archivos (1 para un solo archivo, 2+ para múltiples)
- Devuelve ruta(s) de archivo en las respuestas
- Los archivos se almacenan en `/media/form_uploads/{form-slug}/`
- Caso de uso: Carga de currículums, envío de documentos, adjuntos de fotos
- Ejemplo: "Cargue su currículum", "Adjunte documentos de apoyo"

**Selector de producto** (`product_select`):
- Selección múltiple de su catálogo de productos
- Configuración:
  - `category_filters`: limitar a categorías específicas (matriz de IDs de categoría)
  - `max_selections`: 1 para un solo producto, 2+ para múltiples
  - `display_mode`: "list" (por defecto) o "grid" (con miniaturas)
- Devuelve IDs/Referencias de producto en las respuestas
- Caso de uso: Recomendaciones de productos, listas de deseos, encuestas de retroalimentación, paquetes
- Ejemplo: "¿Qué productos le interesan?", "Seleccione sus artículos favoritos"

**Fecha** (`date`):
- Interfaz de selector de fecha (ventana emergente de calendario)
- Devuelve formato ISO (YYYY-MM-DD)
- Validación: fecha mínima/máxima
- Caso de uso: Fechas de nacimiento, fechas de eventos, programación de citas, plazos
- Ejemplo: "Fecha de nacimiento", "Fecha de cita preferida"

**Hora** (`time`):
- Selector de hora (horas y minutos)
- Devuelve formato de hora ISO (HH:MM)
- Caso de uso: Horas de cita, ventanas de disponibilidad
- Ejemplo: "Hora preferida", "Disponible después"

**Fecha y hora** (`datetime`):
- Selector combinado de fecha y hora
- Devuelve datetime completo en formato ISO
- Caso de uso: Programación de eventos, reservación de citas
- Ejemplo: "Hora de inicio del evento", "Ventana de entrega"

## Campos de diseño (no entrada)

**Encabezado de sección** (`heading`):
- Texto de encabezado para organizar secciones del formulario
- Configuración: nivel de encabezado (h2, h3, h4)
- Sin recopilación de datos
- Caso de uso: Dividir formularios largos en secciones lógicas
- Ejemplo: "Información personal", "Detalles de contacto", "Preferencias"

**Párrafo descriptivo** (`paragraph`):
- Bloque de texto enriquecido para instrucciones o información
- Sin recopilación de datos
- Soporta formato básico (negrita, cursiva, enlaces)
- Caso de uso: Instrucciones de paso, descargos legales, explicaciones
- Ejemplo: Notificación de política de privacidad, explicación de consentimiento GDPR

**Línea divisora** (`divider`):
- Línea horizontal visual separadora
- Sin recopilación de datos
- Caso de uso: Organización visual entre secciones

**Campo oculto** (`hidden`):
- Campo invisible con valor programático
- Configuración: `default_value` (requerido)
- No se muestra etiqueta o texto de ayuda a los usuarios
- Caso de uso: Parámetros UTM, datos de seguimiento, identificadores de sesión, códigos de referidos
- Ejemplo: Campo oculto con valor de parámetro de URL

## Reglas de validación de campo

**Campos obligatorios**:
- Active el cuadro de verificación "Obligatorio" en la configuración del campo
- Aparece un asterisco rojo (*) junto a la etiqueta
- El formulario no se puede enviar si los campos obligatorios están vacíos
- Error personalizado: "Este campo es obligatorio" (o mensaje personalizado)

**Longitud mínima/máxima** (campos de texto):
- Establezca el recuento mínimo de caracteres: evita respuestas demasiado cortas
- Establezca el recuento máximo de caracteres: evita entrada excesiva
- Ejemplo: Campo de mensaje requiere mínimo 10 caracteres (evita respuestas como "ok")

**Valor mínimo/máximo** (campos numéricos):
- Establezca el valor numérico mínimo: evita edades negativas, cantidades
- Establezca el valor numérico máximo: limita la entrada a un rango razonable
- Ejemplo: Campo de edad requiere mínimo 18, máximo 120

**Patrón de validación** (expresión regular):
- Expresión regular personalizada para validación compleja
- Patrones comunes:
  - Código postal: `^×{5}(-×{4})?$` (formato de EE.UU.)
  - Teléfono: `^(×{3}) ×{3}-×{4}$` (formato de EE.UU.)
  - Código de producto: `^[A-Z]{2}×{4}$` (2 letras, 4 dígitos)
- Mensaje de error personalizado requerido al usar patrones

**Validación de archivos**:
- Tamaño máximo de archivo: evita subidas grandes (por defecto 5MB)
- Tipos permitidos: lista blanca de extensiones específicas (seguridad)
- Ejemplo: Campo de currículum permite ["pdf", "doc", "docx"], máximo 2MB

## Lógica condicional

Cree formularios dinámicos donde los campos aparezcan o desaparezcan según las respuestas del usuario:

**Cómo funcionan las reglas condicionales**:
1. El usuario responde al campo "fuente" (el disparador)
2. El sistema evalúa la regla: operador + valor de comparación
3. Si la condición es verdadera, se ejecuta la acción (mostrar/ocultar/requerir campo o paso)
4. Se pueden encadenar múltiples reglas (la regla A desencadena la regla B)

**Operadores disponibles**:
- **Igual a** (`equals`): coincidencia exacta (ejemplo: país igual a "US")
- **No igual a** (`not_equals`): cualquier cosa excepto el valor
- **Contiene** (`contains`): texto incluye subcadena (insensible a mayúsculas/minúsculas)
- **Mayor que** (`greater_than`): comparación numérica (ejemplo: edad > 18)
- **Menor que** (`less_than`): comparación numérica (ejemplo: calificación < 3)
- **Vacío** (`is_empty`): el campo no tiene valor
- **No vacío** (`is_not_empty`): el campo tiene cualquier valor
- **En la lista** (`in_list`): el valor es uno de ["Opción1", "Opción2"]

**Acciones disponibles**:
- **Mostrar campo** - Mostrar campo oculto
- **Ocultar campo** - Ocultar campo (el valor se borra si se oculta)
- **Requerir campo** - Hacer el campo obligatorio
- **No requerir campo** - Hacer el campo opcional
- **Establecer valor** - Rellenar el campo con un valor
- **Mostrar paso** - Mostrar paso oculto (solo para múltiples pasos)
- **Ocultar paso** - Ocultar paso (solo para múltiples pasos)
- **Saltar a paso** - Saltar a un paso específico (solo para múltiples pasos)

**Ejemplos de reglas**:
- SI `contact_method` IGUAL A "phone" ENTONCES mostrar_campo `phone_number`
- SI `rating` MENOR QUE "3" ENTONCES requerir_campo `improvement_feedback`
- SI `country` EN_LA_LISTA ["US", "CA"] ENTONCES mostrar_paso `shipping_details`
- SI `budget` MAYOR QUE "10000" ENTONCES mostrar_campo `enterprise_features`

**Crear reglas condicionales**:
1. Haga clic en la pestaña "Reglas condicionales" en el panel derecho
2. Haga clic en "Agregar regla"
3. Seleccione el campo fuente (disparador)
4. Seleccione el operador (cómo comparar)
5. Ingrese el valor de comparación (contra qué comparar)
6. Seleccione la acción (qué hacer)
7. Seleccione el objetivo (campo o paso afectado)
8. Opcional: Establezca la prioridad (las reglas con mayor prioridad se evalúan primero)
9. Guarde la regla

**Prioridad de reglas**:
- Números más altos se evalúan primero (prioridad 100 antes que prioridad 10)
- Use la prioridad cuando las reglas se contradigan o se encadenen
- Ejemplo: Regla A (prioridad 100) muestra el campo, Regla B (prioridad 50) lo requiere (A se ejecuta primero, luego B)

## Patrones de campo comunes

**Formulario de contacto**:
- Nombre completo (texto, obligatorio)
- Correo electrónico (correo electrónico, obligatorio)
- Teléfono (teléfono)
- Asunto (selector con opciones: "Ventas", "Soporte", "Alianzas")
- Mensaje (área de texto, obligatorio, mínimo 10 caracteres)

**Retroalimentación del producto**:
- Producto (product_select, selección única)
- Calificación general (rating_stars, 5 estrellas)
- Condicional: SI calificación < 3 ENTONCES requerir "¿Qué podemos mejorar?" (área de texto)
- Recomendación (rating_nps)

**Solicitud de empleo**:
- Paso 1: Personal (nombre, correo electrónico, teléfono)
- Paso 2: Currículum (carga de archivos, permitir ["pdf", "doc"], máximo 2MB)
- Paso 3: Disponibilidad (fecha de inicio, grupo de casillas de verificación para días laborables)
- Condicional: SI "years_experience" > 5 ENTONCES mostrar_campo "experiencia_de_liderazgo"

## Consejos

- **Use los tipos de campos adecuados** - Campo de correo electrónico para correos (no texto), proporciona validación y teclados móviles mejores
- **Mantenga las etiquetas cortas** - Use el texto de ayuda para detalles, no las etiquetas
- **Agrupe campos relacionados** - Use encabezados y líneas divisoras para organización visual
- **Pruebe la validación** - Previsualice el formulario y intente enviar datos inválidos
- **Límite el tamaño de carga de archivos** - Máximo de 5MB evita sobrecarga del servidor por archivos grandes
- **Use lógica condicional con moderación** - Demasiadas reglas confunden a los usuarios; mantenga los formularios simples
- **Establezca valores máximos realistas** - Máximo de edad de 120, máximo de cantidad de 100 (evita errores de escritura como 1000)
- **Proporcione ejemplos de patrones** - Si usa validación de expresión regular, muestre un ejemplo en el texto de ayuda
- **Haga obvio que los campos sean obligatorios** - Nombre y correo electrónico para formularios de contacto, siempre obligatorios
- **Use botones de opción para 2-4 opciones** - Selector para 5+ opciones (mejora la experiencia del usuario)
- **Campos de ancho medio para entradas cortas** - Teléfono y código postal pueden ser de ancho medio, ahorra espacio vertical
- **Selectores de productos para listas de deseos** - Permita a los clientes seleccionar múltiples productos para recomendaciones

Recuerde: preserve todo el formato de markdown, rutas de imágenes, bloques de código y términos técnicos exactamente como se muestran en las reglas de preservación.