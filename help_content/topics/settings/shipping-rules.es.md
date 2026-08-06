---
title: Reglas de envío
---

Las reglas de envío aplican ajustes de costo condicionales a los métodos de envío según el contenido del carrito, atributos del cliente y zonas de entrega: ofrezca automáticamente envío gratis por encima de $50, agregue recargos para áreas remotas o descuente el envío para clientes VIP. Las reglas utilizan ejecución basada en prioridad (prioridad más alta primero) con banderas de parada opcionales para evitar más procesamiento. Cada regla evalúa múltiples condiciones (valor del carrito, peso, zonas, productos, grupos de clientes) y ejecuta uno de 6 tipos de ajuste cuando todas las condiciones coincidan.

Use las reglas de envío cuando necesite costos de envío dinámicos que cambien según el contexto del pedido, no solo tarifas estáticas de métodos de envío.

## Tipos de reglas de envío

Las reglas de envío aplican 6 tipos de ajustes de costo:

### Descuento porcentual

**¿Qué hace?**: Reduce el costo de envío en porcentaje (ej., 25% de descuento).

**Fórmula**: `nuevo_costo = costo_base × (1 - porcentaje/100)`

**Ejemplo**:
```
costo_base: $20
Descuento: 25%
Resultado: $15
```

**Casos de uso**:
- Descuento para clientes VIP (20% de descuento en todos los envíos)
- Promociones estacionales (15% de descuento en envíos en diciembre)
- Descuento por pedido en volumen (10% de descuento en envíos para 5+ artículos)

---

### Descuento fijo

**¿Qué hace?**: Resta una cantidad fija del costo de envío.

**Fórmula**: `nuevo_costo = costo_base - monto` (mínimo $0)

**Ejemplo**:
```
costo_base: $15
Descuento: $5
Resultado: $10
```

**Casos de uso**:
- Bonificación para primer cliente ($5 de descuento en envío de primer pedido)
- Recompensa por registro al boletín ($3 de descuento en envío)
- Beneficio del programa de lealtad ($10 de descuento en envío por mes)

---

### Costo fijo

**¿Qué hace?**: Reemplaza el costo de envío a una cantidad específica.

**Fórmula**: `nuevo_costo = monto_fijo`

**Ejemplo**:
```
costo_base: $25
Establecer en: $9.99
Resultado: $9.99
```

**Casos de uso**:
- Venta rápida (envío fijo de $5 para todos los pedidos de hoy)
- Envío específico por categoría (libros siempre $3.99 de envío)
- Promociones basadas en tiempo (envío limitado a $9.99 esta semana)

---

### Envío gratis

**¿Qué hace?**: Establece el costo de envío a $0.

**Fórmula**: `nuevo_costo = $0`

**Ejemplo**:
```
costo_base: $18
La regla se aplica
Resultado: $0
```

**Casos de uso**:
- Envío gratis por encima de $50
- Envío gratis para productos específicos (artículos promocionales)
- Envío gratis para clientes VIP
- Envío gratis en pedidos con 3+ artículos

---

### Recargo (fijo)

**¿Qué hace?**: Añade una cantidad fija al costo de envío.

**Fórmula**: `nuevo_costo = costo_base + monto`

**Ejemplo**:
```
costo_base: $12
Recargo: $5
Resultado: $17
```

**Casos de uso**:
- Tarifa de entrega a áreas remotas
- Manejo de artículo de gran tamaño
- Recargo por entrega el sábado
- Tarifa de empaque para artículos frágiles

---

### Recargo (porcentual)

**¿Qué hace?**: Aumenta el costo de envío en porcentaje.

**Fórmula**: `nuevo_costo = costo_base × (1 + porcentaje/100)`

**Ejemplo**:
```
costo_base: $20
Recargo: 15%
Resultado: $23
```

**Casos de uso**:
- Recargo de temporada alta (20% durante las fiestas)
- Prima de entrega exprés (recargo del 50%)
- Recargo por combustible (variable según tasas actuales)

