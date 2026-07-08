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
  <a href="README.ar.md">العربية</a> |
  <strong>हिन्दी</strong> |
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
  <strong>उन व्यापारियों के लिए सेल्फ़-होस्टेड ई-कॉमर्स जो अपनी दुकान का स्वामित्व रखना चाहते हैं।</strong>
</p>

<p align="center">
  <a href="https://spwig.com">वेबसाइट</a> &nbsp;•&nbsp;
  <a href="https://docs.spwig.com">दस्तावेज़ीकरण</a> &nbsp;•&nbsp;
  <a href="https://community.spwig.com">समुदाय</a> &nbsp;•&nbsp;
  <a href="https://spwig.com/hi/marketplace">मार्केटप्लेस</a> &nbsp;•&nbsp;
  <a href="https://spwig.com/hi/demos">लाइव डेमो</a>
</p>

<p align="center">
  <a href="LICENSE"><img alt="Licence: AGPL v3" src="https://img.shields.io/badge/licence-AGPL--3.0-blue.svg"></a>
  <a href="https://github.com/Spwig/commerce/actions"><img alt="CI" src="https://img.shields.io/github/actions/workflow/status/Spwig/commerce/test.yml?branch=main&label=tests"></a>
  <a href="https://github.com/Spwig/commerce/releases"><img alt="Release" src="https://img.shields.io/github/v/release/Spwig/commerce"></a>
  <a href="https://github.com/Spwig/commerce/discussions"><img alt="Discussions" src="https://img.shields.io/github/discussions/Spwig/commerce"></a>
</p>

## Spwig क्या है?

Spwig एक पूर्ण-सुविधायुक्त ई-कॉमर्स प्लेटफ़ॉर्म है: कैटलॉग, कार्ट, चेकआउट,
ऑर्डर, ग्राहक, भुगतान, शिपिंग, थीम, पेज बिल्डर, एडमिन API,
POS, सब्सक्रिप्शन, लॉयल्टी, ब्लॉग, SEO — पूरा स्टैक। **Django 5**,
**PostgreSQL**, और **Redis** के साथ निर्मित, Docker कंटेनरों के एक
सेट के रूप में शिप होता है, $5 के VPS पर या आपके अपने हार्डवेयर पर
चलता है।

होस्टेड प्लेटफ़ॉर्मों के विपरीत, **कोड, डेटाबेस, और ग्राहक डेटा का स्वामित्व
आपके पास होता है।** कोई प्रति-लेनदेन शुल्क नहीं। कोई लॉक-इन नहीं। यदि आप
इसे फ़ोर्क करके अपने रास्ते जाना चाहते हैं, तो लाइसेंस स्पष्ट रूप से इसकी
अनुमति देता है।

<br />

## संस्करण

एक ही बाइनरी। एक हस्ताक्षरित लाइसेंस फ़ाइल रनटाइम पर फ़ीचर फ़्लैग को टॉगल
करती है। जब आप `docker compose up` चलाते हैं तो डिफ़ॉल्ट रूप से आपको
Community मिलता है; अपग्रेड करना केवल एक कुंजी है जिसे आप एडमिन में
पेस्ट करते हैं।

| | Community | Pro | Enterprise |
|---|:---:|:---:|:---:|
| पूर्ण ई-कॉमर्स, थीम, पेज बिल्डर, POS UI | ✓ | ✓ | ✓ |
| अपने स्वयं के भुगतान प्रदाता लाएँ | ✓ | ✓ | ✓ |
| अपने स्वयं के शिपिंग प्रदाता लाएँ | ✓ | ✓ | ✓ |
| मार्केटप्लेस एक्सेस (प्रीमियम थीम + एकीकरण) | ✓ | ✓ | ✓ |
| Spwig-होस्टेड पता ऑटोकंप्लीट | निःशुल्क · दर-सीमित | उच्चतर सीमा | उच्चतम सीमा |
| Spwig-होस्टेड GeoIP (विज़िटर स्थान) | निःशुल्क · दर-सीमित | उच्चतर सीमा | उच्चतम सीमा |
| पुश सूचनाएँ (iOS एडमिन ऐप) | निःशुल्क · दर-सीमित | उच्चतर सीमा | उच्चतम सीमा |
| पॉइंट-ऑफ़-सेल (POS टर्मिनल समर्थन) | – | ✓ | ✓ |
| वार्म IPs + DKIM के साथ होस्टेड ईमेल गेटवे | – | ✓ | ✓ |
| प्राथमिकता समर्थन | – | ✓ | ✓ |
| एंटरप्राइज़ SSO (Azure AD, Okta) | – | – | ✓ |

