---
title: Personalización del Portal de Afiliados
---

El portal de afiliados de Spwig es la página de aterrizaje orientada al público donde los posibles afiliados aprenden sobre su programa y se registran. Personalizar este portal le permite alinear el mensaje, la marca y la llamada a la acción con la posición única de su tienda. Un portal bien diseñado atrae a afiliados de alta calidad y convierte a los visitantes en socios activos.

## ¿Qué es el Portal de Afiliados?

El portal de afiliados está accesible en `/affiliate/` en el dominio de su tienda. Sirve como:

- **Página de descubrimiento** — Donde los posibles afiliados aprenden sobre su estructura de comisiones, beneficios y requisitos
- **Punto de entrada de registro** — Formulario de registro para nuevos afiliados (registro de invitado o basado en cuenta)
- **Puerta de entrada de inicio de sesión** — Los afiliados existentes pueden iniciar sesión para acceder a su panel
- **Mostrador de marca** — Refleja la identidad de su tienda y la propuesta de valor del programa de afiliados

El portal es completamente personalizable a través de la configuración de afiliados en el administrador, incluyendo el mensaje del héroe, resaltos de características, flujos paso a paso y opciones de registro.

![Página de aterrizaje del portal de afiliados](/static/core/admin/img/help/affiliate-portal-customization/portal-landing.webp)

## Acceso a la configuración

Navegue a **Marketing > Programa de Afiliados > Configuración del Portal** para personalizar el portal.

El modelo de configuración de afiliados es un **singleton** — tiene exactamente un registro de configuración para toda su tienda. Todos los campos son **traducibles** usando el sistema de traducción de Spwig, por lo que puede personalizar el mensaje para cada idioma que su tienda admita.

## Sección del héroe

La sección del héroe es la primera cosa que ven los posibles afiliados. Incluye:

- **Título** — Encabezado principal (ej. "Únete a nuestro programa de afiliados")
- **Subtítulo** — Texto de apoyo que explica el valor del programa (ej. "Gane comisiones promocionando productos premium a su audiencia")
- **Estadísticas** — Métricas que se muestran automáticamente:
  - Total de programas activos
  - Total de afiliados activos
  - Tasa promedio de comisión (calculada en todos los programas activos)
- **Botones de CTA** — Generados automáticamente:
  - **Iniciar sesión** — Para afiliados existentes
  - **Convertirse en afiliado** — Inicia el flujo de registro

### Personalización del mensaje del héroe

| Campo | Valor de ejemplo | Propósito |
|-------|------------------|---------|
| **Título del héroe** | "Únete a Nosotros y Gana" | Atrape la atención con un encabezado enfocado en beneficios |
| **Subtítulo del héroe** | "Únete a 500+ afiliados que ganan comisiones competitivas en cada venta que refieras" | Proporcione prueba social y aclarar la oferta |

Las estadísticas se calculan **automáticamente** y se actualizan en tiempo real según sus programas y afiliados activos. No puede editar manualmente estos valores.

## Sección de características

La sección de características destaca **6 tarjetas de beneficio personalizables** que explican por qué los afiliados deben unirse a su programa. Cada tarjeta de característica contiene:

- **Icono** — Clase de icono de FontAwesome (ej. `fa-dollar-sign`, `fa-chart-line`, `fa-headset`)
- **Título** — Encabezado del beneficio (ej. "Comisiones competitivas")
- **Descripción** — Explicación de 1-2 oraciones (ej. "Gane hasta el 15% en cada venta que refieras")

### Características predeterminadas

Spwig proporciona características predeterminadas cuando instala por primera vez la aplicación de afiliados:

| Icono | Título | Descripción |
|------|-------|-------------|
| `fa-dollar-sign` | Comisiones competitivas | Gane comisiones generosas en cada venta que refieras |
| `fa-link` | Enlaces de seguimiento fáciles | Obten enlaces de seguimiento únicos que funcionan en cualquier lugar |
| `fa-chart-line` | Análisis en tiempo real | Rastrea clics, conversiones y ganancias en tu panel |
| `fa-calendar-check` | Pagos confiables | Recibe tus pagos a tiempo mediante PayPal o transferencia bancaria |
| `fa-headset` | Soporte dedicado | Nuestro equipo está aquí para ayudarte a tener éxito |
| `fa-gift` | Materiales de marketing | Accede a banners, imágenes y contenido promocional |

### Personalización de características

Las características se almacenan como un **array JSON** en la base de datos. Edite directamente en el formulario del administrador:

```json
[
  {
    "icon": "fa-percent",
    "title": "Hasta el 20% de comisión",
    "description": "Gane comisiones líderes en la industria en ventas de productos premium"
  },
  {
    "icon": "fa-rocket",
    "title": "Aprobación rápida",
    "description": "Obtenga aprobación en 24 horas y comience a promocionar inmediatamente"
  },
  {
    "icon": "fa-mobile-alt",
    "title": "Panel móvil",
    "description": "Administre sus enlaces y rastree sus ganancias desde cualquier dispositivo"
  }
]
```

