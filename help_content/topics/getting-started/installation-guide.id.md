---
title: Panduan Instalasi
---

Panduan ini akan membimbing Anda melalui proses instalasi Spwig di server Anda sendiri. Seluruh proses ini otomatis — satu perintah menangani pengaturan Docker, pembuatan database, konfigurasi layanan, dan sertifikat SSL.

## Sebelum Anda memulai

Anda memerlukan:

- Server yang berjalan dengan **Ubuntu 22.04 atau 24.04** (Debian 12 juga didukung)
- **Akses root atau sudo** ke server
- Setidaknya **4 GB RAM** dan **20 GB ruang disk** (8 GB RAM disarankan)
- **Token lisensi** dari pembelian Spwig Anda (periksa bukti email Anda)
- Secara opsional, **nama domain** yang diarahkan ke alamat IP server Anda

> **Tips:** Anda dapat menginstal tanpa domain dan menambahkannya nanti menggunakan alat konfigurasi domain. Toko Anda akan dapat diakses melalui alamat IP server Anda sementara waktu.

## Menjalankan penginstal

Koneksikan ke server Anda melalui SSH dan jalankan perintah instalasi dari email konfirmasi pembelian Anda. Tampilannya seperti ini:

```bash
curl -fsSL https://spwig.com/install.sh | sudo bash -s -- --token YOUR_LICENSE_TOKEN
```

Ganti `YOUR_LICENSE_TOKEN` dengan token dari email Anda.

Penginstal menjalani delapan fase secara otomatis:

1. **Pemeriksaan pra-penerbangan** — memverifikasi server Anda memenuhi persyaratan (OS, disk, RAM, port)
2. **Validasi token** — memastikan lisensi Anda dan mengekstrak konfigurasi toko Anda
3. **Deteksi mode** — menentukan mode instalasi terbaik untuk server Anda (lihat di bawah)
4. **Konfigurasi** — menghasilkan kata sandi aman, kredensial database, dan konfigurasi layanan
5. **Unduh gambar** — menarik gambar aplikasi Spwig dari registri
6. **Pemulai layanan** — memulai database, cache, aplikasi, dan pekerja latar belakang secara berurutan
7. **Pengaturan SSL** — mendapatkan sertifikat SSL jika Anda memiliki domain yang dikonfigurasikan
8. **Penyelesaian** — membuat akun admin Anda dan menghasilkan skrip kepraktisan

Proses ini memakan waktu 5–15 menit tergantung pada kecepatan internet server Anda.

## Mode instalasi

Penginstal secara otomatis mendeteksi lingkungan server Anda dan memilih mode terbaik. Anda juga dapat menentukan satu secara manual dengan bendera `--mode`.

### Mode mandiri

**Terbaik untuk:** Server dedikasi dan instance VPS di mana Spwig adalah satu-satunya aplikasi web.

- Menggunakan port 80 dan 443 secara langsung
- Menangani sertifikat SSL secara otomatis melalui Let's Encrypt
- Ini adalah mode yang paling umum dan disarankan

### Mode sidecar

**Terbaik untuk:** Server yang sudah menjalankan aplikasi web lain (WordPress, situs perusahaan, dll.) di port 80/443.

- Spwig berjalan di port alternatif (dideteksi otomatis, biasanya 8080 atau 8443)
- Penginstal menghasilkan blok konfigurasi nginx untuk Anda tambahkan ke server web yang sudah ada
- Server web yang sudah ada menangani SSL dan memproksi lalu lintas ke Spwig

### Mode lokal

**Terbaik untuk:** Pengembangan dan pengujian di komputer Anda sendiri.

- Hanya dapat diakses di `localhost` atau `127.0.0.1`
- Menggunakan sertifikat SSL mandiri (browser Anda akan menampilkan peringatan keamanan — ini normal)
- Fitur debug diaktifkan
- Tidak diperlukan validasi lisensi

## Apa yang terjadi selama instalasi

### Docker

