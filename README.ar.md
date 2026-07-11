<p align="center">
  <a href="README.md">English</a> |
  <a href="README.fr.md">Français</a> |
  <a href="README.es.md">Español</a> |
  <a href="README.de.md">Deutsch</a> |
  <a href="README.ja.md">日本語</a> |
  <a href="README.zh-Hans.md">简体中文</a> |
  <a href="README.zh-Hant.md">繁體中文</a> |
  <a href="README.pt.md">Português</a> |
  <a href="README.ru.md">Русский</a> |
  <strong>العربية</strong> |
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
  <strong>منصة تجارة إلكترونية ذاتية الاستضافة للتجار الذين يريدون امتلاك متاجرهم.</strong>
</p>

<p align="center">
  <a href="https://spwig.com">الموقع الإلكتروني</a> &nbsp;•&nbsp;
  <a href="https://docs.spwig.com">التوثيق</a> &nbsp;•&nbsp;
  <a href="https://community.spwig.com">المجتمع</a> &nbsp;•&nbsp;
  <a href="https://spwig.com/ar/marketplace">السوق</a> &nbsp;•&nbsp;
  <a href="https://spwig.com/ar/demos">عروض حية</a>
</p>

<p align="center">
  <a href="LICENSE"><img alt="Licence: AGPL v3" src="https://img.shields.io/badge/licence-AGPL--3.0-blue.svg"></a>
  <a href="https://github.com/Spwig/commerce/actions"><img alt="CI" src="https://img.shields.io/github/actions/workflow/status/Spwig/commerce/test.yml?branch=main&label=tests"></a>
  <a href="https://github.com/Spwig/commerce/releases"><img alt="Release" src="https://img.shields.io/github/v/release/Spwig/commerce"></a>
  <a href="https://github.com/Spwig/commerce/discussions"><img alt="Discussions" src="https://img.shields.io/github/discussions/Spwig/commerce"></a>
</p>

## ما هي Spwig؟

Spwig منصة تجارة إلكترونية متكاملة الميزات: كتالوج، سلة تسوق، إتمام الشراء،
طلبات، عملاء، مدفوعات، شحن، قوالب، أداة بناء الصفحات، واجهة API للإدارة،
POS، اشتراكات، برامج ولاء، مدونة، SEO — الحزمة الكاملة. مبنية باستخدام
**Django 5** و **PostgreSQL** و **Redis**، وتُشحن كمجموعة من حاويات Docker،
وتعمل على VPS بقيمة 5 دولارات أو على خوادمك الخاصة.

على عكس المنصات المستضافة، **أنت تمتلك الكود وقاعدة البيانات وبيانات
العملاء.** لا رسوم على كل معاملة. لا تقييد. إذا أردت تفريعها والذهاب في
طريقك الخاص، فإن الرخصة تسمح بذلك صراحةً.

<br />

## الإصدارات

نفس البرنامج الثنائي. يقوم ملف رخصة موقّع بتبديل علامات الميزات في وقت التشغيل.
الإصدار المجتمعي هو ما تحصل عليه افتراضياً عند تشغيل `docker compose up`؛
الترقية عبارة عن مفتاح تلصقه في لوحة الإدارة.

| | Community | Pro | Enterprise |
|---|:---:|:---:|:---:|
| تجارة إلكترونية كاملة، قوالب، أداة بناء الصفحات، واجهة POS | ✓ | ✓ | ✓ |
| استخدام مزودي دفع من اختيارك | ✓ | ✓ | ✓ |
| استخدام مزودي شحن من اختيارك | ✓ | ✓ | ✓ |
| الوصول إلى السوق (قوالب وتكاملات مدفوعة) | ✓ | ✓ | ✓ |
| الإكمال التلقائي للعناوين المستضاف من Spwig | مجاني · محدود المعدل | حد أعلى | أعلى حد |
| GeoIP المستضاف من Spwig (تحديد موقع الزائر) | مجاني · محدود المعدل | حد أعلى | أعلى حد |
| إشعارات Push (تطبيق إدارة iOS) | مجاني · محدود المعدل | حد أعلى | أعلى حد |
| نقاط البيع (دعم أجهزة POS) | ✓ | ✓ | ✓ |
| بوابة بريد إلكتروني مستضافة مع IPs محمّاة و DKIM | – | ✓ | ✓ |
| دعم ذو أولوية | – | ✓ | ✓ |
| SSO للمؤسسات (Azure AD، Okta) | – | – | ✓ |

<br />

## البداية السريعة

### الخيار 1 — التثبيت بأمر واحد (موصى به)

