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
  <a href="README.hi.md">हिन्दी</a> |
  <a href="README.id.md">Bahasa Indonesia</a> |
  <a href="README.it.md">Italiano</a> |
  <a href="README.ko.md">한국어</a> |
  <strong>Türkçe</strong> |
  <a href="README.vi.md">Tiếng Việt</a> |
  <a href="README.th.md">ไทย</a>
</p>

<p align="center">
  <img src="https://spwig.com/images/logo.svg" alt="Spwig" width="200">
</p>

<h1 align="center">Spwig</h1>

<p align="center">
  <strong>Mağazasının sahibi olmak isteyen satıcılar için kendi sunucunda barındırılan e-ticaret.</strong>
</p>

<p align="center">
  <a href="https://spwig.com">Web Sitesi</a> &nbsp;•&nbsp;
  <a href="https://docs.spwig.com">Belgeler</a> &nbsp;•&nbsp;
  <a href="https://community.spwig.com">Topluluk</a> &nbsp;•&nbsp;
  <a href="https://spwig.com/tr/marketplace">Pazar Yeri</a> &nbsp;•&nbsp;
  <a href="https://spwig.com/tr/demos">Canlı Demolar</a>
</p>

<p align="center">
  <a href="LICENSE"><img alt="Licence: AGPL v3" src="https://img.shields.io/badge/licence-AGPL--3.0-blue.svg"></a>
  <a href="https://github.com/Spwig/commerce/actions"><img alt="CI" src="https://img.shields.io/github/actions/workflow/status/Spwig/commerce/test.yml?branch=main&label=tests"></a>
  <a href="https://github.com/Spwig/commerce/releases"><img alt="Release" src="https://img.shields.io/github/v/release/Spwig/commerce"></a>
  <a href="https://github.com/Spwig/commerce/discussions"><img alt="Discussions" src="https://img.shields.io/github/discussions/Spwig/commerce"></a>
</p>

## Spwig nedir?

Spwig tam donanımlı bir e-ticaret platformudur: katalog, sepet, ödeme,
siparişler, müşteriler, ödemeler, kargo, temalar, sayfa oluşturucu, yönetim API'si,
POS, abonelikler, sadakat, blog, SEO — tüm yığın. **Django 5**,
**PostgreSQL** ve **Redis** ile geliştirilmiştir; bir Docker
konteyner seti olarak dağıtılır ve 5 dolarlık bir VPS'te veya kendi donanımınızda çalışır.

Barındırılan platformların aksine, **kodun, veritabanının ve
müşteri verilerinin sahibi sizsiniz.** İşlem başına ücret yok. Bağımlılık yok. Fork'layıp
kendi yolunuza gitmek isterseniz, lisans buna açıkça izin verir.

<br />

## Sürümler

Aynı ikili dosya. İmzalı bir lisans dosyası, özellik bayraklarını çalışma zamanında değiştirir.
Community, `docker compose up` çalıştırdığınızda varsayılan olarak elde ettiğinizdir;
yükseltme, yönetim paneline yapıştırdığınız bir anahtardır.

| | Community | Pro | Enterprise |
|---|:---:|:---:|:---:|
| Tam e-ticaret, temalar, sayfa oluşturucu, POS arayüzü | ✓ | ✓ | ✓ |
| Kendi ödeme sağlayıcılarınızı getirin | ✓ | ✓ | ✓ |
| Kendi kargo sağlayıcılarınızı getirin | ✓ | ✓ | ✓ |
| Pazar yeri erişimi (premium temalar + entegrasyonlar) | ✓ | ✓ | ✓ |
| Spwig tarafından barındırılan adres otomatik tamamlama | Ücretsiz · hız sınırlı | Daha yüksek limit | En yüksek limit |
| Spwig tarafından barındırılan GeoIP (ziyaretçi konumu) | Ücretsiz · hız sınırlı | Daha yüksek limit | En yüksek limit |
| Push bildirimleri (iOS yönetim uygulaması) | Ücretsiz · hız sınırlı | Daha yüksek limit | En yüksek limit |
| Satış noktası (POS terminal desteği) | ✓ | ✓ | ✓ |
| Sıcak IP'ler + DKIM ile barındırılan e-posta ağ geçidi | – | ✓ | ✓ |
| Öncelikli destek | – | ✓ | ✓ |
| Kurumsal SSO (Azure AD, Okta) | – | – | ✓ |

<br />

## Hızlı başlangıç

### Seçenek 1 — Tek satırlık kurulum (önerilen)

