---
title: Zonas de Envío
---

Las zonas de envío definen regiones geográficas para tarifas de envío dirigidas: agrupe países, estados o códigos postales en zonas, luego vincule métodos de envío a zonas específicas para un control preciso de las tarifas. Las zonas utilizan coincidencias basadas en prioridad cuando las direcciones califican para múltiples zonas (la prioridad más alta gana). Este sistema permite estrategias de precios sofisticadas: cobrar más por áreas remotas, ofrecer envío gratuito dentro del país o proporcionar tarifas con descuento para regiones específicas.

Use zonas cuando necesite diferentes costos de envío para diferentes áreas geográficas, desde la división simple entre nacional e internacional hasta precios por niveles en múltiples regiones complejos.

## Entendiendo Zonas de Envío

**¿Qué son las zonas?**: Regiones geográficas con nombre definidas por patrones de país, estado/provincia y códigos postales.

**¿Cómo funcionan las zonas?**:
1. El cliente ingresa la dirección de envío en la caja de pago
2. El sistema evalúa todas las zonas activas
3. Las zonas que coinciden con la dirección del cliente son candidatas
4. Si múltiples zonas coinciden, la zona con mayor prioridad gana
5. Los métodos de envío vinculados a la zona ganadora se muestran
6. Los métodos no vinculados a ninguna zona (o vinculados a una zona coincidente) se muestran

**Componentes de la zona**:
- **Nombre**: Identificador de la zona (ej. "Nacional", "UE", "Áreas Remotas")
- **Países**: Lista de códigos de países incluidos (vacío = todos los países)
- **Estados/Provincias**: Restricciones de estado por país (opcional)
- **Patrones de código postal**: Patrones de expresión regular para coincidencias de códigos postales (opcional)
- **Prioridad**: Número más alto = mayor prioridad cuando coinciden múltiples zonas

---

## Lógica de coincidencia de zonas

Las zonas utilizan **estrechamiento progresivo** para coincidir con direcciones:

### Nivel 1: Coincidencia de país

**Lista de países vacía** → Zona coincide con TODOS los países

**Lista de países proporcionada** → El país de la dirección debe estar en la lista

Ejemplo:
```
Zona: "Nacional"
Países: ["US"]
→ Coincide: Cualquier dirección de EE.UU.
→ No coincide: Canadá, Reino Unido, etc.
```

### Nivel 2: Coincidencia de estado/provincia

**Ningún estado definido** → Zona coincide con TODOS los estados en los países permitidos

**Estados definidos para países específicos** → El estado de la dirección debe coincidir

Ejemplo:
```
Zona: "West Coast"
Países: ["US"]
Estados: {"US": ["CA", "OR", "WA"]}
→ Coincide: Direcciones de California, Oregon, Washington
→ No coincide: Nueva York, Texas, etc.
```

### Nivel 3: Coincidencia de códigos postales

**Ningún patrón definido** → Zona coincide con TODOS los códigos postales en los países/estados permitidos

**Patrones definidos** → El código postal de la dirección debe coincidir con al menos un patrón

Ejemplo:
```
Zona: "Metro de Los Ángeles"
Países: ["US"]
Estados: {"US": ["CA"]}
Patrones de código postal: ["^90[0-9]{3}$", "^91[0-9]{3}$"]
→ Coincide: 90001, 91210, 90245
→ No coincide: 94102 (San Francisco)
```

**Ejemplos de patrones de expresión regular**:
- `^90[0-9]{3}$` - Área de Los Ángeles (90000-90999)
- `^[A-Z][0-9][A-Z] [0-9][A-Z][0-9]$` - Formato de código postal canadiense (K1A 0B1)
- `^SW[0-9]{1,2}` - Códigos postales de Londres, Reino Unido, que comienzan con SW

---

## Selección de zona basada en prioridad

Cuando múltiples zonas coinciden con una dirección, **la prioridad** determina qué zona se aplica:

**¿Cómo funciona la prioridad?**:
- Número más alto = mayor prioridad
- Si la dirección coincide con zonas con prioridad 100 y 50, la prioridad 100 gana
- Solo los métodos de envío de la zona ganadora están disponibles

**Casos de uso**:

**Escenario 1: Específico sobrescribe general**
```
Zona A: "Áreas remotas de Alaska"
  Países: ["US"]
  Estados: {"US": ["AK"]}
  Prioridad: 100

Zona B: "EE.UU. Nacional"
  Países: ["US"]
  Prioridad: 50

Dirección: Anchorage, AK
→ Coincide con ambas zonas
→ Prioridad 100 gana
→ Se aplica la zona "Áreas remotas de Alaska" (costo de envío más alto)
```

