---
title: Personalización de plantillas de recibos
---

Las plantillas de recibos controlan el aspecto y el contenido de los recibos térmicos impresos en tus terminales de punto de venta (POS). Personaliza el texto del encabezado y pie de página, agrega tu logotipo, configura campos de cumplimiento (identificadores fiscales, números de registro comercial) e incluye códigos QR promocionales. Las plantillas admiten el objetivo de alcance: crea una plantilla predeterminada para todas las tiendas, plantillas específicas de grupo para regiones o plantillas específicas de tienda para ubicaciones individuales. El sistema utiliza reglas de prioridad de alcance para determinar qué plantilla se aplica al imprimir un recibo.

Utiliza las plantillas de recibos para mantener la coherencia de la marca, cumplir con los requisitos de cumplimiento regional y mejorar la participación del cliente a través de elementos promocionales.

![Lista de plantillas de recibos](/static/core/admin/img/help/receipt-template-customization/receipt-list.webp)

## Bases de las plantillas de recibos

Las plantillas de recibos definen la estructura y el contenido de los recibos impresos por impresoras térmicas ESC/POS. Cada plantilla especifica:

**Configuración física**:
- Ancho del papel (58mm o 80mm)
- Imagen del logotipo (en monocromo para impresión térmica)
- Tamaño de fuente y espaciado

**Secciones de contenido**:
- Texto del encabezado (nombre de la tienda, dirección, información de contacto)
- Datos dinámicos de la transacción (artículos, precios, totales, métodos de pago)
- Texto del pie de página (política de devolución, mensaje de agradecimiento, redes sociales)
- Campos de cumplimiento (identificadores fiscales, números de registro comercial)
- Código QR promocional con etiqueta

**Objetivo de alcance**:
- Plantilla predeterminada (aplica a todas las tiendas a menos que se anule)
- Plantilla de grupo (aplica a todas las tiendas de un grupo)
- Plantilla de tienda (aplica a una tienda específica/almacén)

## Reglas de prioridad de alcance

Cuando un terminal imprime un recibo, el sistema selecciona una plantilla usando esta jerarquía (prioridad más alta a más baja):

| Prioridad | Alcance | Ejemplo | Caso de uso |
|-----------|--------|--------|-------------|
| **1** | Específico de tienda | Plantilla de la tienda de París | Requisitos de cumplimiento fiscal únicos en Francia |
| **2** | Específico de grupo | Plantilla de tiendas europeas | Mostrar IVA para todas las ubicaciones de la UE |
| **3** | Predeterminado | Plantilla global | Recurso de respaldo para todas las tiendas no configuradas |

**Cómo funciona**:
1. Verificar si la tienda tiene una plantilla dedicada (específica del almacén)
2. Si no, verificar si el grupo de la tienda tiene una plantilla de grupo
3. Si no, usar la plantilla predeterminada

**Ejemplo**:
- Plantilla predeterminada: "Recibo estándar" (sin asignación de alcance)
- Plantilla de grupo: "Recibo de la UE" (asignada al grupo de tiendas europeas) - incluye registro de IVA
- Plantilla de tienda: "Recibo de París" (asignada al almacén de París) - incluye número de SIRET francés

**Resultado**:
- Terminal de la tienda de París: Usa "Recibo de París" (más específico)
- Terminal de la tienda de Berlín (en el grupo de tiendas europeas, sin plantilla de tienda): Usa "Recibo de la UE" (nivel de grupo)
- Terminal de la tienda de Nueva York (sin grupo, sin plantilla de tienda): Usa "Recibo estándar" (respaldo predeterminado)

## Configuración del ancho del papel

Las impresoras térmicas de recibos usan papel de 58mm o 80mm. Elige según tu hardware de impresora:

| Ancho del papel | Caracteres por línea | Mejor para | Uso típico |
|----------------|---------------------|------------|-------------|
| **58mm** | ~32 caracteres | Pequeño tamaño, portátil | Camiones de comida, POS móvil, quioscos |
| **80mm** | ~48 caracteres | Retail estándar | La mayoría de las tiendas minoristas, restaurantes |

