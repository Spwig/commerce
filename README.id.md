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
  <strong>Bahasa Indonesia</strong> |
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
  <strong>E-commerce swakelola untuk merchant yang ingin memiliki toko mereka sendiri.</strong>
</p>

<p align="center">
  <a href="https://spwig.com">Situs Web</a> &nbsp;•&nbsp;
  <a href="https://docs.spwig.com">Dokumentasi</a> &nbsp;•&nbsp;
  <a href="https://community.spwig.com">Komunitas</a> &nbsp;•&nbsp;
  <a href="https://spwig.com/id/marketplace">Marketplace</a> &nbsp;•&nbsp;
  <a href="https://spwig.com/id/demos">Demo Langsung</a>
</p>

<p align="center">
  <a href="LICENSE"><img alt="Licence: AGPL v3" src="https://img.shields.io/badge/licence-AGPL--3.0-blue.svg"></a>
  <a href="https://github.com/Spwig/commerce/actions"><img alt="CI" src="https://img.shields.io/github/actions/workflow/status/Spwig/commerce/test.yml?branch=main&label=tests"></a>
  <a href="https://github.com/Spwig/commerce/releases"><img alt="Release" src="https://img.shields.io/github/v/release/Spwig/commerce"></a>
  <a href="https://github.com/Spwig/commerce/discussions"><img alt="Discussions" src="https://img.shields.io/github/discussions/Spwig/commerce"></a>
</p>

## Apa itu Spwig?

Spwig adalah platform e-commerce berfitur lengkap: katalog, keranjang, checkout,
pesanan, pelanggan, pembayaran, pengiriman, tema, page builder, API admin,
POS, langganan, loyalitas, blog, SEO — seluruh tumpukan. Dibangun dengan
**Django 5**, **PostgreSQL**, dan **Redis**, dikirim sebagai sekumpulan container
Docker, berjalan di VPS seharga $5 atau di perangkat keras Anda sendiri.

Berbeda dengan platform hosted, **Anda memiliki kode, database, dan
data pelanggan.** Tidak ada biaya per transaksi. Tidak ada lock-in. Jika Anda ingin
melakukan fork dan menempuh jalan Anda sendiri, lisensi secara eksplisit mengizinkan hal itu.

<br />

## Edisi

Biner yang sama. Sebuah berkas lisensi yang ditandatangani mengaktifkan feature flags saat runtime.
Community adalah yang Anda dapatkan secara default ketika Anda menjalankan `docker compose up`;
peningkatan adalah kunci yang Anda tempelkan ke dalam admin.

| | Community | Pro | Enterprise |
|---|:---:|:---:|:---:|
| E-commerce lengkap, tema, page builder, UI POS | ✓ | ✓ | ✓ |
| Bawa penyedia pembayaran Anda sendiri | ✓ | ✓ | ✓ |
| Bawa penyedia pengiriman Anda sendiri | ✓ | ✓ | ✓ |
| Akses marketplace (tema premium + integrasi) | ✓ | ✓ | ✓ |
| Autocomplete alamat yang di-host Spwig | Gratis · dibatasi rate | Batas lebih tinggi | Batas tertinggi |
| GeoIP yang di-host Spwig (lokasi pengunjung) | Gratis · dibatasi rate | Batas lebih tinggi | Batas tertinggi |
| Push notification (aplikasi admin iOS) | Gratis · dibatasi rate | Batas lebih tinggi | Batas tertinggi |
| Point-of-sale (dukungan terminal POS) | ✓ | ✓ | ✓ |
| Gateway email hosted dengan IP hangat + DKIM | – | ✓ | ✓ |
| Dukungan prioritas | – | ✓ | ✓ |
| SSO Enterprise (Azure AD, Okta) | – | – | ✓ |

<br />

## Mulai cepat

### Opsi 1 — Instalasi satu baris (direkomendasikan)

