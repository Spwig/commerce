---
title: Pengaturan CDN
---

A Content Delivery Network (CDN) menyimpan salinan gambar, stylesheet, dan skrip toko Anda di server di seluruh dunia. Ketika seorang pelanggan mengunjungi toko Anda, file-file ini disajikan dari server terdekat dengan mereka, bukan dari server hosting utama Anda. Hal ini mengurangi waktu muat halaman, terutama untuk pelanggan yang berada jauh dari tempat toko Anda berada.

Spwig sudah mengoptimalkan pengiriman aset statis secara bawaan dengan kompresi pra Brotli dan gzip, penyimpanan cache aset dengan header tidak tergantikan selama 1 tahun, dan negosiasi konten yang tepat. Menambahkan CDN bersifat opsional, tetapi dapat meningkatkan kecepatan lebih lanjut untuk toko dengan basis pelanggan internasional.

## Apakah Toko Anda Membutuhkan CDN?

Tidak setiap toko mendapatkan manfaat yang sama dari CDN. Gunakan panduan ini untuk memutuskan:

**CDN disarankan jika**:
- Pelanggan Anda tersebar di beberapa negara atau benua
- Toko Anda memiliki banyak gambar produk atau halaman berat media
- Anda ingin waktu muat halaman yang tercepat secara global
- Anda menjual ke wilayah yang jauh dari server hosting Anda (misalnya, server di Eropa, pelanggan di Asia)

**CDN kemungkinan tidak diperlukan jika**:
- Pelanggan Anda sebagian besar lokal atau berada di negara yang sama dengan server Anda
- Toko Anda memiliki katalog kecil dengan sedikit gambar
- Penyedia hosting Anda sudah menyertakan CDN bawaan

Ketika ragu, CDN tidak akan merusak kinerja. Layanan seperti Cloudflare menawarkan tingkat gratis, jadi tidak ada biaya untuk mencoba.

## Cara Spwig Bekerja dengan CDN

Spwig sudah siap CDN secara default. Anda tidak perlu mengubah kode atau pengaturan apa pun di panel admin Spwig Anda. Berikut adalah hal-hal yang sudah Spwig lakukan untuk Anda:

- **File statis dengan fingerprint** -- Setiap file CSS, JavaScript, dan gambar memiliki hash versi unik dalam nama file-nya. Ini berarti CDN dapat dengan aman menyimpan file-file ini selama waktu yang lama tanpa menyajikan konten yang usang.
- **Header cache yang bertahan lama** -- Aset statis disajikan dengan header cache tidak tergantikan selama 1 tahun, memberi tahu CDN dan browser untuk menyimpannya secara agresif.
- **File yang dikompresi sebelumnya** -- Spwig mengkompresi aset menggunakan Brotli dan gzip, sehingga CDN Anda dapat mengirimkan file yang lebih kecil tanpa proses tambahan.
- **Negosiasi konten yang tepat** -- Spwig mengirimkan header tipe konten dan enkripsi yang benar yang bergantung pada CDN untuk penyimpanan cache yang tepat.

Yang Anda butuhkan hanyalah mengarahkan DNS domain Anda ke penyedia CDN, dan semuanya berfungsi secara otomatis.

## Mengatur Cloudflare

Cloudflare adalah CDN paling populer dan menawarkan tingkat gratis yang bekerja dengan baik untuk sebagian besar toko. Ikuti langkah-langkah berikut:

**Langkah 1: Membuat Akun Cloudflare**
- Kunjungi cloudflare.com dan daftarkan akun gratis

**Langkah 2: Tambahkan Domain Anda**
- Klik **Tambahkan Situs** dan masukkan nama domain toko Anda
- Pilih rencana **Gratis** (cukup untuk sebagian besar toko)

**Langkah 3: Perbarui Nameserver DNS**
- Cloudflare akan menampilkan dua nameserver (misalnya, `anna.ns.cloudflare.com`)
- Masuk ke penyedia domain Anda (tempat Anda membeli domain Anda)
- Ganti nameserver saat ini dengan nameserver Cloudflare
- Perubahan DNS dapat memakan waktu hingga 24 jam untuk berlaku