Jika Docker belum terinstal, penginstal menawarkan untuk menginstalnya untuk Anda. Spwig berjalan sepenuhnya di dalam kontainer Docker — tidak ada yang diinstal langsung di sistem operasi server Anda di luar Docker.

### Layanan yang dibuat

Penginstal menciptakan layanan berikut:

| Layanan | Tujuan |
|---------|---------|
| **Database** (PostgreSQL 16) | Menyimpan semua data toko Anda — produk, pesanan, pelanggan, pengaturan |
| **Cache** (Redis) | Mempercepat muat halaman dan mengelola antrian tugas latar belakang |
| **Connection pooler** (PgBouncer) | Mengelola koneksi database secara efisien |
| **Object storage** (MinIO) | Menyimpan gambar, file, dan media yang diunggah |
| **Application** (Spwig) | Toko itu sendiri — panel admin dan toko online |
| **Web server** (Nginx) | Menyajikan toko Anda kepada pengunjung dengan kompresi dan caching |
| **Background worker** (Celery) | Memproses email, terjemahan, analitik, dan tugas latar belakang lainnya |
| **Task scheduler** (Celery Beat) | Menjalankan tugas yang dijadwalkan seperti cadangan otomatis dan kampanye email |
| **Translator** | Layanan terjemahan berbasis AI untuk toko multibahasa |
| **Upgrader** | Menangani pembaruan komponen dari pasar Spwig |

### Akun admin

Di akhir instalasi, Anda diminta untuk membuat akun admin. Ini adalah akun yang akan Anda gunakan untuk masuk ke panel admin toko Anda.

### Mode pemeliharaan

Toko Anda dimulai dalam **mode pemeliharaan** — pengunjung melihat halaman "Coming Soon". Ini memberi Anda waktu untuk mengonfigurasi toko Anda (menambahkan produk, mengatur metode pembayaran, menyesuaikan tema) sebelum diluncurkan.

Ketika Anda siap, jalankan skrip kenyamanan yang dibuat oleh installer:

```bash
./go-live.sh
```

Atau nonaktifkan mode pemeliharaan dari **Admin > Store Settings > Maintenance**.

## Setelah instalasi

Setelah installer selesai, Anda akan melihat ringkasan dengan:

- URL toko Anda
- URL panel admin Anda (biasanya `https://yourdomain.com/en/admin/`)
- Lokasi file konfigurasi Anda
- Skrip kenyamanan yang tersedia

### Skrip kenyamanan

Installer membuat skrip ini di direktori instalasi Anda:

- **`./go-live.sh`** — mengeluarkan toko Anda dari mode pemeliharaan
- **`./configure-domain.sh`** — menambahkan atau mengubah domain Anda dan memperoleh sertifikat SSL

### Langkah selanjutnya

1. Masuk ke panel admin Anda
2. Lengkapi **Setup Wizard** — ini memandu Anda melalui nama toko, mata uang, zona waktu, dan pengaturan dasar
3. Tambahkan produk Anda
4. Konfigurasikan metode pembayaran
5. Pilih dan sesuaikan tema
6. Jalankan `./go-live.sh` ketika siap

## Menginstal di pasar awan

Spwig tersedia sebagai aplikasi satu klik di beberapa penyedia awan:

- **DigitalOcean** — sebarkan dari DigitalOcean Marketplace
- **Akamai (Linode)** — sebarkan dari Linode Marketplace
- **Vultr** — sebarkan dari Vultr Marketplace

Gambar pasar ini datang dengan installer yang sudah dipasang. Setelah membuat server, SSH masuk dan ikuti instruksi di layar untuk menyelesaikan pengaturan dengan token lisensi Anda.

## Mendapatkan bantuan

Jika instalasi gagal atau Anda mengalami kesalahan:

1. Jalankan **alat diagnostik**: `./doctor.sh` (dibuat selama instalasi)
2. Dokter memeriksa semua layanan, koneksi, SSL, dan masalah umum
3. Gunakan `./doctor.sh --fix` untuk mencoba perbaikan otomatis
4. Hubungi dukungan Spwig dengan output dokter jika masalahnya masih berlanjut