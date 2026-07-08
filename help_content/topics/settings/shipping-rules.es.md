---
title: Reglas de Envío
---

Las reglas de envío aplican ajustes condicionales de costos a los métodos de envío según el contenido del carrito, atributos del cliente y zonas de entrega — ofrezca automáticamente envío gratuito por encima de $50, agregue recargos para áreas remotas o descuente el envío para clientes VIP. Las reglas usan ejecución basada en prioridad (primero las de mayor prioridad) con banderas de parada opcionales para evitar un procesamiento adicional. Cada regla evalúa múltiples condiciones (valor del carrito, peso, zonas, productos, grupos de clientes) y ejecuta uno de los 6 tipos de ajuste cuando todas las condiciones coincidan.

Use reglas de envío cuando necesite costos de envío dinámicos que cambien según el contexto del pedido, no solo tasas estáticas de métodos de envío.

## Tipos de Reglas de Envío

Las reglas de envío aplican 6 tipos de ajustes de costo:

### Descuento por Porcentaje

**¿Qué hace**: Reduce el costo de envío por porcentaje (ejemplo: 25% de descuento).

**Fórmula**: `nuevo_costo = costo_base × (1 - porcentaje/100)`

**Ejemplo**:
```
Costo base: $20
Descuento: 25%
Resultado: $15
```

**Casos de uso**:
- Descuento para clientes VIP (20% de descuento en todos los envíos)
- Promociones estacionales (15% de descuento en envíos en diciembre)
- Descuento por pedidos en cantidad (10% de descuento en envíos para 5+ artículos)

---

### Descuento Fijo

**¿Qué hace**: Resta una cantidad fija del costo de envío.

**Fórmula**: `nuevo_costo = costo_base - monto` (mínimo $0)

**Ejemplo**:
```
Costo base: $15
Descuento: $5
Resultado: $10
```

**Casos de uso**:
- Bonificación para primeros clientes ($5 de descuento en envío del primer pedido)
- Recompensa por registro en boletín ($3 de descuento en envío)
- Beneficio de programa de fidelidad ($10 de descuento en envío por mes)

---

### Costo Fijo

**¿Qué hace**: Reemplaza el costo de envío por un monto específico.

**Fórmula**: `nuevo_costo = monto_fijo`

**Ejemplo**:
```
Costo base: $25
Establecer en: $9.99
Resultado: $9.99
```

**Casos de uso**:
- Venta flash (envío plano de $5 para todos los pedidos hoy)
- Envío específico por categoría (libros siempre con envío de $3.99)
- Promociones basadas en tiempo (envío limitado a $9.99 esta semana)

---

### Envío Gratuito

**¿Qué hace**: Establece el costo de envío en $0.

**Fórmula**: `nuevo_costo = $0`

**Ejemplo**:
```
Costo base: $18
Regla se aplica
Resultado: $0
```

**Casos de uso**:
- Envío gratuito por encima de $50
- Envío gratuito para productos específicos (artículos promocionales)
- Envío gratuito para clientes VIP
- Envío gratuito en pedidos con 3+ artículos

---

### Recargo (Fijo)

**¿Qué hace**: Añade una cantidad fija al costo de envío.

**Fórmula**: `nuevo_costo = costo_base + monto`

**Ejemplo**:
```
Costo base: $12
Recargo: $5
Resultado: $17
```

**Casos de uso**:
- Tarifa de entrega para áreas remotas
- Manejo de artículos de gran tamaño
- Recargo por entrega en sábados
- Tarifa de empaque para artículos frágiles

---

### Recargo (Porcentaje)

**¿Qué hace**: Aumenta el costo de envío por porcentaje.

**Fórmula**: `nuevo_costo = costo_base × (1 + porcentaje/100)`

**Ejemplo**:
```
Costo base: $20
Recargo: 15%
Resultado: $23
```

**Casos de uso**:
- Recargo de temporada pico (20% durante las vacaciones)
- Recargo premium por envío exprés (50% de recargo)
- Recargo por combustible (variable según las tasas actuales)

---

## Condiciones de la Regla