[Spwig installer](https://github.com/Spwig/spwig) menyiapkan semuanya
dalam satu perintah: Docker, PostgreSQL, Redis, MinIO, TLS via Cloudflare atau
self-signed, wizard boot pertama, pengguna admin. Image yang ditandatangani ditarik dari
`registry.spwig.com`.

```bash
curl -fsSL https://spwig.com/install.sh | sudo bash
```

Peningkatan terjadi melalui admin — lihat [UPGRADING.md](UPGRADING.md).

### Opsi 2 — Dari kode sumber

Anda ingin membangun dari repo ini, mengutak-atiknya, atau mengirimkan sebuah fork:

```bash
git clone https://github.com/Spwig/commerce.git spwig
cd spwig
cp .env.example .env
docker compose up -d
docker compose exec web ./manage.py migrate --noinput
docker compose exec web ./manage.py createsuperuser
```

Storefront di `http://localhost`, admin di `http://localhost/id/admin/`.
Edisi Community aktif otomatis saat boot pertama — tanpa perjalanan bolak-balik
ke server lisensi, tanpa kunci yang diperlukan. Perbarui nanti dengan `git pull` dan
`docker compose build`.

<br />

## Fitur

<table>
  <tr>
    <td width="50%" valign="top">
      <h3>Storefront & checkout</h3>
      <p>Server-rendered secara default — time-to-first-byte yang cepat, bekerja
      tanpa JavaScript, mobile-first (80% traffic berasal dari layar
      kecil). Mode headless opsional via
      <a href="https://github.com/Spwig/headless-sdk">Spwig headless
      SDK</a> dan <a href="https://github.com/Spwig/react">komponen
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
      <h3>Page builder</h3>
      <p>Merchant membangun halaman storefront dari widget yang dapat digunakan kembali — bagian
      hero, grid produk, testimoni, embed — dan melihat pratinjau langsung
      di admin. Widget dipasang dari marketplace atau dari
      repositori komponen Anda sendiri.</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>Manajemen pesanan & pelanggan</h3>
      <p>Setiap pesanan, pengembalian dana, perpanjangan langganan, unduhan digital,
      dan titik kontak pelanggan di satu tempat. Operasi massal,
      peran staf dengan cakupan izin, dapat diekspor ke CSV/XLSX, aplikasi
      admin mobile (iOS) dengan push notification.</p>
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
      <h3>Tema & branding</h3>
      <p>Design token (warna, tipografi, spasi) menggerakkan setiap
      permukaan — storefront dan admin. Ubah satu token, semuanya
      diperbarui. Tema tersedia di
      <a href="https://github.com/Spwig/components">Spwig/components</a>
      dan dipasang melalui marketplace; tulis milik Anda sendiri dengan
      <a href="https://github.com/Spwig/theme-sdk">theme SDK</a>.</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>Point of sale</h3>
      <p>Terminal POS lengkap untuk merchant fisik:
      pemindaian barcode, pembayaran terpisah, pencetakan struk, integrasi
      cash drawer, tampilan menghadap pelanggan, mode offline. Edisi
      Community mengirim kode-nya tetapi permukaan admin menampilkan CTA
      untuk upgrade — patch saja jika Anda melakukan fork, itu tidak masalah.</p>
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
      <h3>Ekosistem provider</h3>
      <p>Apa pun yang berkomunikasi dengan sistem eksternal — pembayaran,
      pengiriman, kurs mata uang, terjemahan, GeoIP, SMS, email — adalah
      provider yang dapat dipasang. Bangun milik Anda sendiri dengan
      <a href="https://github.com/Spwig/provider-sdks">provider SDKs</a>,
      publikasikan ke marketplace, atau host sendiri registry privat.</p>
    </td>
  </tr>
</table>

<br />

## Arsitektur

- **Single-tenant.** Setiap instalasi adalah satu toko, satu merchant, satu
  Django Site. Merchant multi-toko menjalankan satu instalasi Spwig per toko.
- **Monolit modular.** Bukan mesh microservice. Sebuah proses Django tunggal
  menangani storefront + admin + REST API + Celery workers.
  Sederhana untuk di-deploy, dipahami, dan di-fork.
- **Gerbang fitur runtime.** Community/Pro/Enterprise semuanya menjalankan
  biner yang sama. Lisensi yang ditandatangani mengaktifkan flag — tanpa penghapusan kode.

Tur lengkap: [ARCHITECTURE.md](ARCHITECTURE.md).

<br />

## Komunitas & dukungan

- **Diskusi.** Pertanyaan terbuka, ide, show-and-tell:
  [github.com/Spwig/commerce/discussions](https://github.com/Spwig/commerce/discussions).
- **Forum komunitas.** [community.spwig.com](https://community.spwig.com)
  — thread berbentuk panjang, resep praktik terbaik, showcase ekstensi.
- **Laporan bug.** [Issues](https://github.com/Spwig/commerce/issues)
  dengan langkah-langkah reproduksi. Lihat [SECURITY.md](SECURITY.md) untuk
  pengungkapan kerentanan.
- **Dukungan komersial.** Tersedia untuk lisensi Pro dan Enterprise.

<br />

## Berkontribusi

Kami menggunakan **DCO** (Developer Certificate of Origin) — setiap commit
di-sign off dengan `git commit -s`. Tanpa dokumen, tanpa CLA. Panduan lengkap di
[CONTRIBUTING.md](CONTRIBUTING.md).

Catatan untuk asisten koding AI yang bekerja di repo ini ada di
[CLAUDE.md](CLAUDE.md).

<br />

## Ekosistem

Proyek open-source terkait di bawah [organisasi Spwig](https://github.com/Spwig):

| Repo | Apa itu |
|---|---|
| [Spwig/commerce](https://github.com/Spwig/commerce) | Repo ini — platform inti (AGPL-3.0-or-later) |
| [Spwig/spwig](https://github.com/Spwig/spwig) | Installer satu baris |
| [Spwig/components](https://github.com/Spwig/components) | Tema, integrasi, dan utilitas (AGPL-3.0-or-later) |
| [Spwig/theme-sdk](https://github.com/Spwig/theme-sdk) | SDK untuk membangun tema (Apache-2.0) |
| [Spwig/provider-sdks](https://github.com/Spwig/provider-sdks) | SDK untuk membangun provider pembayaran / pengiriman / dll. (Apache-2.0) |
| [Spwig/headless-sdk](https://github.com/Spwig/headless-sdk) | SDK klien headless / API (Apache-2.0) |
| [Spwig/react](https://github.com/Spwig/react) | Pustaka komponen React (Apache-2.0) |

<br />

## Lisensi

Spwig menggunakan [AGPL-3.0-or-later](LICENSE). Anda dapat menjalankannya, memodifikasinya,
mendistribusikannya, menawarkannya sebagai layanan hosted — semuanya diizinkan. Versi yang
dimodifikasi yang ditawarkan melalui jaringan harus menyediakan kode sumbernya untuk
para penggunanya. Itulah inti dari AGPL dibandingkan GPL.

Integrasi provider yang dibangun dengan SDK bersifat Apache-2.0, sehingga membangun
integrasi pembayaran / pengiriman / SMS proprietary di atas SDK
tidak memicu AGPL. Ini disengaja — kami menginginkan ekosistem
provider yang berkembang.

<br />

## Privasi & telemetri

Spwig mengirim satu ping anonim per hari ke `updates.spwig.com/api/v1/telemetry/`:

- UUID instalasi (dihasilkan saat boot pertama, disimpan secara lokal)
- Versi Spwig
- Edisi (community / pro / enterprise / trial / dev)
- Negara (diselesaikan dari IP di ingress; IP itu sendiri tidak disimpan)
- Jumlah bucket dari feature flags (penyedia pembayaran yang dikonfigurasi, tema
  yang terpasang) — tidak pernah data pelanggan atau pesanan mentah

**Opt out** dengan `SPWIG_TELEMETRY=0` di environment Anda. Itu akan membalik
`settings.SPWIG_TELEMETRY_ENABLED` dan tugas beat harian menjadi no-op.

<br />

<p align="center">
  <sub>
    Dibangun dengan penuh perhatian di Singapura.
    <br />
    <a href="https://spwig.com">spwig.com</a> — <a href="https://docs.spwig.com">docs</a> — <a href="https://community.spwig.com">community</a>
  </sub>
</p>
