---
title: Ketersediaan Wilayah
---

Ketersediaan wilayah mengontrol wilayah penjualan mana dari wilayah penjualan Anda di mana produk dapat dijual, dan bagaimana penjual di luar wilayah tersebut mengalami katalog Anda. Gunakan ini ketika produk dilisensikan hanya untuk negara tertentu, ketika persediaan cadangan untuk pasar lokal, atau ketika Anda meluncurkan produk baru secara bertahap per wilayah.

Ini membangun pada **Wilayah Penjualan**, yang mengelompokkan negara-negara menjadi pasar bernama (lihat panduan Wilayah Penjualan untuk menyetelnya). Sekali wilayah Anda ada, Anda dapat membatasi produk individu untuk mereka dan menentukan bagaimana produk yang dibatasi tampak kepada pembeli yang tidak dapat membelinya.

## Membatasi produk ke wilayah tertentu

Setiap produk memiliki pengaturan **Ketersediaan Wilayah** di halaman editnya. Buka **Produk > Semua Produk**, pilih produk, dan temukan di bagian **Status** bersama **Status**, **Unik**, dan **Sembunyikan dari Toko**.

![Bagian Status formulir edit produk, dengan dropdown Ketersediaan Wilayah diatur menjadi "Hanya di wilayah yang dipilih" bersama dengan Fitur dan Sembunyikan dari Toko](/static/core/admin/img/help/region-availability/product-region-availability-field.webp)

| Pilihan | Artinya | 
|--------|---------------| 
| **Tersedia di semua wilayah** | Tidak ada pembatasan. Produk dijual di mana-mana. Ini adalah default untuk setiap produk. | 
| **Hanya di wilayah yang dipilih** | Daftar izin. Produk hanya dijual di wilayah yang Anda pilih di bawah ini — di mana pun, itu dianggap tidak tersedia. | 
| **Semua wilayah kecuali yang dipilih** | Daftar blokir. Produk dijual di mana pun *kecuali* wilayah yang Anda pilih di bawah ini. | 

### Memilih wilayah-wilayahnya

Di bawah bagian Status, sebuah tabel berjudul **Ketersediaan Wilayah (wilayah yang dipilih)** mendaftar wilayah-wilayah yang diterapkan mode di atas.

1. Atur **Ketersediaan Wilayah** menjadi **Hanya di wilayah yang dipilih** atau **Semua wilayah kecuali yang dipilih**.
2. Di tabel **Ketersediaan Wilayah (wilayah yang dipilih)**, klik **Tambahkan Wilayah lainnya** dan pilih **Wilayah Penjualan**.
3. Ulangi untuk setiap wilayah yang ingin Anda tambahkan.
4. Klik **Simpan**.

![Tabel inline "Ketersediaan Wilayah (wilayah yang dipilih)" dengan baris Amerika Utara dan Eropa ditambahkan](/static/core/admin/img/help/region-availability/product-region-availability-inline.webp)

Jika **Ketersediaan Wilayah** diatur menjadi **Tersedia di semua wilayah**, apa pun yang ada di tabel ini diabaikan — hapus dulu mode dropdown jika Anda ingin menghilangkan pembatasan tanpa menghapus baris-barisnya.

Untuk melihat keseluruhan katalog setiap aturan wilayah produk dalam satu daftar (membantu saat meninjau banyak produk sekaligus), buka **Ketersediaan Wilayah Produk** di `/admin/catalog/productregionvisibility/`.

## Menampilkan kepada pembeli di mana produk tidak dikirimkan

Ketika wilayah pembeli tidak sesuai dengan aturan ketersediaan produk, Anda mengontrol apa yang mereka lihat di **Pengaturan Tampilan Persediaan**, di bawah bagian **Ketersediaan Wilayah**. Halaman ini belum memiliki pintasan sidebar — buka langsung di `/admin/catalog/stockdisplaysettings/`.

![Pengaturan Tampilan Persediaan, bagian Ketersediaan Wilayah — dropdown tampilan Wilayah yang diatur menjadi "Tampilkan, dicatat sebagai tidak tersedia"](/static/core/admin/img/help/region-availability/stock-display-region-availability.webp)

