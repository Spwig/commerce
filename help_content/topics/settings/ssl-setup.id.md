---
title: Pengaturan SSL
---

SSL (Secure Sockets Layer) mengenkripsi koneksi antara browser pelanggan Anda dan toko Anda. Ketika SSL aktif, URL toko Anda dimulai dengan `https://` dan browser menampilkan ikon kunci. SSL sangat penting untuk menerima pembayaran, melindungi data pelanggan, dan memperbaiki peringkat di mesin pencari.

Spwig mendukung beberapa mode SSL untuk cocok dengan berbagai konfigurasi hosting. Panduan ini menjelaskan setiap mode dan membantu Anda memilih yang tepat.

## Memilih Mode SSL

| Mode | Terbaik untuk | Biaya Sertifikat | Perbaruan |
|------|----------|-----------------|---------|
| **Let's Encrypt** | Kebanyakan toko | Gratis | Otomatis |
| **Cloudflare Origin CA** | Toko yang menggunakan proxy Cloudflare | Gratis | Manual (sampai 15 tahun) |
| **Sertifikat Kustom** | Toko dengan sertifikat yang dibeli | Beragam | Manual |
| **Dikelola Secara Eksternal** | Load balancer, Cloudflare Flexible | N/A | N/A |
| **Sertifikat Mandiri** | Pengembangan dan pengujian | Gratis | Manual |
| **Tidak Ada (HTTP)** | Pengembangan lokal saja | N/A | N/A |

Jika Anda tidak yakin mode mana yang harus digunakan, **Let's Encrypt** adalah pilihan terbaik untuk kebanyakan toko. Ini gratis, otomatis, dan dipercayai oleh semua browser.

## Let's Encrypt

Let's Encrypt menyediakan sertifikat SSL gratis yang diperbarui secara otomatis setiap 60-90 hari. Ini adalah pilihan yang disarankan untuk kebanyakan pedagang.

**Persyaratan:**
- Domain Anda harus menunjuk ke server Anda (catatan A di DNS)
- Port 80 harus dapat diakses dari internet (untuk verifikasi sertifikat)
- Alamat email untuk notifikasi kedaluwarsa sertifikat

**Langkah pengaturan:**
1. Buka **Pengaturan > Pengaturan Situs** dan buka tab **Domain & SSL**
2. Masukkan nama domain Anda
3. Pilih **Let's Encrypt**
4. Masukkan alamat email admin Anda
5. Klik **Terapkan Konfigurasi**

Spwig menangani semuanya secara otomatis: memverifikasi domain Anda, mendapatkan sertifikat, mengonfigurasi NGINX, dan mengatur perbaruan otomatis.

## Cloudflare Origin CA

Sertifikat Cloudflare Origin CA mengenkripsi koneksi antara server edge Cloudflare dan toko Anda. Sertifikat ini gratis dan dapat bertahan hingga 15 tahun, tetapi hanya **dipercayai oleh Cloudflare** -- browser yang terhubung langsung ke server Anda akan melihat peringatan sertifikat.

Mode ini ideal jika Anda menggunakan Cloudflare sebagai proxy (cloud oranye aktif) untuk domain Anda. Cloudflare menampilkan sertifikat yang dipercayai oleh sendiri kepada pengunjung, dan sertifikat Origin CA mengamankan koneksi antara Cloudflare dan server Anda.

**Persyaratan:**
- Akun Cloudflare dengan domain Anda yang ditambahkan
- Sertifikat Origin CA dan kunci pribadi yang dihasilkan dari dashboard Cloudflare
- Mode SSL/TLS Cloudflare diatur ke **Full (Strict)**

**Menghasilkan sertifikat Origin CA:**
1. Masuk ke dashboard Cloudflare Anda
2. Pilih domain Anda
3. Buka **SSL/TLS > Origin Server**
4. Klik **Buat Sertifikat**
5. Pilih RSA atau ECC (RSA paling kompatibel)
6. Tambahkan domain Anda (misalnya, `example.com` dan `*.example.com`)
7. Pilih periode validitas (15 tahun disarankan)
8. Klik **Buat** dan salin sertifikat dan kunci pribadi

**Mengatur di Spwig:**
1. Buka **Pengaturan > Pengaturan Situs** dan buka tab **Domain & SSL**
2. Masukkan nama domain Anda
3. Pilih **Cloudflare Origin CA**
4. Tempel sertifikat ke bidang **Sertifikat (PEM)**
5. Tempel kunci pribadi ke bidang **Kunci Pribadi (PEM)**
6. Klik **Terapkan Konfigurasi**

