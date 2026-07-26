---
title: Pengantar Migrasi Data
---

Jika produk, pelanggan, dan pesanan Anda saat ini berada di WooCommerce, Shopify, atau Magento — atau hanya dalam beberapa file CSV — alat migrasi akan membawa data tersebut ke toko Spwig baru Anda sehingga Anda tidak perlu memasukkannya kembali secara manual. Alat ini menangani kategori, produk, pelanggan, pesanan, ulasan, dan kupon, serta untuk WooCommerce, juga dapat membawa konten blog dan, dengan plugin jembatan, program afiliasi Anda.

Cari di bilah sisi admin di bawah **System Dashboard > Data Import/Export** (terlihat oleh superuser pada instalasi self-hosted; jika Anda tidak melihatnya, tanyakan kepada siapa pun yang mengelola instalasi Anda). Halaman ini berjudul **Data Import & Export**, menampilkan setiap migrasi yang telah Anda mulai dengan kartu statistik untuk Total Migrations, Completed, In Progress, dan Failed, serta tombol **Start New Migration**, **View Logs**, dan **Field Mappings**. Migrasi hanya dapat dibuat melalui wizard.

## Platform yang Didukung

Spwig terhubung langsung ke tiga platform, plus file CSV biasa:

- **WooCommerce** — jalur paling lengkap; data ekstensi (langganan, bundel, kartu hadiah, pemesanan) dan program afiliasi Anda juga dapat dibawa.
- **Shopify** — terhubung melalui aplikasi khusus yang Anda buat di dashboard pengembang Shopify Anda.
- **Magento 2** — terhubung melalui token integrasi dari admin Magento Anda.
- **File CSV** — lima file terpisah (produk, kategori, pelanggan, pesanan, ulasan), untuk platform lain atau data yang telah dipersiapkan secara manual.

> **Catatan:** BigCommerce, PrestaShop, Squarespace, dan Wix tidak didukung sebagai koneksi langsung. Jika Anda pindah dari salah satu ini, ekspor katalog dan data pelanggan Anda ke CSV dan gunakan jalur CSV alih-alih — lihat [Importing from CSV Files](csv-import).

## Apa yang Ditransfer, Berdasarkan Platform

Cakupan bervariasi berdasarkan platform — periksa tabel ini terhadap toko Anda sendiri sebelum menetapkan tanggal peluncuran.

| Data | WooCommerce | Shopify | Magento 2 | CSV |
|---|---|---|---|---|
| Kategori | Ya, dengan hierarki | Ya, sebagai Koleksi (datar) | Ya | Ya |
| Produk | Ya | Ya | Ya | Ya (file yang diperlukan) |
| Gambar produk | Ya | Ya | Ya | Tidak |
| Variasi | Ya | Ya | Ya | Tidak |
| Pelanggan + alamat | Ya | Ya | Ya | Ya |
| Pesanan | Ya | Ya, hanya 60 hari terakhir kecuali lingkup `read_all_orders` ditambahkan | Ya | Ya |
| Ulasan | Ya | Tidak didukung sama sekali | Biasanya tidak tersedia — Magento Community tidak memiliki titik akhir REST untuk ulasan | Ya |
| Kupon / diskon | Ya | Ya | Ya | Tidak |
| Blog / konten CMS | Ya (posting, kategori, tag, gambar) | Ya (artikel) | Ya (halaman CMS) | Tidak |
| Afiliasi, komisi, pembayaran | Ya, memerlukan plugin Spwig Migration Bridge | Tidak | Tidak | Tidak |
| Deteksi bidang kustom | Ya | Tidak — metafield Shopify tidak dibaca | Tidak | n/a |

Pemilik toko Shopify harus merencanakan untuk memasukkan kembali data metafield (spesifikasi produk kustom, bidang pelanggan tambahan) secara manual setelah impor, karena tidak terdeteksi atau ditransfer. Untuk semua hal lainnya, lihat [Migration Field Mapping](migration-field-mapping) untuk melihat bagaimana bidang sumber dipetakan ke bidang Spwig.

