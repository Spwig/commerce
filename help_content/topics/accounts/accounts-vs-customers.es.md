---
title: Cuentas vs. Clientes
---

Los comerciantes suelen preguntar: "¿Cuál es la diferencia entre una cuenta y un cliente?" Esta confusión es común porque cada cliente es una cuenta, pero no todas las cuentas son clientes. Esta guía aclarará la distinción y explicará cuándo utilizar cada interfaz de administración.

![Lista de usuarios](/static/core/admin/img/help/accounts-vs-customers/user-list.webp)

## ¿Qué es una cuenta?

Una **cuenta** es el objeto principal de autenticación en Spwig. Cualquier persona que pueda iniciar sesión en su plataforma — miembro del personal o cliente — tiene una cuenta. Las cuentas se gestionan en el sistema de autenticación de Spwig y se almacenan en el modelo `User`.

Todas las cuentas tienen:
- **Dirección de correo electrónico** — El identificador principal y credencial de inicio de sesión
- **Nombre de usuario** — Un nombre de usuario único (generado automáticamente a partir del correo electrónico por defecto)
- **Contraseña** — Hasheada y almacenada de forma segura
- **bandera is_staff** — Determina si la cuenta puede acceder al backend de administración

Las cuentas también pueden autenticarse a través de proveedores de OAuth (Google, Facebook, etc.) configurados en **Configuración > Autenticación**.

## ¿Qué es un cliente?

Un **cliente** es un tipo especial de cuenta con `is_staff=False`. Los clientes compran en su tienda en línea, realizan pedidos y gestionan sus perfiles. Cada cuenta de cliente se extiende automáticamente con:

- **CustomerProfile** — Almacena preferencias, estado de suscripción al boletín y valores de campos personalizados
- **CustomerMetrics** — Rastrea el valor de vida (LTV), puntuaciones RFM, historial de pedidos y datos de segmentación
- **OrderHistory** — Enlaces a todos los pedidos realizados por este cliente

Los clientes pueden ser:
- **Clientes registrados** — Creados a través del registro en la tienda en línea o en el administrador
- **Usuarios invitados** — Cuentas temporales creadas durante el checkout como invitado (nombre de usuario comienza con `guest_`)
- **Clientes importados** — Migrados desde otras plataformas a través de la importación CSV

## La Diferencia Principal

| Atributo | Cuenta | Cliente |
|-----------|---------|----------|
| **Propósito** | Autenticación y autorización | Compras, pedidos y análisis |
| **Ámbito** | Miembros del personal Y clientes | Solo clientes |
| **bandera is_staff** | Verdadero O Falso | Siempre Falso |
| **Datos extendidos** | Ninguno (solo campos principales) | CustomerProfile + CustomerMetrics |
| **Ubicación en el administrador** | Configuración > Usuarios | Clientes > Perfiles de clientes |
| **Puede iniciar sesión** | Sí | Sí |
| **Puede realizar pedidos** | Solo si tiene CustomerProfile | Sí |
| **Puede acceder al administrador** | Solo si is_staff=True | No |

En resumen:
- Una **cuenta** es cualquier persona que pueda iniciar sesión
- Un **cliente** es una cuenta que compra y realiza pedidos

## Los Miembros del Personal También Son Cuentas

Los miembros del personal son cuentas con `is_staff=True`. Pueden iniciar sesión en el backend de administración y realizar acciones según sus permisos de **StaffRole** asignados.

Los miembros del personal pueden tener opcionalmente un **CustomerProfile** si también compran en la tienda en línea. Por ejemplo, si usted (el comerciante) coloca un pedido de prueba en su propia tienda, se crea un CustomerProfile para su cuenta de personal. Esto NO afecta su acceso al administrador.

Los permisos de personal se controlan mediante:
- **StaffRole** — Define qué secciones y acciones del administrador puede acceder el miembro del personal
- **bandera is_superuser** — Concede acceso completo sin restricciones (use con moderación)

Gestionar miembros del personal en **Configuración > Gestión de Personal**.

