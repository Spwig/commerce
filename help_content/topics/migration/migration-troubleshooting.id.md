---
title: Pemecahan Masalah Migrasi
---

Sebagian besar migrasi selesai tanpa insiden, tetapi koneksi gagal, impor berakhir dengan timeout, dan kadang-kadang proses berhenti sebelum selesai. Topik ini membahas diagnosis koneksi yang gagal, membaca log kemajuan saat impor berjalan, dan — yang paling penting — pilihan apa saja yang sebenarnya tersedia setelah terjadi masalah, termasuk apa yang sebenarnya dilakukan oleh Retry, Cancel, dan Rollback.

## Gagal koneksi pada langkah 2

Checkbox **Test connection before proceeding** secara default aktif dan merupakan diagnosis pertama — ini memvalidasi kredensial terhadap platform sumber sebelum Anda menyetujui bagian lain dari wizard. Jika gagal, pesan kesalahan biasanya menunjuk salah satu dari berikut:

- **WooCommerce** — URL toko yang hilang `https://` atau memiliki bagian jalur di akhir; kunci konsumen/rahasia yang salah ketik atau dibuat ulang; atau kunci API REST yang dibuat tanpa izin **Read** di **WooCommerce > Settings > Advanced > REST API**.
- **Shopify** — Domain toko tidak dalam format `yourstore.myshopify.com`; Client ID/Secret dari aplikasi yang salah; atau, paling umum, aplikasi yang dibuat di Dev Dashboard tetapi tidak pernah **diinstal** — membuat versi aplikasi tidak cukup, Anda membutuhkan tautan distribusi khusus dan klik **Install**. Spwig juga memberi peringatan jika `read_products`, `read_customers`, atau `read_orders` tidak termasuk dalam cakupan aplikasi.
- **Magento 2** — URL toko yang mengarah ke toko depan, bukan akar API, atau token integrasi yang dibuat tetapi tidak pernah diaktifkan (**Save > Activate > Allow**).
- **Masalah SSL** — sertifikat yang sudah kedaluwarsa, self-signed, atau dikonfigurasi dengan salah gagal koneksi sebelum kredensial diperiksa, menampilkan kesalahan umum, bukan kesalahan otentikasi. Jika kredensial terlihat benar, periksa sertifikat berikutnya.

Uji ulang koneksi setelah setiap perbaikan, bukan mengubah beberapa kredensial sekaligus — ini memisahkan mana yang salah.

## Membaca log langsung pada langkah 5

Saat impor berjalan, langkah 5 menampilkan log aktivitas saat terjadi. Klik **Show Details** untuk memperluasnya menjadi entri individu — level dan pesan — bukan hanya ringkasan langkah saat ini. Ini adalah cara tercepat untuk melihat apa yang terjadi jika kemajuan terlihat macet: dinding entri "dilewati" untuk satu jenis data biasanya hanya berarti Skip existing items berfungsi seperti yang dimaksudkan, bukan berarti sesuatu terjebak.

Tampilan log hanya menampilkan **500 entri terbaru**, sehingga pada migrasi besar, entri awal akan menggulir keluar dari pandangan saat impor masih berjalan. Jika Anda membutuhkan log lengkap setelah satu jenis data selesai, gunakan **Download Logs** di halaman hasilnya — tidak ada batasan seperti itu.

## Arti sebenarnya dari migrasi yang gagal

Ini adalah hal paling penting untuk dipahami jika migrasi gagal.

Ketika migrasi gagal, halaman penyelesaian memberi tahu Anda dengan jelas apa yang terjadi: item yang diimpor sebelum terjadinya error masih ada di toko Anda, tidak ada yang dihapus secara otomatis, dan memperbaiki masalah lalu menjalankan impor lagi akan melewati apa pun yang sudah berhasil masuk pada kali pertama. Terimalah ini apa adanya. Tidak ada langkah dalam impor yang berjalan di dalam transaksi database yang bisa dibatalkan sebagai satu unit — apa pun yang berhasil diimpor sebelum titik kegagalan, produk, kategori, pelanggan, pesanan, apa pun yang berhasil diselesaikan oleh pekerjaan itu, tetap ada di toko Anda persis seperti saat dibuat. Migrasi yang gagal adalah migrasi **parsial**, bukan migrasi yang dibatalkan.

Kegagalan juga menandai pekerjaan sebagai tidak dapat dikembalikan, sehingga tombol **Rollback** tidak akan tersedia pada **impor** yang gagal — tombol hanya muncul setelah migrasi selesai, atau jika rollback dari migrasi yang selesai gagal sebagian, dalam hal ini Spwig menawarkan tombol kembali agar Anda dapat mencoba lagi. Situasi satu-satunya di mana Anda paling ingin mengembalikan secara otomatis — impor yang gagal — tetap menjadi situasi di mana tombol tidak ditawarkan.

