---
title: Métodos de envío
---

Los métodos de envío son las opciones de entrega orientadas al cliente que se muestran en la caja de pago; cada método calcula los costos de envío utilizando diferentes estrategias de precios. Spwig admite 7 tipos de métodos que van desde tarifas planas simples hasta precios en tiempo real calculados por transportistas complejos. Los métodos pueden restringirse según el valor mínimo/máximo del pedido, el peso y las zonas geográficas. Los clientes seleccionan su método preferido durante el pago, y el costo calculado se agrega al total del pedido.

Use esta guía para configurar métodos de envío que coincidan con su modelo de negocio, desde envíos con tarifas planas básicas hasta precios por niveles basados en zonas sofisticados.

## Tipos de métodos de envío

Spwig proporciona 7 tipos de métodos de envío, cada uno con diferentes lógicas de cálculo de costos:

### Envío con tarifa plana

**¿Qué es**: costo fijo independientemente del contenido del carrito, destino o peso.

**¿Cuándo usarlo**:
- Tiendas simples con costos de envío predecibles
- Un solo tipo de producto (tamaño/peso similar)
- Solo envío nacional con tarifas estándar de transportista
- Promociones de envío gratuito (use con reglas de envío)

**Configuración**:
- Establezca **Tipo de método** = Tarifa plana
- Ingrese **Costo fijo** (p. ej., $9.99)
- Opcional: Establezca restricciones de valor mínimo/máximo del pedido

**Ejemplo**: "Envío estándar - $9.99" para todos los pedidos nacionales.

---

### Envío gratuito

**¿Qué es**: opción de envío sin costo (ningún cargo para el cliente).

**¿Cuándo usarlo**:
- Promociones de envío gratuito
- Pedidos de alto valor (combine con valor mínimo del pedido)
- Alternativa de recogida local
- Beneficios del programa de fidelidad

**Configuración**:
- Establezca **Tipo de método** = Envío gratuito
- Opcional: Establezca **Valor mínimo del pedido** (p. ej., gratuito sobre $50)
- Funciona bien con reglas de envío para envío gratuito condicional

**Ejemplo**: "Envío gratuito en pedidos superiores a $50" con min_order_value = $50.

---

### Envío basado en peso

**¿Qué es**: costo calculado a partir de una tabla de tarifas por niveles basada en el peso total del carrito.

**¿Cuándo usarlo**:
- Productos con pesos variables (libros, hardware, productos de supermercado)
- Modelos de tarifas de transportistas basados en peso
- Relación predecible de peso a costo

**Configuración**:
1. Establezca **Tipo de método** = Basado en peso
2. Cree **Tabla de tarifas de envío** con basis_type = "weight"
3. Agregue **Niveles de tarifas de envío** (p. ej., 0-5kg = $10, 5-10kg = $15, 10-20kg = $25)
4. Opcional: Restringir a zonas específicas

**Ejemplo**:
```
0-2kg: $8
2-5kg: $12
5-10kg: $18
10kg+: $25
```

**¿Cómo funciona**: El carrito calcula el peso total → encuentra el nivel coincidente → devuelve la tarifa del nivel.

---

### Envío basado en precio

**¿Qué es**: costo calculado a partir de una tabla de tarifas por niveles basada en el subtotal del carrito.

**¿Cuándo usarlo**:
- El costo de envío se correlaciona con el valor del pedido
- Incentivar valores más altos del carrito (tarifa más baja por dólar en niveles más altos)
- Alternativa simple al basado en peso para artículos de precios similares

**Configuración**:
1. Establezca **Tipo de método** = Basado en precio
2. Cree **Tabla de tarifas de envío** con basis_type = "price"
3. Agregue **Niveles de tarifas de envío** (p. ej., $0-$50 = $9.99, $50-$100 = $14.99, $100+ = $19.99)

**Ejemplo**:
```
$0-$25: $6.99
$25-$75: $9.99
$75-$150: $12.99
$150+: Gratis
```

**¿Cómo funciona**: El carrito calcula el subtotal → encuentra el nivel coincidente → devuelve la tarifa del nivel.

---

### Tarifas en tiempo real de transportista

**¿Qué es**: tarifas en vivo obtenidas de APIs de transportistas (FedEx, UPS, DHL) en la caja de pago.

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
5. Opcional: Agregar porcentaje de markup o markup fijo

**Requisitos**:
- Cuenta activa del transportista (FedEx, UPS, DHL, etc.)
- Credenciales de API del transportista
- Paquetes de envío definidos (para cálculo de peso dimensional)

**Ejemplo**: El método "FedEx Ground" obtiene tarifas en vivo de FedEx basadas en el peso del carrito, dimensiones y destino en la caja de pago.

