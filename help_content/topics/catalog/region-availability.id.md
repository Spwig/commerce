---
title: Ketersediaan Wilayah
---

Ketersediaan wilayah mengontrol wilayah penjualan mana dari wilayah penjualan Anda di mana produk dapat dijual, dan bagaimana penjual belanja di luar wilayah tersebut mengalami katalog Anda. Gunakan ini ketika produk dilisensikan hanya untuk negara tertentu, ketika persediaan cadangan untuk pasar lokal, atau ketika Anda menerbitkan produk baru secara bertahap per wilayah.

Ini membangun pada **Wilayah Penjualan**, yang mengelompokkan negara-negara menjadi pasar bernama (lihat panduan Wilayah Penjualan untuk menyiapkan yang tersebut). Setelah wilayah Anda ada, Anda dapat membatasi produk individu untuk mereka dan memutuskan bagaimana produk yang dibatasi muncul bagi pembeli yang tidak dapat membelinya.

## Membatasi produk ke wilayah tertentu

Setiap produk memiliki pengaturan **Ketersediaan Wilayah** di halaman editnya. Buka **Produk > Semua Produk**, pilih produk, dan temukan di bagian **Status** bersama **Status**, **Unggulan**, dan **Sembunyikan dari Toko**.

<!-- screenshots-needed:
- url: /en/admin/catalog/product/1/change/
  filename: product-region-availability-field.webp
  description: Halaman edit produk yang digulir ke bagian Status, dengan dropdown Ketersediaan Wilayah terlihat dan diatur ke "Hanya di wilayah yang dipilih"
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
  notes: Gunakan produk dengan setidaknya 2 wilayah yang sudah dipilih di bawah, jika memungkinkan, agar tabel inline memiliki baris yang terlihat dalam screenshot kedua.
-->

| Opsi | Apa artinya |
|--------|---------------|
| **Tersedia di semua wilayah** | Tidak ada pembatasan. Produk dijual di mana-mana. Ini adalah default untuk setiap produk. |
| **Hanya di wilayah yang dipilih** | Daftar izin. Produk hanya dijual di wilayah yang Anda pilih di bawah ini — di mana pun, itu dianggap tidak tersedia. |
| **Semua wilayah kecuali yang dipilih** | Daftar blokir. Produk dijual di mana pun *kecuali* wilayah yang Anda pilih di bawah ini. |

### Memilih wilayah-wilayahnya

Di bawah bagian Status, sebuah tabel dengan judul **Ketersediaan Wilayah (wilayah yang dipilih)** mendaftar wilayah-wilayah yang diterapkan mode di atas.

1. Atur **Ketersediaan Wilayah** ke **Hanya di wilayah yang dipilih** atau **Semua wilayah kecuali yang dipilih**.
2. Di tabel **Ketersediaan Wilayah (wilayah yang dipilih)**, klik **Tambahkan Wilayah lainnya** dan pilih **Wilayah Penjualan**.
3. Ulangi untuk setiap wilayah yang ingin ditambahkan.
4. Klik **Simpan**.

<!-- screenshots-needed:
- url: /en/admin/catalog/product/1/change/
  filename: product-region-availability-inline.webp
  description: Tabel inline "Ketersediaan Wilayah (wilayah yang dipilih)" dengan dua atau tiga baris wilayah yang ditambahkan
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
-->

Jika **Ketersediaan Wilayah** diatur ke **Tersedia di semua wilayah**, apa pun di tabel ini diabaikan — kosongkan dropdown mode terlebih dahulu jika Anda ingin menghapus pembatasan tanpa menghapus baris-barisnya.

Untuk melihat keseluruhan katalog setiap aturan wilayah produk dalam satu daftar (membantu saat meninjau banyak produk sekaligus), buka **Ketersediaan Wilayah Produk** di `/admin/catalog/productregionvisibility/`.

## Menampilkan kepada pembeli di mana produk tidak dikirimkan

