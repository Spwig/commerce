<p align="center">
  <a href="README.md">English</a> |
  <a href="README.fr.md">Français</a> |
  <a href="README.es.md">Español</a> |
  <a href="README.de.md">Deutsch</a> |
  <a href="README.ja.md">日本語</a> |
  <a href="README.zh-Hans.md">简体中文</a> |
  <a href="README.zh-Hant.md">繁體中文</a> |
  <a href="README.pt.md">Português</a> |
  <strong>Русский</strong> |
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
  <strong>Самостоятельно размещаемая платформа электронной коммерции для продавцов, которые хотят владеть своим магазином.</strong>
</p>

<p align="center">
  <a href="https://spwig.com">Сайт</a> &nbsp;•&nbsp;
  <a href="https://docs.spwig.com">Документация</a> &nbsp;•&nbsp;
  <a href="https://community.spwig.com">Сообщество</a> &nbsp;•&nbsp;
  <a href="https://spwig.com/ru/marketplace">Маркетплейс</a> &nbsp;•&nbsp;
  <a href="https://spwig.com/ru/demos">Живые демо</a>
</p>

<p align="center">
  <a href="LICENSE"><img alt="Licence: AGPL v3" src="https://img.shields.io/badge/licence-AGPL--3.0-blue.svg"></a>
  <a href="https://github.com/Spwig/commerce/actions"><img alt="CI" src="https://img.shields.io/github/actions/workflow/status/Spwig/commerce/test.yml?branch=main&label=tests"></a>
  <a href="https://github.com/Spwig/commerce/releases"><img alt="Release" src="https://img.shields.io/github/v/release/Spwig/commerce"></a>
  <a href="https://github.com/Spwig/commerce/discussions"><img alt="Discussions" src="https://img.shields.io/github/discussions/Spwig/commerce"></a>
</p>

## Что такое Spwig?

Spwig — это полнофункциональная платформа электронной коммерции: каталог, корзина,
оформление заказа, заказы, клиенты, платежи, доставка, темы, конструктор страниц, административный API,
POS, подписки, программы лояльности, блог, SEO — весь стек целиком. Построена на
**Django 5**, **PostgreSQL** и **Redis**, поставляется как набор Docker-контейнеров,
работает на VPS за $5 или на вашем собственном железе.

В отличие от размещённых у поставщика платформ, **вы владеете кодом, базой данных и
данными клиентов.** Никаких комиссий за транзакции. Никакой привязки к вендору. Если вы захотите
сделать форк и пойти своим путём, лицензия явно это разрешает.

<br />

## Редакции

Один и тот же бинарный файл. Подписанный лицензионный файл переключает флаги функций во время выполнения.
Community — это то, что вы получаете по умолчанию при запуске `docker compose up`;
обновление — это ключ, который вы вставляете в админку.

| | Community | Pro | Enterprise |
|---|:---:|:---:|:---:|
| Полная электронная коммерция, темы, конструктор страниц, интерфейс POS | ✓ | ✓ | ✓ |
| Собственные платёжные провайдеры | ✓ | ✓ | ✓ |
| Собственные провайдеры доставки | ✓ | ✓ | ✓ |
| Доступ к маркетплейсу (премиум-темы + интеграции) | ✓ | ✓ | ✓ |
| Автозаполнение адресов на серверах Spwig | Бесплатно · с ограничением скорости | Более высокий лимит | Максимальный лимит |
| GeoIP на серверах Spwig (местоположение посетителя) | Бесплатно · с ограничением скорости | Более высокий лимит | Максимальный лимит |
| Push-уведомления (админ-приложение iOS) | Бесплатно · с ограничением скорости | Более высокий лимит | Максимальный лимит |
| Точка продаж (поддержка терминала POS) | – | ✓ | ✓ |
| Размещённый email-шлюз с прогретыми IP + DKIM | – | ✓ | ✓ |
| Приоритетная поддержка | – | ✓ | ✓ |
| Корпоративный SSO (Azure AD, Okta) | – | – | ✓ |

<br />

## Быстрый старт