**¿Cómo funciona**:
1. El cliente ingresa la dirección en la caja de pago
2. El sistema llama a la API del transportista con el origen, destino, dimensiones del paquete y peso
3. El transportista devuelve la cotización de tarifa
4. Se aplica un markup opcional
5. La tarifa se muestra al cliente

---

### Recogida local

**¿Qué es**: el cliente recoge el pedido en una ubicación física (sin costo de entrega).

**¿Cuándo usarlo**:
- Tiendas minoristas que ofrecen recogida
- Opciones de recogida en almacén
- Eventos o puestos de mercado
- Eliminar costos de envío para clientes locales

**Configuración**:
1. Establezca **Tipo de método** = Recogida local
2. Cree **Ubicación** (Configuración > Envío > Ubicaciones)
   - Establezca la dirección, horas de operación, capacidad de recogida
3. Vincule ubicación(es) al método
4. Opcional: Establezca el tiempo de preparación de recogida (p. ej., "Listo en 2 horas")

**Experiencia del cliente**:
- Selecciona "Recogida local" en la caja de pago
- Elige la ubicación de recogida (si hay varias)
- Elige la fecha/hora de recogida según la disponibilidad
- Recibe una notificación cuando el pedido esté listo

**Ejemplo**: "Recogida en tienda - Gratis" con 3 ubicaciones minoristas, listo dentro de 24 horas.

---

### Envío por tabla de tarifas

**¿Qué es**: precios por niveles flexibles basados en peso, precio o cantidad con objetivo de zonas avanzado.

**¿Cuándo usarlo**:
- Precios complejos (diferentes tarifas por zona Y peso)
- Necesita más control que solo basado en peso o precio
- Múltiples factores de precios (p. ej., peso + destino + cantidad)

**Configuración**:
1. Establezca **Tipo de método** = Tabla de tarifas
2. Cree **Tabla de tarifas de envío**
3. Defina **basis_type**: peso, precio o cantidad
4. Agregue **Niveles de tarifas de envío** con valores mínimos/máximos
5. Opcional: Restringir niveles a zonas o países específicos

**Diferencia con basado en peso/precio**: La tabla de tarifas admite restricciones geográficas por nivel, permitiendo diferentes tarifas para el mismo peso/precio en diferentes zonas.

**Ejemplo**:
```
Zona A (Nacional):
  0-5kg: $10
  5-10kg: $15

Zona B (Remota):
  0-5kg: $18
  5-10kg: $25
```

**¿Cómo funciona**: El carrito calcula el valor de base (peso/precio/cantidad) → encuentra el nivel coincidente para la zona del cliente → devuelve la tarifa del nivel.

---

## Configuración de métodos de envío

Todos los métodos de envío comparten estas configuraciones comunes:

### Configuración básica

- **Nombre**: identificador interno (no se muestra a los clientes)
- **Nombre de visualización**: nombre orientado al cliente en la caja de pago (p. ej., "Envío estándar", "Envío exprés")
- **Descripción**: texto de ayuda opcional mostrado en la caja de pago (p. ej., "Entrega en 3-5 días hábiles")
- **Tipo de método**: uno de los 7 tipos mencionados anteriormente
- **Activo**: conmutador para habilitar/deshabilitar el método sin eliminarlo

### Configuración de costos

- **Costo fijo**: solo para métodos de tarifa plana
- **Tabla de tarifas**: para métodos basados en peso, precio, tabla de tarifas
- **Cuenta del proveedor**: para métodos de tarifas en tiempo real de transportista
- **Clase de impuesto**: aplicar impuesto al costo de envío (si aplica)

### Restricciones

**Restricciones de valor del pedido**:
- **Valor mínimo del pedido**: el método solo está disponible si el subtotal del carrito es ≥ cantidad (p. ej., envío gratuito sobre $50)
- **Valor máximo del pedido**: el método se oculta si el subtotal del carrito > cantidad (p. ej., tarifa plana solo para pedidos inferiores a $100)

**Restricciones de peso**:
- **Peso mínimo**: el método solo está disponible si el peso del carrito es ≥ cantidad
- **Peso máximo**: el método se oculta si el peso del carrito > cantidad (común para opciones de envío de bajo peso)

**Restricciones geográficas**:
- **Zonas de envío**: vincule el método a zonas específicas (nacionales, internacionales, regionales)
- Zonas vacías = disponible para todas las direcciones
- Múltiples zonas = disponible para cualquier zona coincidente

### Configuración avanzada

