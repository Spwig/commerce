---
title: Настройка CDN
---

A Content Delivery Network (CDN) stores copies of your store's images, stylesheets, and scripts on servers around the world. When a customer visits your store, these files are served from the server closest to them rather than from your main hosting server. This reduces page load times, especially for customers located far from where your store is hosted.

Spwig already optimizes static asset delivery out of the box with Brotli and gzip pre-compression, fingerprinted asset caching with 1-year immutable headers, and proper content negotiation. Adding a CDN is optional, but it can further improve speed for stores with an international customer base.

## Does Your Store Need a CDN?

Not every store benefits equally from a CDN. Use these guidelines to decide:

**A CDN is recommended if**:
- Your customers are spread across multiple countries or continents
- Your store features many product images or media-heavy pages
- You want the fastest possible page load times worldwide
- You sell to regions far from your hosting server (e.g., server in Europe, customers in Asia)

**A CDN is likely unnecessary if**:
- Your customers are mostly local or within the same country as your server
- Your store has a small catalog with few images
- Your hosting provider already includes a built-in CDN

When in doubt, a CDN does not hurt performance. Services like Cloudflare offer free tiers, so there is no cost to try.

## How Spwig Works with CDNs

Spwig is CDN-ready by default. You do not need to change any code or settings inside your Spwig admin panel. Here is what Spwig already does for you:

- **Fingerprinted static files** -- Every CSS, JavaScript, and image file includes a unique version hash in its filename. This means CDNs can safely cache these files for a long time without serving outdated content.
- **Long-lived cache headers** -- Static assets are served with 1-year immutable cache headers, telling CDNs and browsers to cache them aggressively.
- **Pre-compressed files** -- Spwig pre-compresses assets using Brotli and gzip, so your CDN can deliver smaller files without extra processing.
- **Proper content negotiation** -- Spwig sends the correct content-type and encoding headers that CDNs rely on for proper caching.

All you need to do is point your domain's DNS to the CDN provider, and everything works automatically.

## Setting Up Cloudflare

Cloudflare is the most popular CDN and offers a free tier that works well for most stores. Follow these steps:

**Step 1: Create a Cloudflare Account**
- Visit cloudflare.com and sign up for a free account

**Step 2: Add Your Domain**
- Click **Add a Site** and enter your store's domain name
- Select the **Free** plan (sufficient for most stores)

**Step 3: Update Your DNS Nameservers**
- Cloudflare will show you two nameservers (e.g., `anna.ns.cloudflare.com`)
- Log in to your domain registrar (where you purchased your domain)
- Replace your current nameservers with the Cloudflare nameservers
- DNS changes can take up to 24 hours to take effect

**Step 4: Configure SSL/TLS**
- In the Cloudflare dashboard, go to **SSL/TLS**
- Set the encryption mode to **Full (strict)**
- This ensures all traffic between Cloudflare and your server stays encrypted

**Step 5: Verify It Is Working**
- Once DNS propagates, visit your store and check for the `cf-cache-status` header in your browser (see Verifying Your CDN below)

## Setting Up AWS CloudFront

If you already use Amazon Web Services, CloudFront integrates naturally with your infrastructure:

1. Open the **CloudFront** console in your AWS account
2. Create a new **Distribution** with your store's domain as the origin
3. Set the **Origin Protocol Policy** to "HTTPS Only"
4. Under **Cache Behavior**, set **Cache Policy** to "CachingOptimized" for static assets
5. Add your store's domain as an **Alternate Domain Name (CNAME)**
6. Attach an SSL certificate from AWS Certificate Manager
7. Update your domain's DNS to point to the CloudFront distribution URL

Ценообразование CloudFront основано на использовании.

Для большинства магазинов расходы минимальны, поскольку статические активы Spwig кэшируются в течение длительного времени.

## Рекомендуемые настройки CDN

Для достижения наилучших результатов настройте свой CDN так, чтобы кэшировать правильный контент и пропускать остальной.

**Что кэшировать** (статические активы):
- `/static/` -- Все стили, скрипты, шрифты и активы темы
- `/media/` -- Изображения товаров и загруженные медиафайлы
- Файлы изображений (`.jpg`, `.png`, `.webp`, `.svg`, `.gif`)
- Файлы шрифтов (`.woff`, `.woff2`)

**Что НЕ кэшировать** (динамические страницы):
- `/admin/` -- Панель администратора должна всегда предоставлять свежий контент
- `/cart/` -- Страницы корзины содержат данные, специфичные для сессии
- `/checkout/` -- Страницы оформления заказа никогда не должны кэшироваться из-за безопасности
- `/accounts/` -- Страницы учетных записей клиентов содержат частную информацию
- Любая страница, требующая входа или отображающая персонализированный контент

