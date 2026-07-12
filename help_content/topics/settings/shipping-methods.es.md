---
title: Métodos de envío
---

Los métodos de envío son las opciones de entrega orientadas al cliente que se muestran durante el proceso de pago—cada método calcula los costos de envío utilizando diferentes estrategias de precios. Spwig admite 7 tipos de métodos que van desde tarifas planas simples hasta precios en tiempo real calculados por transportistas complejos. Los métodos pueden restringirse según el valor mínimo/máximo del pedido, el peso y las zonas geográficas. Los clientes seleccionan su método preferido durante el pago, y el costo calculado se agrega al total del pedido.

Use esta guía para configurar métodos de envío que coincidan con su modelo de negocio, desde envíos con tarifas planas básicas hasta precios basados en zonas sofisticados.

## Tipos de métodos de envío

Spwig proporciona 7 tipos de métodos de envío, cada uno con lógica diferente para el cálculo de costos:

### Envío con tarifa plana

**¿Qué es**: Costo fijo independientemente del contenido del carrito, destino o peso.

**¿Cuándo usarlo**:
- Tiendas simples con costos de envío predecibles
- Un solo tipo de producto (tamaño/peso similar)
- Envío nacional solo con tarifas estándar de transportistas
- Promociones de envío gratuito (use con promociones de envío)

**Configuración**:
- Establezca **Tipo de método** = Tarifa plana
- Ingrese **Costo fijo** (p. ej., $9.99)
- Opcional: Establezca restricciones de valor mínimo/máximo del pedido

**Ejemplo**: "Envío estándar - $9.99" para todos los pedidos nacionales.

---

### Envío gratuito

**¿Qué es**: Opción de envío sin costo (sin cargo para el cliente).

**¿Cuándo usarlo**:
- Promociones de envío gratuito
- Pedidos de alto valor (combine con valor mínimo del pedido)
- Alternativa de recogida local
- Beneficios de programas de lealtad

**Configuración**:
- Establezca **Tipo de método** = Envío gratuito
- Opcional: Establezca **Valor mínimo del pedido** (p. ej., gratuito sobre $50)
- Funciona bien con promociones de envío para envío gratuito condicional

**Ejemplo**: "Envío gratuito en pedidos superiores a $50" con min_order_value = $50.

---

### Envío basado en peso

**¿Qué es**: Costo calculado a partir de una tabla de tarifas por tramos basada en el peso total del carrito.

**¿Cuándo usarlo**:
- Productos con pesos variables (libros, hardware, alimentos)
- Modelos de precios de transportistas basados en peso
- Relación predecible entre peso y costo

**Configuración**:
1. Establezca **Tipo de método** = Basado en peso
2. Cree **Tabla de tarifas de envío** con basis_type = "weight"
3. Agregue **Tramos de tarifas de envío** (p. ej., 0-5kg = $10, 5-10kg = $15, 10-20kg = $25)
4. Opcional: Restringir a zonas específicas

**Ejemplo**:
```
0-2kg: $8
2-5kg: $12
5-10kg: $18
10kg+: $25
```

**Cómo funciona**: El carrito calcula el peso total → encuentra el tramo coincidente → devuelve la tarifa del tramo.

---

### Envío basado en precio

**¿Qué es**: Costo calculado a partir de una tabla de tarifas por tramos basada en el subtotal del carrito.

**¿Cuándo usarlo**:
- Costo de envío correlacionado con el valor del pedido
- Incentivar valores más altos del carrito (tarifa más baja por dólar en tramos más altos)
- Alternativa simple al basado en peso para artículos con precios similares

**Configuración**:
1. Establezca **Tipo de método** = Basado en precio
2. Cree **Tabla de tarifas de envío** con basis_type = "price"
3. Agregue **Tramos de tarifas de envío** (p. ej., $0-$50 = $9.99, $50-$100 = $14.99, $100+ = $19.99)