| Pilihan | Yang dilihat pembeli | 
|--------|-------------------| 
| **Tampilkan, dicatat sebagai tidak tersedia** (default) | Produk tetap muncul dalam daftar, dengan badge "Tidak tersedia" dan pesan "Tidak dikirim ke [wilayah]" alih-alih tombol Tambahkan ke Keranjang. Sebuah banner juga muncul di bagian atas halaman daftar ("Beberapa produk tidak dikirim ke [tujuan]) dengan tautan untuk menyaring hanya produk yang dikirim ke sana. | 
| **Sembunyikan dari daftar** | Produk dihapus dari daftar dan hasil pencarian sepenuhnya untuk pembeli di wilayah tersebut. | 

![Daftar produk toko depan yang dikirim ke Eropa — banner "Beberapa produk tidak dikirim ke Eropa" di atas grid, dan kartu produk yang dicatat "Tidak tersedia" dengan pesan "Tidak dikirim ke Eropa"](/static/core/admin/img/help/region-availability/storefront-region-restricted-listing.webp)

Halaman produk yang dibatasi selalu menampilkan pesan 'Produk ini tidak dikirim ke [wilayah]' ketika pengguna mencapainya secara langsung (misalnya, dari tautan yang dibagikan atau hasil pencarian mesin pencari) — ini berlaku terlepasai pilihan daftar mana pun yang Anda pilih di atas, karena tautan langsung melewati daftar sepenuhnya.

## Memungkinkan pengguna memilih atau menemukan wilayah mereka

Spwig dapat mendeteksi wilayah pengguna secara otomatis dan menawarkan opsi perubahan, dan Anda dapat menambahkan pemilih sehingga pengguna dapat mengubahnya kapan saja.

### Sebelum memulai

Anda perlu dua hal yang dikonfigurasi dengan benar agar deteksi dan perubahan wilayah berjalan dengan baik:

1. **Wilayah Penjualan** — negara-negara di setiap wilayah dan mata uang default setiap wilayah. Jika Anda tidak melihat **Wilayah Penjualan** di bawah **Inventaris** di bilah samping, aktifkan **Izinkan Banyak Gudang** di bawah **Pengaturan > Pengaturan Toko > E-commerce** untuk menampilkan tautan menu (Anda tidak perlu menggunakan banyak gudang — pengaturan ini hanya membuka item menu). Anda juga dapat langsung pergi ke `/admin/catalog/salesregion/`.
2. **Negara Pengiriman** — negara-negara yang sebenarnya dikirimkan toko Anda. Biasanya sudah tersedia: setiap negara yang Anda tambahkan ke Zona Pengiriman akan secara otomatis ditambahkan di sini juga. Untuk meninjau atau menyesuaikan daftar secara manual, buka langsung `/admin/shipping/shippingcountry/` (saat ini belum memiliki tautan bilah samping).

### Konfirmasi wilayah otomatis

Spwig mendeteksi wilayah pengguna dari lokasinya dan menerapkannya secara otomatis. Ketika hal itu membuat mereka berada di wilayah *selain* pasar utama toko Anda (pasar utama) — dan Anda memiliki dua atau lebih Wilayah Penjualan aktif — Spwig menampilkan konfirmasi pada kunjungan pertama mereka sehingga mereka tahu wilayah mana yang mereka kunjungi dan dapat mengubahnya:

> **Kami menetapkan wilayah Anda ke [Wilayah]**
> Kami memilih ini dari lokasi Anda sehingga Anda melihat produk dan harga yang benar. Salah? Pilih negara Anda.
> Kirim ke: [pemilih negara]  **[Terus berbelanja]**

![Penghalang konfirmasi "Kami menetapkan wilayah Anda ke Amerika Utara" di toko, dengan pemilih negara "Kirim ke" dan tombol "Terus berbelanja"](/static/core/admin/img/help/region-availability/region-confirmation-modal.webp)

Memilih negara yang berbeda di pemilih mengubah mereka secara langsung. Mengabaikan atau mengklik **Terus berbelanja** mempertahankan wilayah saat ini mereka, dan mereka tidak akan diminta lagi di browser ini. Pengunjung yang sudah berada di wilayah default toko Anda sama sekali tidak ditampilkan konfirmasi ini.

### Menambahkan Pemilih Kirim-ke di bagian header atau footer Anda

Jika Anda lebih suka memungkinkan pengguna mengubah wilayah mereka sendiri kapan saja (bukan hanya mengandalkan pesan otomatis), tambahkan widget **Pemilih Kirim-ke** ke bagian header atau footer Anda.

1. Navigasi ke **Desain > Header Builder** (atau **Footer Builder**).
2. Seret widget **Pemilih Kirim-ke** dari Perpustakaan Widget ke dalam baris.
3. Klik **Simpan**.

![Perpustakaan widget Builder Header dengan kelompok Toko yang ditonjolkan, menunjukkan widget Pemilih Kirim-ke bersama Shopping Cart, Menu Akun, dan Pemilih Bahasa](/static/core/admin/img/help/region-availability/ship-to-selector-widget-library.webp)

Widget ini tidak memerlukan pengaturan — secara otomatis mendaftar Negara Pengiriman aktif Anda, dan menampilkan pilihan saat ini pengguna (atau negara yang dideteksi GeoIP, jika mereka belum memilih satu pun). Memilih negara yang berbeda memperbarui wilayah mereka secara langsung dan memuat ulang ketersediaan produk dan harga halaman tersebut.

Pemilih Kirim-ke tidak memiliki formulir pengaturan khusus saat ini. Jika Anda ingin mengubah gaya tombolnya (outline, solid, atau hilang) atau menyembunyikan label "Kirim ke", buka pengaturan widget di builder dan sunting langsung bidang **Konfigurasi Kustom (JSON)** menggunakan `button_style` dan `show_label`.

### Mata uang mengikuti wilayah

Jika toko Anda mendukung lebih dari satu mata uang (diatur di bawah **Pengaturan > Multi-Mata Uang**), beralih wilayah — baik melalui pesan atau Pemilih Kirim-ke — juga beralih ke mata uang default wilayah tersebut.

Jika toko Anda hanya memiliki satu mata uang, atau belum secara eksplisit mengaktifkan mata uang kedua, mata uang akan tetap seperti semula ketika pembeli beralih wilayah.

## Tips

- Biarkan **Ketersediaan Wilayah** pada **Tersedia di semua wilayah** kecuali Anda memiliki alasan khusus untuk membatasi suatu produk — opsi ini paling sederhana dan tidak memerlukan pemeliharaan saat Anda menambahkan wilayah baru nanti.
- Gunakan **Hanya di wilayah yang dipilih** untuk daftar putih kecil (misalnya, produk yang diluncurkan di satu negara terlebih dahulu) dan **Semua wilayah kecuali yang dipilih** untuk daftar hitam kecil (misalnya, seluruh dunia kecuali negara di mana barang ini tidak memiliki lisensi) — pilih mana yang membutuhkan baris yang lebih sedikit saat menyiapkan.
- Jika pembeli melaporkan suatu produk tidak muncul padahal seharusnya terlihat, periksa **Pengaturan Ketersediaan Wilayah** produk tersebut dan apakah negara mereka ditangani oleh **Wilayah Penjualan** aktif dan **Negara Pengiriman** aktif.
- **Sembunyikan dari daftar** menjaga agar katalog Anda tetap rapi bagi pembeli yang tidak dapat membeli item tertentu, tetapi juga berarti merchandising dan pencarian akan terlihat lebih tipis di wilayah tersebut — **Tampilkan, dengan status tidak tersedia** biasanya lebih baik jika Anda tetap ingin pembeli menjelajahi katalog lengkap Anda meskipun mereka tidak bisa melakukan pembelian.
- Uji perilaku wilayah dengan menambahkan Pemilih Alamat Pengiriman ke bagian header dan beralih antar negara sendiri sebelum mengandalkan deteksi GeoIP selama peluncuran.
- Tetapkan nilai prioritas wilayah Anda secara sengaja — wilayah aktif dengan prioritas tertinggi adalah cadangan untuk pembeli yang negaranya tidak terdeteksi atau tidak cocok dengan wilayah apa pun.