Las reglas evalúan **Todas las condiciones deben pasar** para que la regla se aplique:

### Validez de Tiempo

- **Fecha de inicio**: La regla solo está activa después de esta fecha
- **Fecha de fin**: La regla solo está activa antes de esta fecha
- **Casos de uso**: Promociones estacionales, ofertas limitadas en el tiempo

**Ejemplo**: Envío gratuito solo en el fin de semana de Black Friday
```
Inicio: 2026-11-27 00:00
Fin: 2026-11-30 23:59
```

---

### Rango de Valor del Carrito

- **Valor mínimo del carrito**: El subtotal del carrito debe ser ≥ monto
- **Valor máximo del carrito**: El subtotal del carrito debe ser ≤ monto
- **Casos de uso**: Umbral de envío gratuito, descuentos escalonados

**Ejemplo**: Envío gratuito para pedidos de $50 a $200
```
Mínimo: $50
Máximo: $200
```

---

### Rango de Peso del Carrito

- **Peso mínimo**: El peso total del carrito debe ser ≥ monto
- **Peso máximo**: El peso total del carrito debe ser ≤ monto
- **Casos de uso**: Descuentos para envíos ligeros, recargos por artículos pesados

**Ejemplo**: Recargo de $5 para pedidos superiores a 20kg
```
Peso mínimo: 20kg
Peso máximo: null (ilimitado)
```

---

### Rango de Cantidad de Items

- **Cantidad mínima de items**: El carrito debe tener ≥ cantidad de artículos
- **Cantidad máxima de items**: El carrito debe tener ≤ cantidad de artículos
- **Casos de uso**: Descuentos por pedidos en cantidad, tarifas por artículos únicos

**Ejemplo**: Envío gratuito para 5+ artículos
```
Items mínimos: 5
Items máximos: null
```

---

### Zona de Envío

- **Zonas**: La regla solo se aplica si la dirección del cliente coincide con al menos una zona seleccionada
- **Selección vacía**: La regla se aplica a TODAS las zonas
- **Casos de uso**: Recargos o descuentos específicos de zona

**Ejemplo**: Envío gratuito solo para la zona nacional
```
Zonas: ["Zona Nacional de EE.UU."]
```

---

### Método de Envío

- **Métodos**: La regla solo se aplica a métodos de envío específicos
- **Selección vacía**: La regla se aplica a TODOS los métodos
- **Casos de uso**: Promociones específicas de método

**Ejemplo**: 25% de descuento en envío exprés
```
Métodos: ["Envío Exprés"]
```

---

### Requisitos de Producto

**Requiere productos**: El carrito debe contener al menos uno de estos productos

**Requiere categorías**: El carrito debe contener al menos un producto de estas categorías

**Casos de uso**: Envío gratuito específico de producto, paquetes promocionales

**Ejemplo**: Envío gratuito cuando el carrito contiene "Artículo Promocional A"
```
Requiere productos: [ID de producto 123]
```

---

### Exclusiones de Producto

**Excluye productos**: La regla no se aplica si el carrito contiene cualquiera de estos productos

**Excluye categorías**: La regla no se aplica si el carrito contiene cualquier producto de estas categorías

**Casos de uso**: Excluir artículos pesados o de gran tamaño del envío gratuito

**Ejemplo**: Envío gratuito excepto para la categoría de muebles
```
Excluye categorías: [Muebles]
```

---

### Grupo de Cliente

- **Grupos de clientes**: La regla solo se aplica a clientes en grupos seleccionados (VIP, Mayorista, etc.)
- **Selección vacía**: La regla se aplica a TODOS los grupos de clientes
- **Casos de uso**: Beneficios VIP, descuentos mayoristas

**Ejemplo**: Descuento del 15% en envío para miembros VIP
```
Grupos de clientes: ["VIP"]
```

---

### Cliente Primero

- **Cliente primero**: Conmutador para restringir la regla a clientes sin pedidos anteriores
- **Casos de uso**: Ofertas de bienvenida para nuevos clientes

**Ejemplo**: $5 de descuento en envío para primer pedido
```
Cliente primero: Sí
```