Jadi, ketika migrasi gagal:


1. **Periksa apa yang sebenarnya telah diimpor**, menggunakan jumlah yang terimpor, dilewati, atau gagal, serta log yang diunduh untuk membangun gambaran apa yang ada di toko Anda versus apa yang tidak berhasil masuk.

2. **Putuskan cara membersihkannya.** Untuk jumlah data yang kecil dan tidak lengkap, tinjau secara manual dan hapus apa yang tidak Anda inginkan melalui tampilan daftar admin normal.

Untuk impor yang lebih besar atau lebih berantakan, seringkali lebih cepat untuk membersihkan data yang telah diimpor sendiri sebelum memulai ulang daripada menyesuaikan setiap item satu per satu.

3. **Jalankan ulang dengan opsi Skip existing items diaktifkan**, terlepas dari jalur pembersihan yang Anda ambil — ini adalah cara mencegah data yang berhasil bertahan dari duplikasi pada upaya berikutnya.

## Ulangi

**Ulangi** memulai ulang impor dari awal secara lengkap. Ini menghapus penghitung dan log pekerjaan sebelumnya dan mengimpor semuanya dari awal — ini **tidak** melanjutkan dari titik di mana upaya gagal berhenti. Pertahankan **Skip existing items** diaktifkan agar item yang sudah masuk pada kali pertama tidak diduplikasi pada putaran kedua.

Jika migrasi berhenti karena mencapai **batas 4 jam**, pesan yang Anda lihat adalah akurat: menjalankan impor lagi dimulai dari awal dan melewatkan item yang sudah diimpor, bukan melanjutkan dari titik di mana migrasi berhenti. Untuk toko yang cukup besar untuk mencapai batas waktu, mengulang seluruh proses secara berulang jarang menyelesaikan; alih-alih itu, kurangi cakupan setiap jalannya dengan memilih lebih sedikit jenis data di langkah 3 (produk dalam satu jalur, pesanan dalam jalur lain) dan membuat beberapa putaran yang lebih kecil.

## Batal

**Batal** tersedia pada migrasi yang sedang berjalan, dan menandai pekerjaan sebagai gagal langsung di dashboard. Ini **tidak** menghentikan tugas impor latar belakang, yang terus berjalan dan menulis data hingga mencapai titik berhenti alami. Harapkan jumlah yang diimpor terus meningkat untuk sementara waktu setelah Anda membatalkan — biarkan mereka stabil sebelum memutuskan apa yang perlu dibersihkan, bukan bertindak berdasarkan jumlah yang dicatat saat Anda mengklik Batal.

## Tidak ada tombol jeda atau melanjutkan

Spwig tidak mendukung menjeda migrasi yang sedang berlangsung dan melanjutkannya nanti. Tombol **Lanjutkan** di dashboard digunakan untuk kasus yang berbeda: migrasi yang dikonfigurasi melalui wizard tetapi belum pernah dimulai. Ini membuka ulang wizard di tempat Anda meninggalkan konfigurasinya — tidak terkait dengan migrasi yang sudah berjalan.

## Rollback

> **Peringatan:** Rollback adalah tindakan permanen dan merusak. Baca bagian ini secara lengkap sebelum menggunakan.

Rollback ditawarkan pada migrasi **selesai**, dan kembali ditawarkan pada migrasi yang rollback sebelumnya gagal sebagian (status **Rollback Gagal**), sehingga rollback yang terhenti dapat dicoba ulang. Ini hanya menghapus apa yang dibuat oleh impor itu sendiri, dan mempertahankan apa pun yang sekarang toko Anda bergantung padanya:

- Pelanggan yang telah dipindahkan yang telah membuat pesanan asli sejak impor **akan tetap dipertahankan** — akun, alamat, sejarah loyalitas, dan kredit toko tetap bersamanya, dan pesanan asli tersebut tetap tidak tersentuh. Hanya pesanan yang dibuat oleh impor yang dihapus.

- Produk yang telah dipindahkan yang masih dirujuk oleh pesanan, bundel, kartu hadiah, atau slot konfigurasi **akan tetap dipertahankan**. Pesanan milik pelanggan lain tidak pernah diubah — rollback tidak dapat lagi menghapus item pesanan dari pesanan yang tidak terkait atau meninggalkannya dengan total yang salah.

- Apa pun yang tetap dipertahankan akan dilaporkan kembali kepada Anda dengan nama dan jumlah, beserta alasan — misalnya, "1 Produk tetap dipertahankan, masih dirujuk oleh item pesanan" — sehingga Anda tahu secara tepat apa yang masih ada dan mengapa.

- Afiliasi, komisi, dan pembayaran yang dibuat oleh impor **akan dihapus**, bersama dengan akun afiliasi apa pun yang dibuat oleh impor. Afiliasi yang terlampir ke pelanggan yang sudah ada tetap mempertahankan akun mereka; hanya catatan afiliasi yang dihapus.

