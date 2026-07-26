---
title: Setelah Pemindahan Anda
---

Pemindahan yang selesai adalah awal dari tinjauan Anda, bukan akhirnya. Langkah 6 dari wizard memberi Anda ringkasan apa yang telah dipindahkan, alat untuk memperbaiki tautan yang masih mengarah ke situs lama Anda, dan laporan yang dapat Anda unduh untuk catatan Anda. Topik ini membimbing Anda melalui hal-hal yang perlu diperiksa sebelum Anda mempertimbangkan pemindahan sebagai selesai, termasuk pekerjaan pajak, pengiriman, dan go-live yang wizard itu sendiri tidak lakukan untuk Anda.

## Membaca hasil Anda

Di bagian atas halaman penyelesaian, Anda akan melihat baris kartu statistik — satu per jenis data (Produk, Kategori, Pelanggan, Pesanan, dan sebagainya) — diikuti oleh tabel **Ringkasan Impor** dengan kolom Impor, Dilewati, Gagal, dan Total untuk setiap langkah yang berjalan.

- **Impor** — item yang berhasil dibuat di Spwig.
- **Dilewati** — item yang dimiliki platform sumber Anda, tetapi Spwig tidak membuatnya. Ini hampir selalu diharapkan: dengan **Lewati item yang sudah ada** diaktifkan di langkah 3, apapun yang cocok dengan item yang sudah ada di Spwig (berdasarkan SKU, email, dll.) akan dibiarkan begitu saja daripada diduplikasi. Jumlah dilewati yang tinggi setelah percobaan ulang biasanya hanya berarti upaya pertama sudah membuat catatan tersebut.
- **Gagal** — item yang Spwig coba buat tetapi gagal karena masalah data, ketergantungan yang hilang, atau kesalahan di sisi sumber. Jumlah gagal yang tidak nol layak untuk diselidiki; lihat [Pemecahan Masalah Pemindahan](migration-troubleshooting) untuk cara membaca log dan pilihan bersih Anda.

> **Catatan:** Jika ada langkah yang menunjukkan kegagalan, jangan asumsikan toko membatalkan sesuatu untuk mengimbangi — tidak. Apapun yang telah diimpor sebelum kegagalan berada di toko Anda bersama dengan segala sesuatu yang berhasil. Tinjau dengan cara yang sama seperti hasil parsial normal.

## Penulisan Ulang Tautan

Produk, halaman, dan posting blog yang diimpor dari platform lama Anda sering kali berisi tautan kembali ke domain asli mereka — URL gambar, tautan "produk terkait", referensi silang internal. Jika Spwig mendeteksi salah satu dari ini dalam konten yang baru saja diimpor, panel **Penulisan Ulang Tautan** akan muncul di halaman penyelesaian.

Setiap tautan yang terdeteksi dikelompokkan berdasarkan halaman atau produk yang berasal darinya, dan ditampilkan dengan:

- **URL Asli** — tautan persis seperti yang muncul dalam konten yang diimpor.
- **URL yang Disarankan** — tebakan terbaik Spwig untuk halaman yang setara di toko baru Anda, jika ditemukan.
- **Kesesuaian** — persentase kepercayaan untuk saran tersebut. Tautan yang tidak memiliki kesesuaian yang masuk akal ditampilkan sebagai **Tidak Ada** dan tidak memiliki URL yang disarankan untuk disetujui.

Untuk setiap tautan, Anda dapat **Menyetujui** saran atau **Melewati** satu per satu. **Menyetujui otomatis tingkat kepercayaan tinggi** menyetujui semua saran dengan persentase 85% atau lebih dalam satu klik — penghemat waktu, tetapi tetap layak untuk diperiksa secara acak setelahnya. Saran di bawah ambang batas tersebut adalah yang layak untuk dibuka secara manual: kesesuaian 50-70% mungkin merupakan produk yang benar tetapi dengan nama yang salah, atau mungkin jauh dari target, dan hanya pandangan manusia yang bisa menentukan.

Menyetujui atau melewati hanya menandai tautan — tidak ada perubahan dalam konten Anda sampai Anda mengklik **Terapkan Tautan yang Disetujui**, yang menulis ulang semua tautan yang disetujui sekaligus. Artinya, aman untuk bekerja melalui daftar ini dalam beberapa sesi sebelum mengkomitmen.