---

## Prioridad y Ejecución de Reglas

Las reglas se ejecutan en **orden de prioridad** (número más alto = ejecución más temprana):

### Mecánica de Prioridad

**Ejecución de ejemplo**:
```
Regla A (Prioridad 100): Envío gratuito si el carrito > $50
Regla B (Prioridad 50): 10% de descuento en todos los envíos
Regla C (Prioridad 1): $2 de recargo para zonas remotas

Carrito: $60, zona remota
Costo base de envío: $15

Paso 1: Evalúa Regla A (Prioridad 100)
  Carrito > $50? SÍ
  Aplicar: Establecer costo a $0
  Costo ahora: $0

Paso 2: Evalúa Regla B (Prioridad 50)
  Aplicar 10% de descuento a $0
  Costo ahora: $0 (aún gratuito)

Paso 3: Evalúa Regla C (Prioridad 1)
  Añadir $2 de recargo a $0
  Costo ahora: $2

Costo final: $2
```

**Bandera de detener reglas adicionales**:

Si la Regla A tiene `stop_further_rules = True`:
```
Regla A (Prioridad 100, stop_further_rules=True): Envío gratuito si el carrito > $50
Regla B (Prioridad 50): 10% de descuento
Regla C (Prioridad 1): $2 de recargo

Carrito: $60
Costo base: $15

Paso 1: Aplica Regla A, establece costo a $0
        stop_further_rules = True → DETENER

Costo final: $0 (Reglas B y C nunca se ejecutan)
```

---

## Crear Reglas de Envío

**Flujo de trabajo paso a paso**:

1. **Navegar a Reglas**
   - Configuración > Envío > Reglas de Envío
   - Haga clic en "Añadir Regla de Envío"

2. **Configuración Básica**
   - **Nombre**: Identificador interno (ejemplo: "Envío Gratuito por encima de $50")
   - **Descripción**: Notas opcionales (no se muestran a los clientes)
   - **Activo**: Conmutador para habilitar/deshabilitar
   - **Prioridad**: Establecer orden de ejecución (100 para alta prioridad, 1 para baja)

3. **Elegir Tipo de Regla**
   - Seleccionar tipo de ajuste (descuento %, descuento fijo, costo fijo, gratuito, recargo %, recargo fijo)
   - Ingresar monto o porcentaje

4. **Establecer Bandera de Parada** (Opcional)
   - Marcar "Detener Reglas Adicionales" si esta regla debe prevenir que las reglas de menor prioridad se ejecuten
   - Usar para reglas finales/absolutas (ejemplo: el envío gratuito no debe tener recargos añadidos después)

5. **Definir Condiciones** (Opcional - dejar vacío para "siempre aplicar")
   - Validez de tiempo: Fechas de inicio y fin
   - Valor del carrito: Mínimo/máximo
   - Peso del carrito: Mínimo/máximo
   - Cantidad de items: Mínimo/máximo
   - Zonas: Seleccionar zonas aplicables
   - Métodos: Seleccionar métodos aplicables
   - Productos: Requeridos o excluidos
   - Cliente: Grupos o solo primeros clientes

6. **Guardar Regla**
   - Haga clic en Guardar
   - La regla se activa inmediatamente (si el conmutador de activo está en Sí)

---

## Escenarios Comunes de Reglas de Envío

### Escenario 1: Envío Gratuito por encima de $50

**Objetivo**: Ofrecer envío gratuito cuando el subtotal del carrito sea ≥ $50.

**Configuración**:
```
Nombre: Envío Gratuito por encima de $50
Tipo: Envío Gratuito
Prioridad: 100
Condiciones:
  Valor mínimo del carrito: $50
Detener reglas adicionales: Sí
```

---

### Escenario 2: Recargo por Zonas Remotas

**Objetivo**: Añadir un recargo de $10 para entregas a zonas remotas.

**Configuración**:
```
Nombre: Recargo por Zonas Remotas
Tipo: Recargo (Fijo)
Monto: $10
Prioridad: 50
Condiciones:
  Zonas: ["Zonas Remotas"]
Detener reglas adicionales: No
```