Ketika wilayah pembeli tidak sesuai dengan aturan ketersediaan produk, Anda mengontrol apa yang mereka lihat di **Pengaturan Tampilan Persediaan**, di bagian **Ketersediaan Wilayah**. Halaman ini belum memiliki pintasan sisi kanan — buka langsung di `/admin/catalog/stockdisplaysettings/`.

<!-- screenshots-needed:
- url: /en/admin/catalog/stockdisplaysettings/1/change/
  filename: stock-display-region-availability.webp
  description: Form perubahan Pengaturan Tampilan Persediaan yang digulir ke bidang "Ketersediaan Wilayah", menunjukkan dropdown tampilan yang dibatasi wilayah
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
-->

Simpan semua format markdown, jalur gambar, blok kode, dan istilah teknis.

{
  "table": "| Opsi | Yang dilihat pembeli |
|--------|-------------------|
| **Tampilkan, dicatat sebagai tidak tersedia** (default) | Produk tetap muncul di daftar, dengan badge "Tidak Tersedia" dan catatan "Tidak dikirim ke [wilayah]" menggantikan tombol Tambah ke Keranjang. Sebuah banner juga muncul di bagian atas halaman daftar ("Beberapa produk tidak dikirim ke [tujuan]") dengan tautan untuk menyaring hanya barang-barang yang dikirim ke sana. |
| **Sembunyikan dari daftar** | Produk dihapus dari daftar dan hasil pencarian sepenuhnya untuk pembeli di wilayah tersebut. |",
  "screenshots-needed": "
- url: /en/products/
  filename: storefront-region-restricted-listing.webp
  description: Daftar produk toko dengan banner wilayah di bagian atas dan setidaknya satu kartu produk yang menunjukkan badge "Tidak Tersedia" dan catatan "Tidak dikirim ke [wilayah]"
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
  notes: Membutuhkan pemilihan alamat pengiriman yang hidup (atau deteksi GeoIP) yang menyelesaikan ke wilayah di mana produk demo dibatasi.
",
  "paragraph": "Sebuah produk yang dibatasi selalu menampilkan catatan \"Produk ini tidak dikirim ke [wilayah]\" ketika pembeli mengaksesnya secara langsung (misalnya, dari tautan yang dibagikan atau hasil pencarian mesin pencari) — ini berlaku terlepas dari opsi daftar mana pun yang Anda pilih di atas, karena tautan langsung melewati daftar sepenuhnya.",
  "heading": "## Memungkinkan pembeli memilih atau menemukan wilayah mereka",
  "paragraph2": "Spwig dapat mendeteksi wilayah pembeli secara otomatis dan menawarkan perubahan, dan Anda dapat menambahkan pemilih sehingga pembeli dapat mengubahnya kapan saja.",
  "subheading": "### Sebelum memulai",
  "paragraph3": "Anda membutuhkan dua hal yang dikonfigurasi agar deteksi dan perubahan wilayah bekerja dengan benar:",
  "list": "1. **Wilayah Penjualan** — negara-negara di setiap wilayah dan mata uang default setiap wilayah. Jika Anda tidak melihat **Wilayah Penjualan** di bawah **Inventaris** di bilah sisi, aktifkan **Izinkan Gudang Ganda** di bawah **Pengaturan > Pengaturan Toko > E-Commerce** untuk menampilkan tautan menu (Anda tidak perlu menggunakan gudang ganda — pengaturan ini hanya membuka item menu). Anda juga dapat langsung pergi ke `/admin/catalog/salesregion/`.
2. **Negara Pengiriman** — negara-negara yang sebenarnya dikirim oleh toko Anda. Biasanya sudah tersedia: setiap negara yang Anda tambahkan ke Zona Pengiriman secara otomatis ditambahkan di sini juga. Untuk meninjau atau menyesuaikan daftar secara manual, buka `/admin/shipping/shippingcountry/` secara langsung (ini juga tidak memiliki tautan bilah sisi saat ini).",
  "subheading2": "### Konfirmasi wilayah otomatis",
  "paragraph4": "Spwig mendeteksi wilayah pembeli dari lokasinya dan menerapkannya secara otomatis. Ketika hal itu membuat mereka masuk ke wilayah yang *bukan* pasar utama toko Anda (utama) — dan Anda memiliki dua atau lebih Wilayah Penjualan aktif — Spwig menampilkan konfirmasi pada kunjungan pertama mereka sehingga mereka tahu wilayah mana yang mereka kunjungi dan dapat mengubahnya:"
}


