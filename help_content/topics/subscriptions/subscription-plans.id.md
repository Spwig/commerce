---
title: Rencana Langganan
---

Rencana langganan memungkinkan Anda menawarkan pembayaran berulang untuk produk Anda — idealnya untuk barang habiskan, layanan, kotak yang dikuratori, atau produk apa pun yang pelanggan beli berulang kali. Panduan ini menjelaskan cara membuat dan mengkonfigurasi rencana, menyiapkan tingkatan harga, menambahkan periode percobaan, dan menghubungkan tambahan opsional.

## Mulai

Navigasi ke **Langganan > Rencana Langganan** di bilah sisi admin. Daftar rencana menunjukkan semua rencana Anda dengan model harga, jumlah pelanggan aktif, dan status visibilitasnya.

![Daftar rencana langganan](/static/core/admin/img/help/subscription-plans/plan-list.webp)

Untuk membuat rencana baru, klik tombol **Buat dengan Wizard** — ini membuka wizard pembuatan rencana, yang memandu Anda melalui langkah-langkah penyiapan secara bertahap. Tombol **+ Tambahkan Rencana** di sebelahnya membuka formulir kosong untuk pedagang yang lebih suka mengkonfigurasi semuanya secara manual alih-alih menggunakan wizard.

Sebuah rencana punya kemampuan untuk dibeli — ini adalah template. Setelah Anda membuatnya di sini, sertakan dalam satu atau lebih produk dari tab **Langganan** produk (hanya produk Sederhana, Variabel, dan Digital) agar pelanggan dapat berlangganan. Lihat [Penjualan Produk sebagai Langganan](/help/selling-products-as-subscriptions) untuk langkah tersebut.

## Editor rencana

Membuka rencana yang ada (klik namanya, atau ikon pensil, dari daftar) membawa Anda ke editor rencana. Header menunjukkan nama rencana, model harga, badge status **Aktif**/**Tidak Aktif** dan **Publik**/**Privat**, serta tanggal dibuatnya. Dua tombol di sudut kanan atas header menyimpan perubahan Anda — ikon lingkaran biru menyimpan dan kembali ke daftar, ikon cek biasa menyimpan dan membiarkan Anda tetap di halaman sehingga dapat terus mengedit.

Di bawah header, strip statistik menyajikan rencana secara keseluruhan: **Langganan Aktif**, **Tingkatan Harga**, **Tambahan**, dan **Pendapatan Keseluruhan**.

Bagian lain dari formulir diatur dalam lima tab:

| Tab | Apa yang dikandung |
|-----|-------------------|
| **Umum** | Informasi Rencana (nama, slug, deskripsi) dan Status (aktif/publik) |
| **Harga** | Konfigurasi Harga, Masa Percobaan, dan Batasan & Pembatasan |
| **Tingkatan & Tambahan** | Editor Tingkatan Harga dan Tambahan |
| **Siklus Hidup** | Kebijakan Pembatalan dan Perilaku Perubahan Rencana |
| **Canggih** | Integrasi Penyedia dan Statistik |

Bagian-bagian berikut ini menjelaskan pengaturan setiap tab. Ketika Anda membuat rencana baru langsung dari **+ Tambahkan Rencana** (bukan wizard), bidang yang sama muncul dalam formulir yang dapat digulirkan tunggal alih-alih tab — simpan rencana sekali dan buka kembali untuk mendapatkan editor ber-tab penuh.

## Informasi Rencana (tab Umum)

Kartu **Informasi Rencana** menangkap identitas inti dari rencana Anda.

- **Nama Rencana** — Nama yang dilihat pelanggan saat berlangganan. Klik ikon dunia untuk menambah terjemahan untuk bahasa toko lainnya.
- **Slug** — Identifikasi yang ramah URL yang dihasilkan secara otomatis dari nama (misalnya, `premium-plan`). Ini digunakan secara internal dan dalam integrasi.
- **Deskripsi** — Teks opsional yang menjelaskan apa saja yang termasuk dalam rencana ini. Mendukung terjemahan.

