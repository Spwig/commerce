---
title: Promociones de Envío
---

Las reglas de envío aplican ajustes condicionales de costo a los métodos de envío basados en el contenido del carrito, atributos del cliente y zonas de entrega — ofrezca automáticamente envío gratuito por encima de $50, agregue recargos para áreas remotas o descuente el envío para clientes VIP. Las reglas usan una ejecución basada en prioridad (primero las de mayor prioridad) con banderas de detención opcionales para evitar un procesamiento adicional. Cada regla evalúa múltiples condiciones (valor del carrito, peso, zonas, productos, grupos de clientes) y ejecuta uno de 6 tipos de ajuste cuando todas las condiciones coincidan.

Use promociones de envío cuando necesite costos de envío dinámicos que cambien según el contexto del pedido, no solo tasas estáticas de métodos de envío.

## Tipos de Promociones de Envío

Las reglas de envío aplican 6 tipos de ajustes de costo:

### Descuento por Porcentaje

**¿Qué hace?**: Reduce el costo de envío en un porcentaje (ejemplo: 25% de descuento).

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
- Descuento para pedidos en cantidad (10% de descuento en envíos para 5+ artículos)

---

### Descuento Fijo

**¿Qué hace?**: Resta una cantidad fija del costo de envío.

**Fórmula**: `nuevo_costo = costo_base - monto` (mínimo $0)

**Ejemplo**:
```
Costo base: $15
Descuento: $5
Resultado: $10
```

**Casos de uso**:
- Bonificación para primeros clientes ($5 de descuento en el envío del primer pedido)
- Recompensa por registro en boletín ($3 de descuento en envío)
- Beneficio del programa de lealtad ($10 de descuento en envío por mes)

---

### Sobrescribir Costo

**¿Qué hace?**: Sobrescribe el costo de envío a una cantidad específica.

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

### Envío Gratis

**¿Qué hace?**: Establece el costo de envío en $0.

**Fórmula**: `nuevo_costo = $0`

**Ejemplo**:
```
Costo base: $18
Regla aplicable
Resultado: $0
```

**Casos de uso**:
- Envío gratis por encima de $50
- Envío gratis para productos específicos (artículos promocionales)
- Envío gratis para clientes VIP
- Envío gratis en pedidos con 3+ artículos

---

### Recargo (Fijo)

**¿Qué hace?**: Añade una cantidad fija al costo de envío.

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

**¿Qué hace?**: Aumenta el costo de envío en un porcentaje.

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

## Condiciones de Promoción

Las promociones evalúan **TODAS las condiciones deben pasar** para que la regla se aplique:

### Validez de Tiempo

- **Fecha de inicio**: La regla solo está activa después de esta fecha
- **Fecha de fin**: La regla solo está activa antes de esta fecha
- **Casos de uso**: Promociones estacionales, ofertas con tiempo limitado

**Ejemplo**: Envío gratis solo en el fin de semana de Black Friday
```
Inicio: 2026-11-27 00:00
Fin: 2026-11-30 23:59
```

---

### Rango de Valor del Carrito

- **Valor mínimo del carrito**: El subtotal del carrito debe ser ≥ monto
- **Valor máximo del carrito**: El subtotal del carrito debe ser ≤ monto
- **Casos de uso**: Umbral de envío gratis, descuentos escalonados

**Ejemplo**: Envío gratis para pedidos de $50 a $200
```
Mínimo: $50
Máximo: $200
```

---

### Rango de Peso del Carrito

- **Peso mínimo**: El peso total del carrito debe ser ≥ monto
- **Peso máximo**: El peso total del carrito debe ser ≤ monto
- **Casos de uso**: Descuentos para envíos ligeros, recargos para artículos pesados

**Ejemplo**: Recargo de $5 para pedidos superiores a 20kg
```
Peso mínimo: 20kg
Peso máximo: null (ilimitado)
```

---

### Rango de Cantidad de Artículos


- **Min Item Count**: El carrito debe tener ≥ cantidad de artículos
- **Max Item Count**: El carrito debe tener ≤ cantidad de artículos
- **Use Case**: Descuentos por pedidos en cantidad, tarifas por artículo único

**Ejemplo**: Envío gratis para 5+ artículos
```
Min Items: 5
Max Items: null
```

---

### Zona de Envío

- **Zonas**: La regla solo se aplica si la dirección del cliente coincide con al menos una zona seleccionada
- **Selección vacía**: La regla se aplica a TODAS las zonas
- **Use Case**: Recargos o descuentos específicos de zona