**Langkah 4: Mengatur SSL/TLS**
- Di dashboard Cloudflare, pergi ke **SSL/TLS**
- Atur mode enkripsi menjadi **Full (strict)**
- Ini memastikan semua lalu lintas antara Cloudflare dan server Anda tetap terenkripsi

**Langkah 5: Memverifikasi Apakah Berfungsi**
- Setelah DNS menyebar, kunjungi toko Anda dan periksa header `cf-cache-status` di browser Anda (lihat Memverifikasi CDN Anda di bawah)

## Mengatur AWS CloudFront

Jika Anda sudah menggunakan Amazon Web Services, CloudFront terintegrasi secara alami dengan infrastruktur Anda:

1. Buka konsol **CloudFront** di akun AWS Anda
2. Buat **Distribusi** baru dengan domain toko Anda sebagai asal
3. Atur **Kebijakan Protokol Asal** menjadi "HTTPS Only"
4. Di bawah **Perilaku Cache**, atur **Kebijakan Cache** menjadi "CachingOptimized" untuk aset statis
5. Tambahkan domain toko Anda sebagai **Nama Domain Alternatif (CNAME)**
6. Lampirkan sertifikat SSL dari AWS Certificate Manager
7. Perbarui DNS domain Anda untuk mengarahkan ke URL distribusi CloudFront



Harga CloudFront berbasis penggunaan.

Untuk sebagian besar toko, biayanya minimal karena aset yang difingerprint oleh Spwig dikach untuk periode yang lama.

## Pengaturan CDN yang Direkomendasikan

Untuk hasil terbaik, konfigurasikan CDN Anda untuk meng-cache konten yang tepat dan melewatkan konten lainnya.

**Apa yang perlu dikach** (aset statis):
- `/static/` -- Semua stylesheet, skrip, font, dan aset tema
- `/media/` -- Gambar produk dan file media yang diunggah
- File gambar (`.jpg`, `.png`, `.webp`, `.svg`, `.gif`)
- File font (`.woff`, `.woff2`)

**Apa yang TIDAK perlu dikach** (halaman dinamis):
- `/admin/` -- Panel admin harus selalu menyajikan konten yang segar
- `/cart/` -- Halaman keranjang belanja berisi data sesi spesifik
- `/checkout/` -- Halaman checkout tidak boleh pernah dikach untuk keamanan
- `/accounts/` -- Halaman akun pelanggan berisi data pribadi
- Halaman apa pun yang memerlukan login atau menampilkan konten pribadi

**Aturan kaching umum**:
- **Hormati header cache asal** -- Spwig mengirimkan header cache-control yang benar untuk setiap jenis konten. Konfigurasikan CDN Anda untuk menghormati header-header ini, bukan menggantinya.
- **Aktifkan kompresi Brotli** -- Baik Cloudflare maupun CloudFront mendukung Brotli. Aktifkan untuk memanfaatkan aset yang sudah dikompresi oleh Spwig.
- **Atur TTL Cache Browser menjadi "Hormati Header yang Ada"** -- Ini memungkinkan kebijakan cache bawaan Spwig menggerakkan perilaku.

## Memverifikasi CDN Anda

Setelah pengaturan, konfirmasikan bahwa CDN menyajikan konten Anda dengan benar:

**Langkah 1: Buka Alat Pengembang Browser**
- Di Chrome atau Firefox, tekan **F12** untuk membuka alat pengembang
- Klik tab **Jaringan**

**Langkah 2: Muat Toko Anda**
- Kunjungi halaman utama toko Anda dengan alat pengembang terbuka
- Klik pada permintaan file statis apa pun (misalnya, file `.css` atau `.js`)

**Langkah 3: Periksa Header Respons**
- **Cloudflare**: Cari header `cf-cache-status`. Nilai `HIT` berarti file disajikan dari cache CDN. `MISS` berarti file diambil dari server Anda (hanya permintaan pertama).
- **CloudFront**: Cari header `x-cache`. Nilai `Hit from cloudfront` mengonfirmasi pengiriman melalui CDN.

