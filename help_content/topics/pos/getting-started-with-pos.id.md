---
title: Memulai dengan POS
---

<!-- screenshots-needed:
- url: /en/admin/pos/
  filename: getting-started-dashboard.webp
  description: POS dashboard as it appears on a fresh install with no terminals registered
  save-to: core/static/core/admin/img/help/pos/
- url: /en/admin/pos/terminal-provider/wizard/step1/
  filename: getting-started-provider-wizard-step1.webp
  description: Payment provider wizard first step showing available provider options
  save-to: core/static/core/admin/img/help/pos/
- url: /en/admin/catalog/warehouse/
  filename: getting-started-store-location.webp
  description: Warehouse list showing a store location with the POS toggle enabled
  save-to: core/static/core/admin/img/help/pos/
-->

Spwig POS mengubah tablet atau browser menjadi kasir toko penuh — terhubung dengan katalog produk, inventaris, dan riwayat pesanan Anda. Daftar pemeriksaan ini membawa Anda dari instalasi baru hingga menyelesaikan transaksi pertama Anda. Setiap langkah memiliki tautan ke topik khusus jika Anda ingin detail lengkapnya.

![POS Dashboard](/static/core/admin/img/help/pos/getting-started-dashboard.webp)

## Langkah 1: Aktifkan POS untuk lokasi toko

Terminal POS terkait dengan lokasi toko fisik. Di Spwig, lokasi toko adalah gudang yang ditandai sebagai lokasi ritel.

1. Navigasikan ke **Catalog > Warehouses** di sidebar admin Anda.
2. Buka gudang yang ingin Anda gunakan sebagai toko, atau buat satu baru.
3. Centang toggle **Retail location** dan masukkan **POS display name** (misalnya, "High Street Store"). Nama ini muncul di struk dan pemilih terminal.
4. Simpan gudang.

Jika Anda memiliki beberapa toko atau ingin mengelompokkannya untuk pelaporan regional, buat **Store Group** terlebih dahulu di **POS > Store Groups**, lalu tetapkan setiap gudang ke grup tersebut. Grup toko memungkinkan Anda mengatur mata uang, zona waktu, dan template struk yang sama untuk semua lokasi dalam grup.

## Langkah 2: Buat atau verifikasi setidaknya satu akun staf dengan akses POS

Staf Anda masuk ke POS menggunakan kredensial yang sama yang mereka gunakan untuk admin Spwig. Setiap akun staf dengan status **Active** dan setidaknya izin `pos_admin` dapat mengakses POS.

Untuk memeriksa atau memberikan akses, pergi ke **Settings > Staff Management**, buka akun staf, dan konfirmasi bahwa mereka memiliki peran POS yang sesuai ditetapkan. Tidak diperlukan akun POS terpisah.

## Langkah 3: Daftarkan terminal POS pertama Anda

Terminal merepresentasikan satu register atau perangkat. Anda mendaftarkannya di admin, lalu pasangkan perangkat fisik ke terminal menggunakan kode pasangan sekali pakai.

1. Navigasikan ke **POS > POS Terminals** dan klik **+ Add POS Terminal**.
2. Beri nama terminal (misalnya, "Front Register") dan tetapkan ke lokasi toko yang telah Anda aktifkan di Langkah 1.
3. Simpan terminal. Spwig menghasilkan **kode pasangan 8 karakter** — Anda akan melihatnya di halaman detail terminal.
4. Di perangkat yang ingin Anda gunakan sebagai register, buka browser dan pergi ke `/pos/`.
5. Masukkan kode pasangan saat diminta. Perangkat sekarang terhubung ke terminal ini.

Kode pasangan hanya bisa digunakan sekali. Jika Anda perlu memasangkan ulang perangkat, buka terminal di admin dan klik **Regenerate pairing code**.

Untuk opsi konfigurasi perangkat keras (printer struk, scanner barcode, laci uang), lihat [POS Terminal Setup](pos-terminal-setup).

## Langkah 4: Konfigurasikan penyedia pembayaran

Penyedia pembayaran menghubungkan pembaca kartu Anda ke jaringan pembayaran seperti Stripe Terminal atau Square. Gunakan wizard pengaturan 5 langkah untuk memasukkan kredensial Anda.

1. Navigasikan ke **POS > Payment Providers** dan klik **Configure provider**.
2. Wizard terbuka di `/admin/pos/terminal-provider/wizard/step1/`.

![Payment Provider Wizard](/static/core/admin/img/help/pos/getting-started-provider-wizard-step1.webp)

3. Pilih penyedia Anda (misalnya, **Stripe Terminal**) dan ikuti instruksi di layar untuk semua lima langkah: pilih penyedia → instruksi pengaturan → masukkan kredensial → uji koneksi → konfigurasikan lokasi.
4. Badge hijau **Connected** mengonfirmasi integrasi sudah aktif.


Jika Anda hanya membutuhkan pembayaran tunai dan masukan kartu manual, pilih **Manual** sebagai penyedia — tidak diperlukan kredensial.

Untuk bidang kredensial terperinci untuk setiap penyedia yang didukung, lihat [Pengaturan Penyedia Pembayaran POS](pos-payment-provider-setup).