> **Tips:** Biarkan tautan yang tidak yakin Anda **Melewati** daripada menyetujui tebakan. Anda selalu bisa memperbaiki tautan domain lama yang tersisa secara manual nanti; mengubah ulang tautan yang salah ke puluhan produk akan lebih banyak pekerjaan untuk dibatalkan.

## Memverifikasi data Anda

Anggap kartu statistik sebagai titik awal, bukan bukti bahwa segalanya benar. Luangkan beberapa menit untuk memeriksa secara acak:

- **Produk** — Buka beberapa produk, terutama yang memiliki variasi (ukuran, warna, dll.), dan konfirmasi bahwa opsi variasi dan harga telah masuk dengan benar, dan gambar yang terlampir dan ditampilkan di toko, bukan hanya di admin.
- **Kategori** — Konfirmasi hierarki kategori terlihat benar, terutama jika Anda bermigrasi dari Shopify, di mana koleksi diimpor sebagai daftar datar, bukan pohon bersarang.
- **Akun pelanggan** — Periksa email dan alamat pada beberapa catatan.


Pelanggan yang telah dipindahkan tidak membawa kata sandi lama mereka — Spwig tidak memiliki cara untuk membacanya dari platform sumber — sehingga **pelanggan akan perlu mereset kata sandi mereka** saat pertama kali masuk.

Pertimbangkan untuk mengirimkan email peringatan sebelum Anda meluncurkan.
- **Pemesanan** — Periksa apakah total, status, dan item pesanan pada sampel pesanan sesuai dengan yang Anda lihat di platform lama.
- **Produk yang berasal dari ekstensi** — Jika Anda memindahkan dari WooCommerce dengan ekstensi seperti Subscriptions, Bundles, Gift Cards, Composite Products, atau Bookings, lakukan pemeriksaan acak pada produk yang menggunakan ekstensi tersebut.

Data ekstensi yang tidak dapat dibaca tidak menghambat produk dari diimpor — produk tersebut tetap masuk, hanya tanpa konfigurasi tambahan — sehingga produk-produk ini paling mungkin memerlukan perbaikan manual.

## Mengonfigurasi pajak dan pengiriman

Opsi langkah 4 dari wizard untuk mengimpor pengaturan pajak dan zona pengiriman mencatat preferensi Anda, tetapi tidak diterapkan pada proses impor — tidak ada tarif pajak atau zona pengiriman yang dibuat dari opsi tersebut. Ini adalah hal yang diharapkan: **pengaturan pajak dan pengiriman adalah langkah normal yang terpisah yang Anda selesaikan secara langsung di Spwig** setelah proses impor data selesai, sama seperti yang Anda lakukan saat mengatur toko baru.

**Kontrol Penyesuaian Harga** di langkah yang sama adalah pengecualian — ini benar-benar berlaku untuk impor WooCommerce, CSV, dan Shopify, menggeser harga dasar setiap produk saat dibuat. Jika Anda mengatur satu dan harga Anda terlihat salah, itu adalah tempat perubahan berasal. Lihat [Pemetaan Bidang Migrasi](migration-field-mapping) untuk detailnya.

Sebelum Anda meluncurkan, konfigurasikan:

- Tarif pajak Anda — lihat [Konfigurasi Pajak](tax-configuration) untuk mengatur tarif berdasarkan negara, provinsi, atau wilayah, termasuk eksim yang diperlukan oleh produk Anda.
- Zona dan metode pengiriman Anda — lihat [Mengatur Pengiriman](setup-shipping) untuk mereplikasi opsi pengiriman yang dimiliki pelanggan Anda di platform lama.

Lakukan ini sebelum menguji checkout, sehingga pesanan uji Anda mencerminkan total yang sebenarnya.

## Mendownload laporan Anda

Halaman penyelesaian menawarkan tiga unduhan:

- **Unduh PDF** — ringkasan berformat dengan metadata pekerjaan, jumlah per langkah, dan daftar kesalahan, dibatasi hingga **20 kesalahan pertama**.
- **Unduh CSV** — ringkasan yang sama dalam bentuk spreadsheet, dibatasi hingga **50 kesalahan pertama**.
- **Unduh Log** — setiap entri log untuk pekerjaan tersebut, tanpa batas.

