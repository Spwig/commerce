---
title: Paquetes de Envío
---

# Paquetes de Envío

Los paquetes de envío definen tamaños predefinidos de cajas y sobres para el cálculo de tarifas y el empaquetado automático: especifique las dimensiones internas (espacio útil), el grosor de la pared (dimensiones externas para APIs de transportistas), límites de peso y costo de empaquetado. Los transportistas usan las dimensiones externas para calcular el peso dimensional para cotizaciones de tarifas precisas. Los paquetes tienen un orden de prioridad para algoritmos de empaquetado de cajas que seleccionan automáticamente combinaciones óptimas de paquetes para ajustarse a los artículos del carrito.

Configure paquetes al usar APIs de transportistas para tarifas en tiempo real o cuando necesite cálculos precisos de peso dimensional.

## Configuración de Paquetes

Cada paquete define:

**Dimensiones**:
- **Longitud Interna**: Espacio útil dentro (cm)
- **Ancho Interno**: Espacio útil dentro (cm)
- **Altura Interna**: Espacio útil dentro (cm)
- **Grosor de la Pared**: Grosor del material de empaquetado (cm)

**Dimensiones Externas** (calculadas automáticamente):
```
Longitud Externa = Longitud Interna + (2 × Grosor de la Pared)
Ancho Externo = Ancho Interno + (2 × Grosor de la Pared)
Altura Externa = Altura Interna + (2 × Grosor de la Pared)
```

**Peso y Costo**:
- **Peso de Tara**: Peso del paquete vacío (gramos)
- **Peso Máximo**: Capacidad de carga máxima (gramos)
- **Costo**: Costo del material de empaquetado (para optimización de costos)

**Propiedades**:
- **Nombre**: Identificador del paquete (ej. "Caja Pequeña", "Sobre Grande")
- **Tipo**: Caja o Sobre
- **Prioridad**: Orden de selección de empaquetado automático (menor = mayor prioridad)
- **Activo**: Cambiar disponibilidad

---

## ¿Por Qué Importan las Dimensiones Externas?

Los transportistas calculan **peso dimensional** a partir de las dimensiones externas:

**Fórmula del Peso Dimensional**:
```
Peso Dimensional = (Longitud × Ancho × Altura) / Divisor

Divisores Comunes:
- DHL: 5000
- FedEx/UPS: 5000 (nacional), 6000 (internacional)
```

**Ejemplo**:
```
Caja Pequeña:
Internas: 20cm × 15cm × 10cm
Grosor de la Pared: 0.5cm
Externas: 21cm × 16cm × 11cm

Peso Dimensional = (21 × 16 × 11) / 5000 = 0.74kg

Si el peso real = 0.5kg → El transportista factura a 0.74kg (peso dimensional más alto)
```

**¿Por Qué la Precisión Importa**: Dimensiones inexactas → cotizaciones de tarifas incorrectas → el cliente se ve sobrecargado o subcargado.

---

## Tamaños de Paquetes Comunes

### Sobre Pequeño con Relleno

```
Internas: 25cm × 18cm × 2cm
Grosor de la Pared: 0.3cm
Peso Máximo: 500g
Tipo: Sobre
Uso: Documentos, libros, joyas
```

### Caja Pequeña

```
Internas: 20cm × 15cm × 10cm
Grosor de la Pared: 0.5cm
Peso Máximo: 5kg
Tipo: Caja
Uso: Pequeños electrodomésticos, cosméticos, accesorios
```

### Caja Mediana

```
Internas: 30cm × 25cm × 20cm
Grosor de la Pared: 0.5cm
Peso Máximo: 15kg
Tipo: Caja
Uso: Ropa, zapatos, artículos de cocina
```

### Caja Grande

```
Internas: 45cm × 35cm × 30cm
Grosor de la Pared: 0.6cm
Peso Máximo: 30kg
Tipo: Caja
Uso: Artículos en cantidad, múltiples productos, electrodomésticos grandes
```

---

## Algoritmo de Empaquetado Automático

El sistema selecciona automáticamente paquetes para los artículos del carrito:

**Cómo Funciona**:
1. Calcule el volumen total de los artículos del carrito
2. Ordene los paquetes por prioridad (número más bajo primero)
3. Intente ajustar los artículos en un solo paquete
4. Si no cabe, intente el siguiente tamaño de paquete
5. Si ningún paquete individual cabe, combine múltiples paquetes
6. Optimice según la configuración `optimize_for`