## Langkah 5: Pasangkan pembaca kartu

Dengan penyedia pembayaran terhubung, Anda dapat memasangkan pembaca kartu fisik ke salah satu terminal Anda menggunakan wizard pembaca 3 langkah.

1. Navigasikan ke **POS > Pembaca Kartu** dan klik **Tambahkan pembaca**.
2. Wizard pembaca dimulai di `/admin/pos/reader/wizard/step1/`.
3. Pilih penyedia Anda, lalu pilih **Daftarkan perangkat baru** (masukkan kode yang ditampilkan di layar pembaca) atau **Temukan yang sudah ada** (Spwig mengambil pembaca yang sudah terdaftar dengan penyedia).
4. Pada langkah terakhir, tetapkan pembaca ke terminal yang Anda buat di Langkah 3.

Setiap terminal mendukung satu pembaca kartu yang ditetapkan. Anda dapat mengalihkan pembaca kapan saja dari daftar Pembaca Kartu.

## Langkah 6: Desain struk Anda (opsional untuk hari pertama)

Spwig membuat template struk default secara otomatis. Anda dapat langsung memulai penjualan tanpa menyentuhnya — struk default mencetak nama toko, alamat, penjualan terinci, metode pembayaran, dan footer "Terima kasih atas pembelian Anda!".

Ketika Anda siap untuk menyesuaikan, pergi ke **POS > Template Struk**. Opsi termasuk logo Anda, nomor ID pajak, promosi kode QR, kebijakan pengembalian, dan lebar kertas (58mm atau 80mm untuk printer termal). Anda dapat membuat template terpisah per toko atau per kelompok toko.

## Langkah 7: Buka shift pertama Anda

Shift melacak siapa yang memproses penjualan dan seberapa banyak uang tunai yang seharusnya ada di laci. Kasir membuka dan menutup shift di POS itu sendiri.

1. Di perangkat yang dipasangkan, pergi ke `/pos/` dan masuk dengan kredensial staf Anda.
2. Pilih terminal dan lokasi toko.
3. Spwig meminta Anda untuk **menghitung uang awal** — masukkan jumlah uang tunai yang sudah ada di laci (masukkan `0` jika laci kosong).
4. Klik **Buka Shift**. Sekarang register siap untuk berjualan.

Untuk penjelasan lengkap tentang shift, pergerakan uang tunai, dan laporan rekonsiliasi, lihat [Mengelola Shift POS](pos-shifts).

## Langkah 8: Lakukan penjualan pertama Anda

Setelah shift terbuka, menjual sangat sederhana:

1. Cari produk berdasarkan nama, scan barcode, atau jelajahi kategori untuk menambahkan item ke keranjang.
2. Terapkan diskon atau kode voucher jika diperlukan.
3. Klik **Charge** untuk memulai pembayaran. Pilih metode pembayaran (tunai, kartu melalui pembaca, atau pembayaran terbagi).
4. Untuk pembayaran kartu, pembaca meminta pelanggan untuk menyentuh atau memasukkan kartu mereka.
5. Struk dicetak secara otomatis (atau menampilkan opsi struk digital). Pesanan disimpan ke riwayat pesanan Anda secara real-time.

## Langkah 9: Tutup shift di akhir hari

Menutup shift mengunci register dan menghasilkan ringkasan rekonsiliasi.

1. Dari menu POS, klik **Tutup Shift**.
2. Hitung uang tunai di laci dan masukkan total saat diminta.
3. Spwig menghitung uang tunai yang diharapkan berdasarkan uang awal, penjualan tunai, dan setiap pergerakan uang tunai selama shift, dan menampilkan perbedaannya.
4. Konfirmasi untuk menutup. Laporan shift disimpan dan terlihat di **POS > Shifts** di admin Anda.

Catat setiap uang tunai yang diambil atau ditambahkan ke laci selama hari sebagai **pergerakan uang tunai** (melalui menu shift) daripada menyesuaikan jumlah penutupan — ini menjaga rekonsiliasi Anda akurat.

## Tips

- Selesaikan Langkah 1 hingga 5 sebelum hari perdagangan Anda.

Langkah 6 hingga 9 dapat dilakukan pada hari tersebut.
- Gunakan kata sandi staf yang kuat tetapi mudah diingat — staf POS memasukkan kredensial mereka di register, jadi kata sandi yang terlalu kompleks memperlambat mereka.
- Jika pembaca kartu tidak muncul secara online, klik **Sinkronisasi pembaca** di halaman Pembaca Kartu untuk menarik status terbaru dari penyedia Anda.
- Uji alur penuh (buka shift → penjualan → struk → tutup shift) dengan transaksi uji $0.01 sebelum periode perdagangan sibuk Anda.
- POS berfungsi offline untuk penjualan tunai dasar.

Pembayaran melalui terminal kartu memerlukan koneksi internet untuk mengotorisasi.
- Anda dapat memiliki beberapa terminal di satu lokasi toko — tambahkan catatan terminal baru di admin dan pasangkan dengan perangkat yang berbeda.