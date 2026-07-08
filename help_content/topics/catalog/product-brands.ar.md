---
title: علامات المنتجات
---

تسمح العلامات بالربط بين المنتجات ومصنعيها أو العلامات التجارية، وتمنح العملاء طريقة للتصفح في متجرك حسب العلامة التجارية. لكل علامة تجارية صفحة خاصة في متجرك الإلكتروني حيث يمكن للعملاء اكتشاف جميع المنتجات من هذه العلامة التجارية، والاطلاع على قصة العلامة، والاتصال بموقعها الإلكتروني.

اذهب إلى **الكتالوج > العلامات التجارية** لإدارة علاماتك التجارية.

## لماذا استخدام العلامات التجارية

تقوم العلامات التجارية بمهامين في Spwig:

1. **التنظيم** — تُصنف المنتجات حسب العلامة التجارية، مما يجعل من السهل على العملاء الولاء لعلامة معينة العثور على ما يبحثون عنه
2. **التسويق** — صفحات العلامات التجارية هي مساحة مخصصة لعرض قصة العلامة، الشعار، ونطاق المنتجات الكامل، ويمكن أن تحسن من معدل التحويل للعملاء الذين يهتمون بالعلامات التجارية

كما تعمل العلامات التجارية مع نظام الترويج — يمكنك إجراء مبيعات تشمل جميع المنتجات من علامة تجارية معينة دون الحاجة إلى اختيار المنتجات بشكل فردي.

## إنشاء علامة تجارية

1.

اذهب إلى **الكتالوج > العلامات التجارية**
2.

اضغط على **+ إضافة علامة تجارية**
3.

املأ قسم **المعلومات الأساسية**:
   - **الاسم** — اسم العلامة التجارية كما سيظهر في متجرك الإلكتروني (يجب أن يكون فريدًا)
   - **العنوان** — مسار الرابط URL للصفحة الخاصة بالعلامة التجارية (يتم ملؤه تلقائيًا من الاسم؛ يمكنك تعديله)
   - **الوصف** — وصف قصير للعلامة التجارية يظهر على صفحة العلامة
   - **الموقع الإلكتروني** — عنوان URL لموقع العلامة التجارية الرسمي (اختياري — يظهر كرابط على صفحة العلامة)
4.

أضف أصول العلامة:
   - **الشعار** — صورة شعار العلامة التجارية، المستخدمة في قائمة العلامات التجارية وصفحة العلامة
   - **صورة اللافتة** — صورة لافتة واسعة تُعرض في أعلاة صفحة العلامة
5.

اكتب **قصة العلامة** (اختياري) — مقالة تحريرية أطول عن تاريخ العلامة، قيمها، أو ما يجعلها مميزة.

تظهر هذه القصة على صفحة العلامة التجارية في المتجر، ويمكن أن تكون طريقة فعالة لمشاركة قصة العلامة مع العملاء المهتمين.
6.

احتفظ بجميع التنسيقات المرتبطة بالعلامة، مسارات الصور، كتل الشفرة، والكلمات الفنية.

Configure **SEO** fields:
   - **Meta Title** — the page title shown in search engine results
   - **Meta Description** — the short description shown below the title in search results
7.

Set display options:
   - **Show Brand Page** — controls whether the brand has a publicly accessible page.

Uncheck to hide a brand from the storefront while keeping it in the system.
   - **Is Active** — controls whether the brand is available to assign to products and visible in the store
   - **Is Featured** — marks the brand for featured placement in your theme (e.g., a homepage row of brand logos)
8.

Click **Save**

## Assigning products to a brand

Brands are assigned on individual product records, not from the brand management page. To assign a brand to a product:

1. Navigate to **Catalog > Products** and open the product
2. In the product form, find the **Brand** field
3. Search for and select the appropriate brand
4. Save the product

Once a brand is assigned, the product will appear on that brand's storefront page automatically.

## Brand pages on your storefront

Each brand with **Show Brand Page** enabled gets its own page at `/brand/{slug}/`. The page displays:

- The brand logo and banner image
- The brand name and description
- The brand story (if provided)
- A link to the brand's website (if provided)
- All active products assigned to that brand

Customers can reach brand pages by clicking a brand name on a product page, or through links you create in your navigation or page builder.

## SEO for brand pages

Filling in the **Meta Title** and **Meta Description** fields for each brand helps your brand pages appear well in search results. Effective brand SEO titles typically combine the brand name with what the brand sells:

| Brand | Good Meta Title |
|---|---|
| Levi's | "Levi's Jeans & Clothing — Official Store" |
| KitchenAid | "KitchenAid Stand Mixers & Kitchen Appliances" |
| Patagonia | "Patagonia Outdoor Clothing & Gear" |

إذا تركت حقول SEO فارغة، فإن نموذجك سيستخدم اسم العلامة التجارية كمفتاح افتراضي.

### إنشاء SEO تلقائيًا

إذا تم تفعيل **SEO مُنشأ تلقائيًا** في علامة تجارية، فسيقوم Spwig بإنشاء عنوان ووصف ميتا تلقائيًا عند حفظ العلامة التجارية. هذا مفيد للشركات التي تحتوي على عدد كبير من العلامات التجارية، لكنه يمنحك أقل سيطرة على الكلمات الدقيقة. يمكنك دائمًا استبدال المحتوى المُنشأ تلقائيًا عن طريق كتابة النص مباشرة في الحقول وتعطيل مفتاح إنشاء المحتوى تلقائيًا.

## العلامات التجارية المميزة

يستخدم علم **هل هي مميزة** من قبل النماذج لعرض صف أو شبكة من شعارات العلامات التجارية المختارة - غالبًا على الصفحة الرئيسية. يجب أن تكون عدد العلامات التجارية المميزة قليلًا فقط في كل مرة؛ الرجاء الرجوع إلى وثائق النموذج الخاصة بك لفهم عدد العلامات التجارية المميزة التي تُعرض بشكل مثالي.

## النصائح

- رفع شعار العلامة التجارية كـ PNG أو WebP مع خلفية شفافة - سيظهر بشكل نظيف على أي لون خلفية في نموذجك
- اكتب قصة ممتعة للعلامة التجارية حتى للعلامات التجارية غير المعروفة؛ العملاء الذين لا يعرفون العلامة التجارية يقدرون السياق الذي يساعد في اتخاذ قرار بشأن ما إذا كانت المنتجات مناسبة لهم
- إذا كنت تجري عروضًا ترويجية تستهدف علامات تجارية معينة، تأكد من أن اسم العلامة التجارية في Spwig يتطابق تمامًا - تستخدم العروض العلاقة بين العلامة التجارية والمنتجات لتحديد الأهلية
- عند توقفك عن تقديم منتجات العلامة التجارية، قم بإلغاء تنشيط العلامة التجارية بدلًا من حذفها - الحذف يحذف مرجع العلامة التجارية من جميع المنتجات المرتبطة، بينما يحافظ الإلغاء على التاريخ
- استخدم علم **هل هي مميزة** بحذر؛ الصفحة الرئيسية التي تُعرض 20 شعارًا للعلامات التجارية تفقد تأثيرها مقارنةً بـ 6 إلى 8 علامات تجارية مختارة بعناية