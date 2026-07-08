---
title: Perbaruan Platform
---

Instalasi Spwig Anda dibangun dari kumpulan komponen — tema, widget, integrasi, elemen pembangun halaman, dan koneksi penyedia — masing-masing dengan versi sendiri yang dapat diperbarui secara independen. Registry Komponen memberi Anda pandangan pusat tentang segala sesuatu yang terinstal, menampilkan komponen mana yang memiliki pembaruan yang menunggu, dan memungkinkan Anda menginstal atau mengembalikan pembaruan kapan saja.

![Overview Registry Komponen](/static/core/admin/img/help/platform-updates/component-registry-overview.webp)

## Memahami registry komponen

Navigasikan ke **Ekstensi > Registry Komponen** untuk melihat setiap komponen yang terinstal di toko Anda. Setiap baris menampilkan:

- **Nama** — nama tampilan komponen
- **Tipe** — jenis komponen apa pun (tema, widget, integrasi, dll.)
- **Versi Saat Ini** — versi yang sedang berjalan di toko Anda
- **Status Pembaruan** — apakah pembaruan tersedia
- **Saluran** — saluran pembaruan mana yang diikuti oleh komponen
- **Pembaruan Otomatis** — apakah pembaruan diinstal secara otomatis
- **Kunci** — apakah komponen dibekukan di versi saat ini

Dashboard di bagian atas halaman menampilkan jumlah ringkasan: total komponen yang terinstal, jumlah yang memiliki pembaruan tersedia, dan jumlah yang sudah diperbarui.

### Jenis komponen

| Tipe | Apa itu |
|------|------------|
| Tema | Desain visual toko Anda |
| Widget | Blok pembangun halaman yang dapat digunakan kembali |
| Elemen Pembangun Halaman | Elemen khusus untuk pembangun halaman |
| Utilitas Pembangun Halaman | Alat editor dan utilitas |
| Template Header/Footer | Tata letak header dan footer |
| Penyedia Pengiriman | Integrasi penyedia pengiriman (FedEx, UPS, dll.) |
| Penyedia Email | Layanan pengiriman email |
| Penyedia Pembayaran | Integrasi gateway pembayaran |
| Penyedia Tingkat Tukar | Sumber data tingkat mata uang |
| Penyedia Terjemahan | Layanan terjemahan AI |
| Paket Bahasa | File terjemahan antarmuka |

## Saluran Pembaruan

Setiap komponen mengikuti saluran pembaruan yang mengontrol rilis mana yang diterimanya. Anda dapat menetapkan setiap komponen ke saluran yang berbeda berdasarkan seberapa besar risiko yang Anda terima.

| Saluran | Deskripsi | Terbaik untuk |
|---------|-------------|----------|
| **Stabil** | Rilis siap produksi yang telah diuji secara menyeluruh | Semua komponen di toko yang sedang berjalan |
| **Beta** | Bangunan pra-rilis untuk menguji fitur baru sebelum stabil | Komponen non-kritis yang ingin Anda pratinjau |
| **Pengembangan** | Fitur terbaru, mungkin tidak stabil | Hanya lingkungan pengujian |
| **Keamanan** | Perbaikan keamanan kritis saja, disampaikan dengan prioritas tertinggi | Komponen di mana stabilitas menjadi utama |

Untuk mengubah saluran komponen, klik nama komponen untuk membuka tampilan detail, lalu pilih nilai baru di bidang **Saluran Pembaruan** dan simpan.

## Memeriksa pembaruan

Spwig memeriksa pembaruan secara otomatis pada interval yang dikonfigurasikan di pengaturan server pembaruan Anda (default: setiap 24 jam). Untuk memeriksa segera:

1. Navigasikan ke **Ekstensi > Registry Komponen**
2. Klik tombol **Periksa Pembaruan** di bagian atas halaman
3. Sistem menghubungi server pembaruan Spwig dan memperbarui status pembaruan untuk semua komponen
4. Komponen dengan pembaruan yang tersedia diberi penekanan, dan jumlah **Pembaruan Tersedia** diperbarui

Anda juga dapat memicu pemeriksaan pembaruan untuk komponen individu menggunakan aksi **Periksa Pembaruan** dari menu aksi daftar.

## Menginstal pembaruan

### Memperbarui satu komponen

1. Navigasikan ke **Ekstensi > Registry Komponen**
2. Cari komponen yang ingin Anda perbarui — komponen dengan pembaruan yang tersedia menampilkan indikator pembaruan di sebelah versinya
3. Klik tombol **Instal Pembaruan** di baris komponen tersebut
4. Konfirmasi pembaruan saat diminta
5. Pembaruan diunduh, diverifikasi, dan diinstal — indikator kemajuan menampilkan setiap tahap
6. Setelah selesai, nomor versi **Saat Ini** komponen diperbarui ke nomor versi baru

### Memperbarui beberapa komponen

1.

Pilih kotak centang di sebelah komponen yang ingin Anda perbarui
2.



Pilih **Install updates** dari dropdown **Action**
3.

Klik **Go** untuk melanjutkan
4.

