---
title: Reglas de Negocio Basadas en Ubicación
---

Las reglas de negocio basadas en ubicación le permiten tomar automáticamente acciones cuando un visitante llega desde un país, región o tipo de dispositivo específico. Puede usar reglas para establecer una moneda para clientes de una región específica, redirigir visitantes a una página localizada, mostrar un banner promocional o restringir el acceso a cierto contenido.

Las reglas se evalúan en orden de prioridad cada vez que se establece una sesión de visitante. Cuando se cumple una regla, se ejecutan inmediatamente las acciones configuradas.

## Cómo funcionan las reglas de negocio

Cada regla está compuesta de dos partes:

- **Condiciones** — los criterios que deben cumplirse para que se active la regla (por ejemplo, "el visitante es de Alemania")
- **Acciones** — lo que ocurre cuando todas las condiciones coinciden (por ejemplo, "establecer la moneda en EUR")

Las condiciones y acciones se almacenan como objetos JSON en el formulario de la regla. Spwig evalúa todas las reglas activas en orden de prioridad (de menor número a mayor) y aplica las que coincidan.

## Navegando a las reglas de negocio

Navegue a **Clientes > Reglas de Negocio** para ver todas sus reglas configuradas. La lista muestra el nombre de cada regla, su estado, su prioridad, cuántas veces se ha activado y cuándo se activó por última vez.

Haga clic en cualquier regla para verla o edita, o haga clic en **+ Agregar Regla de Negocio** para crear una nueva.

## Creando una regla de negocio

### Paso 1: información básica

Rellene los detalles de identificación de la regla:

- **Nombre** — un nombre claro y descriptivo (por ejemplo, `Establecer EUR para la Zona Euro`)
- **Descripción** — notas opcionales que explican el propósito de la regla
- **Está activo** — marque esto para habilitar la regla; desmarque para pausarla sin eliminarla
- **Prioridad** — los números más bajos se ejecutan primero; use `10`, `20`, `30` para dejar espacio para reglas futuras

### Paso 2: definir condiciones

En el campo **Condiciones**, ingrese un objeto JSON que describa cuándo debe activarse la regla. Todas las condiciones en el objeto deben ser verdaderas para que la regla coincida.

#### Claves de condición disponibles

| Condición | Formato | Ejemplo |
|-----------|--------|---------|
| `country_in` | Matriz de códigos de país ISO | `["DE", "FR", "IT"]` |
| `country_not_in` | Matriz de códigos de país ISO | `["US", "CA"]` |
| `region_in` | Matriz de nombres de región | `["Bavaria", "Cataluña"]` |
| `region_not_in` | Matriz de nombres de región | `["Quebec"]` |
| `is_mobile` | Booleano | `true` |
| `is_vpn` | Booleano | `false` |

#### Ejemplos de condiciones

Visitantes de Alemania, Francia o Italia:
```json
{
  "country_in": ["DE", "FR", "IT"]
}
```

Visitantes de Estados Unidos que están en un dispositivo móvil:
```json
{
  "country_in": ["US"],
  "is_mobile": true
}
```

Visitantes fuera de la Unión Europea:
```json
{
  "country_not_in": ["AT","BE","BG","CY","CZ","DE","DK","EE","ES","FI","FR","GR","HR","HU","IE","IT","LT","LU","LV","MT","NL","PL","PT","RO","SE","SI","SK"]
}
```

### Paso 3: definir acciones

En el campo **Acciones**, ingrese un objeto JSON que describa lo que debe ocurrir cuando se active la regla.

#### Claves de acción disponibles

| Acción | Formato | Descripción |
|--------|--------|-------------|
| `set_currency` | Cadena de código de moneda | Establezca una moneda predeterminada para el visitante |
| `set_language` | Cadena de código de idioma | Establezca el idioma de visualización |
| `show_banner` | Booleano | Active un banner promocional |
| `redirect_to` | Cadena de ruta de URL | Redirija al visitante a una URL diferente |

#### Ejemplos de acciones

Establecer moneda a Euro:
```json
{
  "set_currency": "EUR"
}
```

Redirigir a una página de aterrizaje localizada:
```json
{
  "redirect_to": "/de/"
}
```

Establecer moneda y idioma juntos:
```json
{
  "set_currency": "GBP",
  "set_language": "en"
}
```

## Ejemplos prácticos

### Ejemplo: regla de moneda de la Zona Euro

**Escenario:** Mostrar automáticamente precios en euros a visitantes de países de la Zona Euro.

| Campo | Valor |
|-------|-------|
| Nombre | `Zona Euro — Establecer EUR` |
| Prioridad | `10` |
| Está activo | Marcado |
| Condiciones | `{"country_in": ["AT","BE","DE","ES","FI","FR","GR","IE","IT","LU","NL","PT"]}` |
| Acciones | `{"set_currency": "EUR"}` |

### Ejemplo: regla de precios del Reino Unido

**Escenario:** Mostrar precios en GBP a visitantes del Reino Unido.

| Campo | Valor |
|-------|-------|
| Nombre | `UK — Establecer GBP` |
| Prioridad | `20` |
| ¿Está activo? | Marcado |
| Condiciones | `"{\"country_in\": [\"GB\"]}"` |
| Acciones | `"{\"set_currency\": \"GBP\"}"` |

### Ejemplo: redirigir a una sección de tienda localizada

**Escenario:** Enviar visitantes de Australia a una página dedicada a Australia.

| Campo | Valor |
|-------|-------|
| Nombre | `Australia — Redirigir` |
| Prioridad | `30` |
| ¿Está activo? | Marcado |
| Condiciones | `"{\"country_in\": [\"AU\"]}"` |
| Acciones | `"{\"redirect_to\": \/au\/}"` |

## Pruebas de reglas

Puedes verificar que una regla coincida con el perfil de visitante esperado sin esperar al tráfico real:

1. En la lista de reglas de negocio, seleccione la regla usando su casilla de verificación
2. Abra el **menú de Acción** y elija **Probar reglas seleccionadas**
3. Haga clic en **Ir**

Spwig evaluará la regla contra un perfil de visitante basado en EE. UU. y reportará si coincidió y qué acciones se habrían desencadenado.

## Monitoreo de la actividad de las reglas

La columna **Disparada** en la lista de reglas muestra cuántas veces se ha disparado cada regla. Haga clic en una regla para ver la marca de **Último disparo** en la sección de Estadísticas.

Use la acción **Restablecer estadísticas** para reiniciar los conteos de disparos si desea comenzar a medir desde una fecha específica después de realizar cambios en una regla.

## Consejos

- Establezca prioridades con saltos (10, 20, 30) en lugar de números secuenciales (1, 2, 3) para poder insertar nuevas reglas más tarde sin renumerar todo
- Las reglas se disparan en orden de prioridad y se aplican todas las reglas coincidentes — si dos reglas establecen la moneda, la acción de la regla con menor prioridad (número más alto) se aplicará al final
- Use el interruptor **¿Está activo?** para pausar temporalmente una regla durante promociones sin eliminar la configuración
- Siempre pruebe una nueva regla antes de activarla en un entorno en vivo para asegurarse de que las condiciones sean correctas
- La detección de VPN (`"is_vpn": true`) está disponible si desea aplicar un tratamiento diferente a los visitantes que ocultan su ubicación, pero tenga en cuenta que algunos clientes legítimos usan VPNs por privacidad