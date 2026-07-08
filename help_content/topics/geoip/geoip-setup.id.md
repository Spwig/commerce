---
title: Pengaturan GeoIP
---

GeoIP memungkinkan toko Anda secara otomatis mendeteksi dari mana setiap pengunjung berasal berdasarkan alamat IP mereka. Ini memungkinkan fitur berbasis lokasi di seluruh toko Anda — dari menampilkan mata uang yang benar secara default, hingga menjalankan aturan bisnis berbasis geografis, hingga melihat pemecahan masalah berdasarkan negara dalam analitik Anda.

Toko Anda sudah dikonfigurasi dengan layanan GeoIP Spwig, sehingga deteksi geografis bekerja secara langsung. Anda juga dapat menghubungkan penyedia tambahan untuk akurasi yang lebih tinggi, menggunakan database yang Anda unduh sendiri, atau mengandalkan header dari CDN untuk pencarian tanpa latensi.

## Cara penyedia bekerja

Navigasikan ke **Pelanggan > Penyedia GeoIP** untuk melihat penyedia yang dikonfigurasikan untuk toko Anda. Setiap penyedia menangani pencarian IP ke lokasi menggunakan metode yang berbeda. Ketika seorang pengunjung tiba, toko Anda meminta penyedia aktif dalam urutan prioritas dan menggunakan hasil yang berhasil pertama.

Banyak penyedia dapat aktif sekaligus — penyedia dengan angka prioritas yang lebih rendah dicoba terlebih dahulu. Jika penyedia dengan prioritas tertinggi gagal atau mengembalikan tidak ada data, penyedia berikutnya dicoba secara otomatis.

### Jenis penyedia yang tersedia

| Penyedia | Deskripsi |
|----------|-------------|
| **Spwig GeoIP** | Pencarian berbasis awan default melalui layanan Spwig. Tidak memerlukan pengaturan apa pun. |
| **MaxMind GeoLite2** | Database offline dari MaxMind. Akurasi tinggi. Memerlukan kunci lisensi gratis. |
| **DB-IP Lite** | Database offline dari DB-IP. Unduh dari situs web mereka. |
| **IP2Location LITE** | Database offline dari IP2Location. Memerlukan pendaftaran gratis. |
| **CDN Edge Headers** | Membaca header lokasi yang disisipkan oleh CDN Anda (misalnya, Cloudflare). Tanpa latensi. |
| **Browser Hints** | Menggunakan zona waktu/bahasa yang diberikan oleh browser sebagai sinyal lokasi yang lembut. |
| **Penyedia Kustom** | Komponen penyedia yang diinstal dari pasar komponen Spwig. |

## Menambahkan penyedia

### Menggunakan layanan GeoIP Spwig (default)

Penyedia GeoIP Spwig ditambahkan secara otomatis pada instalasi baru. Pastikan bahwa penyedia tersebut muncul dalam daftar dan bahwa **Aktif** dicentang. Tidak diperlukan konfigurasi tambahan.

### Menambahkan database MaxMind GeoLite2

MaxMind menawarkan database offline gratis yang memberikan hasil akurat tanpa mengirimkan pencarian ke layanan eksternal.

1. Daftarkan akun gratis di maxmind.com dan buat kunci lisensi
2. Navigasikan ke **Pelanggan > Penyedia GeoIP** dan klik **+ Tambah Penyedia GeoIP**
3. Isi formulir:
   - **Nama**: `MaxMind GeoLite2` (atau nama deskriptif apa pun)
   - **Jenis Penyedia**: MaxMind GeoLite2
   - **Aktif**: dicentang
   - **Prioritas**: `1` (lebih rendah dari default Spwig untuk mencoba terlebih dahulu, atau lebih tinggi untuk digunakan sebagai cadangan)
   - **Kunci Lisensi**: tempelkan kunci lisensi MaxMind Anda
   - **URL Database**: URL unduhan dari dashboard akun MaxMind Anda
4. Klik **Simpan**

Setelah disimpan, pilih penyedia dalam daftar dan gunakan tindakan **Perbarui database penyedia yang dipilih** untuk memverifikasi bahwa URL database dapat diakses.

### Menambahkan header edge CDN

Jika toko Anda berada di balik CDN yang menyisipkan header geolokasi (seperti `CF-IPCountry` dari Cloudflare), Anda dapat menggunakan header tersebut untuk deteksi negara instan tanpa latensi.