---

### Escenario 3: Descuento del 20% para Clientes VIP

**Objetivo**: Los clientes VIP obtienen un 20% de descuento en todos los envíos.

**Configuración**:
```
Nombre: Descuento de Envío para VIP
Tipo: Descuento (Porcentaje)
Porcentaje: 20
Prioridad: 75
Condiciones:
  Grupos de clientes: ["VIP"]
Detener reglas adicionales: No
```

---

### Escenario 4: Tarifa Plana de Diciembre

**Objetivo**: Limitar todos los envíos a $9.99 durante diciembre.

**Configuración**:
```
Nombre: Promoción de Tarifa Plana de Diciembre
Tipo: Establecer Costo
Monto: $9.99
Prioridad: 100
Condiciones:
  Fecha de inicio: 2026-12-01
  Fecha de fin: 2026-12-31
Detener reglas adicionales: Sí
```

---

### Escenario 5: Recargo por Artículos Pesados

**Objetivo**: Añadir una tarifa de $15 para pedidos superiores a 25kg.

**Configuración**:
```
Nombre: Recargo por Pedidos Pesados
Tipo: Recargo (Fijo)
Monto: $15
Prioridad: 50
Condiciones:
  Peso mínimo: 25kg
Detener reglas adicionales: No
```

---

### Escenario 6: Envío Gratuito en Primer Pedido

**Objetivo**: Los nuevos clientes obtienen envío gratuito en su primer pedido.

**Configuración**:
```
Nombre: Envío Gratuito en Primer Pedido
Tipo: Envío Gratuito
Prioridad: 100
Condiciones:
  Cliente primero: Sí
Detener reglas adicionales: Sí
```

---

### Escenario 7: Envío Gratuito por Categoría

**Objetivo**: Envío gratuito para pedidos que contengan artículos de la categoría promocional.

**Configuración**:
```
Nombre: Envío Gratuito para Categoría Promocional
Tipo: Envío Gratuito
Prioridad: 90
Condiciones:
  Requiere categorías: ["Promociones"]
Detener reglas adicionales: Sí
```

---

### Escenario 8: Excluir Muebles del Envío Gratuito

**Objetivo**: Envío gratuito por encima de $50, excepto si el carrito contiene muebles.

**Solución**: Dos reglas

**Regla 1**:
```
Nombre: Envío Gratuito General
Tipo: Envío Gratuito
Prioridad: 50
Condiciones:
  Valor mínimo del carrito: $50
  Excluye categorías: ["Muebles"]
Detener reglas adicionales: No
```

**Regla 2**:
```
Nombre: Descuento de $5 para Pedidos de Muebles
Tipo: Descuento (Fijo)
Monto: $5
Prioridad: 40
Condiciones:
  Requiere categorías: ["Muebles"]
  Valor mínimo del carrito: $50
Detener reglas adicionales: No
```

---

## Estrategias de Combinación de Reglas

### Estrategia 1: Apilamiento de Descuentos

**Permitir que múltiples descuentos se apilen**:
```
Regla A (Prioridad 100): 10% de descuento para VIP → stop_further_rules=No
Regla B (Prioridad 50): 15% de descuento para pedidos >$100 → stop_further_rules=No

Cliente VIP con pedido de $120:
Costo base: $15
Después de Regla A: $13.50 (10% de descuento)
Después de Regla B: $11.48 (15% de descuento de $13.50)
```

### Estrategia 2: Reglas Exclusivas

**Solo una regla se aplica** (prioridad más alta):
```
Regla A (Prioridad 100): Envío gratuito >$50 → stop_further_rules=Yes
Regla B (Prioridad 50): 20% de descuento en todos los envíos → stop_further_rules=Yes

Carrito > $50:
Regla A aplica → Envío gratuito → DETENER
Regla B nunca se ejecuta
```

### Estrategia 3: Recargos Condicionales