**Ejemplo**: Envío gratis solo para la zona nacional
```
Zones: ["Domestic USA"]
```

---

### Método de Envío

- **Métodos**: La regla solo se aplica a métodos de envío específicos
- **Selección vacía**: La regla se aplica a TODOS los métodos
- **Use Case**: Promociones específicas de método

**Ejemplo**: 25% de descuento en Envío Express
```
Methods: ["Express Delivery"]
```

---

### Requisitos del Producto

**Requiere Productos**: El carrito debe contener al menos uno de estos productos

**Requiere Categorías**: El carrito debe contener al menos un producto de estas categorías

**Use Case**: Envío gratis específico por producto, paquetes promocionales

**Ejemplo**: Envío gratis cuando el carrito contiene "Artículo de Promoción A"
```
Requires Products: [Product ID 123]
```

---

### Exclusiones de Producto

**Excluye Productos**: La regla no se aplica si el carrito contiene alguno de estos productos

**Excluye Categorías**: La regla no se aplica si el carrito contiene algún producto de estas categorías

**Use Case**: Excluir artículos pesados o de gran tamaño del envío gratis

**Ejemplo**: Envío gratis excepto para la categoría de muebles
```
Excludes Categories: [Furniture]
```

---

### Grupo de Cliente

- **Grupos de Cliente**: La regla solo se aplica a clientes en los grupos seleccionados (VIP, Mayorista, etc.)
- **Selección vacía**: La regla se aplica a TODOS los grupos de clientes
- **Use Case**: Beneficios VIP, descuentos mayoristas

**Ejemplo**: Descuento del 15% en envío para miembros VIP
```
Customer Groups: ["VIP"]
```

---

### Cliente Primero

- **Cliente Primero**: Cambiar para restringir la regla a clientes sin pedidos anteriores
- **Use Case**: Ofertas de bienvenida para nuevos clientes

**Ejemplo**: $5 de descuento en envío para primer pedido
```
First Time Customer: Yes
```

---

## Prioridad de Promoción y Ejecución

Las promociones se ejecutan en **orden de prioridad** (número más alto = ejecución más temprana):

### Mecánica de Prioridad

**Ejecución Ejemplo**:
```
Promoción A (Prioridad 100): Envío gratis si el carrito > $50
Promoción B (Prioridad 50): 10% de descuento en todo el envío
Promoción C (Prioridad 1): Recargo de $2 para zonas remotas

Carrito: $60, Zona remota
Costo de envío base: $15

Paso 1: Se evalúa la Promoción A (Prioridad 100)
  Carrito > $50? SÍ
  Aplicar: Establecer costo a $0
  Costo ahora: $0

Paso 2: Se evalúa la Promoción B (Prioridad 50)
  Aplicar un descuento del 10% a $0
  Costo ahora: $0 (aún gratis)

Paso 3: Se evalúa la Promoción C (Prioridad 1)
  Añadir un recargo de $2 a $0
  Costo ahora: $2

Costo final: $2
```

**Bandera para Detener Promociones Posteriores**:

Si la Promoción A tiene `stop_further_promotions = True`:
```
Promoción A (Prioridad 100, stop_further_promotions=True): Envío gratis si el carrito > $50
Promoción B (Prioridad 50): 10% de descuento
Promoción C (Prioridad 1): Recargo de $2

Carrito: $60
Base: $15

Paso 1: Se aplica la Promoción A, establece el costo a $0
        stop_further_promotions = True → DETENER

Costo final: $0 (Las reglas B y C nunca se ejecutan)
```

---

## Crear Promociones de Envío

**Flujo de Trabajo Paso a Paso**:

1. **Navegar a Reglas**
   - Configuración > Envío > Promociones de Envío
   - Haga clic en "Añadir Promoción de Envío"

2. **Configuración Básica**
   - **Nombre**: Identificador interno (ej. "Envío Gratis por $50")
   - **Descripción**: Notas opcionales (no se muestran a los clientes)
   - **Activo**: Cambiar para habilitar/deshabilitar
   - **Prioridad**: Establecer el orden de ejecución (100 para alta prioridad, 1 para baja)

3. **Elegir Tipo de Promoción**
   - Seleccionar tipo de ajuste (porcentaje de descuento, descuento fijo, establecer costo, gratis, recargo porcentaje, recargo fijo)
   - Ingresar monto o porcentaje


4. **Establecer bandera de detención** (Opcional)
   - Marque "Detener promociones adicionales" si esta regla debe impedir que las promociones de menor prioridad se ejecuten
   - Úselo para reglas finales/absolutas (por ejemplo, el envío gratuito no debe tener recargos adicionales después)