---

## Condiciones de la regla

Las reglas evalúan **todos los requisitos deben cumplirse** para que se aplique la regla:

### Validez de tiempo

- **Fecha de inicio**: La regla solo está activa después de esta fecha
- **Fecha de finalización**: La regla solo está activa antes de esta fecha
- **Caso de uso**: Promociones estacionales, ofertas con plazo limitado

**Ejemplo**: Envío gratis durante el fin de semana de Black Friday solo
```
Inicio: 2026-11-27 00:00
Finalización: 2026-11-30 23:59
```

---

### Rango de valor del carrito

- **Valor mínimo del carrito**: El subtotal del carrito debe ser ≥ cantidad
- **Valor máximo del carrito**: El subtotal del carrito debe ser ≤ cantidad
- **Caso de uso**: Límites de envío gratis, descuentos por niveles

**Ejemplo**: Envío gratis para pedidos de $50 a $200
```
Mín: $50
Máx: $200
```

---

### Rango de peso del carrito

- **Peso mínimo**: El peso total del carrito debe ser ≥ cantidad
- **Peso máximo**: El peso total del carrito debe ser ≤ cantidad
- **Caso de uso**: Descuentos para envíos ligeros, recargos por artículos pesados

**Ejemplo**: Recargo de $5 para pedidos de más de 20kg
```
Peso mínimo: 20kg
Peso máximo: null (ilimitado)
```

---

### Rango de cantidad de artículos

- **Mínimo de artículos**: El carrito debe tener ≥ cantidad de artículos
- **Máximo de artículos**: El carrito debe tener ≤ cantidad de artículos
- **Escenario de uso**: Descuentos por pedido mayor, tarifas por artículo único

**Ejemplo**: Envío gratis para 5+ artículos
```
Mínimos de artículos: 5
Máximos de artículos: null
```


### Zona de envío

- **Zonas**: La regla solo se aplica si la dirección del cliente coincide con al menos una zona seleccionada
- **Selección vacía**: La regla se aplica a TODAS las zonas
- **Escenario de uso**: Recargos o descuentos específicos de zona

**Ejemplo**: Envío gratis solo para la zona Nacional
```
Zonas: ["Zona Nacional"]
```


### Método de envío

- **Métodos**: La regla solo se aplica a métodos de envío específicos
- **Selección vacía**: La regla se aplica a TODOS los métodos
- **Escenario de uso**: Promociones específicas del método

**Ejemplo**: 25% de descuento en envío urgente
```
Métodos: ["Entrega urgente"]
```


### Requisitos de producto

**Productos requeridos**: El carrito debe contener al menos uno de estos productos

**Categorías requeridas**: El carrito debe contener al menos un producto de estas categorías

**Escenario de uso**: Envío gratis específico del producto, paquetes promocionales

**Ejemplo**: Envío gratis cuando el carrito contenga "Producto de promoción A"
```
Productos requeridos: [ID de producto 123]
```


### Exclusiones de producto

**Productos excluidos**: La regla no se aplica si el carrito contiene alguno de estos productos

**Categorías excluidas**: La regla no se aplica si el carrito contiene productos de estas categorías

**Escenario de uso**: Excluir artículos pesados/u oversized del envío gratis

**Ejemplo**: Envío gratis excepto por la categoría de muebles
```
Categorías excluidas: [Muebles]
```


### Grupo de clientes

- **Grupos de clientes**: La regla solo se aplica a los clientes en los grupos seleccionados (VIP, mayorista, etc.)
- **Selección vacía**: La regla se aplica a TODOS los grupos de clientes
- **Escenario de uso**: Beneficios para clientes VIP, descuentos al por mayor

**Ejemplo**: Descuento del 15% en envío para miembros VIP
```
Grupos de clientes: ["VIP"]
```


### Cliente por primera vez

- **Cliente por primera vez**: Conmutador para restringir la regla a los clientes sin pedidos anteriores
- **Escenario de uso**: Ofertas de bienvenida para nuevos clientes