<br />

## त्वरित प्रारंभ

### विकल्प 1 — एक-पंक्ति स्थापना (अनुशंसित)

[Spwig इंस्टॉलर](https://github.com/Spwig/spwig) एक ही कमांड में सब कुछ
सेट कर देता है: Docker, PostgreSQL, Redis, MinIO, Cloudflare के माध्यम से
TLS या सेल्फ़-साइन्ड, फ़र्स्ट-बूट विज़ार्ड, एडमिन उपयोगकर्ता। हस्ताक्षरित
इमेज `registry.spwig.com` से खींची जाती हैं।

```bash
curl -fsSL https://spwig.com/install.sh | sudo bash
```

अपग्रेड एडमिन के माध्यम से होते हैं — [UPGRADING.md](UPGRADING.md) देखें।

### विकल्प 2 — स्रोत से

आप इस रेपो से बिल्ड करना चाहते हैं, इस पर हैक करना चाहते हैं, या एक फ़ोर्क शिप करना चाहते हैं:

```bash
git clone https://github.com/Spwig/commerce.git spwig
cd spwig
cp .env.example .env
docker compose up -d
docker compose exec web ./manage.py migrate --noinput
docker compose exec web ./manage.py createsuperuser
```

स्टोरफ़्रंट `http://localhost` पर, एडमिन `http://localhost/hi/admin/` पर।
Community संस्करण पहले बूट पर स्वतः-सक्रिय होता है — कोई लाइसेंस सर्वर
राउंड-ट्रिप नहीं, कोई कुंजी आवश्यक नहीं। बाद में `git pull` और
`docker compose build` के साथ अपग्रेड करें।

<br />

## विशेषताएँ

<table>
  <tr>
    <td width="50%" valign="top">
      <h3>स्टोरफ़्रंट और चेकआउट</h3>
      <p>डिफ़ॉल्ट रूप से सर्वर-रेंडर्ड — तेज़ टाइम-टू-फ़र्स्ट-बाइट, JavaScript
      के बिना काम करता है, मोबाइल-फ़र्स्ट (80% ट्रैफ़िक छोटी स्क्रीन पर
      होता है)। वैकल्पिक हेडलेस मोड
      <a href="https://github.com/Spwig/headless-sdk">Spwig headless
      SDK</a> और <a href="https://github.com/Spwig/react">React
      कंपोनेंट्स</a> के माध्यम से।</p>
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
      <h3>पेज बिल्डर</h3>
      <p>व्यापारी पुनः प्रयोज्य विजेट्स से स्टोरफ़्रंट पेज बनाते हैं — हीरो
      सेक्शन, प्रोडक्ट ग्रिड, प्रशंसापत्र, एम्बेड — और एडमिन में लाइव
      पूर्वावलोकन करते हैं। विजेट्स मार्केटप्लेस से या आपके अपने
      कंपोनेंट रिपॉज़िटरी से इंस्टॉल होते हैं।</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>ऑर्डर और ग्राहक प्रबंधन</h3>
      <p>प्रत्येक ऑर्डर, रिफ़ंड, सब्सक्रिप्शन नवीनीकरण, डिजिटल डाउनलोड,
      और ग्राहक टचपॉइंट एक ही स्थान पर। बल्क ऑपरेशन,
      अनुमति-दायरे वाली स्टाफ़ भूमिकाएँ, CSV/XLSX में निर्यात योग्य, पुश
      सूचनाओं के साथ मोबाइल एडमिन ऐप (iOS)।</p>
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
      <h3>थीम और ब्रांडिंग</h3>
      <p>डिज़ाइन टोकन (रंग, टाइपोग्राफ़ी, स्पेसिंग) हर सतह को संचालित करते
      हैं — स्टोरफ़्रंट और एडमिन दोनों। एक टोकन बदलें, सब कुछ अपडेट हो
      जाता है। थीम
      <a href="https://github.com/Spwig/components">Spwig/components</a>
      में रहती हैं और मार्केटप्लेस के माध्यम से इंस्टॉल होती हैं; अपनी थीम
      <a href="https://github.com/Spwig/theme-sdk">theme SDK</a> के साथ लिखें।</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>पॉइंट ऑफ़ सेल (Pro+)</h3>
      <p>ईंट-और-मोर्टार व्यापारियों के लिए पूर्ण POS टर्मिनल:
      बारकोड स्कैनिंग, विभाजित भुगतान, रसीद प्रिंटिंग, कैश ड्रॉअर
      एकीकरण, ग्राहक-सामने प्रदर्शन, ऑफ़लाइन मोड। Community
      संस्करण कोड शिप करता है लेकिन एडमिन सतह एक अपग्रेड CTA दिखाती
      है — यदि आप फ़ोर्क करते हैं तो इसे पैच कर दें, यह ठीक है।</p>
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
      <h3>प्रदाता पारिस्थितिकी तंत्र</h3>
      <p>कुछ भी जो किसी बाहरी प्रणाली से बात करता है — भुगतान,
      शिपिंग, विनिमय दरें, अनुवाद, GeoIP, SMS, ईमेल — एक
      प्लग करने योग्य प्रदाता है। अपना स्वयं का
      <a href="https://github.com/Spwig/provider-sdks">provider SDKs</a>
      के साथ बनाएँ, मार्केटप्लेस पर प्रकाशित करें, या एक निजी रजिस्ट्री सेल्फ़-होस्ट करें।</p>
    </td>
  </tr>
</table>

<br />

## आर्किटेक्चर

- **सिंगल-टेनेंट।** प्रत्येक इंस्टॉल एक दुकान, एक व्यापारी, एक
  Django Site है। बहु-दुकान व्यापारी प्रति दुकान एक Spwig इंस्टॉल चलाते हैं।
- **मॉड्यूलर मोनोलिथ।** माइक्रोसर्विस मेश नहीं। एक एकल Django
  प्रोसेस स्टोरफ़्रंट + एडमिन + REST API + Celery वर्कर्स को संभालती है।
  डिप्लॉय करना, समझना और फ़ोर्क करना सरल है।
- **रनटाइम फ़ीचर गेट्स।** Community/Pro/Enterprise सभी एक ही
  बाइनरी चलाते हैं। एक हस्ताक्षरित लाइसेंस फ़्लैग को टॉगल करता है — कोई कोड स्ट्रिपिंग नहीं।

पूर्ण दौरा: [ARCHITECTURE.md](ARCHITECTURE.md)।

<br />

## समुदाय और समर्थन

- **चर्चाएँ।** ओपन-एंडेड प्रश्न, विचार, शो-एंड-टेल:
  [github.com/Spwig/commerce/discussions](https://github.com/Spwig/commerce/discussions)।
- **समुदाय फ़ोरम।** [community.spwig.com](https://community.spwig.com)
  — लंबे-रूप के थ्रेड, सर्वोत्तम-अभ्यास रेसिपी, एक्सटेंशन प्रदर्शन।
- **बग रिपोर्ट।** पुनरुत्पादन चरणों के साथ
  [Issues](https://github.com/Spwig/commerce/issues)। भेद्यता प्रकटीकरण के
  लिए [SECURITY.md](SECURITY.md) देखें।
- **वाणिज्यिक समर्थन।** Pro और Enterprise लाइसेंसों के लिए उपलब्ध।

<br />

## योगदान

हम **DCO** (Developer Certificate of Origin) का उपयोग करते हैं — प्रत्येक कमिट
`git commit -s` के साथ साइन-ऑफ़ होता है। कोई कागज़ी कार्रवाई नहीं, कोई CLA नहीं। पूर्ण गाइड
[CONTRIBUTING.md](CONTRIBUTING.md) में।

रेपो पर काम कर रहे AI कोडिंग सहायकों के लिए नोट्स
[CLAUDE.md](CLAUDE.md) में हैं।

<br />

## पारिस्थितिकी तंत्र

[Spwig org](https://github.com/Spwig) के तहत संबंधित ओपन-सोर्स परियोजनाएँ:

| Repo | यह क्या है |
|---|---|
| [Spwig/commerce](https://github.com/Spwig/commerce) | यह रेपो — मुख्य प्लेटफ़ॉर्म (AGPL-3.0-or-later) |
| [Spwig/spwig](https://github.com/Spwig/spwig) | एक-पंक्ति इंस्टॉलर |
| [Spwig/components](https://github.com/Spwig/components) | थीम, एकीकरण, और उपयोगिताएँ (AGPL-3.0-or-later) |
| [Spwig/theme-sdk](https://github.com/Spwig/theme-sdk) | थीम बनाने के लिए SDK (Apache-2.0) |
| [Spwig/provider-sdks](https://github.com/Spwig/provider-sdks) | भुगतान / शिपिंग / आदि प्रदाता बनाने के लिए SDKs (Apache-2.0) |
| [Spwig/headless-sdk](https://github.com/Spwig/headless-sdk) | हेडलेस / API क्लाइंट SDK (Apache-2.0) |
| [Spwig/react](https://github.com/Spwig/react) | React कंपोनेंट लाइब्रेरी (Apache-2.0) |

<br />

## लाइसेंस

Spwig [AGPL-3.0-or-later](LICENSE) है। आप इसे चला सकते हैं, संशोधित कर सकते हैं,
वितरित कर सकते हैं, इसे होस्टेड सेवा के रूप में पेश कर सकते हैं — सब अनुमत है। संशोधित
संस्करण जो एक नेटवर्क पर पेश किए जाते हैं, उन्हें अपने उपयोगकर्ताओं को अपना स्रोत उपलब्ध
कराना चाहिए। यही GPL पर AGPL का पूरा उद्देश्य है।

SDKs के साथ बनाए गए प्रदाता एकीकरण Apache-2.0 हैं, इसलिए SDKs के ऊपर
एक स्वामित्व वाला भुगतान / शिपिंग / SMS एकीकरण बनाने से
AGPL ट्रिगर नहीं होता। यह जानबूझकर है — हम एक फलता-फूलता
प्रदाता पारिस्थितिकी तंत्र चाहते हैं।

<br />

## गोपनीयता और टेलीमेट्री

Spwig `updates.spwig.com/api/v1/telemetry/` पर प्रति दिन एक अनाम पिंग भेजता है:

- इंस्टॉल UUID (पहले बूट पर उत्पन्न, स्थानीय रूप से संग्रहीत)
- Spwig संस्करण
- संस्करण (community / pro / enterprise / trial / dev)
- देश (प्रवेश पर IP से हल किया गया; IP स्वयं संग्रहीत नहीं है)
- फ़ीचर फ़्लैग की बकेट गणना (कॉन्फ़िगर किए गए भुगतान प्रदाता, इंस्टॉल की
  गई थीम) — कभी भी कच्चा ग्राहक या ऑर्डर डेटा नहीं

अपने वातावरण में `SPWIG_TELEMETRY=0` के साथ **ऑप्ट आउट** करें। यह
`settings.SPWIG_TELEMETRY_ENABLED` को पलट देता है और दैनिक बीट टास्क कुछ नहीं करता।

<br />

<p align="center">
  <sub>
    सिंगापुर में सावधानी से निर्मित।
    <br />
    <a href="https://spwig.com">spwig.com</a> — <a href="https://docs.spwig.com">docs</a> — <a href="https://community.spwig.com">community</a>
  </sub>
</p>