1. Navigasikan ke **Pelanggan > Penyedia GeoIP** dan klik **+ Tambah Penyedia GeoIP**
2. Atur **Jenis Penyedia** menjadi **CDN Edge Headers**
3. Atur **Prioritas** menjadi `0` (prioritas tertinggi, karena header adalah sumber tercepat)
4. Dalam bidang **Konfigurasi**, tentukan header mana yang digunakan oleh CDN Anda:
   ```json
   {
     "header_name": "CF-IPCountry"
   }
   ```
5. Klik **Simpan**

## Menguji penyedia

Setelah menambahkan penyedia, Anda dapat memverifikasi bahwa penyedia tersebut berfungsi dengan benar:

1. Dalam daftar Penyedia GeoIP, pilih penyedia menggunakan kotak centangnya
2. Buka dropdown **Tindakan** dan pilih **Uji penyedia yang dipilih**
3. Klik **Lanjutkan**

Spwig akan mengirimkan pencarian uji untuk alamat IP yang diketahui (DNS publik Google, `8.8.8.8`) dan menampilkan hasilnya. Uji yang berhasil menampilkan negara yang dikembalikan dan waktu respons dalam milidetik.

## Menetapkan prioritas penyedia

Ketika beberapa penyedia aktif, bidang **Priority** mengontrol mana yang dicoba terlebih dahulu.

Angka yang lebih rendah berarti prioritas yang lebih tinggi.

Sebagai contoh, untuk menggunakan header CDN terlebih dahulu (paling cepat) dan beralih ke Spwig GeoIP:

| Provider | Priority |
|----------|----------|
| CDN Edge Headers | 0 |
| Spwig GeoIP | 10 |

Anda dapat mengedit prioritas secara langsung dalam tampilan daftar — kolom **Priority** dapat diedit secara inline.

## Memantau kinerja penyedia

Setiap catatan penyedia melacak statistik akurasinya sendiri:

- **Total Lookups** — jumlah total pencarian IP yang dicoba
- **Successful Lookups** — pencarian yang mengembalikan hasil
- **Failed Lookups** — pencarian yang mengembalikan tidak ada data atau kesalahan
- **Average Response (ms)** — rata-rata waktu respons dalam milidetik
- **Accuracy** — persentase pencarian yang berhasil

Jika penyedia menunjukkan tingkat akurasi yang rendah atau waktu respons yang tinggi, pertimbangkan untuk menyesuaikan prioritasnya atau menonaktifkannya dalam favor dari opsi yang berkinerja lebih baik.

## Pemetaan negara

Navigasikan ke **Customers > Country Mappings** untuk mengonfigurasi default per-negara untuk mata uang, bahasa, pajak, dan pengiriman. Setiap entri negara mengontrol:

- **Default Currency** — mata uang yang dipilih secara default untuk pengunjung dari negara tersebut
- **Default Language** — bahasa yang ditampilkan untuk pengunjung dari negara tersebut
- **Tax Rate** — persentase pajak default yang diterapkan untuk negara tersebut
- **Is EU Member** / **Requires VAT** — digunakan untuk logika kepatuhan pajak EU
- **Shipping Zone** — menghubungkan negara ke zona pengiriman
- **Supports COD** — mengaktifkan pembayaran tunai saat pengiriman untuk negara tersebut

Anda dapat mengedit bidang **Is Active**, **Default Currency**, dan **Default Language** secara langsung dalam daftar tanpa membuka setiap catatan.

## Tips

- Penyedia Spwig GeoIP bekerja langsung tanpa konfigurasi — hanya tambahkan penyedia tambahan jika Anda membutuhkan akurasi yang lebih tinggi atau operasi offline
- Jika Anda menggunakan Cloudflare, penyedia CDN Edge Headers adalah pilihan terbaik: tidak menambahkan latensi dan tidak menghitung terhadap kuota API apa pun
- Hanya aktifkan penyedia yang benar-benar Anda butuhkan — memiliki banyak penyedia aktif tidak meningkatkan akurasi jika penyedia pertama sudah berhasil
- Periksa statistik akurasi secara mingguan dan nonaktifkan penyedia dengan tingkat keberhasilan di bawah 80%
- Pemetaan negara digunakan sebagai default; pelanggan selalu dapat mengubah mata uang dan bahasa mereka secara manual di toko online