**Ejemplo**: $5 de descuento en envío para el primer pedido
```
Cliente por primera vez: Sí
```


## Prioridad de regla y ejecución

Las reglas se ejecutan en orden de **prioridad** (número más alto = ejecución más temprana):

### Mecánica de prioridad

**Ejecución de ejemplo**:
```
Regla A (Prioridad 100): Envío gratis si el carrito > $50
Regla B (Prioridad 50): 10% de descuento en todo el envío
Regla C (Prioridad 1): Recargo de $2 para zonas remotas

Carrito: $60, zona remota
Costo base de envío: $15

Paso 1: Evaluar Regla A (Prioridad 100)
  ¿Carrito > $50? SÍ
  Aplicar: Establecer costo a $0
  Costo ahora: $0

Paso 2: Evaluar Regla B (Prioridad 50)
  Aplicar 10% de descuento a $0
  Costo ahora: $0 (todavía gratis)

Paso 3: Evaluar Regla C (Prioridad 1)
  Añadir recargo de $2 a $0
  Costo ahora: $2

Costo final: $2
```

**Bandera de detener reglas posteriores**:

Si la Regla A tiene `stop_further_rules = True`:
```
Regla A (Prioridad 100, stop_further_rules=True): Envío gratis si el carrito > $50
Regla B (Prioridad 50): 10% de descuento en todo el envío
Regla C (Prioridad 1): Recargo de $2 para zonas remotas

Carrito: $60
Base: $15

Paso 1: Regla A se aplica, establece costo a $0
        stop_further_rules = True → DETENER

Costo final: $0 (Reglas B y C nunca se ejecutan)
```


## Creando reglas de envío

**Flujo de trabajo paso a paso**:

1. **Navegar a Reglas**
   - Configuración > Envío > Reglas de envío
   - Haga clic en "Añadir regla de envío"

2. **Configuración básica**
   - **Nombre**: identificador interno (ej.: "Envío gratis sobre $50")
   - **Descripción**: notas opcionales (no mostradas a los clientes)
   - **Activo**: conmutador para habilitar/deshabilitar
   - **Prioridad**: Establezca el orden de ejecución (100 para alta prioridad, 1 para baja)

3. **Elija el tipo de regla**
   - Seleccione el tipo de ajuste (porcentaje de descuento, descuento fijo, costo fijo, gratis, porcentaje de recargo, recargo fijo)
   - Ingrese monto o porcentaje

4. **Establezca la bandera de detención** (Opcional)
   - Marque "Detener reglas posteriores" si esta regla debe evitar que reglas de menor prioridad se ejecuten
   - Úselo para reglas finales/absolutas (ej.: el envío gratis no debe tener recargos posteriores)

5. **Definir condiciones** (Opcional - dejar en blanco para "aplicar siempre")
  - Validez del tiempo: Fechas de inicio/fin
  - Valor del carrito: Mínimo/máximo
  - Peso del carrito: Mínimo/máximo
  - Cantidad de artículos: Mínimo/máximo
  - Zonas: Seleccionar zonas aplicables
  - Métodos: Seleccionar métodos aplicables
  - Productos: Requeridos o excluidos
  - Clientes: Grupos o solo primeras veces

6. **Guardar regla**
  - Haga clic en Guardar
  - La regla se activa inmediatamente (si el interruptor de activo está en Sí)


## Escenarios comunes de reglas de envío

### Escenario 1: Envío gratis por encima de $50

**Objetivo**: Ofrecer envío gratis cuando el subtotal del carrito ≥ $50.

**Configuración**:
```
Nombre: Envío gratis por encima de $50
Tipo: Envío gratis
Prioridad: 100
Condiciones:
  Valor mínimo del carrito: $50
Detener reglas posteriores: Sí
```


### Escenario 2: Recargo por zona remota

**Objetivo**: Añadir un recargo de $10 para entregas en zonas remotas.

