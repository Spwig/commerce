<p align="center">
  <a href="README.md">English</a> |
  <a href="README.fr.md">Français</a> |
  <strong>Español</strong> |
  <a href="README.de.md">Deutsch</a> |
  <a href="README.ja.md">日本語</a> |
  <a href="README.zh-Hans.md">简体中文</a> |
  <a href="README.zh-Hant.md">繁體中文</a> |
  <a href="README.pt.md">Português</a> |
  <a href="README.ru.md">Русский</a> |
  <a href="README.ar.md">العربية</a> |
  <a href="README.hi.md">हिन्दी</a> |
  <a href="README.id.md">Bahasa Indonesia</a> |
  <a href="README.it.md">Italiano</a> |
  <a href="README.ko.md">한국어</a> |
  <a href="README.tr.md">Türkçe</a> |
  <a href="README.vi.md">Tiếng Việt</a> |
  <a href="README.th.md">ไทย</a>
</p>

<p align="center">
  <img src="https://spwig.com/images/logo.svg" alt="Spwig" width="200">
</p>

<h1 align="center">Spwig</h1>

<p align="center">
  <strong>E-commerce autoalojado para comerciantes que quieren ser dueños de su tienda.</strong>
</p>

<p align="center">
  <a href="https://spwig.com">Sitio web</a> &nbsp;•&nbsp;
  <a href="https://docs.spwig.com">Documentación</a> &nbsp;•&nbsp;
  <a href="https://community.spwig.com">Comunidad</a> &nbsp;•&nbsp;
  <a href="https://spwig.com/es/marketplace">Marketplace</a> &nbsp;•&nbsp;
  <a href="https://spwig.com/es/demos">Demos en vivo</a>
</p>

<p align="center">
  <a href="LICENSE"><img alt="Licence: AGPL v3" src="https://img.shields.io/badge/licence-AGPL--3.0-blue.svg"></a>
  <a href="https://github.com/Spwig/commerce/actions"><img alt="CI" src="https://img.shields.io/github/actions/workflow/status/Spwig/commerce/test.yml?branch=main&label=tests"></a>
  <a href="https://github.com/Spwig/commerce/releases"><img alt="Release" src="https://img.shields.io/github/v/release/Spwig/commerce"></a>
  <a href="https://github.com/Spwig/commerce/discussions"><img alt="Discussions" src="https://img.shields.io/github/discussions/Spwig/commerce"></a>
</p>

## ¿Qué es Spwig?

Spwig es una plataforma de e-commerce completa: catálogo, carrito, checkout,
pedidos, clientes, pagos, envíos, temas, constructor de páginas, API de
administración, POS, suscripciones, fidelización, blog, SEO — todo el stack.
Construida con **Django 5**, **PostgreSQL** y **Redis**, se distribuye como
un conjunto de contenedores Docker y corre en un VPS de 5 dólares o sobre
tu propio hardware.

A diferencia de las plataformas alojadas, **eres dueño del código, de la
base de datos y de los datos de tus clientes.** Sin comisiones por
transacción. Sin ataduras. Si quieres hacer un fork y seguir tu propio
camino, la licencia lo permite explícitamente.

<br />

## Ediciones

Mismo binario. Un archivo de licencia firmado activa banderas de
funcionalidades en tiempo de ejecución. Community es lo que obtienes por
defecto al ejecutar `docker compose up`; actualizar es una clave que pegas
en el administrador.

| | Community | Pro | Enterprise |
|---|:---:|:---:|:---:|
| E-commerce completo, temas, constructor de páginas, UI de POS | ✓ | ✓ | ✓ |
| Proveedores de pago propios | ✓ | ✓ | ✓ |
| Proveedores de envío propios | ✓ | ✓ | ✓ |
| Acceso al Marketplace (temas e integraciones premium) | ✓ | ✓ | ✓ |
| Autocompletado de direcciones alojado por Spwig | Gratis · con límite de uso | Límite mayor | Límite máximo |
| GeoIP alojado por Spwig (ubicación del visitante) | Gratis · con límite de uso | Límite mayor | Límite máximo |
| Notificaciones push (app de administración iOS) | Gratis · con límite de uso | Límite mayor | Límite máximo |
| Punto de venta (soporte de terminal POS) | ✓ | ✓ | ✓ |
| Pasarela de correo alojada con IP calentadas + DKIM | – | ✓ | ✓ |
| Soporte prioritario | – | ✓ | ✓ |
| SSO empresarial (Azure AD, Okta) | – | – | ✓ |

<br />