- **Prioridad**: orden de visualización en la caja de pago (número más bajo = más alto en la lista)
- **Tarifa de manejo**: tarifa adicional plana agregada al costo calculado
- **Umbral de envío gratuito**: establezca automáticamente el costo a $0 si el subtotal del carrito ≥ umbral (alternativa al min_order_value)

---

## Crear un método de envío

**Flujo de trabajo paso a paso**:

1. **Navegue a Métodos de envío**
   - Vaya a Configuración > Carrito > Métodos de envío
   - Haga clic en "Añadir método de envío"

2. **Elija el tipo de método**
   - Seleccione el tipo adecuado según su estrategia de precios
   - El tipo determina los campos de configuración de costo disponibles

3. **Configure la información básica**
   - Nombre: referencia interna (p. ej., "domestic_ground")
   - Nombre de visualización: orientado al cliente (p. ej., "Envío terrestre")
   - Descripción: período de entrega (p. ej., "5-7 días hábiles")

4. **Establezca el cálculo de costos**
   - **Tarifa plana**: ingrese costo fijo
   - **Peso/Precio/Tabla de tarifas**: cree tabla de tarifas (ver a continuación)
   - **En tiempo real**: vincule cuenta del proveedor
   - **Gratuito/Recogida**: no se necesita configuración de costo

5. **Agregue restricciones (opcional)**
   - Valor mínimo/máximo del pedido
   - Peso mínimo/máximo
   - Zonas de envío

6. **Establezca la prioridad**
   - Números más bajos aparecen primero en la caja de pago
   - Recomendado: Gratis (1), Recogida local (2), Estándar (3), Exprés (4)

7. **Active el método**
   - Conmutador "Activo" = Sí
   - Guardar

---

## Crear tablas de tarifas

Para métodos basados en peso, precio y tabla de tarifas:

**Paso 1: Crear tabla de tarifas**
- Vaya a Configuración > Envío > Tablas de tarifas
- Haga clic en "Añadir tabla de tarifas"
- Establezca **Nombre** (p. ej., "Tiers de peso nacional")
- Establezca **Tipo de base**: peso, precio o cantidad

**Paso 2: Añadir niveles**
- Haga clic en "Añadir nivel"
- Establezca **Valor mínimo** y **Valor máximo** (rango para coincidir)
- Establezca **Tarifa** (costo para este nivel)
- Opcional: Restringir a zonas o países específicos
- Guardar nivel

**Paso 3: Repetir para todos los niveles**
- Cubra el rango completo (0 a valor máximo esperado)
- Asegúrese de no tener lagunas (p. ej., 0-5, 5-10, 10-20, 20+)
- Use `null` para el valor máximo en el último nivel (ilimitado)

**Paso 4: Vincular a método de envío**
- Edite el método de envío
- Seleccione la tabla de tarifas desde el menú desplegable
- Guardar

**Ejemplo de tabla basada en peso**:
```
Nombre: Tiers de peso nacional
Base: Peso

Niveles:
1. Mín: 0g, Máx: 2000g, Tarifa: $8
2. Mín: 2000g, Máx: 5000g, Tarifa: $12
3. Mín: 5000g, Máx: 10000g, Tarifa: $18
4. Mín: 10000g, Máx: null, Tarifa: $25
```

---

## Escenarios de envío comunes

### Escenario 1: Envío nacional básico

**Objetivo**: tarifa plana de $9.99 para todos los pedidos nacionales.

**Solución**:
- Tipo de método: Tarifa plana
- Costo fijo: $9.99
- Zona de envío: "Nacional" (solo su país)

---

### Escenario 2: Envío gratuito sobre $50

**Objetivo**: incentivar valores más altos del carrito con umbral de envío gratuito.

**Solución Opción A** (Recomendada):
- Tipo de método: Envío gratuito
- Valor mínimo del pedido: $50
- Nombre de visualización: "Envío gratuito (Pedidos $50+)")

**Solución Opción B** (Usando reglas):
- Tipo de método: Tarifa plana
- Costo fijo: $9.99
- Cree regla de envío:
  - Condición: Valor del carrito ≥ $50
  - Acción: Establecer costo a $0

---

### Escenario 3: Envío basado en peso nacional + internacional

**Objetivo**: diferentes tarifas para nacional vs internacional basadas en peso.

**Solución**:
1. Cree 2 zonas: "Nacional", "Internacional"
2. Cree 2 tablas de tarifas: "Tarifas de peso nacional", "Tarifas de peso internacional"
3. Cree 2 métodos:
   - "Envío nacional" → vincula a zona nacional + tabla de tarifas nacional
   - "Envío internacional" → vincula a zona internacional + tabla de tarifas internacional

---

### Escenario 4: Opciones de múltiples transportistas

**Objetivo**: permitir que los clientes elijan entre FedEx Ground, FedEx Express, UPS Ground.