**Langkah 4: Uji dari Lokasi Lain**
- Gunakan alat gratis seperti gtmetrix.com atau webpagetest.org untuk menguji toko Anda dari lokasi geografis berbeda
- Bandingkan waktu muat sebelum dan sesudah pengaturan CDN

## Masalah Umum

### Konten Ketinggalan Setelah Perubahan Tema

**Masalah**: Setelah memperbarui tema atau membuat perubahan desain, pelanggan masih melihat versi lama.

**Solusi**: Bersihkan cache CDN Anda. Di Cloudflare, pergi ke **Caching > Configuration > Purge Everything**. Di CloudFront, buat **Invalidation** untuk `/*`. Catatan bahwa aset yang difingerprint oleh Spwig biasanya mencegah masalah ini karena file yang diperbarui mendapatkan nama file baru secara otomatis. Masalah ini paling umum memengaruhi aset yang tidak difingerprint seperti unggahan kustom.

---

### Peringatan Konten Tercampur

**Masalah**: Browser Anda menampilkan peringatan keamanan tentang "konten tercampur" setelah mengaktifkan CDN.

**Solusi**: Pastikan mode SSL CDN Anda diatur ke **Full (strict)**, bukan "Flexible". Mode Flexible dapat menyebabkan server Anda menerima permintaan HTTP alih-alih HTTPS, yang menyebabkan peringatan konten tercampur. Di Cloudflare, periksa **SSL/TLS > Overview** dan verifikasi mode.

---

### Panel Admin Berjalan Lambat

**Masalah**: Panel admin terasa lebih lambat setelah menambahkan CDN.

**Solusi**: CDN tidak boleh meng-cache halaman admin. Buat **Page Rule** (Cloudflare) atau **Cache Behavior** (CloudFront) yang mengatur caching menjadi "Bypass" untuk URL apa pun yang cocok dengan `/admin/*`. Ini memastikan permintaan admin langsung pergi ke server Anda tanpa beban overhead CDN.

---

### Gambar Tidak Memuat

**Masalah**: Gambar produk atau file media mengembalikan kesalahan setelah pengaturan CDN.

**Solusi**: Verifikasi bahwa origin CDN Anda dikonfigurasikan dengan protokol yang benar (HTTPS) dan port. Juga periksa bahwa firewall server Anda memungkinkan koneksi dari rentang IP CDN.

## Tips

Jaga semua format markdown, jalur gambar, blok kode, dan istilah teknis.

- **Mulai dengan tier gratis Cloudflare** -- Ini mencakup kebutuhan kebanyakan toko dan hanya memakan waktu beberapa menit untuk diatur
- **Selalu gunakan mode SSL penuh (strict)** -- Mode fleksibel menciptakan kerentanan keamanan dan dapat mengganggu alur checkout
- **Bersihkan cache CDN Anda setelah pembaruan tema besar** -- Meskipun file yang diberi tanda jari oleh Spwig menangani sebagian besar kasus, pengosongan cache penuh memastikan tidak ada konten yang usang tersisa
- **Jangan cache halaman checkout atau keranjang belanja** -- Mengcache halaman-halaman ini dapat mengungkap data satu pelanggan ke pelanggan lain
- **Uji dari lokasi pelanggan Anda** -- Gunakan alat gratis seperti webpagetest.org untuk mengukur kinerja dunia nyata dari wilayah di mana pelanggan Anda berbelanja
- **Pantau analitik CDN Anda** -- Baik Cloudflare maupun CloudFront menyediakan dashboard yang menampilkan tingkat cache hit, bandwidth yang dihemat, dan lalu lintas berdasarkan negara
- **Jaga TTL DNS Anda rendah selama proses pengaturan** -- Atur TTL DNS menjadi 300 detik (5 menit) saat beralih ke CDN, lalu tingkatkan setelah semuanya dikonfirmasi berfungsi dengan baik
- **CDN tidak menggantikan hosting yang baik** -- Server asal Anda tetap penting untuk halaman dinamis seperti checkout, keranjang, dan admin.

Pilih hosting berkualitas bersama dengan CDN