**No se pueden mezclar anchos**: Todos los terminales que usan la misma plantilla deben tener impresoras del mismo ancho de papel. Si tienes tipos de impresora mixtos, crea plantillas separadas para cada ancho.

**Límites del tamaño del logotipo**:
- **58mm**: Ancho máximo 384 píxeles (recomendado: 350px)
- **80mm**: Ancho máximo 576 píxeles (recomendado: 550px)

Los logotipos que exceden el ancho máximo se reducen automáticamente, lo que puede reducir la calidad.

## Configuración del logotipo

Los logotipos de recibos deben ser **monocromáticos** (solo negro y blanco) para la compatibilidad con impresoras térmicas:

**Requisitos del logotipo**:
- Formato de archivo: PNG, JPG o WebP
- Modo de color: Monocromo (píxeles negros sobre fondo blanco)
- Dimensiones recomendadas:
  - Papel de 58mm: 350px de ancho × 100-150px de alto
  - Papel de 80mm: 550px de ancho × 150-200px de alto
- Tamaño del archivo: <100KB (las impresoras térmicas tienen memoria limitada)

**Creación de logotipos monocromáticos**:
1. Comienza con tu logotipo regular (en color o escala de grises)
2. Usa un editor de imágenes para convertirlo en puro negro y blanco (sin grises)
3. Aumenta el contraste para asegurar que los elementos negros sean sólidos
4. Exporta como PNG con fondo transparente o blanco

**Posición del logotipo**:
- Siempre centrado horizontalmente
- Se imprime en la parte superior del recibo (por encima del texto del encabezado)
- Seguido de un espaciado automático (evita el acercamiento con el contenido)

**Seleccionar logotipo**:
- Haz clic en **Explorar biblioteca de medios** en el formulario de la plantilla
- Selecciona el activo del logotipo monocromo
- La vista previa muestra cómo aparecerá el logotipo en el recibo

**Sin logotipo**: Deja el campo de logotipo en blanco si prefieres la marca solo con texto (el texto del encabezado puede incluir el nombre de la tienda).

## Texto del encabezado

El texto del encabezado aparece inmediatamente después del logotipo (o en la parte superior si no hay logotipo). Contenido típico:

**Nombre de la tienda y dirección**:
```
Nombre de tu tienda
123 Main Street
City, State 12345
Teléfono: (555) 123-4567
```

**Horario de atención**:
```
Lunes-Viernes: 9am-9pm
Sábado-Domingo: 10am-6pm
```

**Lema o eslogan**:
```
Productos de calidad, servicio excepcional
```

**Formato**:
- Usa saltos de línea para separar la información
- Alineación centrada automáticamente
- Mantén las líneas bajo el límite de caracteres para el ancho del papel (32 caracteres para 58mm, 48 para 80mm)

**Variables disponibles** (opcional):
- `{store_name}` - Reemplazado por el nombre del almacén
- `{order_date}` - Reemplazado por la fecha de la transacción
- `{order_number}` - Reemplazado por el número de pedido

La mayoría de los comerciantes usan texto estático en lugar de variables para la consistencia del encabezado.

## Texto del pie de página

El texto del pie de página aparece después de los detalles de la transacción (artículos, totales, pago). Contenido típico:

**Política de devolución**:
```
Devoluciones dentro de los 30 días con recibo
Crédito de tienda o intercambio solo
```

**Mensaje de agradecimiento**:
```
¡Gracias por comprar con nosotros!
Síguenos en @yourstore
```

**Servicio al cliente**:
```
¿Tienes preguntas? Llama al (555) 123-4567
o envía un correo electrónico a support@yourstore.com
```

**Consejos de formato**:
- Mantén la información más importante primero (política de devolución, contacto)
- Usa saltos de línea para mejorar la legibilidad
- Considera agregar una línea de separación (`---`) entre secciones

## Campos de cumplimiento

Muchas jurisdicciones requieren información específica en los recibos:

**Etiqueta de identificador fiscal** - Etiqueta personalizable para el número de identificación fiscal:
- EE.UU.: "Tax ID" o "EIN"
- UE: "VAT Number" o "VAT Reg No"
- Canadá: "GST/HST Number"
- Australia: "ABN"