**Ejemplo**:
```
$0-$25: $6.99
$25-$75: $9.99
$75-$150: $12.99
$150+: Gratis
```

**Cómo funciona**: El carrito calcula el subtotal → encuentra el tramo coincidente → devuelve la tarifa del tramo.

---

### Tarifas de transportista en tiempo real

**¿Qué es**: Tarifas en vivo obtenidas de las APIs de transportistas (FedEx, UPS, DHL) durante el pago.

**¿Cuándo usarlo**:
- Costos de envío variables según el destino
- Opciones múltiples de transportistas para los clientes
- Precios exactos de transportistas sin tablas de tarifas manuales
- Envío internacional con precios complejos

**Configuración**:
1. Establezca **Tipo de método** = En tiempo real
2. Cree **Cuenta del proveedor** (Configuración > Envío > Cuentas de proveedores)
3. Ingrese las credenciales de la API del transportista (número de cuenta, clave de API, secreto)
4. Vincule la cuenta del proveedor al método de envío
5. Opcional: Agregue un porcentaje de markup o markup fijo

**Requisitos**:
- Cuenta activa del transportista (FedEx, UPS, DHL, etc.)
- Credenciales de API del transportista
- Paquetes de envío definidos (para cálculo de peso dimensional)



**Ejemplo**: El método "FedEx Ground" obtiene tarifas en vivo de FedEx basadas en el peso del carrito, dimensiones y destino en el momento del pago.

**Cómo funciona**:
1. El cliente ingresa su dirección en el momento del pago
2. El sistema llama a la API del transportista con el origen, destino, dimensiones del paquete y peso
3. El transportista devuelve la cotización de tarifa
4. Aplicación opcional de margen de beneficio
5. La tarifa se muestra al cliente

---

### Recogida en tienda

**¿Qué es?**: El cliente recoge su pedido en una ubicación física (sin costo de envío).

**¿Cuándo usarlo?**:
- Tiendas minoristas que ofrecen recogida
- Opciones de recogida en almacén
- Eventos o puestos de mercado
- Eliminar costos de envío para clientes locales

**Configuración**:
1. Establecer **Tipo de método** = Recogida en tienda
2. Crear **Ubicación** (Configuración > Envío > Ubicaciones)
   - Establecer dirección, horario de atención, capacidad de recogida
3. Vincular ubicación(es) al método
4. Opcional: Establecer tiempo de preparación de recogida (ej. "Listo en 2 horas")

**Experiencia del cliente**:
- Elige "Recogida en tienda" en el momento del pago
- Elige la ubicación de recogida (si hay varias)
- Elige la fecha/hora de recogida según la disponibilidad
- Recibe una notificación cuando el pedido esté listo

**Ejemplo**: "Recogida en tienda - Gratis" con 3 ubicaciones minoristas, listo dentro de 24 horas.

---

### Envío por tabla de tarifas

**¿Qué es?**: Precios flexibles por tramos basados en peso, precio o cantidad con objetivo de zona avanzado.

**¿Cuándo usarlo?**:
- Precios complejos (diferentes tarifas por zona Y peso)
- Necesidad de más control que solo basado en peso o precio
- Varios factores de precios (ej. peso + destino + cantidad)

**Configuración**:
1. Establecer **Tipo de método** = Envío por tabla de tarifas
2. Crear **Tabla de tarifas de envío**
3. Definir **basis_type**: peso, precio o cantidad
4. Añadir **Tramos de tarifas de envío** con valores mínimos/máximos
5. Opcional: Restringir tramos a zonas o países específicos

**Diferencia con basado en peso/precio**: La tabla de tarifas admite restricciones geográficas por tramo, permitiendo diferentes tarifas para el mismo peso/precio en diferentes zonas.

**Ejemplo**:
```
Zona A (Nacional):
  0-5kg: $10
  5-10kg: $15

Zona B (Remota):
  0-5kg: $18
  5-10kg: $25
```