**Общие правила кэширования**:
- **Уважайте заголовки кэширования источника** -- Spwig отправляет правильные заголовки cache-control для каждого типа контента. Настройте свой CDN так, чтобы уважать эти заголовки, а не переопределять их.
- **Включите сжатие Brotli** -- И Cloudflare, и CloudFront поддерживают Brotli. Включите его, чтобы воспользоваться предварительно сжатыми активами Spwig.
- **Установите TTL браузерного кэша в "Уважать существующие заголовки"** -- Это позволяет политике кэширования, встроенной в Spwig, управлять поведением.

## Проверка вашего CDN

После настройки убедитесь, что CDN правильно предоставляет ваш контент:

**Шаг 1: Открыть инструменты разработчика браузера**
- В Chrome или Firefox нажмите **F12**, чтобы открыть инструменты разработчика
- Нажмите вкладку **Сеть**

**Шаг 2: Загрузить ваш магазин**
- Посетите домашнюю страницу вашего магазина с открытыми инструментами разработчика
- Нажмите на любой запрос статического файла (например, файл `.css` или `.js`)

**Шаг 3: Проверить заголовки ответа**
- **Cloudflare**: Ищите заголовок `cf-cache-status`. Значение `HIT` означает, что файл был получен из кэша CDN. `MISS` означает, что он был получен с вашего сервера (только первый запрос).
- **CloudFront**: Ищите заголовок `x-cache`. Значение `Hit from cloudfront` подтверждает доставку через CDN.

**Шаг 4: Проверка с другого расположения**
- Используйте бесплатный инструмент, например, gtmetrix.com или webpagetest.org, чтобы проверить ваш магазин с разных географических местоположений
- Сравните время загрузки до и после настройки CDN

## Распространенные проблемы

### Старый контент после обновления темы

**Проблема**: После обновления вашей темы или внесения изменений в дизайн клиенты все еще видят старую версию.

**Решение**: Очистите кэш вашего CDN. В Cloudflare перейдите в **Caching > Configuration > Purge Everything**. В CloudFront создайте **Invalidation** для `/*`. Обратите внимание, что фингерпринтированные активы Spwig обычно предотвращают эту проблему, поскольку обновленные файлы получают новые имена автоматически. Эта проблема чаще всего влияет на нефингерпринтованные активы, такие как пользовательские загрузки.

---

### Предупреждения о смешанном содержимом

**Проблема**: Ваш браузер показывает предупреждение о безопасности о "смешанном содержимом" после включения CDN.

**Решение**: Убедитесь, что режим SSL вашего CDN установлен в **Full (strict)**, а не в "Flexible". Режим Flexible может привести к тому, что ваш сервер будет получать запросы HTTP вместо HTTPS, что вызовет предупреждения о смешанном содержимом. В Cloudflare проверьте **SSL/TLS > Overview** и убедитесь, что режим установлен правильно.

---

### Панель администратора работает медленно

**Проблема**: Панель администратора кажется медленной после добавления CDN.

**Решение**: CDN не должен кэшировать страницы администратора. Создайте **Page Rule** (Cloudflare) или **Cache Behavior** (CloudFront), который устанавливает кэширование в "Bypass" для любого URL, соответствующего `/admin/*`. Это гарантирует, что запросы администратора отправляются напрямую на ваш сервер без излишков CDN.

---

### Не загружаются изображения

**Проблема**: Изображения товаров или медиафайлы возвращают ошибки после настройки CDN.

**Решение**: Проверьте, правильно ли настроен источник вашего CDN с правильным протоколом (HTTPS) и портом. Также проверьте, разрешает ли брандмауэр вашего сервера подключения с диапазонов IP-адресов CDN.

## Советы

Сохраните всю разметку Markdown, пути к изображениям, блоки кода и технические термины.

- **Начните с бесплатного тарифа Cloudflare** -- Он охватывает потребности большинства магазинов и занимает всего несколько минут на настройку
- **Всегда используйте режим Full (strict) SSL** -- Режим Flexible создает уязвимости в безопасности и может нарушить процесс оформления заказа
- **Очистите кэш CDN после крупных обновлений темы** -- Хотя файлы с отпечатками Spwig решают большинство случаев, полная очистка кэша гарантирует, что не останется устаревшего содержимого
- **Не кэшируйте страницы оформления заказа и корзины** -- Кэширование этих страниц может привести к тому, что данные одного клиента будут доступны другому
- **Тестируйте с точки зрения расположения ваших клиентов** -- Используйте бесплатные инструменты, такие как webpagetest.org, чтобы измерить реальную производительность с регионов, где ваши клиенты совершают покупки
- **Мониторьте аналитику вашего CDN** -- И Cloudflare, и CloudFront предоставляют панели управления, показывающие показатели кэширования, сэкономленный пропускной способность и трафик по странам
- **Сохраняйте низкое значение TTL DNS во время настройки** -- Установите TTL DNS на 300 секунд (5 минут) при переходе на CDN, а затем увеличьте его, когда все будет подтверждено как работающее
- **CDN не заменяет хорошее хостинг-окружение** -- Ваш сервер-источник все равно важен для динамических страниц, таких как оформление заказа, корзина и администрирование.

Выберите качественное хостинг-окружение вместе с CDN