**Valor del identificador fiscal** - El número de identificación real:
- Ingresado una vez en la plantilla, aparece en todos los recibos
- Ejemplo: "VAT Number: GB123456789"

**Etiqueta de registro comercial** - Etiqueta personalizable para el registro comercial:
- Francia: "SIRET"
- Alemania: "Handelsregister"
- Reino Unido: "Company Registration Number"

**Valor del registro comercial** - El número real de registro:
- Ejemplo: "SIRET: 123 456 789 00010"

**Mostrar "Powered by Spwig"** - Conmutador para mostrar o ocultar la marca "Powered by Spwig":
- Habilitado por defecto (apoya el desarrollo de la plataforma)
- Désactivelo para operaciones de marca blanca

**Ejemplos de cumplimiento por región**:

**Unión Europea**:
- Etiqueta de identificador fiscal: "VAT Number"
- Valor del identificador fiscal: "GB123456789"
- Muestra el número de registro de la empresa si lo requiere el país

**Estados Unidos**:
- Generalmente no hay requisito de identificador fiscal en recibos (varía por estado)
- Puede incluir EIN para transacciones B2B

**Francia (específica)**:
- SIRET obligatorio en todos los recibos
- Etiqueta de registro comercial: "SIRET"
- Valor del registro comercial: "123 456 789 00010"

**Australia**:
- Se recomienda ABN (número de empresa australiana) para empresas registradas en GST
- Etiqueta de identificador fiscal: "ABN"

Verifica los requisitos de los recibos de tu jurisdicción local antes de lanzar.

## Promociones con códigos QR

Incluye un código QR en la parte inferior de los recibos para impulsar la participación del cliente:

**URL del código QR** - Destino al escanear:
- Revisión: `https://yourstore.com/reviews/leave-review`
- Programa de lealtad: `https://yourstore.com/loyalty/join`
- Descuento en la próxima compra: `https://yourstore.com/discount/THANKYOU`
- Redes sociales: `https://instagram.com/yourstore`
- Página principal del sitio web: `https://yourstore.com`

**Etiqueta del código QR** - Texto mostrado encima del código QR:
- "Escanea para dejar una reseña y obtener un 10% de descuento en tu próxima compra"
- "Únete a nuestro programa de lealtad - escanea aquí"
- "Síguenos en Instagram - escanea para conectarte"
- "Califica tu experiencia"

**Mejores prácticas para códigos QR**:
- Usa URLs cortas (URLs largas generan códigos densos y difíciles de escanear)
- Prueba el código QR con múltiples cámaras de teléfono antes del despliegue
- Incluye una propuesta de valor clara en la etiqueta (qué obtiene el cliente al escanear)
- Rastrea los escaneos del código QR para medir su efectividad (usa URL con parámetro de seguimiento)

**Códigos QR dinámicos** (Avanzado):
- Usa un servicio de redirección de QR (bit.ly, tinyurl) para crear una URL corta
- Dirige la redirección a diferentes destinos estacionalmente sin reimprimir recibos
- Ejemplo: `https://bit.ly/yourstoreqr` → redirige a la promoción actual

## Crear plantillas para diferentes alcances

**Plantilla predeterminada** (punto de partida recomendado):
1. Navega a **POS > Plantillas de recibos**
2. Haz clic en **+ Añadir plantilla de recibo**
3. Deja los campos **Almacén** y **Grupo de tiendas** en blanco (esto la hace la predeterminada)
4. Configura el ancho del papel que coincida con el tipo de impresora más común
5. Añade logotipo, encabezado, pie de página
6. Configura campos de cumplimiento para tu mercado principal
7. Guarda

Esta plantilla se aplica a todas las tiendas a menos que se anule.

**Plantilla de grupo** (para variaciones regionales):
1. Crea una nueva plantilla
2. Selecciona **Grupo de tiendas** (por ejemplo, "Tiendas europeas")
3. Deja **Almacén** en blanco
4. Ajusta los campos de cumplimiento para la región (por ejemplo, formato de IVA)
5. Ajusta el texto del encabezado (por ejemplo, dirección regional)
6. Guarda

Esta plantilla se aplica a todas las tiendas del grupo.

