---
title: Customer Display Promo Slides
---

Las diapositivas promocionales se muestran en la pantalla orientada al cliente cuando el terminal de POS esté inactivo (sin transacción activa). Cree un carrusel de imágenes que muestre promociones estacionales, lanzamientos de nuevos productos, políticas de tienda, eventos próximos y beneficios del programa de fidelidad. Las diapositivas pueden dirigirse a tiendas o grupos específicos mediante la asignación de alcance: realice promociones de fin de año solo en tiendas de EE. UU., o muestre información de eventos locales solo en ubicaciones relevantes. Las diapositivas activas se alternan automáticamente cada 5-10 segundos, creando una señalización digital atractiva que mantiene informados a los clientes mientras esperan.

Use las diapositivas promocionales para aumentar la conciencia sobre las promociones actuales, educar a los clientes sobre las políticas y fomentar la participación con programas de fidelidad y eventos.

![Lista de diapositivas promocionales](/static/core/admin/img/help/customer-display-promo-slides/promoslide-list.webp)

## Comportamiento de la Pantalla del Cliente

Cuando un terminal de POS esté inactivo (ningún cliente en el mostrador, ninguna transacción en curso), la pantalla orientada al cliente muestra:

**Modo Carrusel**:
- Se recorre todas las diapositivas activas
- Cada diapositiva se muestra durante 5-10 segundos (configurable por terminal)
- Transiciones suaves entre diapositivas
- Se repite continuamente hasta que comience la transacción

**Durante la Transacción**:
- El carrusel se detiene inmediatamente
- La pantalla cambia a la vista de transacción (artículos, total acumulado, prompts de pago)
- El carrusel reanuda cuando se completa la transacción y el terminal vuelve a estar inactivo

**Sin Diapositivas Configuradas**:
- La pantalla muestra un mensaje de "Bienvenido" con la marca de la tienda
- Pantalla estática (sin carrusel)

**Requisitos Técnicos**:
- La pantalla del cliente puede ser un monitor separado o la misma pantalla que el cajero (la aplicación POS admite el modo de imagen en imagen)
- La sincronización se realiza mediante el API BroadcastChannel (comunicación en el mismo dispositivo) o WebSocket (pantallas en dispositivos separados)

## Asignación de Alcance

Al igual que las plantillas de recibos, las diapositivas promocionales admiten la asignación basada en alcance (de mayor prioridad a menor):

| Prioridad | Alcance | Ejemplo | Caso de Uso |
|-----------|--------|--------|------------|
| **1** | Específico de tienda | Diapositivas de la tienda de París | Diapositiva de evento de festival de verano en París |
| **2** | Específico de grupo | Diapositivas de tiendas europeas | Diapositiva de política de privacidad de GDPR solo para la UE |
| **3** | Todas las tiendas | Diapositivas globales | "Envío gratuito en pedidos >$50" (promoción a nivel de empresa) |

**Cómo funciona el alcance**:
- El terminal muestra las diapositivas que coinciden con su alcance de tienda (diapositivas específicas de tienda)
- Más las diapositivas que coinciden con su alcance de grupo (si la tienda está en un grupo)
- Más las diapositivas sin asignación de alcance (diapositivas globales)
- Resultado: La tienda puede mostrar 3-5 diapositivas (combinación de diapositivas con alcance y globales)

**Ejemplo**:
- Diapositiva global: "Nuevo Programa de Fidelidad - Únete Hoy" (sin alcance)
- Diapositiva de grupo: "Venta de Memorial Day - 30% de Descuento" (solo grupo de tiendas de EE. UU.)
- Diapositiva de tienda: "Grand Opening - Tienda Principal de NYC" (solo tienda de NYC)

**El terminal de la tienda de NYC** muestra todas las 3 diapositivas (tienda + grupo + global)
**El terminal de la tienda de Londres** muestra solo la diapositiva global (no está en el grupo de tiendas de EE. UU., no es tienda de NYC)

## Requisitos de Imagen

Las diapositivas promocionales son imágenes a pantalla completa optimizadas para monitores de pantalla del cliente:

**Proporción de aspecto**: 16:9 (pantalla ancha)

**Resolución Recomendada**: 1920×1080 píxeles (Full HD)
- Escala limpiamente a la mayoría de las pantallas modernas
- Equilibrio de tamaño de archivo (calidad vs velocidad de carga)

**Resoluciones Aceptadas**:
- Mínimo: 1280×720 (HD)
- Óptimo: 1920×1080 (Full HD)
- Máximo: 3840×2160 (4K) - no recomendado (tamaño de archivo grande, carga más lenta)

**Formato de Archivo**: JPG, PNG o WebP
- JPG para fotografías
- PNG para gráficos con transparencia (aunque se recomienda fondo sólido)
- WebP para el tamaño de archivo más pequeño

**Tamaño de Archivo**: <500KB por diapositiva
- Archivos más grandes ralentizan la carga del carrusel
- Comprija las imágenes antes de subirlas (use la optimización de la Biblioteca de Medios)