Navigasi ke **Desain > Pembuat Header** (atau **Pembuat Kaki**) .
2.

Seret **Widget Pemilih Alamat Pengiriman** dari Perpustakaan Widget ke dalam sebuah baris.
3.

Klik **Simpan**.

<!-- screenshots-needed:
- url: /en/theme/header/builder/
  filename: ship-to-selector-widget-library.webp
  description: Pembuat Header dengan sidebar Perpustakaan Widget terbuka dan widget Pemilih Alamat Pengiriman terlihat/ditonjolkan
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
-->

Widget ini tidak memerlukan pengaturan — secara otomatis mendaftar Negara Pengiriman aktif Anda, dan menunjukkan pilihan pengguna saat ini (atau negara yang dideteksi oleh GeoIP, jika mereka belum memilih satu pun). Memilih negara lain akan segera memperbarui wilayah mereka dan memuat ulang ketersediaan produk dan harga halaman tersebut.

Pemilih Alamat Pengiriman tidak memiliki formulir pengaturan khusus saat ini. Jika Anda ingin mengubah gaya tombolnya (garis, padat, atau transparan) atau menyembunyikan label "Kirim ke", buka pengaturan widget di pembuat dan sunting langsung bidang **Konfigurasi Kustom (JSON)**, dengan menggunakan `button_style` dan `show_label`.

### Mata Uang mengikuti wilayah

Jika toko Anda mendukung lebih dari satu mata uang (diatur di bawah **Pengaturan > Multi-Mata Uang**), beralih ke wilayah — baik melalui prompt atau Pemilih Alamat Pengiriman — juga mengubah mata uang yang ditampilkan menjadi mata uang default wilayah tersebut. Jika toko Anda hanya memiliki satu mata uang, atau belum secara eksplisit mengaktifkan yang kedua, mata uang tetap tidak berubah saat pengguna beralih wilayah.

## Tips

- Biarkan **Ketersediaan Wilayah** pada **Tersedia di semua wilayah** kecuali Anda memiliki alasan khusus untuk membatasi produk — opsi ini paling sederhana dan tidak memerlukan pemeliharaan saat Anda menambahkan wilayah di masa depan.
- Gunakan **Hanya di wilayah yang dipilih** untuk daftar izin kecil (misalnya, produk yang diluncurkan di satu negara terlebih dahulu) dan **Semua wilayah kecuali yang dipilih** untuk daftar blokir kecil (misalnya, seluruhnya kecuali negara di mana barang tidak memiliki lisensinya) — pilih mana pun yang membutuhkan baris yang lebih sedikit untuk disiapkan.
- Jika pengguna melaporkan produk yang hilang yang seharusnya terlihat, periksa pengaturan **Ketersediaan Wilayah** produk tersebut dan apakah negara mereka ditangani oleh **Wilayah Penjualan** aktif dan **Negara Pengiriman** aktif.
- **Sembunyikan dari daftar** menjaga tampilan katalog Anda tetap bersih bagi pengguna yang tidak dapat membeli item tertentu, tetapi juga berarti merchandising dan pencarian akan terlihat lebih tipis di wilayah tersebut — **Tampilkan, dengan status tidak tersedia** biasanya lebih baik jika Anda tetap ingin pengguna menjelajahi katalog lengkap Anda bahkan di wilayah di mana mereka tidak dapat melakukan pembelian.
- Uji perilaku wilayah dengan menambahkan Pemilih Alamat Pengiriman ke bagian header dan beralih antara negara-negara sendiri sebelum mengandalkan deteksi GeoIP selama peluncuran.
- Tetapkan nilai prioritas wilayah Anda secara sengaja — wilayah aktif dengan prioritas tertinggi adalah cadangan untuk pengguna yang negaranya tidak terdeteksi atau tidak cocok dengan wilayah apa pun.