**Modos de Optimización**:
- **Costo**: Minimizar el costo de empaquetado
- **Volumen**: Minimizar el espacio desperdiciado
- **Conteo**: Minimizar el número de paquetes

**Ejemplo**:
```
Artículos del Carrito:
- Artículo A: 10cm × 8cm × 5cm, 200g
- Artículo B: 15cm × 12cm × 8cm, 400g

Paquetes (por prioridad):
1. Caja Pequeña (20×15×10, prioridad=1)
2. Caja Mediana (30×25×20, prioridad=2)

Algoritmo:
Pruebe Caja Pequeña: Ambos artículos caben
Resultado: 1× Caja Pequeña (optimizado para conteo)
```

---

## Prioridad de Paquetes

**La prioridad determina el orden de empaquetado**:

Prioridad 1 (más alta): Se prueban primero paquetes pequeños
Prioridad 10: Paquetes grandes como último recurso

**Estrategia**:
- Paquetes pequeños = números de prioridad bajos (1-3)
- Paquetes medianos = prioridad media (4-6)
- Paquetes grandes = números de prioridad altos (7-10)

**¿Por Qué**: Comience con el paquete más pequeño, escale si es necesario → minimiza el costo de envío.

---

## Precisión del Grosor de la Pared

Mida el empaque real:

**Cómo Medir**:
1. Obtenga una caja vacía
2. Mida las dimensiones interiores (internas)
3. Mida las dimensiones exteriores (externas)
4. Calcule: `(Externa - Interna) / 2 = Grosor de la Pared`

**Ejemplo**:
```
Ancho Interno: 20cm
Ancho Externo: 21cm
Grosor de la Pared: (21 - 20) / 2 = 0.5cm
```

**Grosores Comunes**:
- Sobre con relleno: 0.2-0.4cm
- Cartón de una pared: 0.4-0.6cm
- Cartón de dos paredes: 0.8-1.0cm

---

## Crear Configuración de Paquete

**Paso a Paso**:

1. Configuración > Envío > Paquetes de Envío
2. Haga clic en "Añadir Paquete de Envío"
3. Ingrese nombre (ej. "Caja Mediana")
4. Seleccione tipo (Caja o Sobre)
5. Ingrese dimensiones internas (L × W × H en cm)
6. Ingrese grosor de la pared (cm)
7. El sistema calcula automáticamente las dimensiones externas
8. Ingrese peso de tara (peso del paquete vacío en gramos)
9. Ingrese peso máximo (capacidad de carga en gramos)
10. Opcional: Ingrese costo (para optimización de costos)
11. Establezca prioridad (1-10)
12. Active el paquete = Sí
13. Guarde

---

## Pruebas de Selección de Paquetes

**Prueba Manual**:
1. Añada productos al carrito de prueba
2. Proceda al checkout
3. Seleccione método de envío en tiempo real (usa paquetes)
4. Verifique que se devuelva una tarifa razonable
5. Revise la respuesta del transportista (los registros de API muestran paquetes seleccionados)

**Vista Previa de Empaquetado Automático**:
- Algunas cuentas de proveedores de envío muestran desglose de paquetes
- Vea qué paquetes se seleccionaron para el carrito
- Verifique el empaquetado óptimo

---

## Consejos

- **Mida con precisión** - Dimensiones inexactas → tarifas incorrectas de transportista
- **Incluya grosor de la pared** - Crítico para peso dimensional
- **Comience con 3-4 tamaños** - Pequeño, mediano, grande cubre la mayoría de los escenarios
- **Establezca pesos máximos realistas** - Capacidad de la caja, no límite teórico
- **Use la prioridad con sabiduría** - Cajas pequeñas prioridad 1, cajas grandes prioridad 10
- **Pruebe con productos reales** - Verifique que el empaquetado automático seleccione tamaños correctos
- **Actualice cuando cambie el empaquetado** - Nuevo proveedor = re-medir dimensiones
- **Considere artículos especiales** - Artículos frágiles pueden necesitar tamaños de caja específicos
- **Mantenga paquetes activos mínimos** - Demasiadas opciones ralentizan el algoritmo de empaquetado automático
- **Documente el empaquetado** - Nota qué productos encajan en qué paquetes