**Configuración**:
```
Nombre: Recargo por zona remota
Tipo: Recargo (Fijo)
Monto: $10
Prioridad: 50
Condiciones:
  Zonas: ["Zonas remotas"]
Detener reglas posteriores: No
```


### Escenario 3: Descuento del 20% para clientes VIP

**Objetivo**: Los clientes VIP obtienen un 20% de descuento en todos los envíos.

**Configuración**:
```
Nombre: Descuento de envío para VIP
Tipo: Descuento (Porcentaje)
Porcentaje: 20
Prioridad: 75
Condiciones:
  Grupos de clientes: ["VIP"]
Detener reglas posteriores: No
```


### Escenario 4: Tarifa plana de Navidad

**Objetivo**: Todos los envíos con un límite de $9.99 durante diciembre.

**Configuración**:
```
Nombre: Promoción de tarifa plana de diciembre
Tipo: Costo fijo
Monto: $9.99
Prioridad: 100
Condiciones:
  Fecha de inicio: 2026-12-01
  Fecha final: 2026-12-31
Detener reglas posteriores: Sí
```


### Escenario 5: Recargo por artículo pesado

**Objetivo**: Añadir un cargo de $15 para pedidos de más de 25kg.

**Configuración**:
```
Nombre: Recargo por pedido pesado
Tipo: Recargo (Fijo)
Monto: $15
Prioridad: 50
Condiciones:
  Peso mínimo: 25kg
Detener reglas posteriores: No
```


### Escenario 6: Envío gratis para primer pedido

**Objetivo**: Los clientes nuevos obtienen envío gratis en su primer pedido.

**Configuración**:
```
Nombre: Envío gratis para primer pedido
Tipo: Envío gratis
Prioridad: 100
Condiciones:
  Cliente nuevo: Sí
Detener reglas posteriores: Sí
```


### Escenario 7: Envío gratis específico por categoría

**Objetivo**: Envío gratis para pedidos que contengan artículos de categoría promocional.

**Configuración**:
```
Nombre: Envío gratis por categoría promocional
Tipo: Envío gratis
Prioridad: 90
Condiciones:
  Categorías requeridas: ["Promociones"]
Detener reglas posteriores: Sí
```


### Escenario 8: Excluir muebles del envío gratis

**Objetivo**: Envío gratis por encima de $50, excepto si el carrito contiene muebles.

**Solución**: Dos reglas

**Regla 1**:
```
Nombre: Envío gratis general
Tipo: Envío gratis
Prioridad: 50
Condiciones:
  Valor mínimo del carrito: $50
  Categorías excluidas: ["Muebles"]
Detener reglas posteriores: No
```

**Regla 2**:
```
Nombre: Descuento de $5 para pedidos de muebles
Tipo: Descuento (Fijo)
Monto: $5
Prioridad: 40
Condiciones:
  Categorías requeridas: ["Muebles"]
  Valor mínimo del carrito: $50
Detener reglas posteriores: No
```


## Estrategias de combinación de reglas

### Estrategia 1: Descuentos acumulables

**Permitir que varios descuentos se acumulen**:
```
Regla A (Prioridad 100): 10% de descuento para VIP → stop_further_rules=No
Regla B (Prioridad 50): 15% de descuento en pedidos >$100 → stop_further_rules=No

Cliente VIP con pedido de $120:
Base: $15
Después de la Regla A: $13.50 (10% de descuento)
Después de la Regla B: $11.48 (15% de descuento de $13.50)
```


### Estrategia 2: Reglas exclusivas

**Solo se aplica una regla** (prioridad más alta):
```
Regla A (Prioridad 100): Envío gratis >$50 → stop_further_rules=Sí
Regla B (Prioridad 50): 20% de descuento en todos los envíos → stop_further_rules=Sí

Carrito > $50:
La Regla A se aplica → Envío gratis → DETENER
La Regla B nunca se ejecuta
```


### Estrategia 3: Recargos condicionales