## Usuarios Invitados

El checkout como invitado crea cuentas temporales con nombres de usuario generados automáticamente que comienzan con `guest_`. Estas cuentas:
- Tienen `is_staff=False` (son clientes)
- Tienen un CustomerProfile (para asociar pedidos)
- Tienen una contraseña aleatoria (el invitado no puede iniciar sesión a menos que se convierta en un cliente registrado)
- Se excluyen por defecto de los análisis de clientes

Los invitados pueden convertirse en clientes registrados mediante:
1. Crear una cuenta en la tienda en línea con el mismo correo electrónico
2. Verificar su dirección de correo electrónico
3. El sistema fusiona el historial de pedidos del invitado en la nueva cuenta registrada

Gestionar la configuración de conversión de invitados en **Configuración > Checkout > Checkout como invitado**.

## ¿Dónde Encontrar Cada Una

| Ubicación en el administrador | Qué gestionas | Casos de uso clave |
|----------------|-----------------|---------------|
| **Configuración > Usuarios** | Todas las cuentas (personal + clientes) | Restablecer contraseñas, activar/desactivar cuentas, asignar permisos de personal |
| **Configuración > Gestión de Personal** | Solo cuentas de personal (is_staff=True) | Asignar roles, gestionar el acceso de miembros del equipo, configurar permisos |
| **Clientes > Perfiles de clientes** | Solo cuentas de clientes (is_staff=False) | Ver preferencias de clientes, historial de pedidos, LTV, puntuaciones RFM, segmentos |
| **Clientes > Análisis** | Métricas y segmentos de clientes | Analizar el comportamiento de los clientes, crear segmentos de marketing, rastrear la retención |

![Lista de perfiles de clientes](/static/core/admin/img/help/accounts-vs-customers/customer-profile-list.webp)

## ¿Cuándo Usar Cada Interfaz

Use **Configuración > Usuarios** cuando necesite:
- Restablecer la contraseña de un cliente
- Desactivar una cuenta comprometida
- Crear manualmente una cuenta de cliente
- Ver conexiones de inicio de sesión de OAuth
- Ver todas las cuentas (personal + clientes) en una lista

Use **Configuración > Gestión de Personal** cuando necesite:
- Añadir un nuevo miembro del equipo
- Asignar o cambiar el rol de un miembro del personal
- Configurar permisos detallados
- Auditar los registros de actividad del personal

Use **Clientes > Perfiles de clientes** cuando necesite:
- Ver el historial de pedidos de un cliente
- Ver las preferencias del cliente y los valores de los campos personalizados
- Ver el estado de suscripción al boletín
- Revisar el LTV y las puntuaciones RFM del cliente
- Gestionar los segmentos de clientes

Use **Clientes > Análisis** cuando necesite:
- Identificar clientes de alto valor
- Crear segmentos de marketing (por ejemplo, "clientes que no han realizado un pedido en 90 días")
- Analizar tendencias del valor de vida del cliente
- Exportar listas de clientes para campañas

## Consejos

- **Los perfiles de clientes se crean automáticamente** — Cuando un cliente realiza su primer pedido (como invitado o registrado), Spwig crea un registro de CustomerProfile y CustomerMetrics para el análisis.
- **El personal también puede ser cliente** — Si un miembro del personal realiza un pedido en la tienda en línea, obtiene un CustomerProfile. Esto es normal y no afecta su acceso al administrador.
- **Las cuentas de invitados ensucian la lista de usuarios** — Use la interfaz de perfiles de clientes para enfocarse en clientes reales y comprometidos. La lista de usuarios incluye todas las cuentas de invitados.
- **Segmentar por is_staff=False** — Cuando exporte listas de clientes para campañas de correo electrónico, siempre filtre para `is_staff=False` para excluir a los miembros del equipo.
- **Las cuentas de OAuth también son cuentas** — Cuando un cliente inicia sesión a través de Google o Facebook, Spwig crea una cuenta y la vincula a su perfil de OAuth. El campo de correo electrónico se completa desde el proveedor de OAuth.