**Cómo funciona**: El carrito calcula el valor de base (peso/precio/cantidad) → encuentra el tramo coincidente para la zona del cliente → devuelve la tarifa del tramo.

---

## Configuración del método de envío

Todos los métodos de envío comparten estas configuraciones comunes:

### Configuración básica

- **Nombre**: Identificador interno (no se muestra a los clientes)
- **Nombre para mostrar**: Nombre visible para el cliente en el momento del pago (ej. "Envío estándar", "Envío exprés")
- **Descripción**: Texto de ayuda opcional mostrado en el momento del pago (ej. "Entrega en 3-5 días hábiles")
- **Tipo de método**: Uno de los 7 tipos anteriores
- **Activo**: Conmutador para habilitar/deshabilitar el método sin eliminarlo

### Configuración de costos

- **Costo fijo**: Solo para métodos de tarifa plana
- **Tabla de tarifas**: Para métodos basados en peso, basados en precio, basados en tabla de tarifas
- **Cuenta del proveedor**: Para métodos de envío en tiempo real con transportistas
- **Clase de impuesto**: Aplicar impuesto al costo de envío (si aplica)

### Restricciones

**Restricciones de valor del pedido**:
- **Valor mínimo del pedido**: El método solo está disponible si el subtotal del carrito es ≥ cantidad (ej. envío gratis por encima de $50)
- **Valor máximo del pedido**: El método se oculta si el subtotal del carrito > cantidad (ej. tarifa plana solo para pedidos por debajo de $100)

**Restricciones de peso**:
- **Peso mínimo**: El método solo está disponible si el peso del carrito es ≥ cantidad
- **Peso máximo**: El método se oculta si el peso del carrito > cantidad (común para opciones de envío para artículos ligeros)

**Restricciones geográficas**:
- **Zonas de envío**: Vincular el método a zonas específicas (nacionales, internacionales, regionales)
- Zonas vacías = disponible para todas las direcciones
- Varias zonas = disponible para cualquier zona coincidente

### Configuración avanzada

- **Prioridad**: Orden de visualización en el momento del pago (número más bajo = más arriba en la lista)
- **Tarifa de manejo**: Tarifa plana adicional añadida al costo calculado
- **Umbral de envío gratis**: Establecer automáticamente el costo a $0 si el subtotal del carrito ≥ umbral (alternativa al min_order_value)

---

## Crear un método de envío

**Flujo de trabajo paso a paso**:

1. **Navegar a Métodos de envío**
   - Ir a Configuración > Carrito > Métodos de envío
   - Hacer clic en "Añadir método de envío"

2. **Elegir tipo de método**
   - Seleccione el tipo adecuado según su estrategia de precios
   - El tipo determina los campos de configuración de costos disponibles

3. **Configurar información básica**
   - Nombre: Referencia interna (ej. "domestic_ground")
   - Nombre para mostrar: Dirigido al cliente (ej. "Envío por Tierra")
   - Descripción: Plazo de entrega (ej. "5-7 días hábiles")

4. **Establecer cálculo de costos**
   - **Tarifa fija**: Ingrese un costo fijo
   - **Peso/Precio/Tarifa por tabla**: Cree una tabla de tarifas (ver más abajo)
   - **En tiempo real**: Vincule la cuenta del proveedor
   - **Gratis/Retiro en tienda**: No se requiere configuración de costos

5. **Agregar restricciones (opcional)**
   - Valor mínimo/máximo del pedido
   - Peso mínimo/máximo
   - Zonas de envío

6. **Establecer prioridad**
   - Los números más bajos aparecen primero en la caja de pago
   - Orden recomendado: Gratis (1), Retiro local (2), Estándar (3), Express (4)

7. **Activar método**
   - Cambie el interruptor "Activo" a Sí
   - Guardar

---

## Crear tablas de tarifas