## Merencanakan Migrasi Anda

- **Lakukan migrasi sebelum Anda diluncurkan**, terhadap instalasi Spwig yang belum menangani lalu lintas nyata, sebelum mengarahkan DNS domain Anda ke sana — dengan cara ini Anda dapat meninjau dan memperbaiki hal-hal tanpa pelanggan melihat katalog yang belum selesai.
- **Biarkan toko lama Anda tetap berjalan dalam mode hanya baca**, sampai Anda memverifikasi salinan Spwig sudah benar.
- **Anggarkan waktu untuk pengaturan pajak dan pengiriman setelahnya** — pengaturan wizard untuk hal ini tampaknya mengimpor tarif dan zona Anda, tetapi tidak diterapkan (lihat [Migration Field Mapping](migration-field-mapping)). Konfigurasikan **Settings > Tax & Currency** dan **Settings > Shipping** secara manual.
- **Periksa secara acak, bukan sekilas** — data ekstensi diimpor berdasarkan upaya terbaik; produk yang data ekstensinya tidak bisa dibaca tetap akan dibuat, hanya tanpa data tersebut. Lihat [After Your Migration](after-migration-review) sebelum mengumumkan apa pun kepada pelanggan.

- **Akses admin ke platform sumber Anda** untuk membuat kredensial API — kunci API REST di WooCommerce, aplikasi khusus di Shopify, atau token integrasi di Magento.

Tidak diperlukan untuk CSV.
- **Cakupan hanya untuk baca** di mana platform sumber menyediakannya — Spwig hanya membaca dari toko lama Anda, tidak pernah menulis kembali ke dalamnya.
- **Anggaran waktu** — setiap eksekusi memiliki batas keras 4 jam.

Untuk toko besar, rencanakan pendekatan bertahap (kategori dan produk terlebih dahulu, pesanan kemudian) daripada satu kali proses.

> **Penting:** Spwig tidak mengenkripsi kredensial API yang Anda masukkan dalam wizard. Setelah migrasi diverifikasi selesai, cabut atau hapus kredensial tersebut di platform sumber.

## Wizard migrasi, langkah demi langkah

Wizard memiliki enam langkah, dengan kemajuan disimpan antar langkah:

1. **Platform** — pilih WooCommerce, Shopify, Magento, atau Impor CSV.
2. **Koneksi** — masukkan kredensial, dengan opsi (diaktifkan secara default) untuk menguji koneksi terlebih dahulu. Panduan khusus platform menjelaskan secara tepat apa yang harus dibuat.
3. **Pratinjau** — jumlah langsung dari toko sumber Anda, contoh dari 5 produk pertama, dan kotak centang untuk jenis data yang akan dimasukkan serta opsi seperti ukuran batch.
4. **Pemetaan** — cara bidang sumber dipetakan ke bidang Spwig, bidang khusus WooCommerce, dan kategori tanpa cocok yang jelas. Detail lengkap dalam [Pemetaan Bidang Migrasi](migration-field-mapping).
5. **Impor** — berjalan di latar belakang; Anda dapat menutup tab dan proses tetap berjalan, dengan log langsung.
6. **Selesai** — ringkasan hasil, alat penggantian tautan untuk konten yang merujuk ke domain lama Anda, dan unduhan laporan PDF/CSV.

## Setelah migrasi Anda

Impor yang sukses bukanlah garis finish — lihat [Setelah Migrasi Anda](after-migration-review) untuk daftar pemeriksaan lengkap yang mencakup verifikasi data, memperbaiki tautan internal yang masih mengarah ke domain lama Anda, dan konfigurasi pajak serta pengiriman yang tidak ditangani oleh wizard untuk Anda.

## Rollback bukanlah jaring keselamatan

Pahami ini sebelum Anda memulai, bukan setelah sesuatu berjalan salah. Rollback ada, tetapi bukan tombol undo seperti yang mungkin terdengar:

- Tidak ada rollback otomatis jika impor gagal di tengah jalan. Apa pun yang telah diimpor sebelum kegagalan tetap ada di toko Anda, dan impor yang gagal tidak dapat di-rollback dari admin — Anda harus meninjau dan membersihkan data parsial secara manual.
- Migrasi yang selesai dapat di-rollback, dan rollback hanya menghapus apa yang dibuat oleh impor itu sendiri — tidak pernah lebih. Pelanggan yang bermigrasi dan telah menempatkan pesanan asli sejak impor tetap mempertahankan akun, alamat, riwayat loyalitas, dan kredit tokonya, dan pesanan asli tersebut tidak disentuh; hanya pesanan yang dibuat oleh impor yang dihapus. Produk yang bermigrasi dan masih dirujuk oleh pesanan, bundel, kartu hadiah, atau slot configurator mana pun juga dipertahankan, dan pesanan milik pelanggan lain tidak pernah diubah.
- Afiliasi, komisi, dan pembayaran yang dibuat oleh impor dihapus, bersama dengan akun afiliasi apa pun yang dibuat oleh impor — afiliasi yang terhubung dengan pelanggan yang sudah ada sebelumnya tetap mempertahankan akunnya, dan hanya catatan afiliasinya yang dihapus. Rencana langganan, tingkat harga, dan sumber daya pemesanan yang dibuat oleh ekstensi toko masih belum dihapus — bersihkan ini secara manual.
- Sebelum Anda mengonfirmasi, Spwig menampilkan pratinjau yang menunjukkan persis apa yang akan dihapus dan apa yang akan dipertahankan, berdasarkan nama dan jumlah, beserta alasannya — dihitung berdasarkan data langsung Anda. Bacalah sebelum mengonfirmasi. Rollback kemudian berjalan di latar belakang, sehingga aman untuk menutup tab; periksa ringkasan migrasi untuk laporannya setelah selesai.
- Rollback tetap merupakan tindakan permanen dan destruktif pada baris data yang dihapusnya, jadi gunakan dengan sengaja — dan bersihkan secara manual apa pun yang dipertahankan Spwig yang sebenarnya tidak Anda inginkan. Namun karena rollback tidak lagi menjangkau lebih dari apa yang dibuat oleh impor, ini bukan lagi alat yang hanya boleh digunakan di hari yang sama seperti sebelumnya.
- Tombol Rollback tetap tersedia pada ringkasan migrasi yang selesai selama catatan pekerjaan masih ada, dan ditawarkan kembali jika upaya rollback itu sendiri gagal di tengah jalan, sehingga Anda dapat mencobanya lagi. Catatan tidak dihapus berdasarkan jadwal apa pun, jadi ini tidak kedaluwarsa dengan sendirinya.

Jika Anda mengalami migrasi yang gagal atau macet, [Pemecahan Masalah Migrasi](migration-troubleshooting) mencakup ulang coba, membatalkan, dan membaca log.

## Tips

- **Mulailah dengan jalur uji kecil** — kategori ditambah beberapa produk memastikan peta bidang terlihat benar sebelum katalog penuh.
- **Baca panduan spesifik platform terlebih dahulu** — [Migrating from WooCommerce](migrate-from-woocommerce), [Migrating from Shopify](migrate-from-shopify), dan [Migrating from Magento](migrate-from-magento) mencakup secara tepat kredensial dan cakupan yang Anda butuhkan.
- **Jangan lewati matriks kemampuan di atas** — mengetahui ulasan Shopify atau variasi CSV tidak akan muncul menyelamatkan Anda dari kejutan setelah Anda beralih DNS.
- **Tahan tab admin platform sumber Anda terbuka** untuk menghasilkan atau menyalin kredensial saat Anda pergi.
- **Treat the wizard's checkboxes literally** — jika pengaturan tidak dijelaskan sebagai berfungsi di sini, konfigurasikan langsung di Spwig daripada mempercayai wizard.