**Escenario 2: Código postal sobrescribe estado**
```
Zona A: "Premium de Manhattan"
  Países: ["US"]
  Estados: {"US": ["NY"]}
  Patrones de código postal: ["^100[0-2][0-9]$"]
  Prioridad: 100

Zona B: "Estado de Nueva York"
  Países: ["US"]
  Estados: {"US": ["NY"]}
  Prioridad: 50

Dirección: Nueva York, NY 10001
→ Coincide con ambas zonas
→ Prioridad 100 gana
→ Se aplica "Premium de Manhattan" (servicio de entrega premium)
```

---

## Creando Zonas de Envío

**Flujo de trabajo paso a paso**:

1. **Navegue a Zonas**
   - Vaya a Configuración > Envío > Zonas de Envío
   - Haga clic en "Añadir Zona de Envío"

2. **Configuración básica**
   - **Nombre**: Identificador descriptivo (ej. "Unión Europea", "West Coast", "Áreas Remotas")
   - **Prioridad**: Establezca la importancia relativa (100 para específico, 50 para general, 1 para caída de respaldo)
   - **Activo**: Conmutador para habilitar/deshabilitar

3. **Definir cobertura geográfica**

   **Opción A: Todos los países** (dejar la lista de países vacía)
   - La zona coincide con todas las direcciones globalmente
   - Use para zonas por defecto/caída de respaldo

   **Opción B: Países específicos**
   - Haga clic en "Añadir país"
   - Seleccione países del menú desplegable (US, CA, UK, etc.)
   - Repita para todos los países incluidos

   **Opción C: Estados/Provincias específicos**
   - Después de añadir países, haga clic en "Añadir Estados" para cada país
   - Seleccione estados del menú desplegable
   - Ejemplo: US → CA, OR, WA para West Coast

   **Opción D: Patrones de código postal** (avanzado)
   - Ingrese patrones de expresión regular (uno por línea)
   - Pruebe los patrones con códigos postales de ejemplo
   - Haga clic en "Validar patrones" para verificar la sintaxis

4. **Vincular a métodos de envío**
   - Los métodos pueden vincularse cuando se edita el método (no en la configuración de la zona)
   - O vincule zonas a métodos existentes: Edite el método → Zonas de envío → Seleccione zonas

5. **Establecer prioridad de visualización**
   - Las zonas con mayor prioridad sobrescriben a las de menor prioridad cuando coinciden múltiples
   - Recomendado: Zonas específicas (100), zonas regionales (50), zona por defecto (1)

6. **Activar zona**
   - Conmutador "Activo" = Sí
   - Guardar

---

## Configuraciones de zona comunes

### Configuración 1: Nacional vs. Internacional

**Objetivo**: Diferentes tarifas para nacional vs. todos los demás países.

```
Zona 1: "Nacional"
  Países: [Código de su país]
  Prioridad: 50

Zona 2: "Internacional"
  Países: [Dejar vacío o seleccionar todos los demás países]
  Prioridad: 1
```

**Métodos de envío**:
- "Envío estándar nacional" → Vinculado a la zona nacional
- "Envío internacional" → Vinculado a la zona internacional

---

### Configuración 2: Internacional de múltiples regiones

**Objetivo**: Diferentes tarifas para UE, América del Norte, Asia, Resto del mundo.

```
Zona 1: "Unión Europea"
  Países: [AT, BE, BG, CY, CZ, DE, DK, EE, ES, FI, FR, GR, HR, HU, IE, IT, LT, LU, LV, MT, NL, PL, PT, RO, SE, SI, SK]
  Prioridad: 100

Zona 2: "América del Norte"
  Países: [US, CA, MX]
  Prioridad: 100

Zona 3: "Asia Pacífico"
  Países: [AU, CN, HK, IN, JP, KR, NZ, SG, TH, TW]
  Prioridad: 100

Zona 4: "Resto del mundo"
  Países: [Dejar vacío]
  Prioridad: 1
```

**Métodos de envío**:
- "Envío UE" → Zona UE
- "Envío América del Norte" → Zona América del Norte
- "Envío Asia Pacífico" → Zona Asia Pacífico
- "Envío internacional estándar" → Zona Resto del mundo

---

### Configuración 3: Recargo por áreas remotas

