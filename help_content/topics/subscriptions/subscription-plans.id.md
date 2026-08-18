---
title: Rencana Langganan
---

Rencana langganan memungkinkan Anda menawarkan pembayaran berulang untuk produk Anda — idealnya untuk barang habiskan, layanan, kotak yang dikuratori, atau produk apa pun yang pelanggan beli berulang kali. Panduan ini menjelaskan cara membuat dan mengkonfigurasi rencana, menyiapkan tingkatan harga, menambahkan periode percobaan, dan menghubungkan tambahan opsional.

## Mulai

Navigasi ke **Langganan > Rencana Langganan** di bilah sisi admin. Daftar rencana menunjukkan semua rencana Anda dengan model harga, jumlah pelanggan aktif, dan status visibilitasnya.

![Daftar rencana langganan](/static/core/admin/img/help/subscription-plans/plan-list.webp)

Untuk membuat rencana baru, klik tombol **Buat dengan Wizard** — ini membuka wizard pembuatan rencana, yang memandu Anda melalui langkah-langkah penyiapan secara bertahap. Tombol **+ Tambahkan Rencana** di sebelahnya membuka formulir kosong untuk pedagang yang lebih suka mengkonfigurasi semuanya secara manual alih-alih menggunakan wizard.

Sebuah rencana punya kemampuan untuk dibeli — ini adalah template. Setelah Anda membangunnya di sini, sertakan dalam satu atau lebih produk dari tab **Langganan** produk (hanya produk Sederhana, Variabel, dan Digital) agar pelanggan bisa berlangganan. Lihat [Penjualan Produk sebagai Langganan](/help/selling-products-as-subscriptions) untuk langkah tersebut.

## Editor rencana

Membuka rencana yang ada (klik namanya, atau ikon pensil, dari daftar) membawa Anda ke editor rencana. Header menunjukkan nama rencana, model harga, badge status **Aktif**/**Tidak Aktif** dan **Publik**/**Privat**, serta tanggal dibuatnya. Dua tombol di sudut kanan atas header menyimpan perubahan Anda — ikon lingkaran biru menyimpan dan kembali ke daftar, ikon cek biasa menyimpan dan membiarkan Anda tetap di halaman sehingga Anda bisa terus mengedit.

Di bawah header, strip statistik menyajikan rencana secara keseluruhan: **Langganan Aktif**, **Tingkatan Harga**, **Tambahan**, dan **Pendapatan Keseluruhan**.

Bagian lain dari formulir diatur dalam lima tab:

| Tab | Apa yang dikandung |
|-----|-------------------|
| **Umum** | Informasi Rencana (nama, slug, deskripsi) dan Status (aktif/publik) |
| **Harga** | Konfigurasi Harga, Masa Percobaan, dan Batasan & Pembatasan |
| **Tingkatan & Tambahan** | Editor Tingkatan Harga dan Tambahan |
| **Siklus Hidup** | Kebijakan Pembatalan dan Perilaku Perubahan Rencana |
| **Canggih** | Integrasi Penyedia dan Statistik |

Bagian-bagian berikut ini menjelaskan pengaturan setiap tab. Ketika Anda membuat rencana baru langsung dari **+ Tambahkan Rencana** (bukan wizard), bidang yang sama muncul dalam formulir yang dapat digulirkan saja alih-alih tab — simpan rencana sekali dan buka kembali untuk mendapatkan editor ber-tab penuh.

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
| **Harga Berjenjang** | Menawarkan opsi komitmen bulanan, kuartal, dan tahunan dengan diskon untuk jangka yang lebih lama |
| **Berdasarkan Jumlah** | Harga per kursi atau pengguna di mana totalnya meningkat sesuai jumlah (misalnya, lisensi tim) |
| **Tarif Tetap** | Harga tetap tunggal tanpa variasi |

Untuk rencana **Berdasarkan Jumlah**, centang **Izinkan Jumlah** dan atur **Jumlah Minimum** (jumlah kursi terendah yang diperlukan) dan secara opsional **Jumlah Maksimum** untuk membatasi jumlah kursi yang dapat dibeli oleh pelanggan.

Simpan semua format markdown, jalur gambar, blok kode, dan istilah teknis.

[![Pricing tab of the plan editor](/static/core/admin/img/help/subscription-plans/edit-form-pricing-tab.webp)](/static/core/admin/img/help/subscription-plans/edit-form-pricing-tab.webp)

## Tingkatan Harga (tab Tingkatan & Tambahan)

Tingkatan harga menentukan frekuensi pembayaran dan opsi diskon yang tersedia bagi pelanggan pada rencana ini. Tambahkan di kartu **Tingkatan Harga** pada tab **Tingkatan & Tambahan**, bersama dengan editor tambahan.