Jika jumlah kegagalan Anda kecil, PDF atau CSV sudah cukup. Untuk migrasi dengan jumlah kegagalan yang besar, unduh lognya — satu-satunya dari tiga yang memiliki catatan lengkap, bukan sampel yang dipotong.

> **Tips:** Rekaman pekerjaan migrasi — termasuk log dan laporan mereka — tetap ada di Spwig selamanya; tidak ada yang menghapusnya secara otomatis. Unduh salinan tetap jika Anda ingin menyimpannya untuk catatan offline atau berbagi dengan seseorang yang tidak memiliki akses administrator, tetapi tidak ada penghitungan mundur yang memaksa Anda melakukannya hari ini.

## Meluncurkan

Setelah Anda puas dengan data, pengaturan pajak, dan pengiriman Anda:

1. **Uji checkout dari awal hingga akhir.** Tambahkan produk ke keranjang, selesaikan checkout, dan konfirmasikan bahwa pajak, pengiriman, dan pembayaran semua dihitung dan diproses dengan benar, sebaiknya dengan metode pembayaran nyata dalam mode uji.
2. **Perbarui DNS Anda** untuk mengarahkan domain Anda ke Spwig hanya setelah uji tersebut berhasil. Jangan beralih DNS terlebih dahulu dan men-debug setelahnya — pelanggan bisa mengalami checkout yang rusak dalam waktu itu.
3. **Biarkan toko lama Anda tetap tersedia dalam keadaan hanya baca atau "tutup"** hingga Anda yakin toko baru menangani pesanan dengan benar. Ini memberi Anda cadangan tanpa mempertaruhkan pesanan yang ditempatkan di toko lama setelah perpindahan.

## Membatalkan kredensial platform sumber

Setelah Anda memverifikasi migrasi selesai dan tidak mengharapkan menjalankannya lagi, kembali ke platform sumber Anda dan batalkan atau hapus kunci API, aplikasi, atau integrasi yang Anda buat untuk platform tersebut (lihat [Migrasi dari WooCommerce](migrate-from-woocommerce) atau panduan platform yang setara untuk mengetahui di mana kredensial tersebut berada).


Spwig tidak memerlukan akses permanen ke toko lama Anda setelah proses impor selesai, sehingga menghapusnya memutus kredensial yang sudah tidak Anda gunakan.

## Tips

- **Dilewati biasanya aman, gagal tidak** — jumlah dilewati yang besar setelah mencoba kembali dengan opsi Skip existing items on diharapkan; jumlah gagal yang tidak nol memerlukan peninjauan log.
- **Jangan terburu-buru untuk Menggunakan Tautan yang Disetujui** — persetujuan dan pengabaian bisa berubah hingga Anda mengklik Apply, jadi ambil waktu Anda untuk yang memiliki tingkat kepercayaan rendah.
- **Atur pajak dan pengiriman sebelum penjualan pertama Anda yang live**, bukan setelahnya — impor tidak melakukannya untuk Anda, dan tingkat pajak yang belum dikonfigurasi mudah terlewat hingga pelanggan mengeluh.
- **Peringatkan pelanggan tentang pengaturan ulang kata sandi** jika Anda mengirimkan daftar pelanggan Anda tentang perpindahan ini, agar login pertama bukanlah kejutan.
- **Unduh laporan Anda sebelum tanda 90 hari** jika Anda membutuhkannya untuk catatan akuntansi atau kepatuhan.
- **Biarkan toko lama tetap aktif dalam mode hanya baca selama beberapa waktu** — biayanya kecil dan memberi Anda jaring pengaman selama hari-hari pertama Anda live di Spwig.

<!-- screenshots-needed:
- url: /admin/migration/migrationjob/wizard/step6/
  filename: step6-results-summary.webp
  description: Halaman penyelesaian migrasi yang menampilkan kartu statistik dan tabel ringkasan Imported/Skipped/Failed/Total
  save-to: core/static/core/admin/img/help/after-migration-review/
  viewport: 1440x900
- url: /admin/migration/migrationjob/wizard/step6/
  filename: step6-link-rewriting.webp
  description: Panel Penulisan Ulang Tautan dengan saran yang dikelompokkan, persentase kepercayaan, dan kontrol Approve/Skip/Apply Approved Links
  save-to: core/static/core/admin/img/help/after-migration-review/
  viewport: 1440x900
-->