**Recomendaciones de Diseño**:
- Alto contraste para legibilidad a distancia (clientes a 2-6 pies de la pantalla)
- Texto grande (mínimo 48pt para texto corporal, 72pt+ para títulos)
- Fuentes en negrita (fuentes delgadas se desvanecen en algunas pantallas)
- Evite detalles pequeños (no serán visibles desde la perspectiva del cliente)
- Incluya una llamada a la acción (lo que debe hacer el cliente: "Pregunte al cajero por detalles", "Regístrese hoy")

## Crear una Diapositiva Promocional

Navegue a **POS > Diapositivas Promocionales** y haga clic en **+ Añadir Diapositiva Promocional**:

![Formulario de Añadir Diapositiva Promocional](/static/core/admin/img/help/customer-display-promo-slides/promoslide-add-form.webp)

**Imagen** - Subir o seleccionar de la Biblioteca de Medios:
- Haga clic en **Explorar Biblioteca de Medios** para seleccionar una imagen existente
- O suba una nueva imagen que cumpla con los requisitos anteriores
- La vista previa muestra cómo aparecerá la imagen en la pantalla

**Título** (Opcional) - Texto superpuesto en la parte superior de la diapositiva:
- Máximo 60 caracteres (el texto más largo se trunca)
- Aparece en una barra oscura semitransparente en la parte superior de la imagen
- Use para el título de la diapositiva ("Venta de Verano", "Nuevos Llegados")
- Deje en blanco si la imagen incluye texto de título

**Subtítulo** (Opcional) - Texto superpuesto debajo del título:
- Máximo 120 caracteres
- Aparece debajo del título en la misma barra semitransparente
- Use para detalles complementarios ("Hasta 50% de descuento", "Regalo gratis con compra")
- Deje en blanco si la imagen es autónoma

**Está Activo** - Conmutador para habilitar/deshabilitar la diapositiva:
- Solo las diapositivas activas aparecen en el carrusel
- Use para la activación estacional (deshabilite después de que termine la promoción)
- Deshabilitar conserva la diapositiva para su reactivación futura

**Orden de Clasificación** - Controla la posición de la diapositiva en el carrusel:
- Los números más bajos aparecen más temprano en la rotación
- Use múltiplos de 10: 10, 20, 30 (permite insertar diapositivas entre existentes)
- Ejemplo: Venta de fin de año (orden de clasificación 10) aparece antes que programa de fidelidad general (orden de clasificación 20)

**Asignación de Alcance** (Opcional):
- **Almacén** - Seleccione para mostrar solo en una tienda específica
- **Grupo de Tiendas** - Seleccione para mostrar solo en tiendas del grupo
- **Dejar ambos en blanco** - Muestra en todas las tiendas (diapositiva global)

## Orden de Clasificación y Flujo del Carrusel

**Ejemplo de Carrusel** (terminal de tienda de NYC):
- Diapositiva 1 (orden de clasificación 10): "Grand Opening - Tienda Principal de NYC" (específica de tienda)
- Diapositiva 2 (orden de clasificación 15): "Venta de Memorial Day - 30% de Descuento" (grupo de tiendas de EE. UU.)
- Diapositiva 3 (orden de clasificación 20): "Nuevo Programa de Fidelidad - Únete Hoy" (global)
- Diapositiva 4 (orden de clasificación 30): "Síguenos en @yourstore" (global)

El carrusel se repite: 1 → 2 → 3 → 4 → 1 → 2 → ...

**Terminal de tienda de Londres** (no está en el grupo de tiendas de EE. UU., tienda diferente):
- Diapositiva 1 (orden de clasificación 20): "Nuevo Programa de Fidelidad - Únete Hoy" (global)
- Diapositiva 2 (orden de clasificación 30): "Síguenos en @yourstore" (global)

El carrusel se repite: 1 → 2 → 1 → 2 → ...

Use el orden de clasificación para priorizar el contenido más importante primero en la rotación.

## Estrategia de Activación Estacional

**Problema**: Crear/eliminar diapositivas para cada promoción estacional es tedioso.

**Solución**: Cree diapositivas una vez, active/desactive estacionalmente:

1. **Crear Diapositivas para Eventos Mayores**:
   - "Venta de Verano" (Está Activo: No, creada con anticipación)
   - "Regreso a Clases" (Está Activo: No, creada con anticipación)
   - "Viernes Negro" (Está Activo: No, creada con anticipación)
   - "Venta de Fin de Año" (Está Activo: No, creada con anticipación)

2. **Activar cuando sea relevante**:
   - 1 de junio: Establecer "Venta de Verano" → Está Activo: Sí
   - 15 de agosto: Establecer "Venta de Verano" → Está Activo: No, establecer "Regreso a Clases" → Está Activo: Sí
   - 20 de noviembre: Establecer "Viernes Negro" → Está Activo: Sí
   - 1 de diciembre: Establecer "Viernes Negro" → Está Activo: No, establecer "Venta de Fin de Año" → Está Activo: Sí

