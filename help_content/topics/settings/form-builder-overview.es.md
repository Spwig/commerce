---
title: Vista general del constructor de formularios
---

El constructor de formularios crea formularios personalizados para la recopilación de datos: formularios de contacto, encuestas, aplicaciones, registros y más. Construya formularios visualmente con campos de arrastrar y soltar, configure reglas de validación, habilite flujos de trabajo de varios pasos y recopile respuestas con análisis detallados. Los formularios se integran de forma fluida con elementos del constructor de páginas, incrustándose en cualquier lugar de su sitio. Todas las solicitudes se almacenan en la base de datos con metadatos completos (dirección IP, navegador, tiempo para completar) para el análisis y la exportación.

Use el constructor de formularios cuando necesite recopilar datos estructurados de los clientes, ya sea información de contacto simple o aplicaciones de varias páginas complejas.

## ¿Qué es el constructor de formularios?

El constructor de formularios es una herramienta de arrastrar y soltar visual para crear formularios personalizados sin código:

**Tipos de formularios compatibles**:
- Formularios de contacto (nombre, correo electrónico, mensaje)
- Encuestas de clientes (calificaciones, comentarios, NPS)
- Registros de productos (garantía, soporte)
- Solicitud de empleo (carga de currículum, varios pasos)
- Registros de eventos (información del asistente, preferencias)
- Solicitud de servicios (requisitos detallados)
- Suscripción al boletín (con casillas de verificación para preferencias)

**Características clave**:
- **22 tipos de campos** - Texto, correo electrónico, teléfono, carga de archivos, calificaciones, selectores de productos y más
- **Formularios de varios pasos** - Divida formularios largos en pasos lógicos con seguimiento de progreso
- **Lógica condicional** - Muestre/oculte campos según las respuestas del usuario
- **Reglas de validación** - Campos obligatorios, longitud mínima/máxima, patrones de expresión regular personalizados
- **Protección contra spam** - Campos de honeypot o Google reCAPTCHA v3
- **Análisis de respuestas** - Trazar tiempo de finalización, dirección IP, navegador, remitente
- **Exportación CSV** - Descargue todas las respuestas para el análisis en Excel/Google Sheets
- **Multilingüe** - Traduzca etiquetas y mensajes del formulario a todos los idiomas activos

## Creando su primer formulario

Navegue a **Configuración > Páginas > Formularios** para acceder al administrador de formularios:

**Paso 1: Crear un nuevo formulario**
- Haga clic en **+ Crear nuevo formulario**
- Ingrese el nombre del formulario (identificador interno, no se muestra a los clientes)
- Ingrese el título del formulario (se muestra como encabezado encima del formulario)
- Opcional: Agregar descripción (texto de ayuda mostrado debajo del título)

**Paso 2: Agregar campos**
- Haga clic en **Editar diseño del formulario** para abrir el constructor visual
- Arrastre tipos de campos desde la barra lateral izquierda al lienzo
- Haga clic en el campo para configurarlo en el panel derecho
- Establezca la etiqueta, el marcador de posición, el texto de ayuda
- Active/desactive el estado obligatorio
- Agregue reglas de validación

**Paso 3: Configurar ajustes del formulario**
- Establezca el texto del botón de envío (por defecto: "Enviar")
- Personalice el mensaje de éxito (mostrado después de la presentación)
- Elija protección contra spam (recomendado honeypot)
- Active/desactive "Requiere inicio de sesión" si es necesario
- Active "Formulario de varios pasos" para formularios complejos

**Paso 4: Activar el formulario**
- Active el estado **Activo**
- Solo los formularios activos aceptan presentaciones
- Guarde el formulario

**Paso 5: Usar en el constructor de páginas**
- Agregue el elemento **Formulario** a cualquier página
- Seleccione su formulario desde el menú desplegable
- El formulario hereda el estilo de la página
- Las presentaciones se envían al backend automáticamente

## Formularios de una página vs. formularios de varios pasos

**Formularios de una página** (por defecto):
- Todos los campos se muestran a la vez
- Desplácese para ver todos los campos
- Botón de envío en la parte inferior
- Mejor para: Formularios de contacto, encuestas cortas, recopilación de datos simples

**Formularios de varios pasos**:
- Campos organizados en pasos numerados
- Barra de progreso muestra el paso actual
- Botones de navegación Atrás/Siguiente
- Envío solo en el último paso
- Opcional: Guardar respuestas parciales (modo de borrador)
- Mejor para: Solicitud de empleo, registros, encuestas complejas, flujos de pago

