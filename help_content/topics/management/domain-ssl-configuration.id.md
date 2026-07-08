---
title: Konfigurasi Domain & SSL
---

Panduan ini menjelaskan cara menghubungkan domain kustom ke toko Spwig Anda dan mengatur sertifikat SSL untuk akses HTTPS yang aman. Anda dapat mengonfigurasi domain selama instalasi atau menambahkannya nanti.

## Menambahkan domain setelah instalasi

Jika Anda menginstal Spwig tanpa domain (menggunakan alamat IP server), Anda dapat menambahkannya kapan saja.

### Langkah 1: Atur DNS

Dengan registrar domain atau penyedia DNS Anda:

1. Buat **catatan A** yang mengarahkan domain (atau subdomain) Anda ke alamat IP server Anda
2. Jika menggunakan subdomain seperti `shop.example.com`, buat catatan A untuk `shop`
3. Tunggu propagasi DNS — ini biasanya memakan waktu 5–60 menit

Verifikasi catatan DNS berfungsi:

```bash
 dig +short shop.example.com
```

Ini harus mengembalikan alamat IP server Anda.

### Langkah 2: Jalankan skrip konfigurasi domain

SSH ke server Anda dan navigasikan ke direktori instalasi Spwig Anda:

```bash
 ./configure-domain.sh
```

Skrip ini akan:

1. Meminta nama domain Anda
2. Memverifikasi DNS mengarah ke server Anda
3. Memperbarui konfigurasi toko
4. Mendapatkan sertifikat SSL gratis dari Let's Encrypt
5. Mengatur server web untuk menggunakan HTTPS
6. Merestart layanan yang relevan

Toko Anda sekarang dapat diakses di `https://yourdomain.com`.

### Langkah 3: Perbarui pengaturan toko

Setelah menambahkan domain, masuk ke panel admin Anda dan pergi ke **Pengaturan Toko**. Verifikasi bahwa **URL Toko** cocok dengan domain baru Anda. Ini memastikan email, faktur, dan tautan menggunakan alamat yang benar.

## Sertifikat SSL

### SSL Otomatis (Let's Encrypt)

Dalam **mode standalone**, installer secara otomatis mendapatkan sertifikat SSL gratis dari Let's Encrypt. Sertifikat ini:

- Diperiksa oleh semua browser utama
- Berlaku selama 90 hari
- Diperbarui secara otomatis — pemeriksaan perbaruan berjalan setiap hari, dan sertifikat diperbarui ketika sisa waktunya kurang dari 30 hari
- Menutupi domain Anda secara tepat (misalnya `shop.example.com`)

Anda tidak perlu mengelola perbaruan secara manual.

### Sertifikat Tanda Tangan Sendiri

Dalam beberapa situasi, Spwig menggunakan sertifikat tanda tangan sendiri:

- **Mode lokal** (pengembangan/pengujian)
- Ketika Let's Encrypt tidak dapat mengakses server Anda (port 80 diblokir firewall, DNS belum menyebar)
- Ketika tidak ada domain yang dikonfigurasi (akses hanya melalui IP)

Sertifikat tanda tangan sendiri mengenkripsi lalu lintas tetapi tidak diakui oleh browser — pengunjung akan melihat peringatan keamanan. Ini diterima untuk pengujian tetapi tidak boleh digunakan dalam produksi.

### Mode SSL Sidecar

Dalam **mode sidecar**, server web yang ada (Apache, Nginx, Caddy, dll.) menangani penutupan SSL. Spwig berjalan di port HTTP di balik proxy Anda. Konfigurasikan SSL di server web utama Anda seperti biasanya.

Installer menghasilkan blok konfigurasi proxy yang dapat Anda tambahkan ke server web Anda. Untuk Nginx, tampilannya mirip dengan:

```nginx
 location / {
     proxy_pass http://127.0.0.1:8080;
     proxy_set_header Host $host;
     proxy_set_header X-Real-IP $remote_addr;
     proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
     proxy_set_header X-Forwarded-Proto $scheme;
 }
```

## Mengganti domain Anda

Untuk beralih ke domain yang berbeda:

1. Atur DNS untuk domain baru (catatan A yang mengarah ke server Anda)
2. Jalankan `./configure-domain.sh` kembali dengan domain baru
3. Skrip memperbarui semua konfigurasi, mendapatkan sertifikat baru, dan merestart layanan
4. Perbarui **Pengaturan Toko** di panel admin dengan URL baru

Domain lama Anda akan berhenti berfungsi setelah konfigurasi diperbarui.

## Penyelesaian Masalah

### "Validasi DNS gagal"

Skrip configure-domain memeriksa bahwa domain Anda mengarah ke server Anda sebelum meminta sertifikat. Jika pemeriksaan ini gagal:

- Verifikasi catatan A dengan `dig +short yourdomain.com`
- Tunggu beberapa menit lagi untuk propagasi DNS
- Periksa bahwa Anda mengonfigurasi domain atau subdomain yang tepat (bukan wildcard)

### "Batas rate Let's Encrypt tercapai"

Let's Encrypt membatasi permintaan sertifikat menjadi 5 per domain per minggu. Jika Anda mencapai batas ini:

Preserve all markdown formatting, image paths, code blocks, and technical terms.

- Tunggu 7 hari sebelum mencoba lagi
- Gunakan subdomain yang berbeda sementara waktu
- Toko tetap dapat diakses melalui HTTP atau dengan sertifikat self-signed selama Anda menunggu

### "Port 80 tidak dapat dijangkau"

Let's Encrypt harus terhubung ke server Anda pada port 80 untuk memverifikasi kepemilikan domain. Pastikan:

- Firewall Anda mengizinkan masuk TCP pada port 80
- Tidak ada aplikasi lain yang memblokir port 80
- Grup keamanan atau firewall jaringan penyedia cloud Anda mengizinkan port 80

### Gagal perbaruan sertifikat

Jika perbaruan otomatis gagal, sertifikat akan kedaluwarsa setelah 90 hari. Untuk memperbarui secara manual:

```bash
docker exec spwig_nginx certbot renew
docker exec spwig_nginx nginx -s reload
```

Periksa log perbaruan untuk detail jika ini gagal. Penyebab paling umum adalah port 80 diblokir oleh perubahan firewall setelah instalasi awal.