**Objetivo**: Añadir recargo para códigos postales remotos dentro de la zona nacional.

```
Zona 1: "Doméstico Remoto"
  Países: [US]
  Patrones de código postal: ["^99[0-9]{3}$", "^96[7-9][0-9]{2}$"]  # Alaska, Hawaii
  Prioridad: 100

Zona 2: "Doméstico Estándar"
  Países: [US]
  Prioridad: 50
```

**Métodos de envío**:
- "Envío remoto" → Zona doméstico remoto (costo más alto)
- "Envío estándar" → Zona doméstico estándar

---

### Configuración 4: Zonas específicas de estado

**Objetivo**: Diferentes tarifas para cada región de EE.UU.

```
Zona 1: "West Coast"
  Países: [US]
  Estados: {"US": ["CA", "OR", "WA"]}
  Prioridad: 100

Zona 2: "East Coast"
  Países: [US]
  Estados: {"US": ["NY", "NJ", "CT", "MA", "PA"]}
  Prioridad: 100

Zona 3: "Midwest"
  Países: [US]
  Estados: {"US": ["IL", "IN", "OH", "MI", "WI"]}
  Prioridad: 100

Zona 4: "South"
  Países: [US]
  Estados: {"US": ["TX", "FL", "GA", "NC", "SC"]}
  Prioridad: 100

Zona 5: "Otros estados de EE.UU."
  Países: [US]
  Prioridad: 50
```

---

## Ejemplos de patrones de código postal

Los códigos postales utilizan **regex** (expresiones regulares) para coincidir con patrones:

### Estados Unidos (Códigos ZIP)

**Formato**: 5 dígitos (ej. 90210)

```
California (90000-96199):  ^9[0-6][0-9]{3}$
New York (10000-14999):    ^1[0-4][0-9]{3}$
Texas (75000-79999, 88500-88599):  ^(7[5-9]|885)[0-9]{2}$
Alaska (99500-99999):      ^99[5-9][0-9]{2}$
```

### Canadá (Códigos postales)

**Formato**: A1A 1A1 (letra-número-letra espacio número-letra-número)

```
Todos los códigos postales canadienses:  ^[A-Z][0-9][A-Z] [0-9][A-Z][0-9]$ 
Ontario (K, L, M, N, P):    ^[KLMNP][0-9][A-Z] [0-9][A-Z][0-9]$ 
Quebec (G, H, J):           ^[GHJ][0-9][A-Z] [0-9][A-Z][0-9]$ 
```

### Reino Unido (Códigos postales)

**Formato**: AA1A 1AA o A1A 1AA

```
London (E, EC, N, NW, SE, SW, W, WC):  ^(E|EC|N|NW|SE|SW|W|WC)[0-9]{1,2}
Manchester (M):                        ^M[0-9]{1,2}
Birmingham (B):                        ^B[0-9]{1,2}
```

### Australia (Códigos postales)

**Formato**: 4 dígitos (ej. 2000)

```
New South Wales (1000-2999):  ^[12][0-9]{3}$
Victoria (3000-3999, 8000-8999):  ^[38][0-9]{3}$
Queensland (4000-4999, 9000-9999):  ^[49][0-9]{3}$
```

### Pruebas de patrones

**Antes de guardar patrones**, pruebe con códigos postales conocidos:

1. Ingrese patrón: `^90[0-9]{3}$`
2. Entrada de prueba: "90210" → Debería coincidir
3. Entrada de prueba: "10001" → Debería NO coincidir
4. Entrada de prueba: "9021" → Debería NO coincidir (solo 4 dígitos)

Use testadores de expresiones regulares en línea (regex101.com) para validar patrones complejos.

---

## Resumen de cobertura de zonas

Las zonas muestran **resumen de cobertura** en la vista de lista del administrador, mostrando qué está incluido:

**Ejemplos**:
- "Todos los países" → Sin restricciones de país
- "US, CA, MX" → 3 países
- "US (CA, OR, WA)" → EE.UU. con 3 estados
- "US (90xxx-91xxx)" → EE.UU. con patrones de código postal

**Use el resumen para**:
- Verificar rápidamente la cobertura de la zona sin abrir
- Detectar superposiciones o lagunas en la cobertura
- Revisar la configuración de la zona a primera vista

---

## Vinculando zonas a métodos de envío

Las zonas y los métodos tienen **relación muchos a muchos**:

**Desde el lado del método** (Recomendado):
1. Edite el método de envío
2. Desplácese hasta la sección "Zonas de envío"
3. Seleccione las zonas aplicables (selección múltiple)
4. Guarde el método

**Desde el lado de la zona**:
- Las zonas no vinculan directamente a métodos
- El vinculo siempre se hace desde la configuración del método

**Comportamiento método-zona**:

**Ninguna zona vinculada** → Método disponible para TODAS las direcciones

**Zonas vinculadas** → Método solo disponible si la dirección del cliente coincide con al menos una zona vinculada

**Ejemplo**:
```
Método: "Envío estándar nacional"
Zonas vinculadas: ["EE.UU. Nacional"]
→ Solo se muestra a direcciones de EE.UU.

Método: "Envío internacional express"
Zonas vinculadas: ["UE", "Asia Pacífico", "Resto del mundo"]
→ Se muestra a todas las direcciones no de EE.UU.
```

---

## Pruebas de coincidencia de zonas

Antes de ir en vivo, pruebe la configuración de zonas:

1. **Crear pedidos de prueba**
   - Use direcciones en diferentes zonas
   - Verifique coincidencias de zonas correctas

2. **Verificar resolución de prioridad**
   - Use una dirección que coincida con múltiples zonas
   - Verifique que la zona con mayor prioridad gane
   - Confirme que aparezcan los métodos de envío esperados

3. **Probar casos límite**
   - Códigos postales de frontera (ej. 90999 vs 91000)
   - Límites de estado
   - Direcciones internacionales con códigos postales similares

4. **Usar herramienta de vista previa de zona** (si está disponible)
   - Ingrese una dirección de prueba
   - Veá cual(es) zona(s) coinciden
   - Vea la resolución de prioridad

---

## Solución de problemas

**Problema 1: No hay métodos de envío disponibles en el checkout**

**Causas**:
- La dirección del cliente no coincide con ninguna zona
- Todos los métodos están vinculados a zonas que no coinciden
- No existen métodos sin restricciones de zona

**Solución**:
- Cree una zona de respaldo (todos los países, prioridad 1)
- O quite las restricciones de zona de al menos un método
- Verifique los patrones de país/estado/código postal de la zona

---

**Problema 2: Coincidencia de zona incorrecta**

**Causas**:
- Se selecciona una zona con menor prioridad a pesar de que una con mayor prioridad coincide
- Error de sintaxis en el patrón de código postal (el patrón falla silenciosamente)
- Mismatch de código de estado (CA vs California)

**Solución**:
- Verifique los valores de prioridad (número más alto = mayor prioridad)
- Pruebe los patrones de código postal con validador de expresiones regulares
- Use códigos de estado de dos letras (CA, no California)

---

**Problema 3: Método inesperado mostrado**

**Causas**:
- El método no tiene zonas vinculadas (disponible en todas partes)
- Múltiples zonas coinciden, la zona inesperada tiene mayor prioridad
- La cobertura de la zona se superpone accidentalmente

**Solución**:
- Revise las zonas vinculadas al método
- Verifique la prioridad de las zonas coincidentes
- Revisa el resumen de cobertura de zonas para superposiciones

---

## Consejos

- **Empiece con 2 zonas** - Nacional e internacional, expanda según sea necesario
- **Use la prioridad con sabiduría** - Zonas específicas 100, regionales 50, respaldo 1
- **Pruebe los patrones de código postal exhaustivamente** - Los errores de regex fallan silenciosamente, causando que las zonas no coincidan
- **Documente la lógica de la zona** - Añada notas a la descripción de la zona explicando la intención de cobertura
- **Evite zonas excesivas** - Demasiadas zonas complican la configuración; use reglas de envío para escenarios complejos
- **Use códigos de estado, no nombres** - "CA" no "California", "NY" no "New York"
- **Cree una zona de respaldo** - Todos los países, prioridad 1, asegura que siempre haya al menos una opción de envío disponible
- **Monitorea el rendimiento de las zonas** - Si muchos clientes ven "no hay envío disponible", revise la cobertura de zonas
- **Actualice las zonas para nuevas regiones** - Añada países a la zona UE cuando nuevos miembros se unan
- **Use nombres descriptivos** - "UE (Excluyendo el Reino Unido)" es mejor que "Zona 3"
- **Pruebe con direcciones reales** - Use direcciones reales de clientes durante las pruebas, no inventadas

Recuerde: Preserve todo el formato markdown, rutas de imágenes, bloques de código y términos técnicos exactamente como se muestran en las reglas de preservación.