**Descuentos primero, recargos al final**:
```
Regla A (Prioridad 100): Envío gratuito >$75
Regla B (Prioridad 75): 15% de descuento VIP
Regla C (Prioridad 50): 10% de descuento general
Regla D (Prioridad 25): $5 de recargo para zonas remotas
Regla E (Prioridad 1): 10% de recargo por combustible

Pedido: $80, zona remota, cliente VIP
Costo base: $20
A: $80 > $75 → Gratuito ($0)
B: VIP → 15% de descuento de $0 = $0
C: 10% de descuento de $0 = $0
D: Zona remota +$5 = $5
E: Combustible +10% de $5 = $5.50

Final: $5.50 (no gratuito debido a recargos)
```

**Para prevenir esto, use stop_further_rules=Yes**:
```
Regla A (Prioridad 100, stop=Yes): Envío gratuito >$75

Mismo pedido:
A: $80 > $75 → Gratuito ($0) → DETENER
Final: $0 (verdaderamente gratuito)
```

---

## Pruebas de Reglas de Envío

**Antes de ir en vivo**:

1. **Crear carritos de prueba**
   - Carrito A: $25 (por debajo del umbral)
   - Carrito B: $55 (por encima del umbral)
   - Carrito C: $200 + zona remota
   - Carrito D: Cliente VIP

2. **Probar cada regla**
   - Proceder al checkout
   - Verificar que se muestre el costo de envío correcto
   - Revisar el orden de ejecución de las reglas

3. **Probar resolución de prioridad**
   - Múltiples reglas coincidentes
   - Verificar que la prioridad más alta se ejecute primero
   - Revisar el comportamiento de stop_further_rules

4. **Probar casos límite**
   - Valor del carrito exactamente en el umbral
   - Múltiples condiciones coincidentes
   - Reglas conflictivas

---

## Solución de Problemas

**Problema 1: Regla no se aplica**

**Causas**:
- La regla está inactiva
- Una o más condiciones no se cumplen
- Una regla de mayor prioridad establece stop_further_rules=Yes
- Validez de tiempo fuera de la fecha actual

**Solución**: Revisar todas las condiciones, verificar la prioridad, verificar el estado activo.

---

**Problema 2: Monto de descuento inesperado**

**Causas**:
- Múltiples reglas apilándose
- Porcentaje aplicado a un costo ya descontado
- Prioridad de regla incorrecta

**Solución**: Verificar el orden de prioridad, revisar las banderas de stop_further_rules, rastrear la ejecución manualmente.

---

**Problema 3: Envío gratuito no funciona**

**Causas**:
- Una regla de menor prioridad de recargo añade costo después de la regla de envío gratuito
- El carrito no cumple con el umbral de valor mínimo
- Productos excluidos en el carrito

**Solución**: Usar stop_further_rules=Yes en la regla de envío gratuito, verificar condiciones, revisar exclusiones.

---

## Consejos

- **Usar alta prioridad para envío gratuito** - Prioridad 100 asegura que se ejecute antes que otros ajustes
- **Establecer stop_further_rules para reglas absolutas** - El envío gratuito debe detener el procesamiento adicional
- **Probar combinaciones de reglas** - Múltiples reglas pueden interactuar de manera inesperada
- **Usar nombres descriptivos** - "Descuento del 20% para VIP (Prioridad 75)" es mejor que "Regla 3"
- **Documentar lógica compleja** - Añadir notas en el campo de descripción
- **Empezar con reglas simples** - Añadir complejidad gradualmente
- **Monitorear el rendimiento de las reglas** - Verificar si las reglas se usan o causan confusión
- **Evitar reglas excesivas** - Demasiadas reglas ralentizan el checkout, usar máximo 5-10
- **Usar zonas para geografía** - Mejor que múltiples reglas similares por país
- **Combinar con métodos** - Reglas + Métodos funcionan juntos para precios sofisticados
- **Establecer ventanas de tiempo claras** - Incluir siempre fechas de fin para promociones
- **Probar casos límite** - Exactamente $50, exactamente 5 artículos, etc.

Recuerde: Preservar todo el formato de markdown, rutas de imágenes, bloques de código y términos técnicos exactamente como se muestran en las reglas de preservación.