### Вариант 1 — Установка одной командой (рекомендуется)

[Установщик Spwig](https://github.com/Spwig/spwig) настраивает всё
одной командой: Docker, PostgreSQL, Redis, MinIO, TLS через Cloudflare или
самоподписанный, мастер первого запуска, пользователь-администратор. Подписанные образы загружаются из
`registry.spwig.com`.

```bash
curl -fsSL https://spwig.com/install.sh | sudo bash
```

Обновления происходят через админку — см. [UPGRADING.md](UPGRADING.md).

### Вариант 2 — Из исходного кода

Вы хотите собрать из этого репозитория, покопаться в нём или выпустить свой форк:

```bash
git clone https://github.com/Spwig/commerce.git spwig
cd spwig
cp .env.example .env
docker compose up -d
docker compose exec web ./manage.py migrate --noinput
docker compose exec web ./manage.py createsuperuser
```

Витрина по адресу `http://localhost`, админка по `http://localhost/ru/admin/`.
Community-редакция автоматически активируется при первом запуске — никаких обращений к
лицензионному серверу, никакого ключа не требуется. Обновляйтесь позже с помощью `git pull` и
`docker compose build`.

<br />

## Возможности

<table>
  <tr>
    <td width="50%" valign="top">
      <h3>Витрина и оформление заказа</h3>
      <p>Серверный рендеринг по умолчанию — быстрое время до первого байта, работает
      без JavaScript, mobile-first (80% трафика приходится на маленькие
      экраны). Опциональный headless-режим через
      <a href="https://github.com/Spwig/headless-sdk">Spwig headless
      SDK</a> и <a href="https://github.com/Spwig/react">React-компоненты</a>.</p>
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
      <h3>Конструктор страниц</h3>
      <p>Продавцы собирают страницы витрины из переиспользуемых виджетов — hero-секций,
      сеток товаров, отзывов, встраиваний — и предварительно просматривают их вживую
      в админке. Виджеты устанавливаются из маркетплейса или из
      вашего собственного репозитория компонентов.</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>Управление заказами и клиентами</h3>
      <p>Каждый заказ, возврат, продление подписки, цифровая загрузка
      и точка касания с клиентом — в одном месте. Массовые операции,
      роли сотрудников с ограничением прав, экспорт в CSV/XLSX, мобильное
      админ-приложение (iOS) с push-уведомлениями.</p>
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
      <h3>Темы и брендинг</h3>
      <p>Дизайн-токены (цвета, типографика, отступы) управляют каждой
      поверхностью — витриной и админкой. Измените токен — обновится всё.
      Темы живут в
      <a href="https://github.com/Spwig/components">Spwig/components</a>
      и устанавливаются через маркетплейс; напишите свою собственную с помощью
      <a href="https://github.com/Spwig/theme-sdk">theme SDK</a>.</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>Точка продаж (Pro+)</h3>
      <p>Полноценный терминал POS для розничных продавцов:
      сканирование штрих-кодов, разделение платежей, печать чеков, интеграция
      с денежным ящиком, дисплей для покупателя, офлайн-режим. Community-редакция
      поставляет код, но административный интерфейс показывает призыв к обновлению —
      если вы делаете форк, можете это удалить, это нормально.</p>
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
      <h3>Экосистема провайдеров</h3>
      <p>Всё, что общается с внешней системой — платежи,
      доставка, курсы валют, перевод, GeoIP, SMS, email — является
      подключаемым провайдером. Создайте свой собственный с помощью
      <a href="https://github.com/Spwig/provider-sdks">provider SDK</a>,
      опубликуйте на маркетплейсе или разместите приватный реестр у себя.</p>
    </td>
  </tr>
</table>

<br />

## Архитектура

- **Single-tenant.** Каждая установка — это один магазин, один продавец, один
  Django Site. Продавцы с несколькими магазинами запускают одну установку Spwig на магазин.
- **Модульный монолит.** Не сеть микросервисов. Один процесс Django
  обслуживает витрину + админку + REST API + Celery-воркеры.
  Просто развернуть, понять и форкнуть.
- **Runtime-гейты функций.** Community/Pro/Enterprise работают на
  одном и том же бинарнике. Подписанная лицензия переключает флаги — никакой вырезки кода.

Подробный обзор: [ARCHITECTURE.md](ARCHITECTURE.md).

<br />

## Сообщество и поддержка

- **Discussions.** Открытые вопросы, идеи, показ и рассказ:
  [github.com/Spwig/commerce/discussions](https://github.com/Spwig/commerce/discussions).
- **Форум сообщества.** [community.spwig.com](https://community.spwig.com)
  — длинные обсуждения, рецепты лучших практик, витрины расширений.
- **Отчёты об ошибках.** [Issues](https://github.com/Spwig/commerce/issues)
  с шагами воспроизведения. См. [SECURITY.md](SECURITY.md) для
  раскрытия уязвимостей.
- **Коммерческая поддержка.** Доступна для лицензий Pro и Enterprise.

<br />

## Участие в разработке

Мы используем **DCO** (Developer Certificate of Origin) — каждый коммит
подписывается через `git commit -s`. Никаких бумаг, никакого CLA. Полное руководство в
[CONTRIBUTING.md](CONTRIBUTING.md).

Заметки для ИИ-ассистентов по кодированию, работающих над репозиторием, находятся в
[CLAUDE.md](CLAUDE.md).

<br />

## Экосистема

Связанные open-source-проекты под [организацией Spwig](https://github.com/Spwig):

| Репозиторий | Что это |
|---|---|
| [Spwig/commerce](https://github.com/Spwig/commerce) | Этот репозиторий — ядро платформы (AGPL-3.0-or-later) |
| [Spwig/spwig](https://github.com/Spwig/spwig) | Установщик одной командой |
| [Spwig/components](https://github.com/Spwig/components) | Темы, интеграции и утилиты (AGPL-3.0-or-later) |
| [Spwig/theme-sdk](https://github.com/Spwig/theme-sdk) | SDK для создания тем (Apache-2.0) |
| [Spwig/provider-sdks](https://github.com/Spwig/provider-sdks) | SDK для создания провайдеров платежей / доставки / и т. д. (Apache-2.0) |
| [Spwig/headless-sdk](https://github.com/Spwig/headless-sdk) | Headless / API-клиент SDK (Apache-2.0) |
| [Spwig/react](https://github.com/Spwig/react) | Библиотека React-компонентов (Apache-2.0) |

<br />

## Лицензия

Spwig распространяется по [AGPL-3.0-or-later](LICENSE). Вы можете запускать её, модифицировать,
распространять, предлагать как размещённый сервис — всё это разрешено. Изменённые
версии, предлагаемые по сети, должны предоставлять свой исходный код
их пользователям. В этом весь смысл AGPL по сравнению с GPL.

Интеграции провайдеров, созданные с помощью SDK, распространяются по Apache-2.0, поэтому создание
проприетарной интеграции платежей / доставки / SMS поверх SDK
не активирует AGPL. Это сделано намеренно — мы хотим процветающую
экосистему провайдеров.

<br />

## Приватность и телеметрия

Spwig отправляет один анонимный пинг в день на `updates.spwig.com/api/v1/telemetry/`:

- UUID установки (генерируется при первом запуске, хранится локально)
- Версия Spwig
- Редакция (community / pro / enterprise / trial / dev)
- Страна (определяется по IP на входе; сам IP не сохраняется)
- Счётчики бакетов флагов функций (настроенные платёжные провайдеры, установленные
  темы) — никогда сырые данные клиентов или заказов

**Отказаться** можно с помощью `SPWIG_TELEMETRY=0` в вашем окружении. Это переключит
`settings.SPWIG_TELEMETRY_ENABLED`, и ежедневная задача beat станет пустой операцией.

<br />

<p align="center">
  <sub>
    Сделано с заботой в Сингапуре.
    <br />
    <a href="https://spwig.com">spwig.com</a> — <a href="https://docs.spwig.com">docs</a> — <a href="https://community.spwig.com">community</a>
  </sub>
</p>