5. **Definir condiciones** (Opcional - deje vacío para "siempre aplicar")
   - Validez temporal: fechas de inicio/fin
   - Valor del carrito: mínimo/máximo
   - Peso del carrito: mínimo/máximo
   - Cantidad de artículos: mínimo/máximo
   - Zonas: seleccione zonas aplicables
   - Métodos: seleccione métodos aplicables
   - Productos: requeridos o excluidos
   - Cliente: grupos o solo primeras compras

6. **Guardar regla**
   - Haga clic en Guardar
   - La regla se activa inmediatamente (si el interruptor de activación está en Sí)

---

## Escenarios comunes de promoción de envío

### Escenario 1: Envío gratuito por $50

**Objetivo**: Ofrecer envío gratuito cuando el subtotal del carrito sea ≥ $50.

**Configuración**:
```
Nombre: Envío gratuito por $50
Tipo: Envío gratuito
Prioridad: 100
Condiciones:
  Valor mínimo del carrito: $50
Detener promociones adicionales: Sí
```

---

### Escenario 2: Recargo por áreas remotas

**Objetivo**: Agregar un recargo de $10 para entregas a zonas remotas.

**Configuración**:
```
Nombre: Recargo por áreas remotas
Tipo: Recargo (Fijo)
Monto: $10
Prioridad: 50
Condiciones:
  Zonas: ["Áreas remotas"]
Detener promociones adicionales: No
```

---

### Escenario 3: Descuento del 20% para clientes VIP

**Objetivo**: Los clientes VIP obtienen un 20% de descuento en todo el envío.

**Configuración**:
```
Nombre: Descuento de envío VIP
Tipo: Descuento (Porcentaje)
Porcentaje: 20
Prioridad: 75
Condiciones:
  Grupos de clientes: ["VIP"]
Detener promociones adicionales: No
```

---

### Escenario 4: Tarifa plana de Navidad

**Objetivo**: Limitar todo el envío a $9.99 durante diciembre.

**Configuración**:
```
Nombre: Promoción de tarifa plana de diciembre
Tipo: Sobrescribir costo
Monto: $9.99
Prioridad: 100
Condiciones:
  Fecha de inicio: 2026-12-01
  Fecha de fin: 2026-12-31
Detener promociones adicionales: Sí
```

---

### Escenario 5: Recargo por artículos pesados

**Objetivo**: Agregar una tarifa de $15 para pedidos superiores a 25 kg.

**Configuración**:
```
Nombre: Recargo por pedidos pesados
Tipo: Recargo (Fijo)
Monto: $15
Prioridad: 50
Condiciones:
  Peso mínimo: 25 kg
Detener promociones adicionales: No
```

---

### Escenario 6: Envío gratuito para primer pedido

**Objetivo**: Los nuevos clientes obtienen envío gratuito en su primer pedido.

**Configuración**:
```
Nombre: Envío gratuito para primer pedido
Tipo: Envío gratuito
Prioridad: 100
Condiciones:
  Cliente de primer tiempo: Sí
Detener promociones adicionales: Sí
```

---

### Escenario 7: Envío gratuito por categoría específica

**Objetivo**: Envío gratuito para pedidos que contengan artículos de la categoría promocional.

**Configuración**:
```
Nombre: Envío gratuito por categoría promocional
Tipo: Envío gratuito
Prioridad: 90
Condiciones:
  Requiere categorías: ["Promociones"]
Detener promociones adicionales: Sí
```

---

### Escenario 8: Excluir muebles del envío gratuito

**Objetivo**: Envío gratuito por $50, excepto si el carrito contiene muebles.

**Solución**: Dos reglas

**Promoción 1**:
```
Nombre: Envío gratuito general
Tipo: Envío gratuito
Prioridad: 50
Condiciones:
  Valor mínimo del carrito: $50
  Excluye categorías: ["Muebles"]
Detener promociones adicionales: No
```

**Promoción 2**:
```
Nombre: Descuento de $5 para pedidos de muebles
Tipo: Descuento (Fijo)
Monto: $5
Prioridad: 40
Condiciones:
  Requiere categorías: ["Muebles"]
  Valor mínimo del carrito: $50
Detener promociones adicionales: No
```

---

## Estrategias de combinación de promociones

### Estrategia 1: Apilamiento de descuentos