**Referencia del icono:** Use cualquier clase de icono gratuita de FontAwesome 5. Explore iconos en [fontawesome.com/icons](https://fontawesome.com/icons) y use el nombre de la clase (ej. `fa-trophy`, `fa-users`, `fa-star`).

## Sección "Cómo funciona"

La sección "Cómo funciona" muestra un **flujo visual de 4 pasos** que explica el viaje del afiliado. Cada paso incluye:

- **Título** — Nombre del paso (ej. "Regístrese")
- **Descripción** — Explicación de 1-2 oraciones de lo que ocurre

### Pasos predeterminados

| Paso | Título | Descripción |
|------|-------|-------------|
| 1 | Regístrese | Cree su cuenta de afiliado gratuita en minutos |
| 2 | Obtenga sus enlaces | Genere enlaces de seguimiento únicos para cualquier producto o página |
| 3 | Promocione | Comparta sus enlaces con su audiencia a través de contenido, redes sociales o correo electrónico |
| 4 | Gane comisiones | Reciba pagos cuando los clientes compren usando sus enlaces de referencia |

### Personalización de pasos

Los pasos se almacenan como un **array JSON**. Puede editarlo en el administrador:

```json
[
  {
    "title": "Solicite unirse",
    "description": "Envíe su solicitud y háganos saber sobre su plataforma"
  },
  {
    "title": "Obtenga aprobación",
    "description": "Nuestro equipo revisará su solicitud dentro de 24 horas"
  },
  {
    "title": "Cree enlaces",
    "description": "Acceda a su panel y genere enlaces de seguimiento de inmediato"
  },
  {
    "title": "Comience a ganar",
    "description": "Gane comisiones en cada venta que refiera — pagado mensualmente mediante PayPal"
  }
]
```

El flujo visual numera automáticamente cada paso (1, 2, 3, 4) en la página de aterrizaje.

## Sección de CTA

La última sección antes del formulario de registro es la **sección de llamada a la acción (CTA)**. Proporciona un último empujón para fomentar el registro.

| Campo | Valor de ejemplo | Propósito |
|-------|------------------|---------|
| **Título de CTA** | "¿Listo para comenzar a ganar?" | Pregunta directa crea urgencia |
| **Descripción de CTA** | "Únete a nuestro programa de afiliados hoy y comienza a ganar comisiones en productos que ya amas y recomiendas." | Refuerza beneficios y elimina fricción |

La sección de CTA muestra automáticamente el botón **Convertirse en afiliado** debajo del texto.

## Configuración de registro

Controla cómo los nuevos afiliados se registran y qué información proporcionan.

### Formulario de registro personalizado

**Campo:** `custom_form` (Clave foránea a un formulario de FormBuilder)

Si tiene un formulario de registro personalizado construido con el Form Builder de Spwig, selecciónelo aquí. Esto le permite recopilar información adicional durante el registro (ej. URL del sitio web, tamaño de audiencia, canales de promoción).

**Dejar en blanco** para usar el formulario de registro de afiliados predeterminado (correo electrónico, contraseña, detalles de pago).

### Permitir registro de invitado

**Campo:** `allow_guest_registration` (Booleano)

- **Marcado** — Los visitantes pueden aplicar sin crear una cuenta de Spwig primero
- **No marcado** — Los visitantes deben iniciar sesión o crear una cuenta de cliente antes de aplicar

**Recomendación:** Active el registro de invitado para reducir la fricción. Siempre puede requerir aprobación para evaluar a los afiliados antes de activarlos.

### Requerir aprobación

**Campo:** `require_approval` (Booleano)

- **Marcado** — Los nuevos afiliados deben esperar la aprobación manual antes de acceder a su panel
- **No marcado** — Los nuevos afiliados se aprueban automáticamente y pueden crear enlaces inmediatamente

**Recomendación:** Active la aprobación manual si desea evaluar a los afiliados para el ajuste de marca, prevención de fraude o programas exclusivos.

### URL de términos y condiciones

**Campo:** `terms_url` (URL)

Enlace opcional a los términos y condiciones de su programa de afiliados. Si se proporciona, el formulario de registro muestra una casilla de verificación que requiere que los afiliados acepten sus términos antes de registrarse.

**Ejemplo:** `/pages/affiliate-terms/`

### Mensaje de bienvenida

**Campo:** `welcome_message` (Texto)

Mensaje mostrado a los afiliados inmediatamente después del registro exitoso. Use esto para:

- Agradecerles por unirse
- Explicar los pasos siguientes (ej. "Revisaremos su solicitud dentro de 24 horas")
- Enlazar a recursos para comenzar

**Ejemplo:"
```
Bienvenido a nuestro programa de afiliados. Hemos recibido su solicitud y la revisaremos dentro de 24 horas. Revise su correo electrónico para confirmación de aprobación y instrucciones de inicio de sesión.
```

## Soporte multilingüe

Todos los campos de texto en la configuración de afiliados son **traducibles** usando el widget de traducción de Spwig:

- Título del héroe
- Subtítulo del héroe
- Características (JSON traducido por idioma)
- Pasos de "Cómo funciona" (JSON traducido por idioma)
- Título de CTA
- Descripción de CTA
- Mensaje de bienvenida

### Cómo funciona la traducción

Cuando edite un campo traducible, verá un widget de traducción que le permite proporcionar contenido para cada idioma habilitado. Para los campos JSON (características, pasos), proporcione objetos JSON separados por idioma:

**Inglés:"
```json
[
  {"icon": "fa-dollar-sign", "title": "Comisiones competitivas", "description": "Gane hasta el 15% en cada venta"}
]
```

**Español:"
```json
[
  {"icon": "fa-dollar-sign", "title": "Comisiones competitivas", "description": "Gane hasta el 15% en cada venta"}
]
```

El portal muestra automáticamente la versión del idioma correcto según la preferencia del idioma del visitante.

## Previsualice sus cambios

Después de personalizar la configuración del portal:

1. **Guarde** sus cambios en el administrador
2. Visite `/affiliate/` en el frontend de su tienda (abierta en una nueva pestaña)
3. **Pruebe el flujo de registro** haciendo clic en "Convertirse en afiliado"
4. **Verifique la coherencia de la marca** — ¿el portal coincide con el diseño y el mensaje de su tienda?

Puede hacer cambios iterativos y recargar la página para ver las actualizaciones inmediatamente.

## Ejemplos de personalización

### Escenario 1: Tienda de moda en línea

**Objetivo:** Recrutar influencers y bloggers de moda.

| Configuración | Valor |
|---------------|-------|
| Título del héroe | "Promociona los estilos que amas y gana" |
| Subtítulo del héroe | "Únete a 1,200+ influencers que ganan 12% de comisión en cada venta" |
| Característica 1 | Icono: `fa-tshirt`, Título: "Colecciones de moda curadas", Descripción: "Promociona ropa premium y accesorios" |
| Característica 2 | Icono: `fa-percentage`, Título: "12% de comisión", Descripción: "Tarifas líderes en la industria en todos los productos" |
| Característica 3 | Icono: `fa-camera`, Título: "Contenido exclusivo", Descripción: "Accede a fotos, videos y activos de campaña del producto" |
| Permitir registro de invitado | Marcado |
| Requerir aprobación | Marcado (revisión manual para ajuste de marca) |

### Escenario 2: Programa de socios B2B de SaaS

**Objetivo:** Recrutar consultores y agencias para referencias de software empresarial.

| Configuración | Valor |
|---------------|-------|
| Título del héroe | "Únete a nosotros para crecer tus ingresos" |
| Subtítulo del héroe | "Gane $500 por referencia empresarial a través de nuestro programa de socios B2B" |
| Característica 1 | Icono: `fa-handshake`, Título: "$500 por referencia", Descripción: "Comisión fija para leads empresariales calificados" |
| Característica 2 | Icono: `fa-clock`, Título: "Ventana de atribución de 180 días", Descripción: "Ventana de atribución prolongada para ciclos de ventas complejos" |
| Característica 3 | Icono: `fa-user-tie`, Título: "Gestor de socios dedicado", Descripción: "Soporte de lujo para tus clientes" |
| Permitir registro de invitado | No marcado (B2B requiere cuenta) |
| Requerir aprobación | Marcado (programa de invitación) |
| URL de términos | `/pages/partner-program-terms/` |

## Consejos

- Personalice su **título del héroe** para enfocarse en beneficios, no en características — "Gane mientras duermes" es más atractivo que "Registro en el programa de afiliados"
- Use **prueba social** en el subtítulo (ej. "Únete a 500+ afiliados") para construir confianza y credibilidad
- Elija **iconos de FontAwesome** que refuercen visualmente cada beneficio — el icono debe comunicar instantáneamente el valor
- Mantenga las descripciones de características a **1-2 oraciones** — el portal está orientado a la conversión, no a una explicación exhaustiva
- Pruebe usted mismo el **flujo de registro** antes de promocionar el portal — detecte puntos de fricción como campos de formulario confusos o enlaces rotos
- Active el **registro de invitado** para reducir la fricción del registro, luego use **requerir aprobación** para evaluar a los afiliados después de que hayan enviado su solicitud
- Use el **mensaje de bienvenida** para establecer expectativas (tiempo de aprobación, pasos siguientes, contacto de soporte) y reducir las consultas de soporte
- Actualice el portal **estacionalmente** para alinearse con campañas — destaque promociones de comisión especiales o lanzamientos de productos

Recuerde: preserve all markdown formatting, image paths, code blocks, and technical terms exactly as shown in the preservation rules.