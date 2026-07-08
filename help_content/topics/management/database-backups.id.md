---
title: Cadangan Database
---

Cadangan rutin melindungi data toko Anda — pesanan, pelanggan, produk, dan konfigurasi — dari kegagalan perangkat keras, penghapusan tidak sengaja, dan kejadian tak terduga lainnya. Sistem cadangan Spwig memungkinkan Anda membuat cadangan sesuai permintaan, mengatur jadwal otomatis, mengunduh cadangan secara lokal, memulihkan dari cadangan yang disimpan, dan menyalin cadangan ke tujuan penyimpanan jarak jauh seperti Amazon S3 atau Google Drive.

Navigasikan ke **Manajemen > Metrik Sistem** dan gunakan tautan di toolbar untuk mengakses alat cadangan.

![Dashboard Sistem dengan alat cadangan](/static/core/admin/img/help/database-backups/system-dashboard.webp)

## Membuat cadangan manual

Lakukan cadangan kapan saja sebelum membuat perubahan signifikan — seperti impor produk, pembaruan tema, atau pembaruan platform.

1. Navigasikan ke **Manajemen > Metrik Sistem**
2. Klik **Buat Cadangan Penuh** dari toolbar
3. Masukkan **Nama** yang deskriptif untuk cadangan (misalnya, `sebelum-import-juli`)
4. Secara opsional tambahkan **Deskripsi** untuk mengingatkan Anda mengapa cadangan ini dibuat
5. Pilih **Jenis Cadangan**:
   - **Sistem Penuh** — mencadangkan database dan semua file media (direkomendasikan)
   - **Hanya Database** — mencadangkan data toko saja, tanpa gambar dan file yang diunggah
6. Pilih **Kompresi** (`gzip` adalah default dan bekerja baik untuk sebagian besar toko)
7. Klik **Buat Cadangan**

Spwig membuat cadangan di latar belakang. Indikator kemajuan menunjukkan tahap saat ini. Ketika selesai, cadangan muncul dalam daftar **Cadangan Database** dengan status **Selesai** dan ukuran file-nya.

## Mengunduh cadangan

Anda dapat mengunduh cadangan yang selesai untuk menyimpan salinan lokal di komputer Anda.

1. Navigasikan ke **Manajemen > Cadangan Database**
2. Cari cadangan yang ingin Anda unduh
3. Klik tombol **Unduh** di sebelahnya

File cadangan diunduh sebagai arsip terkompresi. Simpan di tempat aman — di perangkat terpisah atau penyimpanan awan — sehingga Anda memiliki salinan yang independen dari server Anda.

## Jadwalkan cadangan otomatis

Cadangan otomatis berjalan di latar belakang tanpa tindakan dari Anda, sehingga data Anda dilindungi bahkan jika Anda lupa membuat cadangan manual.

1. Navigasikan ke **Manajemen > Metrik Sistem**
2. Klik **Jadwal Cadangan**
3. Centang **Aktifkan Cadangan Otomatis**
4. Tetapkan **Frekuensi**:
   - **Harian** — berjalan sekali per hari pada waktu yang Anda tentukan
   - **Mingguan** — berjalan sekali per minggu pada hari yang Anda pilih
   - **Bulanan** — berjalan pada hari tertentu dalam bulan
5. Tetapkan **Waktu** cadangan harus berjalan (waktu server, biasanya UTC — 03:00 AM adalah waktu dengan lalu lintas rendah yang baik)
6. Pilih **Jenis Cadangan** (Sistem Penuh atau Hanya Database)
7. Tetapkan **Hari Retensi** — cadangan yang lebih tua dari jumlah hari ini dihapus secara otomatis (default: 30 hari)
8. Secara opsional centang **Enkripsi Cadangan** untuk mengenkripsi file cadangan dalam penyimpanan
9. Jika Anda memiliki tujuan penyimpanan jarak jauh yang dikonfigurasi, pilih mereka di bawah **Tujuan Jarak Jauh** untuk mengunggah cadangan yang dijadwalkan secara otomatis
10. Klik **Simpan Jadwal**

Timestamp **Berikutnya** diperbarui segera dan menunjukkan kapan cadangan otomatis berikutnya akan terjadi.

## Memulihkan dari cadangan

Memulihkan mengganti data toko saat ini dengan isi cadangan. Gunakan ini untuk memulihkan dari kehilangan data atau membatalkan perubahan yang tidak diinginkan.

