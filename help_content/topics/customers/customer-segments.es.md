---
title: Segmentos de clientes
---

Los segmentos de clientes le permiten clasificar automáticamente a sus clientes en grupos significativos según su comportamiento de compra. Una vez que los clientes estén segmentados, puede utilizar esos grupos para enfocar sus esfuerzos de marketing — por ejemplo, ofrecer recompensas de lealtad a clientes VIP o enviar campañas de recuperación a clientes que no han comprado hace un tiempo.

Spwig evalúa los criterios de segmento contra las métricas de cada cliente y los asigna al segmento de mayor prioridad para el cual califiquen. Esto ocurre automáticamente a medida que se actualizan los datos del cliente.

## Tipos de segmento disponibles

Spwig viene con un conjunto de tipos de segmento predefinidos. Cada tipo de segmento tiene un identificador interno fijo, pero puede personalizar el nombre de visualización, la descripción, los criterios y el color para que coincidan con cómo piensa sobre sus clientes.

| Tipo de Segmento | Uso Típico |
|---|---|
| **Cliente Invitado** | Clientes que realizaron una compra sin crear una cuenta |
| **Nuevo Cliente** | Clientes que han realizado su primera compra recientemente |
| **Cliente Regular** | Clientes con un historial de compras constante |
| **Comprador Frecuente** | Clientes que compran con frecuencia (tiempo corto entre pedidos) |
| **Alto Valor** | Clientes con un gasto total alto |
| **Cliente VIP** | Sus clientes más valiosos y leales |
| **Cazador de Ofertas** | Clientes que tienden a comprar durante ventas |
| **En Riesgo** | Clientes que no han comprado hace un tiempo |
| **Inactivo** | Clientes que han estado ausentes durante un período prolongado |

## Entendiendo los criterios de segmento

Cada segmento está definido por una combinación de criterios. Spwig verifica estos contra las métricas almacenadas de cada cliente. Todos los criterios dentro de un segmento se combinan — un cliente debe satisfacer cada condición establecida para calificar.

### Criterios de gasto

- **Mínimo Total Gastado** — el cliente debe haber gastado al menos esta cantidad en todas las órdenes completadas
- **Máximo Total Gastado** — el cliente no debe haber gastado más de esta cantidad

Utilice un rango de gasto para identificar una categoría específica. Por ejemplo, establecer Mínimo en $500 y Máximo en $2,000 identificaría clientes de nivel medio.

### Criterios de cantidad de pedidos

- **Mínimo de Pedidos** — el cliente debe tener al menos este número de órdenes completadas
- **Máximo de Pedidos** — el cliente no debe tener más de este número de órdenes completadas

Combinar Mínimo de Pedidos con un mínimo de gasto es una manera confiable de definir clientes VIP: compran con frecuencia *y* gastan generosamente.

### Criterios de recencia

- **Mínimo de Días desde Última Compra** — la última orden del cliente debe ser al menos este número de días atrás
- **Máximo de Días desde Última Compra** — la última orden del cliente debe estar dentro de este número de días

Los criterios de recencia son esenciales para los segmentos de clientes en riesgo e inactivos. Por ejemplo, establecer Mínimo de Días en 90 y Máximo de Días en 365 identificaría clientes que se han silenciado pero no han sido completamente perdidos.

## Prioridad de segmento

Cuando un cliente califica para más de un segmento, el segmento con el valor de **mayor prioridad** gana. Puede establecer la prioridad para cada segmento en la sección **Configuración de Visualización** del formulario del segmento.

El segmento **Cliente Invitado** siempre se evalúa primero, independientemente del orden de prioridad, porque el estado de invitado se determina por el tipo de cuenta en lugar de los criterios de compra.

## Ver y gestionar segmentos

Navegue hasta **Clientes > Segmentos de Clientes** para ver todos sus segmentos configurados. La lista muestra el nombre de visualización de cada segmento, el tipo interno, el color asignado, la prioridad, la cantidad actual de clientes que coinciden y si el segmento está activo.

![Lista de Segmentos de Clientes](/static/core/admin/img/help/customer-segments/segments-list.webp)