Sejarah loyalitas dan kredit toko mengikuti pelanggan: dihapus jika pelanggan dihapus, tetap dipertahankan jika pelanggan tetap dipertahankan.

Ini tetap **tidak** menghapus rencana langganan, tingkat harga, atau sumber daya pemesanan yang dibuat oleh ekstensi toko — hal-hal ini bertahan setelah rollback dan perlu dibersihkan secara manual jika Anda tidak ingin mereka tetap ada.

Sebelum Anda mengonfirmasi, halaman konfirmasi menampilkan pratinjau tepat apa yang akan dihapus dan apa yang akan tetap ada, dihitung berdasarkan data live Anda — baca hal tersebut sebelum mengklik **Ya, Rollback Migration**.

Rollback kemudian berjalan di latar belakang, bukan di browser Anda, sehingga aman untuk menutup tab; periksa status migrasi untuk melihat laporan apa yang sebenarnya dihapus dan tetap ada setelah selesai.

Karena rollback tidak lagi mencapai lebih jauh dari apa yang dibuat oleh impor, itu bukan lagi alat yang hanya berlaku dalam sehari — pesanan nyata dari pelanggan yang telah dimigrasikan dan penjualan nyata dari produk yang telah dimigrasikan dilindungi sejauh waktu yang telah berlalu sejak migrasi. Ini tetap menjadi tindakan permanen dan merusak pada baris yang dihapus, jadi gunakan secara sengaja, bukan sembarangan, dan bersihkan secara manual apa pun yang tetap ada di Spwig yang sebenarnya tidak Anda inginkan.

Mengenai ketersediaan: tombol Rollback tetap ada di ringkasan migrasi yang selesai selama catatan pekerjaan tersebut masih ada — untuk sebagian besar platform tidak ada tenggat waktu tetap. Magento adalah pengecualian dan kehilangan ketersediaan rollback setelah jendela tertentu, jadi putuskan dengan cepat jika Anda menggunakan Magento. Catatan pekerjaan tidak dihapus berdasarkan jadwal apa pun, sehingga migrasi tetap dapat dirollback secara tak terbatas kecuali Anda menghapus catatannya sendiri.

## Strategi toko besar dan impor lambat

Untuk toko yang cukup besar sehingga satu kali eksekusi berisiko melebihi batas 4 jam:

- **Naikkan ukuran batch** di langkah 3 (hingga 100) — batch yang lebih besar biasanya berarti lebih sedikit perjalanan bolak-balik dan throughput yang lebih cepat.
- **Pisahkan migrasi ke beberapa eksekusi berdasarkan jenis data** — kategori dan produk dalam satu eksekusi, pelanggan dan pesanan dalam eksekusi berikutnya, alih-alih semuanya sekaligus.
- **Biarkan Skip existing items tetap aktif** untuk setiap eksekusi setelah yang pertama, sehingga eksekusi berulang tidak menggandakan apa yang sudah berhasil.
- **Matikan Impor gambar produk.** Mengunduh dan memproses setiap gambar biasanya menjadi faktor terbesar dalam eksekusi yang lambat. Anda dapat menambahkan gambar ke produk secara individual, atau melalui impor CSV terpisah, setelah data lainnya sudah selesai.

## Tips

- **Uji koneksi setelah setiap perubahan kredensial**, bukan hanya sekali di akhir — ini memisahkan nilai mana yang salah.
- **Jangan mengasumsikan pekerjaan yang gagal membersihkan dirinya sendiri** — periksa apa yang sebenarnya ada di toko Anda sebelum memutuskan untuk membersihkan atau mencoba kembali.
- **Skip existing items harus tetap aktif untuk setiap percobaan ulang** — ini adalah satu-satunya hal yang mencegah duplikasi pada ulasan kedua.
- **Jangan melawan batas 4 jam dengan lebih banyak percobaan ulang** — pisahkan berdasarkan jenis data alih-alih itu.
- **Baca pratinjau rollback sebelum mengonfirmasi** — ini menyebutkan tepat apa yang akan dihapus dan apa yang akan tetap ada, dihitung berdasarkan data live Anda, sehingga tidak ada kejutan.

<!-- screenshots-needed:
- url: /admin/migration/migrationjob/wizard/step2/
  filename: step2-connection-test-failed.webp
  description: Form koneksi langkah 2 menampilkan hasil uji koneksi yang gagal dan pesan kesalahan
  save-to: core/static/core/admin/img/help/migration-troubleshooting/
  viewport: 1440x900
- url: /admin/migration/migrationjob/wizard/step6/
  filename: step6-rollback-panel.webp
  description: Panel Rollback halaman penyelesaian dengan teks peringatan dan tombol Rollback Migration pada pekerjaan yang selesai
  save-to: core/static/core/admin/img/help/migration-troubleshooting/
  viewport: 1440x900
-->