> **Penting:** Memulihkan akan mengganti semua data saat ini dengan data cadangan. Toko Anda akan ditempatkan dalam mode perawatan selama pemulihan. Beri tahu tim Anda sebelum menjalankan pemulihan.

1. Navigasikan ke **Manajemen > Metrik Sistem**
2. Klik **Pulihkan** dari toolbar
3. Daftar pemulihan menampilkan semua cadangan yang tersedia dengan tanggal dan ukurannya
4. Klik **Pulihkan** di sebelah cadangan yang ingin Anda gunakan
5. Periksa layar konfirmasi — daftar ini menunjukkan secara tepat apa yang akan diganti
6. Ketik frasa konfirmasi jika diminta, lalu klik **Eksekusi Pemulihan**

Spwig menampilkan bar kemajuan saat pemulihan berjalan melalui tahap-tahapnya (mencadangkan keadaan saat ini, mengunduh cadangan jika jarak jauh, memulihkan database, memulihkan file media). Ketika selesai, toko secara otomatis keluar dari mode perawatan.

## Mengatur penyimpanan jarak jauh

Penyimpanan jarak jauh secara otomatis menyalin cadangan Anda ke tujuan eksternal — Amazon S3, Google Drive, Dropbox, atau server SFTP. Ini melindungi Anda dari kegagalan tingkat server.

1. Navigasikan ke **Manajemen > Metrik Sistem**
2. Klik **Penyimpanan Jarak Jauh**
3. Klik **Tambahkan Tujuan**
4. Penjelajah pengaturan akan memandu Anda melalui tiga langkah:
   - **Langkah 1**: Pilih jenis penyimpanan Anda (S3, Google Drive, Dropbox, atau SFTP)
   - **Langkah 2**: Masukkan kredensial untuk penyedia yang dipilih (lihat detail di bawah ini)
   - **Langkah 3**: Beri nama tujuan dan uji koneksi
5. Setelah uji koneksi berhasil, klik **Simpan**

### Amazon S3 (dan layanan S3 yang kompatibel)

Anda memerlukan:
- **Access Key ID** dan **Secret Access Key** dari pengguna IAM AWS Anda
- **Nama Bucket** — bucket S3 untuk mengunggah cadangan
- **Wilayah** — wilayah AWS tempat bucket berada (misalnya, `us-east-1`)
- Secara opsional sebuah **Prefix** (jalur folder di dalam bucket, misalnya, `spwig-backups/`)

Layanan S3 yang kompatibel (Backblaze B2, Wasabi, MinIO, dll.) bekerja dengan cara yang sama — masukkan URL endpoint kustom saat diminta.

### Google Drive

Klik **Connect with Google** pada langkah kredensial. Spwig membuka jendela otorisasi Google — masuk dan beri izin untuk mengunggah file. Tidak ada kredensial yang perlu disalin secara manual.

### Dropbox

Klik **Connect with Dropbox** pada langkah kredensial. Masuk ke Dropbox dan setujui akses. Cadangan diunggah ke folder `Apps/Spwig` di Dropbox Anda.

### SFTP

Anda memerlukan:
- **Hostname** server SFTP Anda
- **Port** (default: 22)
- **Username** dan **Password** (atau kunci pribadi SSH)
- **Path Remote** — direktori di server untuk mengunggah cadangan

### Menetapkan tujuan sebagai default

Di halaman **Penyimpanan Jarak Jauh**, klik tombol toggle di sebelah tujuan apa pun untuk membuatnya menjadi **default**. Tujuan default secara otomatis menerima setiap cadangan — manual dan jadwal — tanpa perlu memilihnya setiap kali.

## Tips

- Jalankan cadangan manual sebelum setiap perubahan signifikan: impor produk, pengeditan tema, pembaruan platform, atau kampanye diskon
- Jadwalkan cadangan harian pada waktu lalu lintas rendah (misalnya, pukul 03:00) untuk meminimalkan dampak kinerja
- Atur setidaknya satu tujuan penyimpanan jarak jauh agar cadangan tetap ada bahkan jika server itu sendiri mengalami masalah
- Pengaturan **Retention Days** mengontrol seberapa lama cadangan lokal disimpan — 30 hari adalah default yang wajar untuk sebagian besar toko, tetapi tingkatkan jika ruang penyimpanan memungkinkan
- Setelah pemulihan, periksa beberapa pesanan dan produk untuk memastikan data terlihat benar sebelum secara manual mengeluarkan toko dari mode pemeliharaan
- Cadangan terenkripsi menambah lapisan keamanan tetapi memerlukan kunci dekripsi untuk memulihkannya — jangan kehilangkannya