3. **Desactivar después del evento**:
   - Mantiene la biblioteca de diapositivas organizada
   - Reutilice diapositivas año tras año (actualice la imagen si es necesario, mantenga la configuración)

## Ejemplos de Casos de Uso

**Caso de Uso 1: Promoción Estacional**
- Imagen: Fondo rojo con texto blanco "VENTA DE VERANO - HASTA 60% DE DESCUENTO"
- Título: "Venta de Verano"
- Subtítulo: "50-60% de descuento en artículos seleccionados. Pregunte al cajero por detalles."
- Alcance: Todas las tiendas (global)
- Orden de clasificación: 10 (mayor prioridad durante el verano)
- Activo: Solo en junio-agosto

**Caso de Uso 2: Política de Tienda**
- Imagen: Infografía que muestra los pasos de la política de devolución
- Título: "Devoluciones Fáciles"
- Subtítulo: "30 días con recibo. Sin preguntas."
- Alcance: Todas las tiendas (global)
- Orden de clasificación: 40 (prioridad menor que las promociones)
- Activo: Todo el año

**Caso de Uso 3: Lanzamiento de Nuevo Producto**
- Imagen: Foto principal del nuevo producto
- Título: "NUEVO: Auriculares Inalámbricos Pro"
- Subtítulo: "Disponible ahora en tienda y en línea. $199.99"
- Alcance: Todas las tiendas (global)
- Orden de clasificación: 5 (mayor prioridad durante la semana de lanzamiento)
- Activo: Solo durante la semana de lanzamiento, luego desactivar

**Caso de Uso 4: Evento Local**
- Imagen: Afiche de carrera benéfica local
- Título: "Apoya Local"
- Subtítulo: "Únete a nosotros en el 5K de la Comunidad el 15 de junio!"
- Alcance: Tienda específica (solo tienda de NYC)
- Orden de clasificación: 8 (prioridad para esta tienda)
- Activo: 2 semanas antes del evento

**Caso de Uso 5: Programa de Fidelidad**
- Imagen: Visualización de tarjeta de fidelidad con ejemplos de puntos
- Título: "Gana Recompensas"
- Subtítulo: "Únete a nuestro programa de fidelidad y gana 1 punto por cada $1 gastado"
- Alcance: Todas las tiendas (global)
- Orden de clasificación: 30 (contenido permanente)
- Activo: Todo el año

## Administración de Diapositivas

**Vista de Lista de Diapositivas**:
- Muestra todas las diapositivas con vista previa de imagen, título, alcance, estado
- Filtre por activas/inactivas
- Filtre por alcance (ver todas las diapositivas globales, todas las diapositivas de grupo, etc.)

**Activación/Desactivación en Bloque**:
- Seleccione múltiples diapositivas en la lista
- Use la acción de administración para activar o desactivar todas a la vez
- Útil para transiciones estacionales (desactive todas las diapositivas de verano, active todas las diapositivas de otoño)

**Pruebas de Diapositivas**:
- Después de crear o actualizar una diapositiva, navegue al terminal de POS
- Deje que el terminal se quede inactivo (sin transacción)
- Verifique que la diapositiva aparezca en el carrusel
- Compruebe la calidad de la imagen, la legibilidad del texto superpuesto y el tiempo

**Actualización de Diapositivas Activas**:
- Los cambios surten efecto en la próxima actualización del carrusel (normalmente <30 segundos)
- No es necesario reiniciar los terminales

## Consejos

- **Diseñe para la distancia** - Los clientes ven la pantalla desde 2-6 pies de distancia; use texto grande y alto contraste
- **Mantenga el mensaje simple** - La diapositiva se muestra durante <10 segundos; un mensaje claro por diapositiva
- **Use la desactivación estacional** - Cree una vez, active/apague anualmente en lugar de recrear
- **Priorice con el orden de clasificación** - Las promociones más importantes deben tener el orden de clasificación más bajo (aparecen primero)
- **Pruebe en hardware real** - La calibración de color de la pantalla varía; verifique que las diapositivas se vean bien en sus monitores específicos
- **Límite el número de diapositivas activas** - 3-5 diapositivas activas por tienda es óptimo; 10+ diapositivas significa que cada una aparece con poca frecuencia
- **Incluya CTAs** - Dígale a los clientes qué hacer ("Pregunte al cajero", "Visite el sitio web", "Escanee el código QR en el recibo")
- **Actualice regularmente** - Las promociones obsoletas (ventas expiradas, eventos pasados) reducen la confianza del cliente
- **Use el alcance estratégicamente** - Las promociones regionales (alcance de grupo) y eventos locales (alcance de tienda) se sienten más relevantes que el contenido global constante

Recuerde: preserve all markdown formatting, image paths, code blocks, and technical terms exactly as shown in the preservation rules.