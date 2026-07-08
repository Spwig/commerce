---
title: Configuración de impuestos
---

Las tasas de impuestos definen los impuestos sobre ventas, IVA y otros impuestos de consumo aplicados en el momento del pago según la ubicación del cliente y el tipo de producto. Configure tasas a nivel de país/estado/ciudad con exenciones opcionales de categorías de productos. Spwig admite impuestos compuestos (impuesto sobre impuesto), selección de tasas basada en prioridad y grupos de configuración de impuestos preestablecidos para una rápida configuración de sistemas de impuestos regionales (IVA de la UE, impuesto sobre ventas de EE. UU.). Las tasas pueden eximir tipos de productos específicos (alimentos, libros, bienes digitales) o categorías para cumplir con las leyes fiscales locales.

Utilice la configuración de impuestos para garantizar el cumplimiento legal con los requisitos de recopilación de impuestos en sus jurisdicciones de venta.

## Configuración de tasas de impuestos

Cada tasa de impuesto define:

**Ámbito geográfico**:
- País (requerido)
- Estado/Provincia (opcional)
- Ciudad (opcional)
- Patrón de código postal (opcional, expresión regular)

**Detalles de la tasa**:
- **Tasa de impuesto**: Porcentaje (ej. 8,5%)
- **Nombre**: Nombre de visualización (ej. "Impuesto sobre ventas de California")
- **Prioridad**: La prioridad más alta gana cuando coinciden múltiples tasas
- **Activo**: Conmutador sin eliminar

**Exenciones**:
- **Tipos de productos exentos**: Bienes digitales, bienes físicos, servicios
- **Categorías exentas**: Categorías de productos específicas (Alimentos, Libros, Médico)

**Impuesto compuesto**:
- **Es compuesto**: Aplicar esta tasa sobre impuestos anteriores (impuesto sobre impuesto)
- Ejemplo: El IVA de Quebec se compone sobre el IVA general

---

## Escenarios comunes de impuestos

### Impuesto sobre ventas de EE. UU. (a nivel de estado)

```
Nombre: Impuesto sobre ventas de California
País: EE. UU.
Estado: CA
Tasa: 7,25%
Prioridad: 50
```

### IVA de la UE (a nivel de país)

```
Nombre: IVA del Reino Unido
País: GB
Tasa: 20%
Prioridad: 50

Nombre: IVA de Alemania
País: DE
Tasa: 19%
Prioridad: 50
```

### IVA/IVA provincial de Canadá (compuesto)

```
Tasa 1: IVA federal
País: CA
Tasa: 5%
Prioridad: 100
Es compuesto: No

Tasa 2: IVA de Quebec
País: CA
Estado: QC
Tasa: 9,975%
Prioridad: 50
Es compuesto: Sí  (se aplica al subtotal + IVA)
```

### Impuesto a nivel de ciudad

```
Nombre: Impuesto sobre ventas de Seattle
País: EE. UU.
Estado: WA
Ciudad: Seattle
Tasa: 10,1%
Prioridad: 100
```

---

## Exenciones de impuestos

### Exenciones de tipos de productos

Eximir tipos de productos enteros:

- **Bienes digitales**: Software, e-books, música
- **Bienes físicos**: Productos tangibles
- **Servicios**: Consultoría, instalación

Ejemplo: El IVA de la UE no se aplica a bienes digitales para consumidores (en algunos casos)

### Exenciones de categorías

Eximir categorías de productos específicas:

- Alimentos y productos de panadería (a menudo exentos o con tarifa reducida)
- Libros y materiales educativos
- Suministros médicos y medicamentos
- Ropa (algunas jurisdicciones)

Configuración:
```
Nombre: Impuesto sobre ventas de California
Tasa: 7,25%
Categorías exentas: ["Alimentos y bebidas", "Medicamentos de prescripción"]
```

---

## Grupos de configuración de impuestos preestablecidos

Carga rápida de configuraciones de impuestos comunes:

**Preestablecido de impuesto sobre ventas de EE. UU.**:
- Todos los 50 estados + DC
- Tasas a nivel de estado
- Actualización automática cuando cambien las tasas

**Preestablecido de IVA de la UE**:
- Todos los 27 estados miembros de la UE
- Tarifas estándar de IVA
- Lógica de cargo inverso para B2B

**Para usar preestablecidos**:
1. Configuración > Carrito > Configuración de impuestos preestablecidos
2. Seleccionar grupo de preestablecido (ej. "Impuesto sobre ventas de EE. UU. 2026")
3. Haga clic en "Cargar preestablecido"
4. Las tasas se importan automáticamente
5. Personalice según sea necesario

---

## Resolución de prioridad

Cuando coinciden múltiples tasas, la prioridad más alta gana:

Ejemplo:
```
Cliente en Seattle, WA:

Tasa A: Federal de EE. UU. (Prioridad 1) - 0%
Tasa B: Estado de Washington (Prioridad 50) - 6,5%
Tasa C: Ciudad de Seattle (Prioridad 100) - 3,6%

Resultado: Se aplica la tasa de Seattle (10,1% total)
```

---

## Opciones de visualización de impuestos

Configure en Configuración > Carrito > Configuración de impuestos:

- **Los precios incluyen impuestos**: Muestra los precios con impuestos incluidos (estilo de la UE)
- **Mostrar impuesto por separado**: Muestra el impuesto como elemento de línea (estilo de EE. UU.)
- **Redondear impuesto**: Por artículo o por pedido
- **Etiqueta de impuesto**: Personalizar la etiqueta ("IVA", "Impuesto sobre ventas", "IVA")

---

## Pruebas de configuración de impuestos

Antes de ir en vivo:

1. Cree pedidos de prueba desde diferentes jurisdicciones
2. Verifique que se haya aplicado la tasa de impuesto correcta
3. Compruebe que funcionen las exenciones para las categorías excluidas
4. Pruebe el cálculo de impuestos compuestos
5. Revise los elementos de impuesto en las facturas

---

## Notas de cumplimiento

- **EE. UU.**: Las reglas de nexus requieren la recopilación de impuestos en los estados donde tiene presencia física o nexus económico
- **UE**: Las empresas registradas en IVA deben recopilar IVA de clientes de la UE
- **Canadá**: IVA/HST/IVA varía por provincia
- **Consulte a un profesional fiscal**: Las leyes fiscales cambian con frecuencia, verifique los requisitos actuales

---

## Consejos

- **Use presets de impuestos** - Más rápido que la entrada manual, actualización automática
- **Monitoree los umbrales de nexus** - Trazar ventas por estado para nexus económico de EE. UU.
- **Establezca la prioridad correctamente** - Ciudad > Estado > País
- **Pruebe el impuesto compuesto** - Verifique que los cálculos coincidan con las cantidades esperadas
- **Actualice anualmente** - Las tasas de impuestos cambian, revise cada enero
- **Documente las exenciones** - Mantenga registros de por qué las categorías están exentas
- **Use nombres descriptivos** - "Impuesto sobre ventas de California 2026" es mejor que "Impuesto 1"
- **Habilite el impuesto por defecto** - Más seguro que olvidar aplicar impuesto

Remember: Preserve all markdown formatting, image paths, code blocks, and technical terms exactly as shown in the preservation rules.