**Plantilla de tienda** (para necesidades específicas de ubicación):
1. Crea una nueva plantilla
2. Selecciona **Almacén** (por ejemplo, "Tienda de París")
3. Ajusta todos los campos para esta ubicación específica
4. Guarda

Esta plantilla se aplica solo a esta tienda.

**Pruebas de plantillas**:
- Procesa una transacción de prueba en el terminal
- Imprime el recibo
- Verifica la claridad del logotipo, alineación del texto, campos de cumplimiento, escaneabilidad del código QR
- Ajusta la plantilla y vuelve a probar si es necesario

## Diseños comunes de recibos

**Recibo mínimo** (camiones de comida, puestos de venta temporal):
- Sin logotipo (ahorro de espacio)
- Encabezado: solo nombre de la tienda y teléfono
- Pie de página: mensaje de agradecimiento
- Sin código QR

**Recibo de retail estándar**:
- Logotipo (marca en monocromo)
- Encabezado: nombre completo de la tienda, dirección, horario
- Cumplimiento: identificador fiscal
- Pie de página: política de devolución, mensaje de agradecimiento
- Código QR: solicitud de reseña

**Recibo premium de retail**:
- Logotipo (marca completa con palabra logotipo)
- Encabezado: lema, dirección, contacto
- Cumplimiento: identificador fiscal, registro comercial
- Pie de página: política de devolución, servicio al cliente, redes sociales
- Código QR: inscripción en programa de lealtad

**Cadena con múltiples ubicaciones**:
- Plantilla predeterminada: marca corporativa, políticas estándar
- Plantillas de grupo: cumplimiento regional (IVA para UE, GST para Canadá)
- Plantillas de tienda: dirección y teléfono específicos de la ubicación

## Administrar múltiples plantillas

**Convenio de nombres de plantillas**:
- Usa el alcance en el nombre: "Recibo predeterminado", "Recibo del grupo de la UE", "Recibo de la tienda de París"
- Ayuda a identificar qué plantilla se aplica en qué lugar al revisar la lista

**Cambios en plantillas**:
- Los cambios se aplican inmediatamente a los recibos futuros
- Los recibos anteriores (ya impresos) no se ven afectados
- Prueba los cambios en un terminal de baja afluencia antes de desplegar a todas las tiendas

**Duplicación de plantillas**:
- Cuando crees una nueva plantilla similar a una existente, duplica la plantilla existente y modifica
- Evita empezar desde cero

**Eliminar plantillas**:
- No puedes eliminar la plantilla predeterminada mientras existan terminales (debe haber una de respaldo)
- Puedes eliminar plantillas de grupo/tienda (los terminales se retroceden al siguiente nivel en la jerarquía)
- Confirma que no haya terminales activamente usando la plantilla antes de eliminarla

## Consejos

- **Comienza con 80mm si no estás seguro** - El ancho de papel estándar funciona para la mayoría del retail; 58mm es especializado
- **Prueba el logotipo en la impresora real** - Lo que parece bueno en pantalla puede imprimirse mal; prueba temprano
- **Mantén los campos de cumplimiento actualizados** - Los registros fiscales vencidos en los recibos crean problemas legales
- **Los códigos QR con propuesta de valor escanean mejor** - "Escanea para un 10% de descuento" supera a "Escanea aquí" por 10 veces
- **Revisa los límites de caracteres** - El ajuste de texto arruina el formato; cuenta los caracteres por línea antes de desplegar
- **Una plantilla por ancho de papel** - No asigne una plantilla de 80mm a un terminal con impresora de 58mm (el logotipo no cabrá)
- **Imprime recibos de prueba mensualmente** - Las impresoras degradan con el tiempo; verifica que la calidad siga siendo aceptable
- **Usa variables con moderación** - El texto estático es más confiable que variables dinámicas (menos puntos de falla)
- **Haz copia de seguridad de la configuración de la plantilla** - Captura o exporta la configuración de la plantilla antes de cambios importantes (facilita el retorno)
- **El cumplimiento regional varía** - Investiga los requisitos de los recibos locales antes del despliegue; las multas por no cumplimiento pueden ser severas

Recuerda: Preserva todo el formato markdown, rutas de imágenes, bloques de código y términos técnicos exactamente como se muestran en las reglas de preservación.