---
title: Mengelola Akun Pelanggan
---

Akun pelanggan memungkinkan pedagang melacak informasi pelanggan, riwayat pesanan, dan preferensi. Navigasikan ke **Pelanggan > Semua Pelanggan** di bilah sisi admin untuk mengelola akun pelanggan.

![Tambah Pelanggan](/static/core/admin/img/help/managing-customer-accounts/add-customer.webp)

## Memahami Akun Pelanggan vs Profil Pelanggan

**Akun Pelanggan** adalah kredensial login (email/password) yang disimpan dalam model User. **Profil Pelanggan** menyimpan informasi tambahan seperti nomor telepon, tanggal lahir, preferensi, dan analitik. Setiap akun pelanggan memiliki profil yang sesuai yang menyimpan data ekstensif ini.

Ketika Anda mengelola pelanggan di admin, Anda bekerja dengan Profil Pelanggan yang terhubung ke akun User di belakang layar.

## Melihat Semua Pelanggan

Daftar pelanggan menampilkan semua pelanggan yang terdaftar dengan metrik utama:

| Kolom | Deskripsi |
|--------|-------------|
| **Pengguna** | Nama dan alamat email pelanggan |
| **Status Afiliasi** | Apakah pelanggan juga merupakan mitra afiliasi |
| **Nilai Pelanggan** | Jumlah total yang telah dihabiskan oleh pelanggan (dikodekan dengan warna) |
| **Segment Pelanggan** | Segment RFM (Champion, Loyal, At Risk, dll.) |
| **Total Pesanan** | Jumlah pesanan yang selesai |
| **Hari Sejak Pesanan Terakhir** | Kesegaran pembelian terakhir |
| **Pelanggan VIP** | Badge jika pelanggan ditandai sebagai VIP |

### Menyaring Pelanggan

Gunakan bilah saring untuk menyempitkan daftar:

- **Status Afiliasi** — Adalah Afiliasi, Bukan Afiliasi, Afiliasi Tertunda, Aktif, Dijeda, Ditolak
- **Tata Letak Dashboard** — Tata letak dashboard yang dipilih pelanggan
- **Langganan Berita** — Apakah pelanggan memilih untuk menerima berita
- **Email Pemasaran** — Apakah pelanggan memilih untuk menerima email pemasaran
- **Dibuat Pada** — Saring berdasarkan tanggal pendaftaran

### Mencari Pelanggan

Gunakan bilah pencarian untuk menemukan pelanggan berdasarkan:

- Nama pengguna
- Alamat email
- Nama depan
- Nama belakang
- Nomor telepon

## Melihat Detail Pelanggan

Klik nama pelanggan untuk melihat profil lengkap mereka. Halaman detail pelanggan menampilkan:

![Detail Pelanggan](/static/core/admin/img/help/managing-customer-accounts/customer-detail.webp)

### Bagian Informasi Pelanggan

Detail kontak dasar dan status akun:
- **Pengguna** — Tautan ke akun User yang mendasari
- **Telepon** — Nomor telepon pelanggan
- **Tanggal Lahir** — Untuk verifikasi usia dan kampanye ulang tahun

### Preferensi Dashboard

Cara pelanggan mengkustomisasi dashboard akun mereka:
- **Tata Letak Dashboard** — Tampilan grid, daftar, atau kompak
- **Tampilkan Riwayat Pesanan** — Apakah riwayat pesanan muncul di dashboard
- **Tampilkan Daftar Keinginan** — Apakah daftar keinginan muncul di dashboard
- **Tampilkan Produk Terbaru** — Apakah produk yang dilihat baru muncul
- **Tampilkan Rekomendasi** — Apakah rekomendasi produk muncul

### Preferensi Komunikasi

Status pelanggan untuk berbagai komunikasi:
- **Langganan Berita** — Pelanggan memilih untuk menerima berita umum
- **Email Pemasaran** — Pelanggan memilih untuk menerima email promosi
- **Pemberitahuan Pesanan** — Pelanggan memilih untuk menerima pembaruan status pesanan

### Analitik Pelanggan

Ringkasan bacaan tentang perilaku dan nilai pelanggan:
- **Ringkasan Analitik Pelanggan** — Skor RFM, segment, nilai seumur hidup
- **Ringkasan Perilaku Pembelian** — Frekuensi pesanan, nilai rata-rata pesanan, kategori yang dipilih
- **Ringkasan Keterlibatan** — Login terakhir, tingkat pembukaan email, aktivitas situs

Bidang analitik ini dihitung secara otomatis dan tidak dapat diedit secara manual. Lihat [Memahami Analitik Pelanggan](customer-analytics.md) untuk detailnya.

## Membuat Akun Pelanggan

Pedagang dapat membuat akun pelanggan secara manual untuk pesanan telepon, pengambilan di toko, atau pendaftaran awal pelanggan grosir.

1. Klik **+ Tambahkan Profil Pelanggan** di pojok kanan atas
2. Isi bidang yang diperlukan dan opsional:

| Bidang | Diperlukan | Deskripsi |
|-------|----------|-------------|
| **Pengguna** | Ya | Pilih akun User yang sudah ada atau buat yang baru |
| **Telepon** | Tidak | Nomor telepon pelanggan |
| **Tanggal Lahir** | Tidak | Untuk verifikasi usia dan kampanye ulang tahun |
| **Langganan Berita** | Tidak | Langgani pelanggan ke berita |
| **Email Pemasaran** | Tidak | Langgani pelanggan ke email pemasaran |

### Membuat Akun Pengguna Baru Saat Menambahkan Profil

Jika pelanggan belum memiliki akun User:
1. Klik ikon **+** di sebelah bidang Pengguna
2. Masukkan **alamat email** pelanggan (ini menjadi nama pengguna mereka)
3. Secara opsional masukkan **nama depan** dan **nama belakang**
4. Secara opsional atur **kata sandi**
5. Centang **Kirimkan email pengaturan ulang kata sandi** jika Anda tidak mengatur kata sandi
6. Simpan akun Pengguna
7. Lengkapi bidang Profil Pelanggan
8. Klik **Simpan**

### Email Selamat Datang

Setelah membuat akun pelanggan:
- Jika Anda mengatur kata sandi, pelanggan dapat login segera dengan kata sandi tersebut
- Jika Anda tidak mengatur kata sandi, sistem mengirimkan email pengaturan ulang kata sandi agar pelanggan dapat menetapkan kata sandi mereka sendiri
- Anda dapat memicu email selamat datang secara manual melalui sistem email di **Pemasaran > Kampanye Email**

## Mengedit Informasi Pelanggan

Untuk memperbarui detail pelanggan:
1. Navigasikan ke **Pelanggan > Semua Pelanggan**
2. Klik nama pelanggan
3. Modifikasi bidang yang ingin diperbarui
4. Klik **Simpan**

### Apa yang Bisa Anda Edit

**Detail Kontak:**
- Nama (melalui akun User)
- Alamat email (melalui akun User)
- Nomor telepon
- Tanggal lahir

**Preferensi:**
- Status langganan berita
- Pendaftaran email pemasaran
- Preferensi pemberitahuan pesanan
- Tata letak dashboard dan pengaturan visibilitas

### Apa yang Tidak Bisa Anda Edit

Bidang ini dihitung secara otomatis berdasarkan perilaku pelanggan:
- Total pengeluaran / nilai pelanggan
- Jumlah pesanan
- Segment pelanggan (Champion, Loyal, At Risk, dll.)
- Skor RFM
- Prediksi nilai seumur hidup
- Tanggal pesanan terakhir
- Ringkasan analitik

Jika bidang ini terlihat salah, periksa data pesanan mendasar atau picu perhitungan manual di **Pelanggan > Analitik** → **Hitung Ulang Metrik**.

## Catatan Pelanggan

Tambahkan catatan internal tentang pelanggan untuk melacak masalah dukungan, permintaan VIP, atau tugas follow-up.

### Menambahkan Catatan

1. Buka profil pelanggan
2. Gulir ke bagian **Catatan Pelanggan** (mungkin berupa tab terpisah)
3. Klik **+ Tambahkan Catatan**
4. Isi detail catatan:

| Bidang | Deskripsi |
|-------|-------------|
| **Jenis Catatan** | Umum, Masalah Dukungan, Keluhan, Pujian, Layanan VIP, Diperlukan Follow Up, Masalah Pembayaran, Masalah Pengiriman |
| **Judul** | Ringkasan singkat dari catatan |
| **Konten** | Konten catatan yang terperinci |
| **Memerlukan Follow Up** | Centang jika ini memerlukan tindakan |
| **Tanggal Follow Up** | Tanggal untuk follow up |
| **Selesai** | Centang ketika follow up selesai |

### Jenis Catatan

| Jenis | Kasus Penggunaan |
|------|----------|
| **Catatan Umum** | Setiap pengamatan umum tentang pelanggan |
| **Masalah Dukungan** | Catatan tiket dukungan atau masalah |
| **Keluhan** | Keluhan pelanggan untuk pelacakan dan penyelesaian |
| **Pujian** | Umpan balik positif tentang pelanggan atau umpan balik mereka tentang Anda |
| **Layanan VIP** | Permintaan penanganan khusus untuk pelanggan VIP |
| **Diperlukan Follow Up** | Tugas yang memerlukan tindakan pada tanggal tertentu |
| **Masalah Pembayaran** | Catatan tentang masalah pembayaran atau sengketa |
| **Masalah Pengiriman** | Catatan tentang masalah pengiriman atau permintaan pengiriman khusus |

### Melihat Riwayat Catatan

Semua catatan muncul dalam urutan kronologis di profil pelanggan. Setiap catatan menampilkan:
- Tanggal dan waktu pembuatan
- Dibuat oleh (nama anggota staf)
- Badge jenis catatan
- Judul dan konten
- Status follow up jika berlaku

### Catatan Internal vs Catatan yang Terlihat oleh Pelanggan

Semua catatan pelanggan adalah **hanya internal** secara default — pelanggan tidak pernah melihat catatan ini. Mereka hanya untuk komunikasi tim pedagang.

