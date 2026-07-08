---
title: Configuraciones predeterminadas de transportista
---

Las configuraciones predeterminadas de transportista definen transportistas manuales (DHL, FedEx, UPS, transportistas personalizados) para envíos creados sin integración de API. Cada configuración predeterminada proporciona un logotipo del transportista, una plantilla de URL de seguimiento y ajustes de visualización. Las configuraciones predeterminadas del sistema (DHL, FedEx, UPS, USPS) están preconfiguradas y no se pueden eliminar, mientras que las configuraciones personalizadas permiten a los comerciantes agregar transportistas regionales o especializados. Las configuraciones predeterminadas se vinculan a envíos manuales donde los comerciantes ingresan números de seguimiento manualmente en lugar de comprar etiquetas a través de APIs de proveedores.

Use las configuraciones predeterminadas de transportista al crear envíos manuales o cuando desee enlaces de seguimiento sin una integración completa de API.

## Configuraciones predeterminadas del sistema vs. personalizadas

**Configuraciones predeterminadas del sistema** (preinstaladas):
- DHL, FedEx, UPS, USPS, Royal Mail, Canada Post, Australia Post
- No se pueden eliminar (is_system=True)
- Se puede sobrescribir la URL de seguimiento o el logotipo
- Plantillas de URL de seguimiento predeterminadas proporcionadas

**Configuraciones predeterminadas personalizadas** (creadas por el comerciante):
- Transportistas regionales (OnTrac, LaserShip, correo regional)
- Transportistas especializados (transporte de mercancías, entrega de tipo blanquito)
- Se pueden editar o eliminar
- Se requiere una plantilla de URL de seguimiento manual

---

## Configuración de configuraciones predeterminadas de transportista

Cada configuración predeterminada define:

**Configuración básica**:
- **Nombre**: Nombre de visualización del transportista (ej. "DHL Express", "Correos locales")
- **Código**: Identificador interno (ej. "dhl", "local_courier")
- **Logotipo**: Imagen del logotipo del transportista (opcional, se usa el icono si no se proporciona)
- **Icono**: Icono FontAwesome como alternativa (ej. "fa-truck")
- **Activo**: Conmutador de visibilidad

**Configuración de seguimiento**:
- **Plantilla de URL de seguimiento**: Patrón de URL con marcador de posición {tracking_id}
- **Sobrescribir URL de seguimiento**: URL personalizada (sobrescribe la plantilla predeterminada)

**Configuración del sistema** (solo para configuraciones predeterminadas del sistema):
- **Es sistema**: No se puede eliminar
- **Es predeterminada**: Una predeterminada por tipo de transportista

---

## Plantillas de URL de seguimiento

Las URLs de seguimiento usan el marcador de posición {tracking_id}:

**Ejemplos**:

DHL: `https://www.dhl.com/en/express/tracking.html?AWB={tracking_id}`

FedEx: `https://www.fedex.com/fedextrack/?tracknumbers={tracking_id}`

UPS: `https://www.ups.com/track?tracknum={tracking_id}`

USPS: `https://tools.usps.com/go/TrackConfirmAction?tLabels={tracking_id}`

Personalizado: `https://track.localcourier.com/tracking/{tracking_id}`

**Cómo funciona**:
1. El comerciante crea un envío con el número de seguimiento "1234567890"
2. El sistema reemplaza {tracking_id} con el número real
3. El cliente hace clic en el enlace de seguimiento → se redirige al sitio del transportista
4. Resultado: `https://www.dhl.com/en/express/tracking.html?AWB=1234567890`

---

## Crear configuración predeterminada de transportista personalizado

**Paso a paso**:

1. Navegue a **Configuración > Envío > Configuraciones predeterminadas de transportista**
2. Haga clic en "Añadir configuración predeterminada de transportista"
3. Ingrese el nombre (ej. "OnTrac")
4. Ingrese el código (slug: "ontrac")
5. Opcional: Suba una imagen de logotipo
6. Seleccione un icono (fa-truck, fa-shipping-fast, etc.)
7. Ingrese la plantilla de URL de seguimiento con {tracking_id}
8. Active el conmutador = Sí
9. Guarde

**Ejemplo - OnTrac**:
```
Nombre: OnTrac
Código: ontrac
URL de seguimiento: https://www.ontrac.com/tracking.asp?tracking_number={tracking_id}
Icono: fa-truck
Activo: Sí
```

---

## Sobrescribir URLs de seguimiento de configuraciones predeterminadas del sistema

Las configuraciones predeterminadas del sistema pueden tener sobrescrituras de URL de seguimiento:

**Caso de uso**: Su cuenta de transportista tiene un portal de seguimiento especial

**Cómo sobrescribir**:
1. Edite la configuración predeterminada del sistema (ej. DHL)
2. Ingrese la URL de sobrescritura en el campo "Sobrescribir URL de seguimiento"
3. La sobrescritura tiene prioridad sobre la plantilla predeterminada
4. Guarde

**Ejemplo**:
```
Sistema: DHL
URL predeterminada: https://www.dhl.com/en/express/tracking.html?AWB={tracking_id}
URL de sobrescritura: https://track.dhl.com/special-account/{tracking_id}
Resultado: Se usa la URL de sobrescritura para todos los envíos DHL
```

---

## Logotipos de transportistas

**Directrices para logotipos**:
- Formato: PNG o SVG (se prefiere SVG por escalabilidad)
- Tamaño: 200×60px recomendado
- Fondo: Transparente o blanco
- Color: Marca completa del transportista

**Icono alternativo**:
Si no se sube un logotipo, el sistema muestra un icono FontAwesome:
- fa-truck (predeterminado)
- fa-shipping-fast (expreso)
- fa-plane (transporte aéreo)
- fa-box (paquete)

---

## Usar configuraciones predeterminadas de transportista en envíos

Al crear un envío manual:

1. Órdenes > Detalles de la orden > Crear envío
2. Seleccione el modo "Envío manual"
3. Elija el transportista desde el menú desplegable de configuraciones predeterminadas
4. Ingrese el número de seguimiento
5. Opcional: Sobrescriba la URL de seguimiento para este envío
6. Guarde

**Visualización del envío**:
- Se muestra el logotipo del transportista (o icono)
- Se muestra el número de seguimiento
- Enlace de seguimiento clickeable (usa la plantilla de URL predeterminada)

---

## Transportista predeterminado

Una configuración predeterminada puede establecerse como predeterminada por sistema:

**Caso de uso**: El transportista más comúnmente usado se selecciona automáticamente al crear un envío

**Cómo establecer**:
1. Edite la configuración predeterminada del transportista
2. Marque "Es predeterminada"
3. Guarde
4. La predeterminada anterior (si existe) se desactiva automáticamente

**Solo se permite una predeterminada** - al establecer una nueva predeterminada, se elimina la bandera de la predeterminada anterior.

---

## Consejos

- **Use nombres descriptivos** - "DHL Express" es mejor que "DHL"
- **Pruebe URLs de seguimiento** - Verifique que la plantilla funcione con números de seguimiento reales
- **Suba logotipos de transportistas** - Apariencia profesional en correos electrónicos a clientes
- **No elimine configuraciones predeterminadas del sistema** - Están correctamente preconfiguradas
- **Use sobrescrituras con moderación** - Solo cuando el transportista cambie su sistema de seguimiento
- **Establezca predeterminada para el transportista principal** - Ahorra tiempo al crear envíos
- **Mantenga las configuraciones predeterminadas activas** - Solo desactive si el transportista deja de operar
- **Documente transportistas personalizados** - Añada notas sobre transportistas regionales