**Solución**:
1. Cree cuenta del proveedor para API de FedEx
2. Cree cuenta del proveedor para API de UPS
3. Cree 3 métodos en tiempo real:
   - "FedEx Ground" → proveedor FedEx, código de servicio = "FEDEX_GROUND"
   - "FedEx Express" → proveedor FedEx, código de servicio = "FEDEX_EXPRESS"
   - "UPS Ground" → proveedor UPS, código de servicio = "UPS_GROUND"
4. Todos los 3 métodos consultan APIs de transportista en la caja de pago y muestran tarifas en vivo

---

### Escenario 5: Recogida local + envío

**Objetivo**: tienda minorista ofrece opciones de recogida y envío.

**Solución**:
1. Cree ubicación: "Tienda principal" con dirección, horas, tiempo de preparación
2. Cree 2 métodos:
   - "Recogida local" → tipo de recogida local, vincula a ubicación de tienda principal
   - "Envío estándar" → tarifa plana $9.99
3. Los clientes ven ambas opciones en la caja de pago

---

## Pruebas de métodos de envío

Antes de lanzar, pruebe todos los métodos:

1. **Crear carrito de prueba**
   - Añadir productos con diversos pesos/precios
   - Proceder a la caja de pago

2. **Probar cada método**
   - Ingresar direcciones en diferentes zonas
   - Verificar que los métodos correctos aparezcan
   - Comprobar que los costos calculados coincidan con las expectativas

3. **Probar restricciones**
   - Añadir artículos hasta alcanzar el valor mínimo del pedido → verificar que el envío gratuito aparezca
   - Añadir artículos pesados → verificar que los niveles basados en peso funcionen
   - Probar restricciones de zona → verificar que los métodos se oculten para zonas excluidas

4. **Probar métodos en tiempo real** (si aplica)
   - Usar credenciales de prueba del proveedor
   - Verificar que las tarifas se devuelvan correctamente
   - Comprobar la precisión de la tarifa contra el sitio web del transportista

---

## Solución de problemas

**Problema 1: El método no aparece en la caja de pago**

**Causas**:
- El método no está activo
- El carrito no cumple con el valor mínimo/máximo del pedido
- El carrito no cumple con el peso mínimo/máximo
- La dirección del cliente no coincide con ninguna zona vinculada
- No hay niveles de tabla de tarifas que cubran el peso/precio del carrito

**Solución**: Verificar restricciones, verificar el estado activo, asegurarse de que las zonas/niveles cubran la situación del cliente.

---

**Problema 2: Tarifas en tiempo real fallando**

**Causas**:
- Credenciales de API inválidas
- Cuenta del proveedor inactiva
- No se han definido paquetes de envío (el transportista necesita dimensiones)
- No se ha establecido la dirección de origen
- API del transportista caída

**Solución**: Probar conexión del proveedor, verificar credenciales, asegurarse de que los paquetes estén configurados, verificar la dirección de origen en la configuración.

---

**Problema 3: Costo calculado incorrecto**

**Causas**:
- Las tablas de tarifas tienen lagunas o superposiciones
- Los valores mínimos/máximos de nivel están en unidades incorrectas (gramos vs kg)
- Tarifa de manejo agregada inesperadamente
- Regla de envío modificando el costo

**Solución**: Revisar tablas de tarifas, verificar unidades, revisar prioridad de reglas de envío.

---

## Consejos

- **Empiece simple** - Use tarifa plana para el primer método, agregue complejidad según sea necesario
- **Pruebe exhaustivamente** - Verifique que todos los métodos funcionen en entorno de pruebas antes de habilitar en producción
- **Use nombres descriptivos** - "Envío estándar (5-7 días)" es mejor que "Método 1"
- **Establezca tiempos de entrega realistas** - Subestime, sobreentregue para la satisfacción del cliente
- **Ofrezca recogida si es posible** - Reduce costos de envío, mejora la conveniencia del cliente
- **Monitorea la fiabilidad de la API del transportista** - Tenga una tarifa plana como respaldo si fallan las tarifas en tiempo real
- **Use zonas para envío internacional** - Diferentes tarifas por región evitan pérdidas en destinos costosos
- **Combine con reglas de envío** - Las reglas añaden lógica condicional (promociones de envío gratuito, recargos para áreas remotas)
- **Mantenga los métodos limitados** - 2-4 opciones en la caja de pago evita la parálisis de decisión
- **Actualice las tablas de tarifas estacionalmente** - Las tarifas de transportista cambian, revise anualmente
- **Use la prioridad con sabiduría** - Coloque opciones gratuitas/cheaper primero, opciones costosas al final