يقوم [مثبّت Spwig](https://github.com/Spwig/spwig) بإعداد كل شيء في أمر
واحد: Docker، PostgreSQL، Redis، MinIO، TLS عبر Cloudflare أو موقّع ذاتياً،
معالج الإقلاع الأول، مستخدم الإدارة. يتم سحب الصور الموقّعة من
`registry.spwig.com`.

```bash
curl -fsSL https://spwig.com/install.sh | sudo bash
```

تتم الترقيات عبر لوحة الإدارة — راجع [UPGRADING.md](UPGRADING.md).

### الخيار 2 — من المصدر

تريد البناء من هذا المستودع، أو التعديل عليه، أو شحن نسخة متفرعة:

```bash
git clone https://github.com/Spwig/commerce.git spwig
cd spwig
cp .env.example .env
docker compose up -d
docker compose exec web ./manage.py migrate --noinput
docker compose exec web ./manage.py createsuperuser
```

الواجهة الأمامية على `http://localhost`، ولوحة الإدارة على `http://localhost/ar/admin/`.
يتم تفعيل الإصدار المجتمعي تلقائياً عند الإقلاع الأول — دون الحاجة إلى
الاتصال بخادم رخص أو إدخال مفتاح. قم بالترقية لاحقاً باستخدام `git pull` و
`docker compose build`.

<br />

## الميزات

<table>
  <tr>
    <td width="50%" valign="top">
      <h3>الواجهة الأمامية وإتمام الشراء</h3>
      <p>مُصيَّرة من الخادم افتراضياً — زمن استجابة أول بايت سريع، تعمل
      بدون JavaScript، مصممة للجوال أولاً (80% من الزيارات من الشاشات
      الصغيرة). وضع Headless اختياري عبر
      <a href="https://github.com/Spwig/headless-sdk">Spwig headless
      SDK</a> و <a href="https://github.com/Spwig/react">مكونات
      React</a>.</p>
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
      <h3>أداة بناء الصفحات</h3>
      <p>يبني التجار صفحات المتجر من ودجات قابلة لإعادة الاستخدام —
      أقسام Hero، شبكات المنتجات، الشهادات، التضمينات — ويعاينونها
      مباشرةً في لوحة الإدارة. تُثبَّت الودجات من السوق أو من مستودع
      المكونات الخاص بك.</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>إدارة الطلبات والعملاء</h3>
      <p>كل طلب، استرداد، تجديد اشتراك، تنزيل رقمي، ونقطة تواصل مع
      العميل في مكان واحد. عمليات جماعية، أدوار موظفين محددة الصلاحيات،
      تصدير إلى CSV/XLSX، تطبيق إدارة على الجوال (iOS) مع إشعارات
      Push.</p>
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
      <h3>القوالب والهوية البصرية</h3>
      <p>رموز التصميم (الألوان، الخطوط، المسافات) تحكم كل السطوح —
      الواجهة الأمامية ولوحة الإدارة. غيّر رمزاً واحداً، ليتحدث كل شيء.
      تعيش القوالب في
      <a href="https://github.com/Spwig/components">Spwig/components</a>
      وتُثبَّت عبر السوق؛ اكتب قوالبك الخاصة باستخدام
      <a href="https://github.com/Spwig/theme-sdk">theme SDK</a>.</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>نقاط البيع</h3>
      <p>طرفية POS كاملة للتجار أصحاب المتاجر الفعلية:
      مسح الباركود، تقسيم المدفوعات، طباعة الإيصالات، تكامل مع درج
      النقود، شاشة موجهة للعميل، وضع دون اتصال. يشحن الإصدار المجتمعي
      الكود لكن سطح الإدارة يعرض دعوة للترقية — يمكنك إزالتها إذا فرّعت،
      لا مشكلة.</p>
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
      <h3>منظومة المزودين</h3>
      <p>أي شيء يتحدث مع نظام خارجي — المدفوعات، الشحن، أسعار الصرف،
      الترجمة، GeoIP، SMS، البريد الإلكتروني — هو مزود قابل للتوصيل.
      ابنِ مزودك الخاص باستخدام
      <a href="https://github.com/Spwig/provider-sdks">provider SDKs</a>،
      وانشره في السوق، أو استضف سجلاً خاصاً بنفسك.</p>
    </td>
  </tr>
</table>

<br />

## البنية المعمارية

- **أحادية المستأجر.** كل تثبيت هو متجر واحد، تاجر واحد، Site واحد في
  Django. التجار متعددو المتاجر يقومون بتشغيل تثبيت Spwig واحد لكل متجر.
- **متراصة معيارية.** ليست شبكة خدمات دقيقة. عملية Django واحدة تتعامل
  مع الواجهة الأمامية + لوحة الإدارة + REST API + عمّال Celery.
  سهلة النشر والفهم والتفريع.
- **بوابات ميزات في وقت التشغيل.** Community/Pro/Enterprise جميعها تعمل
  بنفس البرنامج الثنائي. رخصة موقّعة تبدّل العلامات — دون تجريد للكود.

جولة كاملة: [ARCHITECTURE.md](ARCHITECTURE.md).

<br />

## المجتمع والدعم

- **المناقشات.** أسئلة مفتوحة، أفكار، عروض ومشاركات:
  [github.com/Spwig/commerce/discussions](https://github.com/Spwig/commerce/discussions).
- **منتدى المجتمع.** [community.spwig.com](https://community.spwig.com)
  — نقاشات مطوّلة، وصفات لأفضل الممارسات، عروض للتوسعات.
- **بلاغات الأخطاء.** [Issues](https://github.com/Spwig/commerce/issues)
  مع خطوات إعادة الإنتاج. راجع [SECURITY.md](SECURITY.md) للإفصاح
  عن الثغرات.
- **الدعم التجاري.** متاح لتراخيص Pro و Enterprise.

<br />

## المساهمة

نستخدم **DCO** (شهادة منشأ المطوّر) — كل commit يوقَّع باستخدام
`git commit -s`. لا أوراق، ولا CLA. الدليل الكامل في
[CONTRIBUTING.md](CONTRIBUTING.md).

ملاحظات لمساعدي الترميز بالذكاء الاصطناعي الذين يعملون على المستودع
موجودة في [CLAUDE.md](CLAUDE.md).

<br />

## المنظومة

المشاريع مفتوحة المصدر ذات الصلة تحت [منظمة Spwig](https://github.com/Spwig):

| المستودع | ماذا يكون |
|---|---|
| [Spwig/commerce](https://github.com/Spwig/commerce) | هذا المستودع — منصة النواة (AGPL-3.0-or-later) |
| [Spwig/spwig](https://github.com/Spwig/spwig) | المثبّت بأمر واحد |
| [Spwig/components](https://github.com/Spwig/components) | قوالب، تكاملات، وأدوات مساعدة (AGPL-3.0-or-later) |
| [Spwig/theme-sdk](https://github.com/Spwig/theme-sdk) | SDK لبناء القوالب (Apache-2.0) |
| [Spwig/provider-sdks](https://github.com/Spwig/provider-sdks) | SDKs لبناء مزودي الدفع / الشحن / إلخ. (Apache-2.0) |
| [Spwig/headless-sdk](https://github.com/Spwig/headless-sdk) | SDK للاستخدام Headless / كعميل API (Apache-2.0) |
| [Spwig/react](https://github.com/Spwig/react) | مكتبة مكونات React (Apache-2.0) |

<br />

## الرخصة

Spwig مرخّصة بموجب [AGPL-3.0-or-later](LICENSE). يمكنك تشغيلها، وتعديلها،
وتوزيعها، وتقديمها كخدمة مستضافة — كل ذلك مسموح. النسخ المعدّلة المقدَّمة
عبر الشبكة يجب أن تتيح مصدرها لمستخدميها. هذه هي النقطة الأساسية لـ AGPL
مقارنة بـ GPL.

تكاملات المزودين المبنية باستخدام SDKs مرخّصة بموجب Apache-2.0، لذا فإن
بناء تكامل مدفوعات / شحن / SMS احتكاري فوق SDKs لا يستدعي AGPL. هذا مقصود
— نريد منظومة مزودين مزدهرة.

<br />

## الخصوصية والقياسات عن بُعد

ترسل Spwig ping مجهول واحد يومياً إلى `updates.spwig.com/api/v1/telemetry/`:

- UUID التثبيت (يُولَّد عند الإقلاع الأول، يُخزَّن محلياً)
- إصدار Spwig
- النسخة (community / pro / enterprise / trial / dev)
- الدولة (تُحدَّد من IP عند الدخول؛ IP نفسه لا يُخزَّن)
- عدّادات مجمَّعة لعلامات الميزات (مزودو الدفع المُهيَّؤون، القوالب
  المثبّتة) — لا تُرسَل أبداً بيانات عملاء أو طلبات خام

**للإلغاء** استخدم `SPWIG_TELEMETRY=0` في بيئتك. هذا يقلب
`settings.SPWIG_TELEMETRY_ENABLED` وتصبح مهمة البث اليومية بلا عمل.

<br />

<p align="center">
  <sub>
    صُنعت بعناية في سنغافورة.
    <br />
    <a href="https://spwig.com">spwig.com</a> — <a href="https://docs.spwig.com">التوثيق</a> — <a href="https://community.spwig.com">المجتمع</a>
  </sub>
</p>