Pembaruan diinstal dalam urutan ketergantungan — komponen yang digantung oleh komponen lain akan diperbarui terlebih dahulu

### Apa yang terjadi selama pembaruan

Proses pembaruan melalui tahapan berikut:

1. **Checking** — memverifikasi pembaruan tersedia dan lisensi Anda valid
2. **Downloading** — mengunduh paket dari server pembaruan Spwig
3. **Verifying** — memeriksa integritas paket melawan checksum SHA-256
4. **Extracting** — membuka file baru
5. **Deploying** — mengaktifkan versi baru
6. **Health check** — memverifikasi komponen berfungsi setelah pembaruan

Jika ada tahapan yang gagal, sistem secara otomatis mencoba memulihkan versi sebelumnya.

## Pembaruan tingkat platform

Selain komponen individu, Spwig dapat menerima pembaruan tingkat platform yang memperbarui mesin toko inti. Pembaruan ini melalui proses yang lebih menyeluruh, termasuk migrasi database dan jendela perawatan singkat.

Riwayat pembaruan platform terlihat di bagian **Platform Updates** dari registry. Setiap entri menampilkan transisi versi (misalnya, `v1.3.2 → v1.3.3`), status, dan durasi proses pembaruan.

Pembaruan keamanan ditandai secara terpisah, dan jika **Auto Install Security Updates** diaktifkan dalam konfigurasi server pembaruan Anda, akan diinstal secara otomatis tanpa memerlukan tindakan manual.

## Melihat riwayat versi

Untuk melihat semua versi yang sebelumnya terinstal dari sebuah komponen:

1. Klik nama komponen untuk membuka tampilan detailnya
2. Gulir ke bagian **Component Versions** di bagian bawah halaman
3. Setiap entri versi menampilkan nomor versi, kapan terinstal, metode instalasi, dan status kesehatannya

Sistem menyimpan tiga versi terakhir yang terinstal yang tersedia untuk rollback. Versi di luar itu secara otomatis dihapus.

## Melakukan rollback komponen

Jika pembaruan menyebabkan masalah, Anda dapat kembali ke versi sebelumnya:

1. Buka tampilan detail komponen
2. Gulir ke bagian **Rollback**
3. Pilih versi yang ingin dipulihkan
4. Klik **Roll Back to this Version**

Hanya versi yang ditandai **Rollback Available** yang dapat dipulihkan. Catatan log rollback mencatat siapa yang memulai rollback dan kapan.

## Mengunci komponen

Mengunci komponen mencegah instalasi pembaruan apa pun, termasuk otomatis. Ini berguna ketika Anda memiliki kustomisasi atau integrasi yang bergantung pada versi tertentu.

1. Buka tampilan detail komponen
2. Centang kotak **Locked** di bagian **Lock & Freeze**
3. Masukkan alasan di **Lock Reason** agar tim Anda memahami mengapa komponen tersebut dibekukan
4. Simpan catatan

Komponen yang dikunci ditampilkan dengan indikator kunci di daftar registry. Untuk membuka kunci, hilangkan centang **Locked** dan simpan.

## Membaca log pembaruan

Log pembaruan mencatat setiap instalasi, pembaruan, rollback, dan operasi pemeriksaan kesehatan:

1. Buka tampilan detail komponen
2. **Update Logs** terlihat inline di bagian bawah halaman
3. Setiap entri menampilkan: tindakan yang diambil, waktu mulai dan selesai, versi lama dan baru, apakah itu otomatis atau manual, dan pesan kesalahan jika operasi gagal

Catatan log dengan status **Failed** mencakup pesan kesalahan lengkap untuk membantu dengan pemecahan masalah.

## Mengaktifkan pembaruan otomatis

Anda dapat memungkinkan Spwig untuk menginstal pembaruan secara otomatis saat tersedia:

1. Buka tampilan detail komponen
2. Centang **Auto Update** di bagian **Version & Update Status**
3. Simpan catatan

Dengan pembaruan otomatis diaktifkan, sistem menginstal pembaruan selama siklus pemeriksaan berikutnya. Pembaruan keamanan mengikuti pengaturan global **Auto Install Security Updates** tanpa memandang pengaturan komponen individu.

## Tips

Jaga semua format markdown, jalur gambar, blok kode, dan istilah teknis.

- Selalu perbarui melalui saluran **Stable** untuk tema dan penyedia pembayaran — ini adalah komponen yang paling berhadapan dengan pelanggan dan stabilitas paling penting
- Kunci komponen sebelum membuat modifikasi khusus terhadapnya, dan catat alasan secara jelas agar anggota tim masa depan tahu tidak untuk memperbarui
- Periksa **Release Notes** pada entri versi komponen sebelum menginstal peningkatan versi besar — perubahan yang memecah akan ditandai di sana
- Setelah pembaruan, kunjungi area yang terkena dampak dari toko Anda untuk memastikan semuanya terlihat dan berfungsi seperti yang diharapkan sebelum menyatakan pembaruan selesai
- Jika pembaruan otomatis diaktifkan pada komponen, pantau **Update Logs** secara berkala untuk memastikan pembaruan otomatis selesai dengan sukses