**Habilitar formulario de varios pasos**:
1. Active "Formulario de varios pasos" en ajustes del formulario
2. Haga clic en la pestaña **Pasos** en el panel derecho
3. Agregue paso (ej. "Información personal", "Detalles de contacto", "Preferencias")
4. Asigne campos a pasos usando el menú desplegable de paso al editar el campo
5. Reordenar pasos arrastrándolos
6. Establecer propiedades del paso: título, descripción, omitible

**Beneficios de formulario de varios pasos**:
- Reduce la abandono del formulario (psicológico: "solo 3 preguntas en esta página")
- Agrupación lógica mejora la UX
- Indicador de progreso motiva la finalización
- Guardado de borrador opcional para formularios largos

## Explicación de ajustes del formulario

**Ajustes básicos**:
- **Nombre interno** - Cómo identifica el formulario en el administrador (no visible para los clientes)
- **Slug** - Identificador amigable para URL (generado automáticamente, usado en puntos finales de API)
- **Título del formulario** - Encabezado mostrado encima del formulario
- **Descripción** - Texto de ayuda opcional mostrado debajo del título
- **Texto del botón de envío** - Personalice la etiqueta del botón (ej. "Enviar mensaje", "Postularse ahora")

**Mensajes**:
- **Mensaje de éxito** - Mostrado después de la presentación exitosa (por defecto: "¡Gracias por su presentación!")
- **Mensaje de error** - Mostrado si la presentación falla (por defecto: "Ocurrió un error. Por favor, inténtelo de nuevo.")

**Seguridad y acceso**:
- **Activo** - Solo los formularios activos aceptan presentaciones (formularios inactivos muestran "Formulario no disponible")
- **Requiere inicio de sesión** - Restringe a usuarios autenticados solo (usuarios anónimos ven el prompt de inicio de sesión)

**Protección contra spam**:
- **Ninguno** - Sin protección (no recomendado, los bots enviarán spam)
- **Campo honeypot** - Campo invisible que captura bots (recomendado para la mayoría de los comerciantes)
- **Google reCAPTCHA v3** - Requiere clave del sitio y clave secreta de Google (protección más fuerte)

**Características avanzadas**:
- **Formulario de varios pasos** - Habilite flujo de trabajo paso a paso
- **Guardar respuestas parciales** - Permita a los usuarios guardar el progreso y reanudar más tarde (solo para formularios de varios pasos)

## Opciones de protección contra spam

**Campo honeypot (recomendado)**:
- Campo invisible agregado al formulario
- Los bots lo llenan (los humanos no pueden verlo)
- Las presentaciones con campo honeypot rellenado se rechazan
- No se requiere configuración
- No hay frustración de CAPTCHA para los usuarios
- Efectivo contra el 95%+ de bots de spam

**Google reCAPTCHA v3**:
- Puntaje de fondo invisible (0.0-1.0)
- Sin desafío "haga clic en los semáforos"
- Requiere configuración:
  1. Cree una cuenta en google.com/recaptcha/admin
  2. Genere clave del sitio y clave secreta
  3. Ingrese las claves en ajustes del constructor de formularios
- Más robusto que honeypot
- Use cuando honeypot sea insuficiente

**Ninguno**:
- Sin protección contra spam
- Solo use para formularios internos o pruebas
- Los formularios públicos serán spamados en gran medida

## Administración de respuestas del formulario

Ver todas las solicitudes en **Configuración > Páginas > Formularios > [Nombre del formulario] > Respuestas**:

**Vista de lista de respuestas**:
- Estado: borrador, presentado, completado
- Presentador: correo electrónico (si inició sesión) o "Anónimo"
- Dirección IP y ubicación (si GeoIP está habilitado)
- Fecha/hora de presentación
- Tiempo para completar (segundos)

**Detalles de respuesta**:
- Todos los valores de campo con etiquetas
- Metadatos: navegador, remitente, idioma
- Seguimiento de progreso (formulario de varios pasos): paso actual, pasos completados
- Resultados de acción (si el formulario desencadena acciones)

**Filtrado de respuestas**:
- Filtre por formulario, estado, rango de fechas
- Busque por correo electrónico del presentador o dirección IP
- Ordene por fecha de presentación, tiempo de finalización

**Exportación de respuestas**:
- Haga clic en el botón **Exportar a CSV**
- Descarga `{form-slug}_responses_{date}.csv`
- Fila de encabezado: Submitted At, User, IP, Status, [Etiquetas de campos]
- Una respuesta por fila
- Abra en Excel, Google Sheets o herramientas de análisis de datos