**Descuentos primero, recargos al final**:
```
Regla A (Prioridad 100): Envío gratis >$75
Regla B (Prioridad 75): 15% de descuento para VIP
Regla C (Prioridad 50): 10% de descuento general
Regla D (Prioridad 25): Recargo de $5 por zona remota
Regla E (Prioridad 1): Recargo del 10% por combustible

Pedido: $80, zona remota, cliente VIP
Base: $20
A: $80 > $75 → Gratis ($0)
B: VIP → 15% de descuento de $0 = $0
C: 10% de descuento de $0 = $0
D: Zona remota +$5 = $5
E: Combustible +10% de $5 = $5.50
```

Final: $5.50 (no es gratis debido a recargos)
```

**Para evitar esto, use stop_further_rules=Si**:
```
Regla A (Prioridad 100, stop=Si): Envío gratis >$75

Mismo pedido:
A: $80 > $75 → Gratis ($0) → DETENER
Final: $0 (verdaderamente gratis)
```

---

## Prueba de reglas de envío

**Antes de ir a producción**:

1. **Crear carritos de prueba**
   - Carrito A: $25 (por debajo del umbral)
   - Carrito B: $55 (por encima del umbral)
   - Carrito C: $200 + zona remota
   - Carrito D: Cliente VIP

2. **Probar cada regla**
   - Proceder al pago
   - Verificar que se muestre el costo de envío correcto
   - Comprobar el orden de ejecución de la regla

3. **Probar la resolución de prioridad**
   - Múltiples reglas que coinciden
   - Verificar que se ejecute primero la prioridad más alta
   - Comprobar el comportamiento de stop_further_rules

4. **Probar casos límite**
   - Valor del carrito exactamente en el umbral
   - Múltiples condiciones que coinciden
   - Reglas que se contradicen

---

## Solución de problemas

**Problema 1: La regla no se aplica**

**Causas**:
- La regla está inactiva
- Una o más condiciones no se cumplen
- Una regla de mayor prioridad establece stop_further_rules=Si
- El período de validez está fuera del período actual

**Solución**: Revise todas las condiciones, verifique la prioridad y confirme el estado activo.

---

**Problema 2: Monto del descuento inesperado**

**Causas**:
- Múltiples reglas que se acumulan
- Porcentaje aplicado a un costo ya con descuento
- Prioridad de regla incorrecta

**Solución**: Verifique el orden de prioridad, revise las banderas de stop_further_rules y trace manualmente la ejecución.

---

**Problema 3: El envío gratis no funciona**

**Causas**:
- Una regla de recargo de menor prioridad agrega costo después de la regla de envío gratis
- El carrito no cumple con el valor mínimo requerido
- Productos excluidos en el carrito

**Solución**: Use stop_further_rules=Si en la regla de envío gratis, verifique las condiciones y compruebe las exclusiones.

---

## Consejos

- **Use alta prioridad para el envío gratis** - Prioridad 100 asegura que se ejecute antes de otros ajustes
- **Establezca stop_further_rules para reglas absolutas** - El envío gratis debe detener el procesamiento adicional
- **Pruebe combinaciones de reglas** - Múltiples reglas pueden interactuar de manera inesperada
- **Use nombres descriptivos** - "Descuento VIP 20% (Prioridad 75)" es mejor que "Regla 3"
- **Documente lógica compleja** - Agregue notas en el campo de descripción
- **Comience con reglas simples** - Añada complejidad gradualmente
- **Supervise el rendimiento de las reglas** - Verifique si las reglas se están usando o causando confusión
- **Evite exceso de reglas** - Demasiadas reglas ralentizan el pago, use un máximo de 5-10
- **Use zonas para geografía** - Mejor que múltiples reglas similares por país
- **Combine con métodos** - Las reglas + Métodos trabajan juntos para precios sofisticados
- **Establezca ventanas de tiempo claras** - Siempre incluya fechas de finalización para promociones
- **Pruebe casos límite** - Exactamente $50, exactamente 5 artículos, etc.