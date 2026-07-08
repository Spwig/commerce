---
title: Pengantar Webhooks
---

Webhooks memungkinkan toko Anda memberi tahu sistem eksternal secara otomatis — seperti alat manajemen stok, ERP, layanan penyelesaian, atau aplikasi khusus — setiap kali terjadi sesuatu di toko Anda. Sebaliknya dari sistem-sistem tersebut yang terus-menerus bertanya "apakah ada perubahan?", toko Anda mengirimkan notifikasi saat kejadian terjadi.

## Apa yang dilakukan webhooks

Ketika terjadi kejadian di toko Anda (sebuah pesanan ditempatkan, pembayaran diterima, produk habis), Spwig mengirimkan permintaan HTTP POST dengan data kejadian ke URL yang Anda konfigurasikan. Sistem penerima kemudian dapat bertindak terhadap data tersebut secara langsung — misalnya, memperbarui stok, memicu label pengiriman, atau mengirimkan notifikasi khusus.

Penggunaan umum webhooks meliputi:

- Sinkronisasi pesanan secara real-time dengan mitra penyelesaian
- Memperbarui stok di ERP ketika stok berubah
- Memicu notifikasi SMS atau push untuk perubahan status pesanan
- Mencatat kejadian di gudang data untuk pelaporan
- Menghubungkan ke alat otomasi seperti Zapier atau Make

## Melihat dan mengelola endpoint

Navigasikan ke **Integrations > Webhooks** untuk melihat semua endpoint webhook yang dikonfigurasikan Anda.

![Daftar endpoint webhook](/static/core/admin/img/help/webhooks-overview/endpoint-list.webp)

Daftar ini menampilkan nama setiap endpoint, URL, status aktif, jumlah kejadian yang didaftarkannya, status kesehatannya, dan kapan terakhir kali endpoint tersebut menerima pengiriman.

### Indikator kesehatan

Kolom **Kesehatan** menunjukkan secara sekilas seberapa baik setiap endpoint berfungsi:

- **Sehat** — Semua pengiriman terbaru berhasil
- **Diturunkan** — Beberapa kegagalan terbaru tetapi endpoint masih aktif
- **Tidak sehat / Dinonaktifkan** — Endpoint secara otomatis dinonaktifkan setelah terlalu banyak kegagalan berurutan (10 secara default). Anda harus mengaktifkannya secara manual setelah masalah mendasar diperbaiki.

## Membuat endpoint webhook

Klik **+ Tambahkan Endpoint Webhook** untuk membuka wizard pengaturan. Wizard ini akan memandu Anda melalui empat langkah.

### Langkah 1: Informasi dasar

- **Nama** — Label ramah untuk mengidentifikasi endpoint ini (misalnya, `Layanan Penyelesaian Pesanan` atau `Sinkronisasi Stok`).
- **URL** — URL lengkap dari server yang akan menerima permintaan POST webhook. Ini harus dapat diakses secara publik (bukan URL localhost).
- **Deskripsi** — Catatan opsional tentang apa yang digunakan endpoint ini.
- **Aktif** — Apakah endpoint ini harus menerima pengiriman. Centang untuk menonaktifkan sementara tanpa menghapus endpoint.

### Langkah 2: Langganan kejadian

Pilih kejadian mana yang harus memicu pengiriman ke endpoint ini. Kejadian dikelompokkan berdasarkan kategori:

#### Kejadian pesanan

| Kejadian | Saat terjadi |
|---------|-------------|
| `order.created` | Pesanan baru ditempatkan |
| `order.paid` | Pembayaran untuk pesanan dikonfirmasi |
| `order.cancelled` | Pesanan dibatalkan |
| `order.fulfilled` | Semua item dalam pesanan dikirim |
| `order.partially_fulfilled` | Beberapa item dalam pesanan dikirim |
| `order.status_changed` | Status pesanan berubah |
| `order.note_added` | Catatan ditambahkan ke pesanan |

#### Kejadian pembayaran

| Kejadian | Saat terjadi |
|---------|-------------|
| `payment.received` | Pembayaran diterima |
| `payment.failed` | Upaya pembayaran gagal |
| `payment.pending` | Pembayaran menunggu konfirmasi |

#### Kejadian pengiriman

| Kejadian | Saat terjadi |
|---------|-------------|
| `shipment.created` | Pengiriman dibuat |
| `shipment.shipped` | Pengiriman dikirimkan |
| `shipment.delivered` | Pengiriman diterima |
| `shipment.returned` | Pengiriman dikembalikan |
| `shipment.tracking_updated` | Informasi pelacakan diperbarui |