Setiap tingkatan memiliki bidang-bidang berikut:

- **Nama Tingkatan** — Label yang ditampilkan kepada pelanggan (misalnya, `Bulanan`, `Tahunan — Hemat 20%`). Mendukung terjemahan.
- **Siklus Pembayaran** — Seberapa sering pelanggan dibebankan: Harian, Mingguan, Bulanan, Kuartalan, Semi-Annual, atau Tahunan.
- **Interval Pembayaran** — Pengali untuk siklus pembayaran. Atur ke `2` dengan Bulanan untuk membebankan setiap 2 bulan.
- **Persentase Diskon** — Diskon yang diterapkan pada harga produk untuk tingkatan ini. Atur ke `0` untuk harga penuh, atau `20` untuk memberi diskon 20%. Diskon ini berlaku tambahan di atas harga penjualan apa pun pada produk itu sendiri.
- **Tingkatan Default** — Tandai satu tingkatan sebagai default untuk memilihnya secara otomatis bagi pelanggan ketika mereka melihat opsi langganan.

Diskon berlaku sejak siklus pembayaran pertama pelanggan, bukan hanya pada pembaruan — tingkatan dengan diskon 20% membebankan 20% lebih sedikit sejak hari pertama (atau dari pembayaran pertama setelah percobaan, jika rencana memiliki satu).

### Contoh: rencana berlapis dengan tiga opsi

Untuk rencana langganan "Kopi Club":

| Nama Tingkatan | Siklus Pembayaran | Diskon |
|-----------|---------------|----------|
| Bulanan | Bulanan | 0% |
| Kuartalan — Hemat 10% | Kuartalan | 10% |
| Tahunan — Hemat 20% | Tahunan | 20% |

## Tambahan rencana (tab Tingkatan & Tambahan)

Tambahan adalah ekstra opsional yang dapat ditambahkan pelanggan ke rencana mereka. Tambahkan di kartu **Tambahan**, langsung di bawah Tingkatan Harga pada tab yang sama:

- **Nama Tambahan** — Nama yang ditampilkan kepada pelanggan. Mendukung terjemahan.
- **Deskripsi** — Apa yang ditawarkan tambahan tersebut.
- **Harga** — Biaya tambahan tersebut.
- **Frekuensi Pembayaran** — Apakah tambahan tersebut dibebankan **Per Siklus Pembayaran** (berulang) atau **Satu Kali** saat memulai langganan.
- **Izinkan Jumlah** — Aktifkan untuk memungkinkan pelanggan membeli beberapa unit tambahan.
- **Wajib** — Centang ini untuk secara otomatis menyertakan tambahan tersebut pada semua langganan baru. Tambahan wajib tidak dapat dihapus oleh pelanggan.

[![Tab Tingkatan & Tambahan dari editor rencana](/static/core/admin/img/help/subscription-plans/edit-form-tiers-addons-tab.webp)](/static/core/admin/img/help/subscription-plans/edit-form-tiers-addons-tab.webp)

## Masa percobaan (tab Harga)

Masa percobaan memungkinkan pelanggan mencoba langganan Anda sebelum pembayaran penuh pertama mereka. Atur ini di kartu **Masa Percobaan**, di bawah Konfigurasi Harga:

- **Masa Percobaan (Hari)** — Jumlah hari percobaan gratis. Atur ke `0` untuk menonaktifkan masa percobaan. Maksimal adalah 365 hari.
- **Harga Percobaan** — Harga diskon opsional selama masa percobaan (misalnya, $1 untuk bulan pertama). Biarkan kosong untuk percobaan sepenuhnya gratis.

## Batasan dan pembatasan (tab Harga)

Kartu **Batasan & Pembatasan**, juga pada tab Harga, berisi:

- **Jumlah Siklus Pembayaran Maksimum** — Jumlah total siklus pembayaran sebelum langganan berakhir secara otomatis. Biarkan kosong untuk pembayaran berulang tak terbatas. Berguna untuk rencana cicilan atau langganan berbatas waktu.

**Biaya Pemasangan** dan **Urutan Pemesanan** bukan bagian dari kartu ini — mereka diatur sekali, ketika Anda membuat rencana pertama melalui alur **Buat dengan Wizard**, dan tidak dapat diubah dari layar sunting setelahnya. Jika Anda perlu menyesuaikan salah satu nilai tersebut, nonaktifkan rencana tersebut dan buat ulang dengan wizard daripada mengedit yang ada. Catatan bahwa biaya pemasangan belum dikenakan secara otomatis saat checkout dalam rilis ini — anggaplah kolom ini sebagai cadangan untuk pembaruan masa depan daripada biaya yang berfungsi.

## Kebbijakan Pembatalan (tab Siklus Hidup)