Kartu **Status** di tab yang sama mengontrol saklar **Aktif** dan **Publik** — lihat [Visibilitas dan status](#visibility-and-status) di bawah ini.

![Tab Umum dari editor rencana](/static/core/admin/img/help/subscription-plans/edit-form-general-tab.webp)

## Model Harga (tab Harga)

Kartu **Konfigurasi Harga** mengontrol bagaimana struktur harga untuk rencana ini:

| Model Harga | Paling Cocok untuk |
|---------------|----------|
| **Harga Berjenjang** | Menawarkan opsi komitmen bulanan, kuartal, dan tahunan dengan diskon untuk jangka yang lebih panjang |
| **Berdasarkan Jumlah** | Harga per kursi atau pengguna di mana totalnya meningkat sesuai jumlah (misalnya, lisensi tim) |
| **Tarif Tetap** | Harga tetap tunggal tanpa variasi |

Untuk rencana **Berdasarkan Jumlah**, centang **Izinkan Jumlah** dan atur **Jumlah Minimum** (jumlah kursi terendah yang diperlukan) dan secara opsional **Jumlah Maksimum** untuk membatasi jumlah kursi yang dapat dibeli oleh pelanggan.

Simpan semua format markdown, jalur gambar, blok kode, dan istilah teknis.

![Tab Harga dari editor rencana](/static/core/admin/img/help/subscription-plans/edit-form-pricing-tab.webp)

## Tingkat harga (Tab Tiers & Add-ons)

Tingkat harga mendefinisikan frekuensi penagihan dan opsi diskon yang tersedia bagi pelanggan pada rencana ini. Tambahkan di kartu **Pricing Tiers** pada tab **Tiers & Add-ons**, berdampingan dengan editor Add-ons.

Setiap tingkat memiliki bidang berikut:

- **Tier Name** — Label yang ditampilkan kepada pelanggan (misalnya, `Monthly`, `Annual — Save 20%`). Mendukung terjemahan.
- **Billing Cycle** — Seberapa sering pelanggan ditagih: Harian, Mingguan, Bulanan, Kuartalan, Semi-Tahunan, atau Tahunan.
- **Billing Interval** — Pengali untuk siklus penagihan. Atur ke `2` dengan Bulanan untuk menagih setiap 2 bulan.
- **Discount Percentage** — Diskon yang diterapkan pada harga produk untuk tingkat ini. Atur ke `0` untuk harga penuh, atau `20` untuk memberikan diskon 20%. Diskon ini ditumpuk di atas harga promo pada produk itu sendiri.
- **Default Tier** — Tandai satu tingkat sebagai default untuk memilihnya secara otomatis bagi pelanggan ketika mereka melihat opsi langganan.

Diskon berlaku mulai dari siklus penagihan pertama pelanggan, bukan hanya pada perpanjangan — tingkat dengan diskon 20% menagih 20% lebih murah sejak hari pertama (atau dari penagihan pertama setelah masa uji coba, jika rencana memiliki masa uji coba).

### Contoh: rencana bertingkat dengan tiga opsi

Untuk rencana langganan "Coffee Club":

| Tier Name | Billing Cycle | Discount |
|-----------|---------------|----------|
| Monthly | Monthly | 0% |
| Quarterly — Save 10% | Quarterly | 10% |
| Annual — Save 20% | Annual | 20% |

## Add-on rencana (Tab Tiers & Add-ons)

Add-ons adalah tambahan opsional yang dapat dilampirkan pelanggan pada rencana mereka. Tambahkan di kartu **Add-ons**, tepat di bawah Pricing Tiers pada tab yang sama:

- **Add-on Name** — Nama yang ditampilkan kepada pelanggan. Mendukung terjemahan.
- **Description** — Apa yang disediakan oleh add-on.
- **Price** — Biaya add-on.
- **Billing Frequency** — Apakah add-on ditagih **Per Billing Cycle** (berulang) atau **One-Time** saat mulai langganan.
- **Allow Quantity** — Aktifkan untuk memungkinkan pelanggan membeli beberapa unit add-on.
- **Required** — Centang ini untuk secara otomatis menyertakan add-on pada semua langganan baru. Add-on yang diwajibkan tidak dapat dihapus oleh pelanggan.

![Tab Tiers & Add-ons dari editor rencana](/static/core/admin/img/help/subscription-plans/edit-form-tiers-addons-tab.webp)

## Masa uji coba (Tab Harga)

Masa uji coba memungkinkan pelanggan mencoba langganan Anda sebelum penagihan penuh pertama. Konfigurasikan ini di kartu **Trial Period**, di bawah Pricing Configuration:

- **Trial Period (Days)** — Jumlah hari uji coba gratis. Atur ke `0` untuk menonaktifkan uji coba. Maksimal 365 hari.
- **Trial Price** — Harga reduksi opsional selama masa uji coba (misalnya, $1 untuk bulan pertama). Kosongkan untuk uji coba yang sepenuhnya gratis.

## Batasan dan pembatasan (Tab Harga)

Kartu **Limits & Restrictions**, juga pada tab Harga, berisi:

- **Maximum Billing Cycles** — Total jumlah siklus penagihan sebelum langganan berakhir secara otomatis. Kosongkan untuk penagihan berulang tanpa batas. Berguna untuk rencana cicilan atau langganan berbatas waktu.

**Setup Fee** dan **Sort Order** bukan bagian dari kartu ini — mereka diatur sekali, ketika Anda pertama kali membuat rencana melalui alur **Create with Wizard**, dan tidak dapat diubah dari layar edit setelahnya. Jika Anda perlu menyesuaikan salah satu nilai, nonaktifkan rencana dan buat ulang dengan wizard alih-alih mengedit yang ada. Perhatikan bahwa biaya setup belum ditagih secara otomatis saat checkout dalam rilis ini — perlakukan bidang ini sebagai cadangan untuk pembaruan masa depan, bukan sebagai tagihan yang berfungsi.

## Kebijakan pembatalan (Tab Lifecycle)

Kendalikan bagaimana pelanggan dapat membatalkan langganan mereka di kartu **Cancellation Policy**:


| Kebijakan | Deskripsi |
|--------|-------------|
| **Batalkan Kapan Saja** | Pelanggan dapat membatalkan segera kapan saja |
| **Batalkan di Akhir Periode** | Pembatalan berlaku di akhir periode yang dibayar — pelanggan tetap memiliki akses hingga kedaluwarsa |
| **Komitmen Minimum Diperlukan** | Pelanggan harus menyelesaikan jumlah minimum siklus penagihan sebelum membatalkan |

Pengaturan tambahan:

- **Komitmen Minimum (Siklus)** — Saat menggunakan kebijakan komitmen, atur jumlah siklus penagihan yang diperlukan (misalnya, `3` untuk minimum 3 bulan).
- **Periode Toleransi (Hari)** — Hari akses lanjutan setelah kegagalan pembayaran sebelum langganan ditangguhkan. Atur ke `0` untuk penangguhan segera.
- **Periode Reaktivasi (Hari)** — Hari setelah pembatalan di mana pelanggan dapat mengaktifkan kembali langganan mereka tanpa berlangganan ulang dari awal.

## Perilaku perubahan paket (Tab Siklus Hidup)

Kartu **Perilaku Perubahan Paket**, di bawah Kebijakan Pembatalan, mengontrol apa yang terjadi ketika pelanggan meningkatkan atau menurunkan paket:

- **Perilaku Peningkatan** — Atur ke **Segera** (tagih jumlah prorata sekarang) atau **Saat Pembaruan** (beralih di tanggal penagihan berikutnya).
- **Perilaku Penurunan** — Atur ke **Segera** (terapkan kredit ke tagihan berikutnya) atau **Saat Pembaruan** (beralih di tanggal penagihan berikutnya).

![Tab siklus hidup dari editor paket](/static/core/admin/img/help/subscription-plans/edit-form-lifecycle-tab.webp)

## Tab Lanjutan

Tab **Lanjutan** berisi pengaturan yang jarang Anda butuhkan sehari-hari:

- **Integrasi Penyedia** — Petakan paket ini ke ID paket/harga dari penyedia pembayaran Anda (misalnya, `{"stripe": "price_xxx", "paypal": "P-xxx"}`), untuk toko yang mengelola langganan secara native melalui penyedia alih-alih mesin penagihan Spwig sendiri.
- **Statistik** — Angka hanya-baca: **Langganan Aktif**, **Total Pendapatan**, dan timestamp **Dibuat Pada** / **Diperbarui Pada** paket. Ini mencerminkan strip statistik di bagian atas halaman.

![Tab lanjutan dari editor paket](/static/core/admin/img/help/subscription-plans/edit-form-advanced-tab.webp)

## Visibilitas dan status (Tab Umum)

- **Aktif** — Hapus centang untuk menonaktifkan paket sehingga tidak ada langganan baru yang dapat dibuat. Langganan yang ada tidak terpengaruh.
- **Publik** — Hapus centang untuk menyembunyikan paket dari halaman yang menghadap pelanggan (berguna untuk paket internal atau lama yang masih digunakan oleh pelanggan langganan yang ada).

## Tips

- Gunakan **periode percobaan** untuk mengurangi keraguan — bahkan percobaan gratis 7 hari yang singkat dapat secara signifikan meningkatkan tingkat konversi pada produk langganan.
- Atur **tiga tingkatan harga** (bulanan, kuartalan, tahunan) dengan diskon yang meningkat untuk mendorong komitmen tahunan dan meningkatkan arus kas Anda.
- Untuk langganan berbasis layanan, atur **Kebijakan Pembatalan** ke **Batalkan di Akhir Periode** agar pelanggan tetap memiliki akses selama periode yang dibayar — ini terasa adil dan mengurangi chargeback.
- Pertahankan **Periode Toleransi** pada 3–7 hari untuk kegagalan pembayaran. Ini memberi pelanggan waktu untuk memperbarui metode pembayaran mereka sebelum kehilangan akses.
- Gunakan bendera **Wajib** pada add-on secara hemat — hanya gunakan untuk hal-hal yang benar-benar wajib (misalnya, perjanjian layanan), bukan sebagai cara untuk menggelembungkan harga.
- Nonaktifkan paket tanpa pelanggan alih-alih menghapusnya — ini melestarikan data historis untuk pelanggan yang sebelumnya berlangganan.