### Crear o editar un segmento

1.

Navegue hasta **Clientes > Segmentos de Clientes**
2.

Haga clic en un segmento existente para editarlo, o haga clic en **+ Agregar Segmento de Cliente** para crear uno nuevo
3.

Preserve all markdown formatting, image paths, code blocks, and technical terms.

Rellene la pestaña **Información del segmento**:
   - **Nombre** — seleccione el tipo de segmento interno desde el menú desplegable
   - **Nombre de visualización** — el nombre legible para humanos que se muestra en el administrador (por ejemplo, "Clientes VIP")
   - **Descripción** — una nota breve interna que explica qué representa este segmento
4.

Establezca criterios en las pestañas relevantes:
   - **Criterios - Gasto** — gasto total mínimo y máximo
   - **Criterios - Pedidos** — conteo mínimo y máximo de pedidos
   - **Criterios - Recencia** — días mínimos y máximos desde la última compra
5.

Configure **Configuración de visualización**:
   - **Color** — un color en formato hexadecimal utilizado para identificar visualmente este segmento en listas
   - **Prioridad** — un número más alto significa que este segmento se evalúa primero
   - **Activo** — desmarque para deshabilitar el segmento sin eliminarlo
6.

Haga clic en **Guardar** para aplicar los cambios

### Ejemplo: Configurando un segmento VIP

Aquí hay un ejemplo realista para un segmento VIP de alto valor:

| Campo | Valor |
|---|---|
| Nombre | `vip` |
| Nombre de visualización | Clientes VIP |
| Gasto total mínimo | $1,000 |
| Pedidos mínimos | 5 |
| Máximo de días desde la última compra | 180 |
| Prioridad | 90 |
| Color | `#FFD700` |

Esto significa: un cliente califica como VIP si ha gastado al menos $1,000, ha realizado al menos 5 pedidos y ha realizado una compra dentro de los últimos 6 meses.

### Ejemplo: Configurando un segmento de riesgo

| Campo | Valor |
|---|---|
| Nombre | `at_risk` |
| Nombre de visualización | En riesgo |
| Días mínimos desde la última compra | 60 |
| Días máximos desde la última compra | 180 |
| Prioridad | 30 |
| Color | `#FF6B35` |

## Usando segmentos para marketing dirigido

Los segmentos se muestran en los perfiles de clientes en todo el administrador, por lo que su equipo sabe inmediatamente a qué nivel pertenece cada cliente. Use esta información para:

- **Ejecutar campañas de cupones dirigidas** — cree cupones restringidos a clientes de un segmento específico, luego use su sistema de correo electrónico para enviarlos solo a ese grupo
- **Priorizar el soporte** — marque a los clientes VIP o de alto valor para que su equipo pueda brindar un servicio prioritario
- **Planificar la reactivación** — revise los segmentos de riesgo y inactivos periódicamente para identificar clientes que necesiten un correo electrónico de recuperación o una oferta especial
- **Ajustar el gasto de marketing** — enfoque el presupuesto de adquisición en canales que atraigan a clientes de alto valor analizando qué cohortes de segmentos convierten

## Consejos

- Comience con los tipos de segmentos predefinidos antes de crear criterios personalizados — cubren las necesidades de segmentación más comunes de forma predeterminada
- Revise periódicamente la cantidad de clientes en cada segmento; un segmento VIP con cero clientes o un segmento de riesgo que esté creciendo rápidamente son ambos dignos de investigación
- Use el campo **Prioridad** con intención — si sus criterios se superponen entre segmentos (por ejemplo, un cliente califica para ambos compradores frecuentes y alto valor), el segmento con mayor prioridad gana
- Desactive los segmentos que no esté usando actualmente en lugar de eliminarlos — puede reactivarlos más tarde sin reconfigurar los criterios
- Los criterios de segmento se verifican contra métricas de clientes almacenadas, que se recalculan automáticamente. Si las cuentas de segmento parecen anticuadas, las métricas pueden recalcularse desde la sección de Métricas de clientes del administrador