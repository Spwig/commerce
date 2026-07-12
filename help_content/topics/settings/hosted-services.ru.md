---
title: Хостированные услуги Spwig
---

Spwig включает три опциональных облачных сервиса, которые ваш магазин может использовать без необходимости настройки или хостинга со стороны: **GeoIP** определяет, где находятся ваши посетители, **Geocoder** преобразует адреса клиентов в координаты на карте, а **Push** отправляет мгновенные уведомления в ваше мобильное приложение администратора Spwig. В бесплатной версии Community каждый сервис имеет щедрый ежемесячный лимит. Когда любой из сервисов приближается к своему пределу, Spwig предупреждает вас в админ-панели, чтобы вы могли решить, следует ли обновить план до того, как клиенты заметят что-либо.

## Три хостированных сервиса

### GeoIP — определение страны посетителя

GeoIP определяет страну каждого посетителя на основе его IP-адреса. Ваш магазин использует эту информацию для автоматического отображения правильной валюты, когда клиент заходит, и для предварительного заполнения поля страны во время оформления заказа. Например, посетитель из Германии увидит цены в евро, а посетитель из Японии — в иенах — без необходимости вручную выбирать валюту.

Каждая загрузка страницы, при которой выполняется поиск GeoIP, учитывается в вашем ежемесячном лимите. Повторные посещения с одного сеанса браузера не учитываются отдельно; результат кэшируется для сеанса. Поиск GeoIP выполняется только на фронтенде магазина, а не в админ-панели.

### Geocoder — адрес в координаты

Geocoder преобразует введенные клиентом адреса в географические координаты (широта и долгота). Ваш магазин использует эти координаты для двух целей: расчета стоимости доставки на основе расстояния, если у вас есть пункты самовывоза или правила доставки на основе радиуса, а также для предоставления автодополнения адреса на странице оформления заказа, чтобы клиенты могли быстро найти свой адрес.

Поиск Geocoder запускается, когда клиент выбирает или подтверждает адрес во время оформления заказа. Как и GeoIP, результаты кэшируются, поэтому один и тот же адрес будет искаться только один раз за сеанс.

### Push — уведомления в приложении администратора

Push отправляет в реальном времени уведомления в ваше мобильное приложение продавца Spwig. Когда поступает новый заказ, когда запасы падают ниже порога или когда клиент отправляет сообщение, Push отправляет мгновенное уведомление на ваше устройство, чтобы вы могли ответить, не открывая админ-панель.

Каждое уведомление, отправленное на ваше устройство, считается за один запрос Push в вашем ежемесячном лимите.

## Бесплатный тариф Community

В бесплатной версии Community Spwig каждый сервис включен без дополнительной оплаты до ежемесячного лимита запросов. Точные лимиты устанавливаются Spwig и могут варьироваться; ваша админ-панель всегда показывает текущие значения для вашей установки. Оплачиваемые планы (Starter, Growth, Pro, Pro Plus) и саморазвернутые установки с оплачиваемой лицензией имеют более высокие лимиты для каждого сервиса.

Когда сервис достигает 100% лимита Community, запросы к этому сервису останавливаются до следующего календарного месяца, когда сбрасывается счетчик. Влияние на ваш магазин зависит от того, какой сервис достиг лимита:

| Сервис | Что происходит при достижении 100% |
|---------|----------------------|
| GeoIP | Автоматическое определение валюты возвращается к стандартной валюте вашего магазина. Клиенты все еще могут вручную менять валюту. |
| Geocoder | Автодополнение адреса перестает предлагать варианты. Клиенты все еще могут вручную вводить свой адрес. Расчет стоимости доставки продолжается с использованием последних известных координат. |
| Push | Новые уведомления в приложении администратора помещаются в очередь, но не доставляются до следующего месяца или обновления. |

Ваш магазин продолжает нормально работать во всех случаях — не теряются заказы, клиенты все еще могут оформлять заказы. Эффекты ограничены удобными функциями.

## Чтение плитки дашборда

Плитка **Использование сервисов Spwig** отображается на главной странице вашей админ-панели. Она показывает прогресс-бар для каждого из трех сервисов.

Каждая строка в плитке имеет одинаковую компоновку:

- **Название сервиса** (слева) — GeoIP, Поиск адреса (Geocoder) или Уведомления Push.
- **Прогресс-бар** (в центре) — заполняется слева направо по мере увеличения использования.

Цвет полосы меняется при приближении к лимитам:
  - **Зеленый** — использование ниже 80%.

Everything is running normally.
  - **Amber** — usage is between 80% and 99%.

The service is still running but getting close to the limit.
  - **Red** — usage has hit 100%.

The service is now throttled for this month.
- **Usage counts** (right) — the exact number of requests used out of the total allowed, for example `3,241 / 10,000`.