## Inicio rápido

### Opción 1 — Instalación en una línea (recomendada)

El [instalador de Spwig](https://github.com/Spwig/spwig) configura todo
con un solo comando: Docker, PostgreSQL, Redis, MinIO, TLS mediante
Cloudflare o autofirmado, asistente de primer arranque y usuario
administrador. Las imágenes firmadas se descargan desde
`registry.spwig.com`.

```bash
curl -fsSL https://spwig.com/install.sh | sudo bash
```

Las actualizaciones se hacen desde el administrador — consulta
[UPGRADING.md](UPGRADING.md).

### Opción 2 — Desde el código fuente

Quieres compilar desde este repositorio, modificarlo o publicar un fork:

```bash
git clone https://github.com/Spwig/commerce.git spwig
cd spwig
cp .env.example .env
docker compose up -d
docker compose exec web ./manage.py migrate --noinput
docker compose exec web ./manage.py createsuperuser
```

Tienda en `http://localhost`, administrador en `http://localhost/es/admin/`.
La edición Community se autoactiva en el primer arranque — sin llamadas
a un servidor de licencias, sin clave requerida. Actualiza más tarde con
`git pull` y `docker compose build`.

<br />

## Funcionalidades

<table>
  <tr>
    <td width="50%" valign="top">
      <h3>Tienda y checkout</h3>
      <p>Renderizada en el servidor por defecto — tiempo de respuesta
      rápido, funciona sin JavaScript, con enfoque mobile-first (el 80%
      del tráfico llega desde pantallas pequeñas). Modo headless opcional
      mediante el
      <a href="https://github.com/Spwig/headless-sdk">SDK headless de
      Spwig</a> y los <a href="https://github.com/Spwig/react">componentes
      de React</a>.</p>
    </td>
    <td width="50%" valign="top">
      <img src="https://spwig.com/images/screenshots/storefront-product.webp" alt="Storefront product page">
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <img src="https://spwig.com/images/screenshots/page-builder.webp" alt="Page builder">
    </td>
    <td width="50%" valign="top">
      <h3>Constructor de páginas</h3>
      <p>Los comerciantes arman las páginas de la tienda con widgets
      reutilizables — secciones hero, cuadrículas de productos,
      testimonios, embeds — y las previsualizan en vivo desde el
      administrador. Los widgets se instalan desde el marketplace o desde
      tu propio repositorio de componentes.</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>Gestión de pedidos y clientes</h3>
      <p>Cada pedido, reembolso, renovación de suscripción, descarga
      digital y punto de contacto con el cliente en un solo lugar.
      Operaciones masivas, roles de personal con permisos acotados,
      exportación a CSV/XLSX, app de administración móvil (iOS) con
      notificaciones push.</p>
    </td>
    <td width="50%" valign="top">
      <img src="https://spwig.com/images/screenshots/order-management.webp" alt="Order management">
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <img src="https://spwig.com/images/screenshots/branding-builder.webp" alt="Branding builder">
    </td>
    <td width="50%" valign="top">
      <h3>Temas y branding</h3>
      <p>Los tokens de diseño (colores, tipografía, espaciados) gobiernan
      cada superficie — tanto la tienda como el administrador. Cambia un
      token y todo se actualiza. Los temas viven en
      <a href="https://github.com/Spwig/components">Spwig/components</a>
      y se instalan desde el marketplace; crea los tuyos con el
      <a href="https://github.com/Spwig/theme-sdk">theme SDK</a>.</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>Punto de venta</h3>
      <p>Terminal POS completa para comerciantes con tienda física:
      escaneo de códigos de barras, pagos divididos, impresión de
      tickets, integración con cajón portamonedas, pantalla orientada al
      cliente y modo offline. La edición Community incluye el código,
      pero la superficie de administración muestra un CTA de mejora —
      si haces un fork y lo eliminas, no hay problema.</p>
    </td>
    <td width="50%" valign="top">
      <img src="https://spwig.com/images/screenshots/pos-terminal.webp" alt="POS terminal">
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <img src="https://spwig.com/images/screenshots/developer-portal.webp" alt="Developer portal">
    </td>
    <td width="50%" valign="top">
      <h3>Ecosistema de proveedores</h3>
      <p>Todo lo que se comunica con un sistema externo — pagos, envíos,
      tipos de cambio, traducción, GeoIP, SMS, correo — es un proveedor
      enchufable. Crea el tuyo con los
      <a href="https://github.com/Spwig/provider-sdks">SDK de proveedores</a>,
      publícalo en el marketplace o autoaloja un registro privado.</p>
    </td>
  </tr>
</table>

<br />

## Arquitectura

- **Single-tenant.** Cada instalación es una tienda, un comerciante, un
  Django Site. Los comerciantes con varias tiendas ejecutan una
  instalación de Spwig por tienda.
- **Monolito modular.** No es una malla de microservicios. Un único
  proceso de Django atiende la tienda + el administrador + la API REST +
  los workers de Celery. Simple de desplegar, de razonar y de hacer un
  fork.
- **Compuertas de funcionalidades en runtime.** Community/Pro/Enterprise
  ejecutan el mismo binario. Una licencia firmada activa las banderas —
  sin borrar código.

Recorrido completo: [ARCHITECTURE.md](ARCHITECTURE.md).

<br />

## Comunidad y soporte

- **Discussions.** Preguntas abiertas, ideas, demostraciones:
  [github.com/Spwig/commerce/discussions](https://github.com/Spwig/commerce/discussions).
- **Foro de la comunidad.** [community.spwig.com](https://community.spwig.com)
  — hilos extensos, recetas de buenas prácticas y muestras de extensiones.
- **Reportes de bugs.** [Issues](https://github.com/Spwig/commerce/issues)
  con pasos de reproducción. Consulta [SECURITY.md](SECURITY.md) para
  la divulgación de vulnerabilidades.
- **Soporte comercial.** Disponible para licencias Pro y Enterprise.

<br />

## Contribuir

Usamos **DCO** (Developer Certificate of Origin) — cada commit se firma
con `git commit -s`. Sin papeleo, sin CLA. Guía completa en
[CONTRIBUTING.md](CONTRIBUTING.md).

Las notas para asistentes de código con IA que trabajen en el repositorio
están en [CLAUDE.md](CLAUDE.md).

<br />

## Ecosistema

Proyectos open-source relacionados bajo la [organización Spwig](https://github.com/Spwig):

| Repo | De qué se trata |
|---|---|
| [Spwig/commerce](https://github.com/Spwig/commerce) | Este repositorio — la plataforma principal (AGPL-3.0-or-later) |
| [Spwig/spwig](https://github.com/Spwig/spwig) | Instalador en una línea |
| [Spwig/components](https://github.com/Spwig/components) | Temas, integraciones y utilidades (AGPL-3.0-or-later) |
| [Spwig/theme-sdk](https://github.com/Spwig/theme-sdk) | SDK para crear temas (Apache-2.0) |
| [Spwig/provider-sdks](https://github.com/Spwig/provider-sdks) | SDK para crear proveedores de pago / envío / etc. (Apache-2.0) |
| [Spwig/headless-sdk](https://github.com/Spwig/headless-sdk) | SDK cliente headless / API (Apache-2.0) |
| [Spwig/react](https://github.com/Spwig/react) | Librería de componentes React (Apache-2.0) |

<br />

## Licencia

Spwig se distribuye bajo [AGPL-3.0-or-later](LICENSE). Puedes ejecutarlo,
modificarlo, distribuirlo y ofrecerlo como servicio alojado — todo está
permitido. Las versiones modificadas ofrecidas a través de una red deben
poner su código fuente a disposición de los usuarios. Ese es justamente
el propósito de AGPL frente a GPL.

Las integraciones de proveedores construidas con los SDK son Apache-2.0,
por lo que crear una integración propietaria de pago / envío / SMS sobre
los SDK no activa AGPL. Esto es intencional — queremos un ecosistema de
proveedores próspero.

<br />

## Privacidad y telemetría

Spwig envía un ping anónimo al día a `updates.spwig.com/api/v1/telemetry/`:

- UUID de instalación (generado en el primer arranque, almacenado localmente)
- Versión de Spwig
- Edición (community / pro / enterprise / trial / dev)
- País (resuelto a partir de la IP en el ingreso; la IP no se almacena)
- Recuentos agrupados de banderas de funcionalidades (proveedores de pago
  configurados, temas instalados) — nunca datos crudos de clientes ni de
  pedidos

**Desactívalo** con `SPWIG_TELEMETRY=0` en tu entorno. Eso invierte
`settings.SPWIG_TELEMETRY_ENABLED` y la tarea diaria queda sin efecto.

<br />

<p align="center">
  <sub>
    Hecho con dedicación en Singapur.
    <br />
    <a href="https://spwig.com">spwig.com</a> — <a href="https://docs.spwig.com">docs</a> — <a href="https://community.spwig.com">comunidad</a>
  </sub>
</p>