[Spwig yükleyicisi](https://github.com/Spwig/spwig) her şeyi tek bir
komutla ayarlar: Docker, PostgreSQL, Redis, MinIO, Cloudflare veya
kendinden imzalı sertifika ile TLS, ilk açılış sihirbazı, yönetici kullanıcı. İmzalı görüntüler
`registry.spwig.com` adresinden çekilir.

```bash
curl -fsSL https://spwig.com/install.sh | sudo bash
```

Yükseltmeler yönetim paneli üzerinden gerçekleşir — bkz. [UPGRADING.md](UPGRADING.md).

### Seçenek 2 — Kaynaktan

Bu depodan derlemek, üzerinde çalışmak veya bir fork göndermek istiyorsanız:

```bash
git clone https://github.com/Spwig/commerce.git spwig
cd spwig
cp .env.example .env
docker compose up -d
docker compose exec web ./manage.py migrate --noinput
docker compose exec web ./manage.py createsuperuser
```

Mağaza `http://localhost` üzerinde, yönetim paneli `http://localhost/tr/admin/` üzerinde.
Community sürümü ilk açılışta otomatik olarak etkinleştirilir — lisans sunucusu
gidiş dönüşü yok, anahtar gerekmez. Daha sonra `git pull` ve
`docker compose build` ile yükseltin.

<br />

## Özellikler

<table>
  <tr>
    <td width="50%" valign="top">
      <h3>Mağaza ve ödeme</h3>
      <p>Varsayılan olarak sunucu tarafında oluşturulur — hızlı ilk bayt süresi,
      JavaScript olmadan çalışır, mobil öncelikli (trafiğin %80'i küçük
      ekranlardan gelir). <a href="https://github.com/Spwig/headless-sdk">Spwig
      headless SDK</a> ve <a href="https://github.com/Spwig/react">React
      bileşenleri</a> üzerinden isteğe bağlı headless modu.</p>
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
      <h3>Sayfa oluşturucu</h3>
      <p>Satıcılar mağaza sayfalarını yeniden kullanılabilir widget'lardan oluşturur — hero
      bölümleri, ürün ızgaraları, referanslar, gömme içerikler — ve yönetim panelinde
      canlı önizler. Widget'lar pazar yerinden veya kendi
      bileşen deponuzdan kurulur.</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>Sipariş ve müşteri yönetimi</h3>
      <p>Her sipariş, iade, abonelik yenilemesi, dijital indirme
      ve müşteri temas noktası tek bir yerde. Toplu işlemler,
      izin kapsamlı personel rolleri, CSV/XLSX olarak dışa aktarılabilir, push bildirimli
      mobil yönetim uygulaması (iOS).</p>
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
      <h3>Temalar ve markalaşma</h3>
      <p>Tasarım token'ları (renkler, tipografi, boşluk) her yüzeyi yönetir
      — mağaza ve yönetim paneli. Bir token'ı değiştirin, her şey
      güncellenir. Temalar
      <a href="https://github.com/Spwig/components">Spwig/components</a>
      içinde yaşar ve pazar yerinden kurulur;
      <a href="https://github.com/Spwig/theme-sdk">theme SDK</a> ile kendinizinkini yazın.</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>Satış noktası</h3>
      <p>Fiziksel mağaza satıcıları için tam POS terminali:
      barkod tarama, bölünmüş ödemeler, fiş yazdırma, para çekmecesi
      entegrasyonu, müşteriye dönük ekran, çevrimdışı mod. Included in every edition — no upgrade required.</p>
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
      <h3>Sağlayıcı ekosistemi</h3>
      <p>Harici bir sistemle konuşan her şey — ödemeler,
      kargo, döviz kurları, çeviri, GeoIP, SMS, e-posta — takılabilir bir
      sağlayıcıdır. <a href="https://github.com/Spwig/provider-sdks">provider SDKs</a>
      ile kendinizinkini oluşturun, pazar yerinde yayınlayın veya özel bir kayıt defterini kendiniz barındırın.</p>
    </td>
  </tr>
</table>

<br />

## Mimari

- **Tek kiracılı.** Her kurulum bir mağaza, bir satıcı, bir
  Django Site'tir. Çok mağazalı satıcılar mağaza başına bir Spwig kurulumu çalıştırır.
- **Modüler monolit.** Bir mikroservis ağı değildir. Tek bir Django
  süreci mağaza + yönetim + REST API + Celery işçilerini yönetir.
  Dağıtımı, akıl yürütmesi ve fork'lanması basittir.
- **Çalışma zamanı özellik kapıları.** Community/Pro/Enterprise'ın hepsi
  aynı ikili dosyayı çalıştırır. İmzalı bir lisans bayrakları değiştirir — kod çıkarma yok.

Tam tur: [ARCHITECTURE.md](ARCHITECTURE.md).

<br />

## Topluluk ve destek

- **Tartışmalar.** Uçtan uca sorular, fikirler, gösterip anlatma:
  [github.com/Spwig/commerce/discussions](https://github.com/Spwig/commerce/discussions).
- **Topluluk forumu.** [community.spwig.com](https://community.spwig.com)
  — uzun soluklu konular, en iyi uygulama tarifleri, uzantı vitrinleri.
- **Hata raporları.** Yeniden üretme adımlarıyla [Issues](https://github.com/Spwig/commerce/issues).
  Güvenlik açığı ifşası için [SECURITY.md](SECURITY.md) dosyasına bakın.
- **Ticari destek.** Pro ve Enterprise lisansları için mevcuttur.

<br />

## Katkıda bulunma

**DCO** (Developer Certificate of Origin) kullanıyoruz — her commit
`git commit -s` ile imzalanır. Kağıt işi yok, CLA yok. Tam kılavuz
[CONTRIBUTING.md](CONTRIBUTING.md) içinde.

Depoda çalışan AI kod yardımcıları için notlar
[CLAUDE.md](CLAUDE.md) içinde.

<br />

## Ekosistem

[Spwig org](https://github.com/Spwig) altındaki ilgili açık kaynak projeler:

| Depo | Nedir |
|---|---|
| [Spwig/commerce](https://github.com/Spwig/commerce) | Bu depo — çekirdek platform (AGPL-3.0-or-later) |
| [Spwig/spwig](https://github.com/Spwig/spwig) | Tek satırlık yükleyici |
| [Spwig/components](https://github.com/Spwig/components) | Temalar, entegrasyonlar ve yardımcı programlar (AGPL-3.0-or-later) |
| [Spwig/theme-sdk](https://github.com/Spwig/theme-sdk) | Tema oluşturma için SDK (Apache-2.0) |
| [Spwig/provider-sdks](https://github.com/Spwig/provider-sdks) | Ödeme / kargo / vb. sağlayıcıları oluşturma için SDK'lar (Apache-2.0) |
| [Spwig/headless-sdk](https://github.com/Spwig/headless-sdk) | Headless / API istemci SDK'sı (Apache-2.0) |
| [Spwig/react](https://github.com/Spwig/react) | React bileşen kütüphanesi (Apache-2.0) |

<br />

## Lisans

Spwig [AGPL-3.0-or-later](LICENSE) lisanslıdır. Onu çalıştırabilir, değiştirebilir,
dağıtabilir, barındırılan bir hizmet olarak sunabilirsiniz — tümüne izin verilir. Bir ağ üzerinden
sunulan değiştirilmiş sürümler, kaynağını kullanıcılarına
sunmalıdır. AGPL'nin GPL'ye göre tüm amacı budur.

SDK'larla oluşturulan sağlayıcı entegrasyonları Apache-2.0'dır, bu nedenle SDK'lar üzerinde
tescilli bir ödeme / kargo / SMS entegrasyonu inşa etmek
AGPL'yi tetiklemez. Bu bilinçlidir — gelişen bir
sağlayıcı ekosistemi istiyoruz.

<br />

## Gizlilik ve telemetri

Spwig günde bir anonim ping'i `updates.spwig.com/api/v1/telemetry/` adresine gönderir:

- Kurulum UUID'si (ilk açılışta oluşturulur, yerel olarak saklanır)
- Spwig sürümü
- Sürüm (community / pro / enterprise / trial / dev)
- Ülke (girişte IP'den çözümlenir; IP'nin kendisi saklanmaz)
- Özellik bayraklarının kova sayıları (yapılandırılmış ödeme sağlayıcıları, kurulu
  temalar) — asla ham müşteri veya sipariş verisi değil

Ortamınızda `SPWIG_TELEMETRY=0` ile **devre dışı bırakın**. Bu,
`settings.SPWIG_TELEMETRY_ENABLED` değerini değiştirir ve günlük beat görevi hiçbir şey yapmaz.

<br />

<p align="center">
  <sub>
    Singapur'da özenle geliştirildi.
    <br />
    <a href="https://spwig.com">spwig.com</a> — <a href="https://docs.spwig.com">docs</a> — <a href="https://community.spwig.com">community</a>
  </sub>
</p>