The label in parentheses shows the time window, typically `(this month)`.

If the tile cannot reach the Spwig update server to fetch your current usage (for example, if your server has no outbound internet access), the counts column shows a dash (`—`) for that service. This does not mean the service is broken; it means the usage display is temporarily unavailable.

### The Upgrade button

When any service reaches 80% or more, an **Upgrade** button appears in the top-right corner of the tile. Clicking it opens the Spwig upgrade page where you can compare plans and raise your service limits. The button disappears once usage drops back below 80% at the start of the next month.

## The quota warning banner

In addition to the dashboard tile, a banner appears at the top of every admin page whenever any service crosses the 80% threshold. The banner only appears on Community installs.

**Amber banner — approaching the limit (80–99%)**

> **Approaching hosted-services limit:** One of your Spwig services is over 80% of its Community-tier quota. Upgrade to raise the limit before it's hit.

This banner is an early heads-up. Your services are still running, and you have time to decide whether to upgrade before the month ends.

**Red banner — limit reached (100%)**

> **Spwig services limit reached:** One of your hosted services has hit its Community-tier quota. Upgrade to keep them running without interruption.

This banner appears when at least one service has hit 100% and is now throttled. Clicking **Upgrade** on either banner opens the same upgrade page as the tile button.

The banner disappears automatically at the start of the next calendar month when the counters reset, or immediately after you upgrade to a paid plan.

## Email alert at 90%

When any service crosses 90% of its quota, Spwig also sends a one-time warning email to the address configured in your store settings (**Settings > Store Settings > Contact > Admin Email**). The email is sent at most once per service per calendar month, so you won't be flooded with messages. No email is sent at 100% because at that point the in-admin banner already makes the situation clear.

If you don't receive the email, check that your admin email address is set correctly under **Settings > Store Settings**.

## Upgrading your plan

When you upgrade from Community to any paid plan, the higher limits take effect immediately — no store restart or configuration change is needed. The dashboard tile will show the new, higher limit the next time it refreshes (within five minutes).

To upgrade, click the **Upgrade** button on the dashboard tile or quota banner, or visit the Spwig upgrade page directly. Paid plans include the same three hosted services (GeoIP, Geocoder, Push) at raised monthly limits, plus access to Spwig-hosted email delivery and priority support.

## Self-hosting and Pro licences

If you run a self-hosted Spwig install with a paid licence, your licence tier determines your service limits, the same as the equivalent hosted plan. Your store still needs outbound internet access to reach `updates.spwig.com` for the platform to fetch and verify your tier configuration. The usage counters displayed in the dashboard tile are pulled from the hosted service endpoints at `geoip.spwig.com`, `geocoder.spwig.com`, and `push.spwig.com`.

There is currently no option to replace GeoIP, Geocoder, or Push with self-hosted alternatives — these services are provided exclusively by Spwig's infrastructure and are included in all editions.

## Tips

Preserve all markdown formatting, image paths, code blocks, and technical terms.

- **Проверяйте плитку регулярно в конце насыщенных месяцев** — акция или распродажа могут значительно увеличить количество запросов GeoIP и Geocoder.

Плитка предупреждает вас заранее, до того как клиенты почувствуют это.
- **Резервная валюта не видна большинству клиентов** — если GeoIP достигнет своего лимита, клиенты увидят валюту по умолчанию вашего магазина.

Это редко становится серьезной проблемой для магазинов, которые в основном обслуживают один рынок; это важнее для действительно международных магазинов.
- **Автодополнение адреса — это удобство, а не препятствие** — когда Geocoder ограничивается, клиенты все равно могут ввести и отправить свой адрес в обычном режиме.

Если вы часто проводите акции, которые приводят к высокому трафику на оформление заказа, рассмотрите возможность обновления до периода высокой активности.
- **Ограничение пропускной способности не приводит к потере уведомлений навсегда** — уведомления, которые были в очереди во время периода ограничения, не доставляются обратно, когда месяц сбрасывается или после обновления.

Если вы сильно зависите от push-уведомлений для получения важных уведомлений о заказах, обновление до достижения лимита гарантирует, что вы ничего не упустите.
- **Кэш в 5 минут означает, что плитка не является полностью в реальном времени** — показатели использования обновляются примерно каждые пять минут в фоновом режиме.

Во время необычно высоких пиков трафика фактическое использование может быть немного выше, чем показывает плитка.
- **Установите адрес электронной почты администратора** — электронное письмо с предупреждением на 90% работает только в том случае, если **Настройки > Настройки магазина > Электронная почта администратора** заполнено.

Стоит убедиться, что это правильно установлено, чтобы вы получали предупреждение до того, как возникнут проблемы.