#### Kejadian stok

| Kejadian | Saat terjadi |
|---------|-------------|
| `inventory.low_stock` | Stok turun di bawah ambang batas |
| `inventory.out_of_stock` | Produk habis |
| `inventory.restocked` | Produk dikembalikan ke stok |
| `inventory.adjusted` | Stok diubah secara manual |

#### Kejadian produk

`product.created`, `product.updated`, `product.deleted`, `product.published`, `product.unpublished`

#### Kejadian pelanggan


`customer.created`, `customer.updated`, `customer.deleted`

#### Acara Langganan

`subscription.created`, `subscription.activated`, `subscription.renewed`, `subscription.cancelled`, `subscription.expired`, `subscription.paused`, `subscription.resumed`, `subscription.payment_failed`

#### Acara Lainnya

`refund.created`, `refund.completed`, `refund.failed`, `cart.abandoned`, `cart.recovered`, `translation.job_completed`, `translation.job_failed`

Untuk menerima semua acara, langganan ke `*` (wildcard). Ini berguna untuk titik akhir log umum tetapi menciptakan lebih banyak lalu lintas — langganan hanya ke acara yang benar-benar Anda butuhkan untuk integrasi produksi.

### Langkah 3: Konfigurasi

- **Max Retries** — Berapa kali Spwig harus mencoba mengirim ulang pengiriman yang gagal sebelum menyerah (default: 5). Setiap percobaan ulang menggunakan jeda eksponensial.
- **Timeout (Detik)** — Berapa lama menunggu server penerima untuk merespons sebelum menandai pengiriman sebagai gagal (default: 30 detik). Tingkatkan hanya jika server Anda dikenal lambat.

### Langkah 4: Keamanan

Setiap titik akhir webhook mendapatkan **kunci tanda tangan** yang dihasilkan secara otomatis — kunci acak 64 karakter. Spwig menggunakan kunci ini untuk menandatangani setiap beban kerja webhook dengan tanda tangan HMAC-SHA256.

Tanda tangan termasuk dalam header permintaan `X-Webhook-Signature`. Server penerima Anda harus memverifikasi tanda tangan ini untuk memastikan permintaan benar-benar berasal dari toko Anda dan tidak dimanipulasi.

Kunci tersebut ditampilkan dalam bentuk tersembunyi di admin. Untuk melihat atau memutar ulang kunci, gunakan API Spwig. Putar ulang kunci Anda segera jika Anda mencurigai bahwa kunci tersebut telah bocor.

## Mematikan dan mengaktifkan kembali titik akhir

Untuk cepat mengaktifkan atau mematikan satu atau beberapa titik akhir tanpa membuka masing-masing:

1. Pilih kotak centang di sebelah titik akhir yang ingin Anda ubah
2. Gunakan dropdown **Action** untuk memilih **Enable selected endpoints** atau **Disable selected endpoints**
3. Klik **Go**

Untuk mengaktifkan kembali titik akhir yang secara otomatis dimatikan karena kegagalan, pilih titik akhir tersebut dan gunakan aksi **Reset failure count**, lalu aktifkan kembali. Perbaiki apa pun yang menyebabkan kegagalan terlebih dahulu, sebaliknya titik akhir akan segera dimatikan lagi.

## Tips

- Langganan hanya ke acara yang benar-benar Anda butuhkan — acara yang tidak diperlukan menciptakan kebisingan di log Anda dan meningkatkan beban pengiriman.
- Selalu verifikasi tanda tangan webhook di server penerima Anda sebelum memproses beban kerja. Ini melindungi Anda dari permintaan palsu.
- Gunakan bidang **Description** untuk mencatat sistem atau integrasi apa yang terhubung dengan titik akhir ini. Ini membantu saat meneliti masalah beberapa bulan kemudian.
- Tetapkan **Timeout** sedikit di atas waktu respons rata-rata server Anda. Timeout 10–15 detik sudah cukup untuk sebagian besar integrasi.
- Jika titik akhir menjadi **Unhealthy**, periksa log pengiriman terlebih dahulu (lihat **Webhook Deliveries**) untuk memahami pola kegagalan sebelum mengaktifkannya kembali.
- Untuk pengujian, arahkan webhook ke alat seperti [webhook.site](https://webhook.site) untuk memeriksa beban kerja mentah tanpa memerlukan server yang berjalan.