Para métodos basados en peso, precio y tarifas por tabla:

**Paso 1: Crear tabla de tarifas**
- Vaya a Configuración > Envío > Tablas de tarifas
- Haga clic en "Añadir tabla de tarifas"
- Establezca **Nombre** (ej. "Domestic Weight Tiers")
- Establezca **Tipo de base**: peso, precio o cantidad

**Paso 2: Añadir tramos**
- Haga clic en "Añadir tramo"
- Establezca **Valor mínimo** y **Valor máximo** (rango para coincidir)
- Establezca **Tarifa** (costo para este tramo)
- Opcional: Restringir a zonas o países específicos
- Guardar tramo

**Paso 3: Repetir para todos los tramos**
- Cubra el rango completo (0 al valor máximo esperado)
- Asegúrese de no tener lagunas (ej. 0-5, 5-10, 10-20, 20+)
- Use `null` para el valor máximo en el tramo final (ilimitado)

**Paso 4: Vincular a método de envío**
- Edite el método de envío
- Seleccione la tabla de tarifas del menú desplegable
- Guardar

**Ejemplo de tabla basada en peso**:
```
Nombre: Domestic Weight Tiers
Base: Peso

Tramos:
1. Mín: 0g, Máx: 2000g, Tarifa: $8
2. Mín: 2000g, Máx: 5000g, Tarifa: $12
3. Mín: 5000g, Máx: 10000g, Tarifa: $18
4. Mín: 10000g, Máx: null, Tarifa: $25
```

---

## Escenarios de envío comunes

### Escenario 1: Envío doméstico básico

**Objetivo**: Tarifa fija de $9.99 para todos los pedidos domésticos.

**Solución**:
- Tipo de método: Tarifa fija
- Costo fijo: $9.99
- Zona de envío: "Doméstico" (solo su país)

---

### Escenario 2: Envío gratis por encima de $50

**Objetivo**: Fomentar valores de carrito más altos con umbral de envío gratis.

**Opción de solución A** (Recomendada):
- Tipo de método: Envío gratis
- Valor mínimo del pedido: $50
- Nombre para mostrar: "Envío gratis (Pedidos $50+)")

**Opción de solución B** (Usando reglas):
- Tipo de método: Tarifa fija
- Costo fijo: $9.99
- Crear promoción de envío:
  - Condición: Valor del carrito ≥ $50
  - Acción: Establecer costo a $0

---

### Escenario 3: Envío basado en peso doméstico + internacional

**Objetivo**: Diferentes tarifas para doméstico vs internacional basado en peso.

**Solución**:
1. Cree 2 zonas: "Doméstico", "Internacional"
2. Cree 2 tablas de tarifas: "Domestic Weight", "International Weight"
3. Cree 2 métodos:
   - "Envío doméstico" → vincula a zona doméstica + tabla de peso doméstico
   - "Envío internacional" → vincula a zona internacional + tabla de peso internacional

---

### Escenario 4: Opciones de múltiples proveedores

**Objetivo**: Permitir a los clientes elegir entre FedEx Ground, FedEx Express, UPS Ground.

**Solución**:
1. Cree cuenta de proveedor para API de FedEx
2. Cree cuenta de proveedor para API de UPS
3. Cree 3 métodos en tiempo real:
   - "FedEx Ground" → proveedor FedEx, código de servicio = "FEDEX_GROUND"
   - "FedEx Express" → proveedor FedEx, código de servicio = "FEDEX_EXPRESS"
   - "UPS Ground" → proveedor UPS, código de servicio = "UPS_GROUND"
4. Todos los 3 métodos consultan APIs de proveedores en la caja de pago y muestran tarifas en vivo

---

### Escenario 5: Retiro local + envío

**Objetivo**: Tienda minorista ofrece opciones de retiro y envío.