Atur bagaimana pelanggan dapat membatalkan langganan mereka di kartu **Kebbijakan Pembatalan**:

| Kebijakan | Deskripsi |
|--------|-------------|
| **Batalkan Kapan Saja** | Pelanggan dapat membatalkan kapan saja |
| **Batalkan di Akhir Masa** | Pembatalan berlaku di akhir periode pembayaran — pelanggan tetap memiliki akses hingga masa berlaku berakhir |
| **Kewajiban Minimal Dibutuhkan** | Pelanggan harus menyelesaikan jumlah siklus pembayaran minimal sebelum membatalkan |

Pengaturan tambahan:

- **Kewajiban Minimal (Siklus)** — Saat menggunakan kebijakan kewajiban, tetapkan jumlah siklus pembayaran yang diperlukan (misalnya, `3` untuk kewajiban minimal 3 bulan).
- **Masa Percaya (Hari)** — Hari akses berkelanjutan setelah kegagalan pembayaran sebelum langganan dihentikan. Atur menjadi `0` untuk penghentian segera.
- **Masa Aktif Kembali (Hari)** — Hari setelah pembatalan di mana pelanggan dapat mengaktifkan kembali langganan mereka tanpa harus berlangganan dari awal.

## Perilaku perubahan rencana (tab Lifecycle)

Kartu **Perilaku Perubahan Rencana**, di bawah Kebijakan Pembatalan, mengontrol apa yang terjadi ketika pelanggan meningkatkan atau menurunkan rencana:

- **Perilaku Peningkatan** — Atur menjadi **Segera** (kenakan biaya jumlah yang sesuai saat ini) atau **Pada Saat Pembaruan Kembali** (berpindah pada tanggal pembayaran berikutnya).
- **Perilaku Penurunan** — Atur menjadi **Segera** (terapkan kredit ke tagihan berikutnya) atau **Pada Saat Pembaruan Kembali** (berpindah pada tanggal pembayaran berikutnya).

![Tab Lifecycle dari pengedit rencana](/static/core/admin/img/help/subscription-plans/edit-form-lifecycle-tab.webp)

## Tab Lanjutan

Tab **Lanjutan** berisi pengaturan yang jarang Anda butuhkan sehari-hari:

- **Integrasi Penyedia** — Peta rencana ini ke ID rencana/harga dari penyedia pembayaran Anda (misalnya, `{"stripe": "price_xxx", "paypal": "P-xxx"}`), untuk toko yang mengelola langganan secara mandiri melalui penyedia daripada mesin pembayaran Spwig sendiri.
- **Statistik** — Angka yang dapat dibaca saja: **Langganan Aktif**, **Pendapatan Total**, dan timestamp **Dibuat Pada** / **Diperbarui Pada** rencana ini. Ini mencerminkan statistik strip di bagian atas halaman.

![Tab Lanjutan dari pengedit rencana](/static/core/admin/img/help/subscription-plans/edit-form-advanced-tab.webp)

## Visibilitas dan status (tab Umum)

- **Aktif** — Nonaktifkan untuk menonaktifkan rencana sehingga tidak ada langganan baru yang dapat dibuat. Langganan yang sudah ada tidak terpengaruh.
- **Publik** — Nonaktifkan untuk menyembunyikan rencana dari halaman yang terlihat oleh pelanggan (berguna untuk rencana internal atau lama yang pengguna yang sudah ada tetap berada di dalamnya).

## Tips

- Gunakan **masa percobaan** untuk mengurangi keraguan — bahkan masa percobaan 7 hari singkat pun dapat secara signifikan meningkatkan tingkat konversi pada produk langganan.
- Atur **tiga tingkatan harga** (bulanan, kuartalan, tahunan) dengan diskon yang meningkat untuk mendorong komitmen tahunan dan meningkatkan aliran kas Anda.
- Untuk langganan berbasis layanan, atur **Kebijakan Pembatalan** menjadi **Batalkan di Akhir Masa** sehingga pelanggan tetap memiliki akses melalui periode pembayaran mereka — ini terasa adil dan mengurangi tuntutan pembayaran kembali.
- Pertahankan **Masa Percaya** pada 3–7 hari untuk kegagalan pembayaran. Hal ini memberi pelanggan waktu untuk memperbarui metode pembayaran mereka sebelum kehilangan akses.
- Gunakan bendera **Wajib** pada tambahan secara terbatas — hanya gunakan untuk hal-hal yang benar-benar wajib (misalnya, perjanjian layanan), bukan sebagai cara untuk menaikkan harga.
- Nonaktifkan rencana yang tidak memiliki pelanggan daripada menghapusnya — ini mempertahankan data historis untuk pelanggan mana pun yang pernah berlangganan.