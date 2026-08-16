---
title: Compra con IA
---

La compra con IA permite a los asistentes de compras con IA encontrar sus productos y, cuando lo permita, comprar en su tienda en nombre del cliente. Está **desactivada por defecto** - activarla es una elección deliberada, y hasta que lo haga, su tienda no expone nada a estos asistentes.

## Activarla

Abra **Configuración → Compra con IA** y active **Compra agente habilitada**. A partir de ese momento, los asistentes que respalden el Protocolo Universal de Comercio pueden descubrir su tienda y leer su catálogo. Nada de su tienda normal cambia.

## El panel de preparación

La parte superior de la página de Compra con IA responde a una pregunta en una sola oración: **¿pueden los asistentes de IA comprar en su tienda ahora mismo?**

- **"Los asistentes de IA pueden comprar en su tienda"** - todo lo necesario para una compra está en su lugar.
- **"Los asistentes de IA pueden navegar por su tienda, pero aún no pueden comprar"** - su tienda es descubrible, pero algo falta antes de que se pueda completar una compra (generalmente un proveedor de pagos conectado).
- **"La parada de emergencia está activa"** o **"Compra agente está desactivada"** - nada se sirve a los asistentes.

Debajo del veredicto verá un breve checklist - proveedor de pagos conectado, cotización de envío posible, productos visibles para asistentes - con una pista al lado de cualquier cosa que aún requiera atención. Los contadores muestran cuántos productos pueden vender los asistentes, cuántos ha ocultado de ellos, cuántos asistentes han visitado y cuántos ha bloqueado.

El checklist refleja su configuración **en vivo**: conéctese a un proveedor de pagos o agregue un método de envío y el veredicto se actualizará la próxima vez que abra la página.

## La parada de emergencia

La **parada de emergencia** es un interruptor separado del principal. úsela para detener inmediatamente toda actividad de asistente - por ejemplo, si algo parece mal - sin deshacer su configuración. Limpie el interruptor para reanudar. Piense en el interruptor principal como "¿esta característica está configurada?" y la parada de emergencia como "deténgase inmediatamente".

## Lo que pueden hacer los asistentes

Dos niveles de acceso, controlados por separado:

- **Lectura** (descubrimiento y navegación) es de menor riesgo. Un asistente puede encontrar su tienda y leer los detalles del producto.
- **Cierre** (comprar realmente) es de mayor riesgo y permanece cerrado para asistentes no verificados, a menos que lo permita.

Una tienda puede ser descubrible sin ser comprable - una forma útil de comenzar.

## Ocultar productos específicos

Cada producto tiene un ajuste de **Visible a agentes de compras con IA** (activado por defecto). Ábralo para mantener un producto específico fuera de los asistentes mientras permanece en su tienda - útil para artículos que prefiere vender solo a través de su sitio web.

## Gestionar asistentes individuales

Cuando un asistente compra por primera vez - o intenta hacerlo - Spwig lo registra bajo **Compra con IA → Identidades de agentes**. Cada entrada muestra el hogar verificado del asistente (el directorio con el que se firma), su nivel de confianza y cuántas solicitudes ha realizado. El nombre y el logotipo que presenta el asistente se muestran solo como detalles *reclamados* - trátelos como una etiqueta, no como prueba de identidad; la parte del hogar verificado es la que se puede confiar.

Cada asistente se encuentra en uno de tres niveles de confianza:

| Nivel de confianza | Qué significa |
|---|---|
| **Limitado (verificado, limitado)** | El predeterminado para un nuevo asistente. Spwig ha registrado su identidad, y lleva la tarifa de valor de pedido, el límite de gasto y las restricciones de pago establecidas en su política (ver más abajo). |
| **Verificado (límites eliminados)** | Una decisión deliberada por su parte de confiar plenamente en este asistente. Sus límites de valor de pedido y gasto diario se borran. |
| **Bloqueado** | El asistente ya no puede comprar en su tienda. Los cierres abiertos se detienen, aunque cualquier pago ya realizado se deja intacto. |

Para detener a un asistente, selecciónelo en la lista y elija **Bloquear asistentes seleccionados**. **Desbloquear asistentes seleccionados** siempre lo devuelve a **Limitado** - nunca directamente a Verificado - porque levantar los límites es un paso separado, deliberado.

Para eliminar por completo los límites de un asistente, selecciónelo y elija **Promover a verificado (eliminar límites)**.

Esto borra su valor máximo de pedido y el límite diario de gasto, y pasa al estado Verificado.

Un asistente bloqueado se omite: cámbielo a no bloqueado primero, y luego promuévalo.

Trátelo como una decisión real de confianza: solo promueva a un asistente del que esté seguro, ya que la verificación elimina las barreras de seguridad con las que comienza un nuevo asistente.

## Establecer límites para un asistente

Abra la página de detalles de un asistente y utilice la sección **Política (límites y ofertas permitidas)** para establecer lo que puede hacer:

| Campo | Qué controla |
|---|---|
| **Valor máximo de pedido** | El mayor pedido único que puede realizar este asistente. Deje en blanco para no tener límite. |
| **Límite diario de gasto** | La cantidad máxima que este asistente puede gastar en todos los pedidos en un día. Deje en blanco para no tener límite. |
| **Permitir códigos de descuento** | Si el asistente puede aplicar códigos de descuento en el momento de pagar. |
| **Permitir tarjetas de regalo** | Si el asistente puede canjear tarjetas de regalo. |
| **Permitir productos digitales** | Si el asistente puede comprar productos digitales. |
| **Límite de tasas (por minuto)** | Cuántas solicitudes puede realizar el asistente a su tienda por minuto. |

Un nuevo asistente comienza con límites concretos de valor de pedido y gasto, y con los códigos de descuento, las tarjetas de regalo y los productos digitales desactivados: la configuración por defecto deliberadamente conservadora. Cambie alguno de estos campos y guárdelo; cada cambio se escribe en **Agent Events** con los valores antes y después, por lo que siempre tendrá un registro de quién cambió qué y cuándo. Promover a un asistente al estado Verificado borra su valor máximo de pedido y su límite diario de gasto para usted: no necesita borrarlos manualmente primero.

## El registro de actividad

**IA Shopping → Agent Events** es un registro inalterable de lo que hicieron los asistentes: cada solicitud verificada, cada intento bloqueado, cada cambio que realizó. Es de solo lectura y no se puede editar ni borrar, por lo que constituye su rastro de pruebas si alguna compra realizada por un asistente se disputa en algún momento.

## Una nota sobre las plataformas de los asistentes

Las empresas que ejecutan estos asistentes (y las normas para aparecer en ellos) son nuevas y cambian con frecuencia. Algunas requieren que se solicite o se cumplan condiciones regionales antes de que sus productos puedan comprarse a través de ellos. Spwig pone su tienda lista; si un determinado asistente le incluye a usted depende de ese asistente.

Preserve all markdown formatting, image paths, code blocks, and technical terms.