**Setelah konfigurasi:**
- Di Cloudflare, atur mode SSL/TLS ke **Full (Strict)**
- Aktifkan proxy Cloudflare (cloud oranye) untuk catatan DNS domain Anda
- Toko Anda akan dapat diakses melalui HTTPS dengan sertifikat yang dipercayai oleh Cloudflare

## Sertifikat Kustom

Gunakan mode ini jika Anda memiliki sertifikat SSL yang dibeli dari otoritas sertifikat (CA) seperti DigiCert, Sectigo, atau GoDaddy, atau jika penyedia hosting Anda telah mengeluarkannya untuk Anda.

**Langkah pengaturan:**
1.

Buka **Pengaturan > Pengaturan Situs** dan buka tab **Domain & SSL**
2.

Masukkan nama domain Anda
3.

Pilih **Sertifikat Kustom**
4.

Jaga semua format markdown, jalur gambar, blok kode, dan istilah teknis tetap utuh.

Tempel sertifikat lengkap Anda (termasuk sertifikat antara) ke dalam bidang **Certificate (PEM)**
5.

Tempel kunci pribadi Anda ke dalam bidang **Private Key (PEM)**
6.

Klik **Apply Configuration**

Sertifikat Anda harus mencakup seluruh rantai: sertifikat domain Anda diikuti oleh sertifikat antara apa pun. Kunci pribadi harus dalam format PEM (dimulai dengan `-----BEGIN PRIVATE KEY-----` atau `-----BEGIN RSA PRIVATE KEY-----`).

## Managed Externally

Pilih mode ini ketika SSL ditutup oleh layanan eksternal sebelum lalu lintas mencapai server Anda. Dalam konfigurasi ini, server Anda hanya menerima lalu lintas HTTP biasa -- tidak ada sertifikat yang diinstal di server itu sendiri.

**Skenario umum:**
- **Cloudflare Flexible SSL** -- Cloudflare mengenkripsi lalu lintas browser ke Cloudflare, tetapi mengirim HTTP ke server Anda
- **Load balancer awan** -- AWS ALB, Google Cloud Load Balancer, atau DigitalOcean Load Balancer menutup SSL dan meneruskan HTTP
- **Reverse proxy** -- Server lain di depan Spwig menangani SSL

**Langkah pengaturan:**
1. Buka **Settings > Site Settings** dan buka tab **Domain & SSL**
2. Masukkan nama domain Anda
3. Pilih **Managed Externally**
4. Klik **Apply Configuration**

Spwig akan mengonfigurasi NGINX untuk hanya menyajikan HTTP dan mempercayai header `X-Forwarded-Proto` dari proxy Anda untuk mendeteksi pengunjung HTTPS dengan benar.

## Self-Signed Certificate

Sertifikat self-signed mengenkripsi koneksi tetapi tidak diakui oleh browser. Pengunjung akan melihat peringatan keamanan yang harus mereka lewati secara manual. Mode ini hanya cocok untuk server pengembangan dan pengujian internal.

**Langkah pengaturan:**
1. Buka **Settings > Site Settings** dan buka tab **Domain & SSL**
2. Masukkan nama domain Anda
3. Pilih **Self-Signed**
4. Klik **Apply Configuration**

Spwig akan menghasilkan sertifikat self-signed secara otomatis. Jangan gunakan mode ini untuk toko produksi.

## Troubleshooting

**Sertifikat tidak berfungsi setelah konfigurasi:**
- Periksa bahwa catatan A domain Anda mengarah ke alamat IP server Anda
- Pastikan port 80 dan 443 terbuka di firewall Anda
- Tunggu beberapa menit agar perubahan DNS menyebar

**Let's Encrypt gagal menerbitkan sertifikat:**
- Periksa bahwa domain Anda menyelesaikan ke alamat IP server ini
- Pastikan port 80 tidak diblokir oleh firewall
- Jika Anda berada di balik Cloudflare, atur sementara DNS ke "DNS only" (awan abu-abu) selama penerbitan sertifikat

**Cloudflare menampilkan "Error 526" (Sertifikat SSL Tidak Valid):**
- Pastikan Anda memilih mode **Cloudflare Origin CA** (bukan Managed Externally)
- Periksa bahwa mode SSL/TLS Cloudflare Anda diatur ke **Full (Strict)**
- Pastikan sertifikat Origin CA tidak sudah kedaluwarsa

**Browser menampilkan "Not Secure" meskipun memiliki SSL:**
- Beberapa halaman mungkin memuat gambar atau skrip melalui HTTP (konten campuran). Periksa konsol pengembang browser Anda untuk peringatan konten campuran.
- Pastikan URL situs Anda di Settings menggunakan `https://`