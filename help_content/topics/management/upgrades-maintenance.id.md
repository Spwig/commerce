---
title: Pembaruan & Pemeliharaan
---

Spwig menerima pembaruan rutin dengan fitur baru, peningkatan kinerja, dan perbaikan keamanan. Panduan ini mencakup cara memperbarui instalasi Anda, menggunakan alat diagnostik, dan menangani tugas pemeliharaan.

## Memperbarui Spwig

### Sebelum Anda memperbarui

1. **Buat cadangan** — pergi ke **Manajemen > Metrik Sistem > Buat Cadangan Penuh** atau jalankan skrip cadangan dari baris perintah. Ini adalah jaring pengaman Anda jika terjadi kesalahan.
2. **Periksa versi saat ini** — terlihat di **Manajemen > Metrik Sistem** atau di footer dashboard admin.
3. **Baca catatan rilis** — tersedia di panel admin di bawah **Manajemen > Pembaruan Komponen** ketika versi baru terdeteksi.

### Menjalankan pembaruan

SSH ke server Anda dan navigasikan ke direktori instalasi Spwig Anda (biasanya `/opt/spwig`):

```bash
./upgrade.sh
```

Skrip pembaruan:

1. **Pemeriksaan pra-penerbangan** — memverifikasi ruang disk, kesehatan Docker, dan status layanan
2. **Pemigrasian database dry-run** — menguji bahwa perubahan database akan diterapkan dengan bersih tanpa benar-benar mengubah apa pun
3. **Masuk ke mode pemeliharaan** — toko Anda menampilkan halaman pemeliharaan untuk pengunjung selama pembaruan
4. **Buat cadangan** — cadangan keamanan otomatis sebelum membuat perubahan
5. **Drain pekerja latar belakang** — menunggu tugas yang sedang berlangsung (pengiriman email, terjemahan) untuk selesai secara elegan
6. **Tarik gambar baru** — mengunduh aplikasi yang diperbarui dari registri Spwig
7. **Terapkan pemigrasian database** — memperbarui skema database Anda untuk versi baru
8. **Menghidupkan ulang layanan** — menghidupkan ulang aplikasi dengan versi baru
9. **Pemeriksaan kesehatan** — memverifikasi bahwa semua layanan berjalan dengan benar
10. **Keluar dari mode pemeliharaan** — toko Anda kembali online

Jika pemeriksaan kesehatan gagal setelah pembaruan, skrip **otomatis mengembalikan** ke versi sebelumnya dan memulihkan cadangan.

### Opsi pembaruan

```bash
./upgrade.sh              # Pembaruan standar dengan mode pemeliharaan
./upgrade.sh --dry-run    # Periksa apa yang akan berubah tanpa menerapkannya
```

## Alat diagnostik

Spwig menyertakan alat diagnostik bawaan yang memeriksa seluruh instalasi Anda untuk masalah:

```bash
./doctor.sh
```

Dokter memeriksa:

| Kategori | Apa yang diperiksa |
|----------|---------------|
| **Sistem** | Ruang disk, penggunaan RAM, beban CPU |
| **Docker** | Kesehatan mesin Docker, status kontainer, versi gambar |
| **Database** | Konektivitas PostgreSQL, status migrasi, kesehatan koneksi pool |
| **Cache** | Konektivitas Redis, penggunaan memori |
| **Penyimpanan objek** | Konektivitas MinIO, ketersediaan bucket |
| **Jaringan** | Resolusi DNS, ketersediaan port, validitas sertifikat SSL |
| **Aplikasi** | Titik akhir kesehatan layanan, status pekerja latar belakang |

Setiap pemeriksaan menampilkan hasil lulus/gagal dengan detail jika ada yang salah.

### Mode perbaikan otomatis

Untuk masalah umum, dokter dapat mencoba perbaikan otomatis:

```bash
./doctor.sh --fix
```

Perbaikan otomatis dapat menyelesaikan:

- Kontainer yang berhenti (menghidupkan ulang)
- Koneksi database yang usang (mengganti ulang koneksi pool)
- Sertifikat SSL yang kedaluwarsa (memicu perbaruan)
- Disk penuh dari gambar Docker lama (membersihkan gambar yang tidak digunakan)

Dokter selalu menjelaskan apa yang akan diperbaikinya sebelum mengambil tindakan.

## Mode pemeliharaan

Mode pemeliharaan menampilkan halaman "toko sementara tidak tersedia" kepada pengunjung saat Anda membuat perubahan. Panel admin Anda tetap dapat diakses.

### Mematikan mode pemeliharaan

Dari panel admin: **Pengaturan Toko > Pemeliharaan > Aktifkan Mode Pemeliharaan**

Atau dari baris perintah:

```bash
docker exec spwig_shop python manage.py maintenance on
```

### Mematikan mode pemeliharaan

Dari panel admin: ubah sakelar mode pemeliharaan menjadi off.

Atau dari baris perintah:

```bash
./go-live.sh
```

### Bypass akses selama pemeliharaan

Saat mode pemeliharaan aktif, Anda dapat mengakses toko secara normal dengan menambahkan parameter rahasia ke URL. Rahasia bypass ditampilkan di file konfigurasi `.env` Anda di bawah `MAINTENANCE_SECRET`.

## Mengelola layanan

### Melihat status layanan

Periksa status semua layanan Spwig:

```bash
docker compose ps
```

Ini menampilkan setiap layanan, statusnya (berjalan, berhenti, berulang), dan status kesehatannya.

### Melihat log

Periksa log untuk layanan tertentu:

```bash
docker logs spwig_shop          # Log aplikasi
docker logs spwig_celery         # Log pekerja latar belakang
docker logs spwig_nginx          # Log akses server web
docker logs spwig_db             # Log database
```

Tambahkan `--tail 100` untuk melihat 100 baris terakhir, atau `--follow` untuk memantau log secara real time.

### Merestart layanan

Jika layanan tertentu perlu direstart:

```bash
docker compose restart shop      # Merestart aplikasi
docker compose restart celery    # Merestart pekerja latar belakang
docker compose restart nginx     # Merestart server web
```

Untuk merestart semua layanan:

```bash
docker compose restart
```

## Pembaruan komponen

Spwig memiliki pasar komponen di mana Anda dapat menginstal tema, penyedia pembayaran, integrasi pengiriman, dan ekstensi lainnya. Komponen diperbarui secara independen dari platform inti.

Navigasikan ke **Manajemen > Pembaruan Komponen** untuk memeriksa pembaruan komponen yang tersedia. Pembaruan diunduh dan diterapkan secara otomatis saat Anda menyetujui.

## Tips

- **Lakukan pembaruan secara teratur** — tetap menggunakan versi terbaru memastikan Anda memiliki perbaikan keamanan dan akses ke fitur baru
- **Selalu lakukan cadangan terlebih dahulu** — meskipun skrip pembaruan membuat cadangan otomatis, memiliki cadangan sendiri memberikan perlindungan tambahan
- **Jalankan doctor setelah masalah terjadi** — jika toko Anda berperilaku tidak terduga, `./doctor.sh` adalah cara tercepat untuk mengidentifikasi masalah
- **Jadwalkan pembaruan saat jam sibuk rendah** — mode pemeliharaan secara singkat mengganggu akses pelanggan, jadi lakukan pembaruan saat jam sibuk rendah
- **Pastikan ruang disk tersedia** — pembaruan membutuhkan ruang sementara untuk gambar dan cadangan baru. Pertahankan setidaknya 5 GB ruang kosong.