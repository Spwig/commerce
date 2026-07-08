---
title: Persyaratan Sistem
---

Spwig berjalan pada sebagian besar server Linux modern. Halaman ini mencakup spesifikasi minimum dan disarankan, apa yang terjadi pada server yang lebih kecil, dan penyedia cloud mana yang bekerja dengan baik.

## Persyaratan minimum

| Sumber daya | Minimum | Disarankan |
|----------|---------|-------------|
| **Sistem operasi** | Ubuntu 22.04 LTS, Ubuntu 24.04 LTS, atau Debian 12 | Ubuntu 24.04 LTS |
| **RAM** | 4 GB | 8 GB atau lebih |
| **Ruangan disk** | 20 GB | 40 GB atau lebih |
| **CPU** | 1 vCPU | 2+ vCPUs |
| **Arsitektur** | x86_64 (AMD64) | x86_64 |
| **Jaringan** | Alamat IP publik (untuk mode standalone) | Alamat IP publik statis |
| **Port** | 80 dan 443 (standalone) atau port alternatif apa pun (sidecar) | 80 dan 443 |

> **Catatan:** Server berbasis ARM (misalnya AWS Graviton, Oracle Ampere) saat ini tidak didukung.

## Tingkatan sumber daya

Pemasang otomatis mendeteksi RAM yang tersedia di server Anda dan memilih tingkatan sumber daya yang sesuai.

### Tingkatan standar (RAM 6 GB+):

Semua layanan berjalan dengan kemampuan penuh:

- Layanan **terjemahan berbasis AI** diaktifkan — terjemahkan deskripsi produk, konten halaman, dan teks SEO ke beberapa bahasa langsung dari panel admin Anda
- Alokasi memori penuh untuk aplikasi, database, dan pekerja latar belakang
- Konkurensi pekerja latar belakang dioptimalkan untuk jumlah CPU Anda

### Tingkatan kecil (RAM 4–6 GB):

Pemasang beradaptasi untuk menghemat memori:

- Layanan terjemahan AI **dinonaktifkan** untuk menghemat sekitar 2 GB RAM. Anda masih dapat mengelola terjemahan secara manual atau menggunakan alat terjemahan eksternal — hanya terjemahan AI bawaan yang terpengaruh.
- Batas memori aplikasi dan pekerja dikurangi
- Semua fitur lain berfungsi secara identik dengan tingkatan standar

> **Tips:** Jika Anda mulai dengan server kecil dan kemudian meningkatkan ke RAM 6 GB+, jalankan kembali pemasang untuk mengaktifkan layanan terjemahan.

## Penyedia cloud yang disarankan

Spwig berjalan pada server Linux apa pun yang memenuhi persyaratan. Penyedia berikut telah diuji dan menawarkan nilai yang baik:

| Penyedia | Rencana yang disarankan | RAM | Disk | Biaya perkiraan |
|----------|-----------------|-----|------|-----------------|
| **DigitalOcean** | Droplet Dasar | 4 GB | 80 GB | $24/bulan |
| **Linode (Akamai)** | Shared 4 GB | 4 GB | 80 GB | $24/bulan |
| **Vultr** | Cloud Compute | 4 GB | 100 GB | $24/bulan |
| **Hetzner** | CX31 | 8 GB | 80 GB | €8/bulan |
| **OVH** | VPS Starter | 4 GB | 80 GB | €7/bulan |

Untuk toko yang memprediksi lalu lintas yang signifikan atau katalog produk besar (10.000+ produk), mulailah dengan 8 GB RAM dan 2+ vCPUs.

## Penggunaan ruang disk

Instalasi Spwig baru menggunakan sekitar 8 GB ruang disk:

| Komponen | Ukuran |
|-----------|------|
| Gambar Docker | ~4 GB |
| Database (toko kosong) | ~200 MB |
| Model terjemahan AI (jika diaktifkan) | ~2 GB |
| File aplikasi dan konfigurasi | ~500 MB |
| Sistem operasi dan mesin Docker | ~3 GB |

Rencanakan ruang tambahan untuk:

- **Gambar produk dan media** — tergantung pada ukuran katalog Anda. Anggarkan 1–5 GB untuk toko biasa dengan ratusan produk.
- **Pertumbuhan database** — tumbuh bersama pesanan, pelanggan, dan data analitik. Toko yang memproses 100 pesanan per hari biasanya tumbuh sekitar ~1 GB per tahun.
- **Cadangan** — jika menyimpan cadangan secara lokal, setiap cadangan penuh sekitar ukuran database Anda ditambah media. Dengan kebijakan retensi 30 hari, anggarkan 2–3× ukuran data saat ini Anda.

## Domain dan DNS

Nama domain bersifat opsional saat instalasi tetapi diperlukan untuk penggunaan produksi. Anda memerlukan:

- Nama domain atau subdomain (misalnya `shop.example.com`)
- **Catatan A** yang mengarah ke alamat IP publik server Anda
- Propagasi DNS selesai (biasanya 5–60 menit setelah menambahkan catatan)

Pemasang secara otomatis mendapatkan sertifikat SSL gratis dari Let's Encrypt ketika domain yang valid terdeteksi. Anda juga dapat menambahkan domain setelah instalasi menggunakan skrip `./configure-domain.sh`.

## Firewall

Jika server Anda memiliki firewall (sebagian besar penyedia cloud mengaktifkan satu secara default), pastikan port berikut terbuka:

| Port | Protocol | Purpose |
|------|----------|---------|
| **22** | TCP | Akses SSH (untuk Anda mengelola server) |
| **80** | TCP | HTTP (diperlukan untuk validasi sertifikat Let's Encrypt) |
| **443** | TCP | HTTPS (lalu lintas aman toko Anda) |

Dalam mode sidecar, buka port alternatif yang ditugaskan oleh installer, bukan 80/443.

## Prasyarat perangkat lunak

Installer menangani pemasangan perangkat lunak secara otomatis. Sebagai referensi, ini adalah komponen yang diinstal atau diverifikasi:

- **Docker Engine** — runtime kontainer (diinstal secara otomatis jika tidak ada)
- **Docker Compose** — orkestrasi layanan (termasuk dengan Docker Engine)
- **curl** — digunakan oleh installer itu sendiri (hadir hampir di semua sistem Linux)

Tidak ada perangkat lunak lain yang perlu dipasang sebelumnya. Spwig tidak memerlukan Anda untuk memasang Python, Node.js, PostgreSQL, Redis, atau Nginx secara manual — semuanya berjalan di dalam kontainer Docker.