## Usando formularios en páginas

**Incrustar formularios**:
1. Abra la página en el constructor de páginas
2. Agregue el elemento **Formulario** desde el panel de elementos
3. Seleccione el formulario desde el menú desplegable
4. Personalice el estilo del contenedor del formulario (fondo, relleno, borde)
5. Guarde y publique la página

**El formulario se renderiza con**:
- Título y descripción del formulario (desde ajustes del formulario)
- Todos los campos en orden (formulario de una página) o paso actual (formulario de varios pasos)
- Botón de envío con texto personalizado
- Mensajes de éxito/error después de la presentación

**Herencia de estilo**:
- Los formularios heredan el estilo del tema de la página
- Los botones usan estilos de botón del tema
- Los campos de entrada usan estilos de entrada del tema
- Se puede agregar una clase CSS personalizada a los campos para un estilo específico

## Interfaz del constructor de formularios

**Barra lateral izquierda - Biblioteca de campos**:
- Organizados por categoría (Texto, Selección, Calificación, Avanzado)
- Arrastre el campo al lienzo o haga clic para agregar
- Buscar para encontrar rápidamente tipos de campos

**Canvas principal - Editor de campos**:
- Manija de arrastre (≡) para reordenar campos
- Haga clic en el campo para seleccionar y editar
- Botón de eliminar (×) en cada campo
- Vista previa visual del campo como configurado
- Estado vacío con instrucciones de zona de arrastre

**Barra lateral derecha - Panel de propiedades**:
- **Pestaña de ajustes del formulario** - Información básica, mensajes, protección contra spam
- **Pestaña de ajustes del campo** - Configure el campo seleccionado (etiqueta, validación, etc.)
- **Pestaña de pasos** - Administre pasos (solo para formularios de varios pasos)
- **Pestaña de reglas condicionales** - Agregue lógica de mostrar/ocultar basada en respuestas

**Funciones de la barra de herramientas**:
- **Deshacer/Rehacer** - Historial completo de edición
- **Vista previa** - Pruebe la funcionalidad del formulario
- **Guardar** - Guarda automáticamente cada 3 segundos mientras se edita
- **Traducciones** - Traduzca el texto del formulario a otros idiomas

## Ejemplos comunes de formularios

**Formulario de contacto**:
- Campos: Nombre completo (obligatorio), Correo electrónico (obligatorio), Teléfono, Mensaje (obligatorio)
- Botón de envío: "Enviar mensaje"
- Éxito: "¡Gracias por contactarnos! Nos responderemos dentro de 24 horas." 

**Encuesta de retroalimentación del producto**:
- Paso 1: Calificación con estrellas, escala de Likert de acuerdo
- Paso 2: Puntuación NPS, sugerencias de mejora
- Condicional: Si calificación < 3, requiere retroalimentación de mejora

**Solicitud de empleo**:
- Paso 1: Información personal (nombre, correo electrónico, teléfono)
- Paso 2: Experiencia (carga de currículum, años de experiencia, referencias)
- Paso 3: Disponibilidad (fecha de inicio, expectativas salariales)
- Guardado parcial habilitado (los candidatos pueden reanudar más tarde)

**Suscripción al boletín con preferencias**:
- Correo electrónico (obligatorio)
- Grupo de casillas de verificación: Intereses (Productos, Ofertas, Actualizaciones del blog)
- reCAPTCHA habilitado (prevenir suscripciones falsas)

## Consejos

- **Empiece con una página** - Agregue varios pasos solo si el formulario tiene más de 10 campos
- **Use honeypot primero** - Solo actualice a reCAPTCHA si el spam persiste
- **Pruebe antes de publicar** - Use el modo de vista previa para verificar la validación y el flujo
- **Descargue regularmente** - Descargue el CSV de respuestas semanalmente para respaldos
- **Monitorea el tiempo de finalización** - Si el promedio >5 minutos, el formulario puede ser demasiado largo
- **Use lógica condicional** - Oculte campos irrelevantes para reducir la percepción de longitud del formulario
- **Habilite el guardado parcial para formularios largos** - Reduce el abandono en aplicaciones de varios pasos
- **Traduzca las etiquetas del formulario** - Use el sistema de traducción integrado para sitios multilingües
- **Requiere inicio de sesión para datos sensibles** - Previene el spam anónimo, vincula las presentaciones a cuentas de usuarios
- **Mantenga mensajes de éxito específicos** - "Nos responderemos dentro de 24 horas" es mejor que "¡Gracias!"