**Solución**:
1. Cree ubicación: "Tienda principal" con dirección, horarios y tiempo de preparación
2. Cree 2 métodos:
   - "Retiro local" → tipo de retiro local, vincula a ubicación de tienda principal
   - "Envío estándar" → tarifa fija $9.99
3. Los clientes ven ambas opciones en la caja de pago

---

## Pruebas de métodos de envío

Antes de lanzar, pruebe todos los métodos:

1. **Crear carrito de prueba**
   - Añadir productos con diversos pesos/precios
   - Proceder al checkout

2. **Probar cada método**
   - Ingresar direcciones en diferentes zonas
   - Verificar que los métodos correctos aparezcan
   - Comprobar que los costos calculados coincidan con las expectativas

3. **Probar restricciones**
   - Añadir artículos hasta alcanzar el valor mínimo de pedido → verificar que el envío gratuito aparezca
   - Añadir artículos pesados → verificar que las escalas basadas en peso funcionen
   - Probar restricciones de zona → verificar que los métodos estén ocultos para zonas excluidas

4. **Probar métodos en tiempo real** (si aplica)
   - Usar credenciales de prueba del transportista
   - Verificar que las tasas se devuelvan con éxito
   - Comprobar la precisión de las tasas contra el sitio web del transportista

---

## Solución de problemas

**Problema 1: Método no aparece en el checkout**

**Causas**:
- El método está inactivo
- El carrito no cumple con el valor mínimo/máximo de pedido
- El carrito no cumple con el peso mínimo/máximo
- La dirección del cliente no coincide con ninguna zona vinculada
- No hay escalas de tabla de tasas que cubran el peso/precio del carrito

**Solución**: Verificar restricciones, verificar el estado activo, asegurarse de que las zonas/escalas cubran la situación del cliente.

---

**Problema 2: Tasas en tiempo real fallando**

**Causas**:
- Credenciales de API inválidas
- Cuenta del proveedor inactiva
- No se han definido paquetes de envío (el transportista necesita dimensiones)
- No se ha establecido la dirección de origen
- API del transportista caída

**Solución**: Probar la conexión con el proveedor, verificar las credenciales, asegurarse de que los paquetes estén configurados, verificar la dirección de origen en la configuración.

---

**Problema 3: Costo calculado incorrecto**

**Causas**:
- Las escalas de la tabla de tasas tienen vacíos o superposiciones
- Los valores mínimos/máximos de las escalas están en unidades incorrectas (gramos vs kg)
- Se añade una tarifa de manejo inesperadamente
- Una regla de envío está modificando el costo

**Solución**: Revisar las escalas de la tabla de tasas, verificar las unidades, verificar la prioridad de las promociones de envío.

---

## Consejos

- **Comenzar sencillo** - Usar tarifa plana para el primer método, añadir complejidad según sea necesario
- **Probar exhaustivamente** - Verificar que todos los métodos funcionen en entorno de pruebas antes de habilitarlos en producción
- **Usar nombres descriptivos** - "Envío estándar (5-7 días)" es mejor que "Método 1"
- **Establecer tiempos de entrega realistas** - Subestimar, superar para la satisfacción del cliente
- **Ofrecer recogida si es posible** - Reduce costos de envío, mejora la comodidad del cliente
- **Monitorear la fiabilidad de la API del transportista** - Tener una tarifa plana como respaldo si las tasas en tiempo real fallan
- **Usar zonas para internacional** - Diferentes tasas por región evitan pérdidas en destinos costosos
- **Combinar con promociones de envío** - Las reglas añaden lógica condicional (promociones de envío gratuito, recargos para áreas remotas)
- **Mantener los métodos limitados** - 2-4 opciones en el checkout previenen la parálisis de decisión
- **Actualizar las tablas de tasas estacionalmente** - Las tasas de los transportistas cambian, revisar anualmente
- **Usar la prioridad con sabiduría** - Colocar opciones gratuitas/baratas primero, opciones costosas al final