Jika Anda perlu berkomunikasi dengan pelanggan, gunakan sistem email di **Pemasaran > Kampanye Email** atau tambahkan komentar pesanan di pesanan spesifik.

## Mengubah Pelanggan Tamu Menjadi Pelanggan Terdaftar

Pelanggan tamu dibuat secara otomatis ketika seseorang menyelesaikan checkout tanpa membuat akun. Nama pengguna mereka mengikuti pola `guest_10374` di mana angka adalah ID unik.

Untuk mengubah tamu menjadi pelanggan terdaftar:

1. Navigasikan ke **Pelanggan > Semua Pelanggan**
2. Cari tamu berdasarkan alamat email pesanan mereka
3. Klik profil pelanggan tamu
4. Klik tautan **Pengguna** untuk mengedit akun User mendasari
5. Ubah **nama pengguna** dari `guest_10374` ke alamat email asli pelanggan
6. Ubah **email** agar sesuai
7. Secara opsional tambahkan **nama depan** dan **nama belakang**
8. Centang **Kirimkan email pengaturan ulang kata sandi** agar pelanggan dapat menetapkan kata sandi
9. Klik **Simpan**

Pelanggan sekarang dapat login dengan alamat email mereka dan akan melihat pesanan tamu mereka sebelumnya dalam riwayat pesanan mereka.

### Mengapa Mengubah Pelanggan Tamu?

- Pesanan tamu tidak dihitung dalam analitik atau segment pelanggan
- Tamu tidak dapat melacak pesanan atau mengakses riwayat pesanan
- Mengubah tamu meningkatkan jumlah pelanggan terdaftar dan meningkatkan akurasi analitik
- Pelanggan terdaftar lebih mungkin melakukan pembelian ulang

## Menonaktifkan vs Menghapus Akun

### Menonaktifkan Akun Pelanggan

Menonaktifkan mencegah login sambil mempertahankan semua data:

1. Buka profil pelanggan
2. Klik tautan **Pengguna** untuk mengedit akun User
3. **Hilangkan centang "Aktif"**
4. Klik **Simpan**

**Apa yang terjadi:**
- Pelanggan tidak dapat login
- Riwayat pesanan tetap ada
- Pelanggan dapat diaktifkan kembali nanti dengan mengecek "Aktif" kembali
- Analitik dan metrik tetap utuh

**Gunakan menonaktifkan untuk:**
- Menangguhkan akun sementara karena sengketa pembayaran
- Memblokir pelanggan yang berbahaya
- Pelanggan yang meminta untuk berhenti menerima akses tetapi tidak menghapus data

### Menghapus Akun Pelanggan

Menghapus menghilangkan akun dan dapat membuat riwayat pesanan terlepas:

1. Buka profil pelanggan
2. Gulir ke bawah dan klik **Hapus**
3. Konfirmasi penghapusan

**Apa yang terjadi:**
- Akun pelanggan dihapus secara permanen
- Profil pelanggan dihapus
- Riwayat pesanan mungkin menjadi terlepas (pesanan ada tetapi tidak terhubung ke pelanggan)
- Tidak dapat dibatalkan

**Gunakan penghapusan untuk:**
- Permintaan penghapusan data GDPR/CCPA (ekspor data terlebih dahulu)
- Akun uji yang seharusnya tidak pernah ada
- Akun duplikat yang dibuat secara tidak sengaja

### Kepatuhan GDPR

Sebelum menghapus akun pelanggan sebagai respons terhadap permintaan GDPR:

1. Navigasikan ke **Pelanggan > Semua Pelanggan**
2. Pilih pelanggan
3. Gunakan tindakan **Ekspor Data** untuk menghasilkan ekspor data lengkap
4. Kirimkan ekspor tersebut ke pelanggan jika mereka meminta
5. Lalu lanjutkan dengan penghapusan

Ekspor mencakup: profil pelanggan, riwayat pesanan, alamat, catatan, dan data analitik.

## Tips

- **Gunakan filter untuk mengidentifikasi pelanggan bernilai tinggi** — Saring berdasarkan Nilai Pelanggan untuk menemukan Champion dan VIP Anda
- **Periksa catatan pelanggan secara teratur** — Periksa tugas follow up terbuka setidaknya seminggu sekali
- **Jangan edit analitik secara manual** — Biarkan sistem menghitung skor RFM dan segment secara otomatis
- **Ubah tamu secara proaktif** — Setelah tamu membuat pembelian kedua, hubungi mereka dan tawarkan untuk membuat akun yang benar
- **Gunakan menonaktifkan alih-alih menghapus** — Menonaktifkan mempertahankan data dan dapat dibatalkan jika diperlukan
- **Tambahkan catatan selama panggilan dukungan** — Dokumentasikan interaksi dukungan agar anggota tim lain memiliki konteks
- **Atur tanggal follow up** — Gunakan sistem tugas follow up dalam catatan untuk memastikan tidak ada yang terlewat
- **Hormati preferensi komunikasi** — Jangan kirimkan email pemasaran ke pelanggan yang telah memilih untuk tidak menerima

