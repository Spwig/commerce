---
title: Servicio de traducción
---

El servicio de traducción proporciona traducciones impulsadas por IA para las descripciones de productos, contenido de páginas, entradas de blog, campos de SEO y otro contenido del comerciante en su tienda. Las traducciones se ejecutan localmente en su servidor o a través de proveedores externos, por lo que su contenido permanece privado y las traducciones ocurren en segundos.

![Gestión de idiomas](/static/core/admin/img/help/translation-service/language-management.webp)

## Cómo funciona

1. Usted **activa idiomas** para su tienda (por ejemplo, inglés, alemán, japonés)
2. Cuando cree o edite contenido (productos, páginas, entradas de blog), escribe en su idioma predeterminado
3. Haga clic en **Traducir** en cualquier campo traducible para generar traducciones de IA en sus idiomas activos
4. Las traducciones se almacenan junto con el contenido original y se sirven automáticamente según el idioma del visitante

## Gestión de idiomas

Navegue a **Configuración > Idiomas** para gestionar los idiomas de su tienda.

### Panel de idiomas

El panel muestra:
- **Total de idiomas** — Todos los idiomas disponibles en el sistema (100+)
- **Idiomas activos** — Idiomas actualmente habilitados para su tienda
- **Cobertura del modelo** — Cuántos idiomas soporta el modelo de traducción instalado

### Activar idiomas

1. Encuentre el idioma en la columna **Idiomas disponibles**
2. Haga clic en el idioma para moverlo a la columna **Idiomas activos**
3. El idioma está disponible inmediatamente para traducciones y aparece en el selector de idiomas de su tienda

### Idioma predeterminado

Un idioma se marca como **predeterminado**. Esto es:
- El idioma en el que escribe el contenido
- El respaldo cuando no existe una traducción
- El idioma mostrado cuando los visitantes no han seleccionado una preferencia

## Modelos de traducción

Spwig incluye un motor de traducción de IA local que se ejecuta completamente en su servidor — no se envía ningún dato a servicios externos.

### Modelos disponibles

| Modelo | Idiomas | Velocidad | Calidad |
|-------|-----------|-------|---------|
| **M2M100-418M** | 100 | Rápido | Buena para pares de idiomas comunes |
| **M2M100-1.2B** | 100 | Moderada | Mejor calidad, uso más alto de recursos |
| **NLLB-200** | 200+ | Moderada | Mejor cobertura, incluyendo idiomas poco comunes |

### Selección de modelos

La página de gestión de idiomas muestra qué modelo está instalado y su cobertura de idioma. El modelo se ejecuta como un servicio local usando CTranslate2 para inferencia eficiente.

## Proveedores externos

Para tiendas que prefieren traducción basada en la nube o necesitan una calidad específica de idioma, Spwig admite proveedores de traducción externos.

| Proveedor | Descripción |
|----------|-------------|
| **DeepL** | Calidad premium de traducción para idiomas europeos y asiáticos |
| **Google Translate** | Amplia cobertura de idiomas con traducción de máquina neuronal |
| **Azure Translator** | Servicio de traducción neuronal de Microsoft |
| **AWS Translate** | Traducción de máquina de Amazon con soporte para terminología personalizada |

### Conectar un proveedor

1. Navegue a **Configuración > Proveedores de traducción**
2. Seleccione el proveedor y escriba su clave de API
3. Establezca el proveedor como el motor de traducción preferido
4. Las traducciones usarán el proveedor externo en lugar del modelo local

Puede usar proveedores externos junto con el modelo local — por ejemplo, use DeepL para idiomas europeos y el modelo local para todo lo demás.

## Traducir contenido

### Traducción a nivel de campo

Los campos traducibles (nombres de productos, descripciones, títulos de SEO, etc.) muestran un **botón de traducción** junto al campo. Haga clic en él para:

1. **Traducir a todos los idiomas activos** — Genera traducciones para cada idioma activo a la vez
2. **Traducir a un idioma específico** — Elija idiomas individuales para traducir

Las traducciones aparecen en las pestañas de idioma del editor. Puede revisar y editar manualmente cualquier traducción generada por máquina.

### Trabajos de traducción masiva

Para grandes cantidades de contenido, use **trabajos de traducción**:

1. Navegue a **Configuración > Trabajos de traducción**
2. Cree un nuevo trabajo seleccionando:
   - **Tipo de contenido** — Productos, páginas, entradas de blog, categorías, etc.
   - **Idioma de origen** — El idioma del que se traducirá
   - **Idiomas de destino** — Uno o más idiomas a los que se traducirá
   - **Ámbito** — Todo el contenido, o solo los campos sin traducir
3. Envíe el trabajo — se ejecuta en segundo plano a través de una cola de tareas
4. Supervise el progreso en la lista de trabajos (en cola → en proceso → completado)

Los trabajos masivos son útiles cuando activa un nuevo idioma y quiere traducir su catálogo completo de una vez.

## Gestión de traducciones

### Revisar traducciones

Cada campo traducido rastrea:
- **Estado de traducción** — Si el campo ha sido traducido por máquina, editado manualmente o está faltando
- **Estado de bloqueo** — Las traducciones bloqueadas no serán sobrescritas por futuras traducciones de máquina
- **Última traducción** — Cuando se generó o editó la traducción por última vez

### Bloquear traducciones

Si edita manualmente una traducción de máquina para mejorarla, **bloquee** el campo para evitar que se sobrescriba la próxima vez que se ejecute una traducción masiva. Los campos bloqueados se omiten durante la traducción automática.

### Cobertura de traducción

El rastreador de cobertura muestra qué porcentaje de su contenido está traducido para cada idioma. Navegue a **Configuración > Idiomas** para ver:
- Porcentajes de finalización por idioma
- Qué tipos de contenido tienen lagunas
- Campos que aún necesitan traducción

## Sobrescrituras de traducción de la interfaz de usuario

Más allá del contenido de productos y páginas, puede personalizar las traducciones de **cadenas de la interfaz de usuario del frontend** — botones, etiquetas, mensajes y otro texto de la interfaz mostrado a los visitantes.

Navegue a **Configuración > Sobrescrituras de la interfaz de usuario** para:
1. Buscar una cadena específica (por ejemplo, "Añadir al carrito")
2. Ingrese su traducción preferida para cada idioma
3. Guardar — la sobrescritura se aplica inmediatamente

Hay aproximadamente 300 cadenas de frontend disponibles para personalización. Las sobrescrituras tienen prioridad sobre las traducciones predeterminadas.

## Consejos

- Comience activando solo los idiomas que sus clientes realmente usan — siempre puede agregar más más tarde.
- Use el **modelo de IA local** para traducciones de uso diario — es rápido, privado y no tiene costo por traducción.
- Considere **DeepL** si necesita la máxima calidad para idiomas europeos clave — produce consistentemente traducciones más naturales que los modelos generales.
- Siempre **revisar las traducciones generadas por máquina** para nombres de productos, términos de marca y copia de marketing — la IA maneja bien el contenido técnico pero puede pasar por alto matices en el texto creativo.
- **Bloquee** cualquier traducción que haya refinado manualmente para protegerla de ser sobrescrita durante ejecuciones de traducción masiva.
- Use **trabajos de traducción masiva** al activar un nuevo idioma para traducir su catálogo completo en una sola pasada en lugar de traducir productos uno por uno.
- Personalice **sobrescrituras de la interfaz de usuario** para coincidir con la voz de su marca — por ejemplo, cambie "Añadir al carrito" a "Comprar ahora" si eso se ajusta mejor a su tienda.