**Permitir que múltiples descuentos se apilen**:
```
Promoción A (Prioridad 100): 10% de descuento para VIP → stop_further_promotions=No
Promoción B (Prioridad 50): 15% de descuento para pedidos >$100 → stop_further_promotions=No

Cliente VIP con pedido de $120:
Base: $15
Después de la Promoción A: $13.50 (10% de descuento)
Después de la Promoción B: $11.48 (15% de descuento de $13.50)
```

### Estrategia 2: Reglas exclusivas

**Solo se aplica una regla** (prioridad más alta):
```
Promoción A (Prioridad 100): Envío gratuito >$50 → stop_further_promotions=Yes
Promoción B (Prioridad 50): 20% de descuento en todo el envío → stop_further_promotions=Yes

Carrito > $50:
Aplica la Promoción A → Envío gratuito → DETENER
La Promoción B nunca se ejecuta
```

### Estrategia 3: Recargos condicionales


```
Promoción A (Prioridad 100): Envío gratis >$75
Promoción B (Prioridad 75): 15% de descuento VIP
Promoción C (Prioridad 50): 10% de descuento general
Promoción D (Prioridad 25): $5 recargo por zona remota
Promoción E (Prioridad 1): 10% recargo por combustible

Pedido: $80, zona remota, cliente VIP
Base: $20
A: $80 > $75 → Gratis ($0)
B: VIP → 15% de $0 = $0
C: 10% de $0 = $0
D: Zona remota +$5 = $5
E: Combustible +10% de $5 = $5.50

Final: $5.50 (no gratis debido a recargos)
```

```
Promoción A (Prioridad 100, stop=Yes): Envío gratis >$75

Mismo pedido:
A: $80 > $75 → Gratis ($0) → STOP
Final: $0 (verdaderamente gratis)
```

## Pruebas de promociones de envío

**Antes de lanzar**:

1. **Crear carritos de prueba**

- Carrito A: $25 (por debajo del umbral)

- Carrito B: $55 (por encima del umbral)

- Carrito C: $200 + zona remota

- Carrito D: cliente VIP

2. **Probar cada regla**

- Ir al checkout

- Verificar que se muestre el costo de envío correcto

- Comprobar la ejecución de la regla

3. **Probar la resolución de prioridad**

- Reglas coincidentes múltiples

- Verificar que la prioridad más alta se ejecute primero

- Comprobar el comportamiento de stop_further_promotions

4. **Probar casos límite**

- Valor del carrito exactamente en el umbral

- Múltiples condiciones coincidentes

- Reglas conflictivas

## Solución de problemas

**Problema 1: La promoción no se aplica**

**Causas**

- La regla está inactiva

- Una o más condiciones no se cumplen

- Una regla de mayor prioridad tiene stop_further_promotions=Yes

- La validez temporal está fuera de la fecha actual

**Solución**: Revisar todas las condiciones, verificar la prioridad, confirmar el estado activo.

## Problema 2: Cantidad de descuento inesperada

- Múltiples promociones acumulándose

- Porcentaje aplicado a un costo ya descontado

- Prioridad de la regla incorrecta

**Solución**: Verificar el orden de prioridad, revisar las banderas de stop_further_promotions, rastrear la ejecución manualmente.

## Problema 3: Envío gratis no funciona

- Una regla de recargo de menor prioridad agrega costo después de la promoción de envío gratis

- El carrito no cumple con el umbral de valor mínimo

- Productos excluidos en el carrito

**Solución**: Usar stop_further_promotions=Yes en la promoción de envío gratis, verificar condiciones, revisar exclusiones.

## Consejos

- **Usar alta prioridad para envío gratis** - Prioridad 100 asegura que se ejecute antes que otros ajustes

- **Establecer stop_further_promotions para reglas absolutas** - El envío gratis debe detener el procesamiento posterior

- **Probar combinaciones de reglas** - Las múltiples promociones pueden interactuar de manera inesperada

- **Usar nombres descriptivos** - "Descuento VIP del 20% (Prioridad 75)" es mejor que "Promoción 3"

- **Documentar lógica compleja** - Añadir notas en el campo de descripción

- **Comenzar con promociones simples** - Añadir complejidad gradualmente

- **Monitorear el rendimiento de las reglas** - Verificar si las reglas se usan o causan confusión

- **Evitar demasiadas promociones** - Demasiadas promociones ralentizan el checkout, usar 5-10 máximo

- **Usar zonas para geografía** - Mejor que múltiples reglas similares por país

- **Combinar con métodos** - Las reglas + métodos trabajan juntos para un preciosificación sofisticada

- **Establecer ventanas de tiempo claras** - Incluir siempre fechas de finalización para promociones

- **Probar casos límite** - Exactamente $50, exactamente 5 artículos, etc.