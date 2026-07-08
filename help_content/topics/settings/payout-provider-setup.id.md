---
title: Payout Provider Setup
---

Pengaturan penyedia pembayaran memungkinkan Anda mengonfigurasi PayPal dan Airwallex untuk pembayaran afiliasi otomatis. Panduan ini menunjukkan cara menghubungkan akun penyedia pembayaran Anda, mengonfigurasi webhooks, dan menguji integrasi Anda.

## Penyedia Pembayaran yang Didukung

Spwig terintegrasi dengan dua penyedia pembayaran untuk mengotomatisasi pembayaran afiliasi:

| Penyedia | Metode Pembayaran | Pemrosesan | Dukungan Batch | Terbaik Untuk |
|----------|------------------|------------|---------------|----------|
| **PayPal** | Transfer akun PayPal | Berbasis API | Ya (hingga 15.000) | Sebagian besar afiliasi, jangkauan global |
| **Airwallex** | Transfer bank internasional | Berbasis API | Tidak (individual) | Transfer bank, pembayaran internasional |

### Perbedaan Utama

**Payouts PayPal**:
- Memerlukan afiliasi memiliki akun PayPal (email pembayaran)
- Memproses batch hingga 15.000 payout sekaligus
- Pemrosesan lebih cepat (1-2 hari kerja)
- Kompleksitas pengaturan lebih rendah
- Biaya: ~2% atau $0,25-$1,00 per pembayaran
- Satu webhook untuk seluruh batch

**Airwallex**:
- Mendukung transfer bank langsung
- Memproses payout individual satu per satu
- Pemrosesan lebih lama (2-5 hari kerja)
- Mendukung beberapa mata uang dan negara
- Biaya bervariasi tergantung negara tujuan
- Webhook individual per payout

Anda dapat mengonfigurasi kedua penyedia dan membiarkan afiliasi memilih metode pembayaran yang mereka prefer.

## Mengapa Menggunakan Penyedia Pembayaran?

Mengintegrasikan penyedia pembayaran menawarkan manfaat signifikan dibandingkan pembayaran manual:

- **Pemrosesan otomatis** — Tidak ada input data manual atau eksekusi pembayaran
- **Efisiensi batch** — Proses puluhan atau ratusan payout dengan satu klik
- **Konfirmasi webhook** — Pembaruan status otomatis ketika pembayaran selesai
- **Pengurangan kesalahan** — Sistem memvalidasi detail akun sebelum pemrosesan
- **Jejak audit** — Rekam jejak lengkap transaksi dan respons penyedia
- **Pembayaran lebih cepat** — Afiliasi menerima dana lebih cepat
- **Skalabilitas** — Kelola program afiliasi yang berkembang tanpa proporsional beban administrasi

Tanpa integrasi penyedia, Anda harus memproses setiap pembayaran secara manual melalui dashboard bank atau PayPal, lalu kembali ke Spwig untuk menandai payout sebagai selesai.

## Pengaturan PayPal

Ikuti langkah-langkah berikut untuk mengonfigurasi PayPal Payouts untuk pembayaran afiliasi otomatis.

### Prasyarat

Sebelum memulai, Anda memerlukan:
- Akun PayPal Business (akun pribadi tidak dapat menggunakan API Payouts)
- Akses ke [Dashboard Pengembang PayPal](https://developer.paypal.com/dashboard/)
- Persetujuan produksi untuk API Payouts (setelah pengujian sandbox)

### Langkah 1: Membuat Aplikasi PayPal

1. **Navigasi** ke [Dashboard Pengembang PayPal](https://developer.paypal.com/dashboard/)
2. **Masuk** dengan akun PayPal Business Anda
3. **Klik** **Aplikasi & Kredensial Saya** di bilah sisi kiri
4. **Pilih** tab **Live** (atau Sandbox untuk pengujian)
5. **Klik** **Buat Aplikasi**
6. **Masukkan nama aplikasi** (misalnya, "Spwig Affiliate Payouts")
7. **Pilih jenis aplikasi**: Merchant
8. **Klik** **Buat Aplikasi**

PayPal menghasilkan kredensial Anda.

### Langkah 2: Dapatkan Kredensial API

Setelah membuat aplikasi:

1. **Salin ID Klien** — String alfanumerik panjang
2. **Klik** **Tampilkan** di bawah Rahasia
3. **Salin Rahasia Klien** — Jaga kerahasiaan ini
4. **Catat mode** — Sandbox atau Live

### Langkah 3: Aktifkan Fitur Payouts

Aplikasi PayPal memerlukan izin eksplisit untuk menggunakan Payouts:

1. **Gulir** ke bagian **Fitur** dalam aplikasi Anda
2. **Cari** fitur **Payouts**
3. **Klik** **Tambahkan** jika belum diaktifkan
4. **Ajukan persetujuan** jika menggunakan mode Live (persetujuan memakan waktu 1-2 hari kerja)

### Langkah 4: Tambahkan Penyedia di Spwig

Sekarang tambahkan akun PayPal ke Spwig:

1. **Navigasi** ke **Pengaturan > Penyedia Pembayaran**
2. **Klik** **+ Tambahkan Akun PayPal**
3. **Isi formulir**:
   - **Nama Akun**: Label deskriptif (misalnya, "Akun PayPal Utama")
   - **ID Klien**: Salin dari Dashboard Pengembang PayPal
   - **Rahasia Klien**: Salin dari Dashboard Pengembang PayPal
   - **Mode**: Pilih Sandbox (pengujian) atau Produksi (live)
   - **Apakah Aktif**: Centang untuk mengaktifkan
4. **Klik Simpan**

Spwig memvalidasi kredensial dengan meminta token akses. Jika validasi gagal, periksa kembali ID Klien dan Rahasia Anda.

### Langkah 5: Uji Koneksi

Verifikasi integrasi PayPal Anda:

1. Buat payout uji di **Program Afiliasi > Payouts**
2. Gunakan email PayPal Anda sendiri sebagai penerima
3. Tetapkan jumlah $0,01 (jika dalam mode Produksi) atau jumlah apa pun (jika Sandbox)
4. Proses dengan penyedia
5. Periksa akun PayPal untuk pembayaran masuk
6. Verifikasi pembaruan webhook mengubah status payout di Spwig

Jika menggunakan mode Sandbox, buat akun PayPal uji di [PayPal Sandbox](https://developer.paypal.com/dashboard/accounts) untuk menerima payout uji.

## Pengaturan Airwallex

Airwallex mendukung transfer bank internasional untuk afiliasi yang memilih deposit langsung.

### Prasyarat

Sebelum memulai, Anda memerlukan:
- Akun Airwallex (buat di [airwallex.com](https://www.airwallex.com))
- Status akun bisnis yang diverifikasi
- Akses API diaktifkan (hubungi dukungan Airwallex jika diperlukan)
- Saldo yang cukup di akun Airwallex Anda

### Langkah 1: Membuat Kredensial API

1. **Masuk** ke [Dashboard Airwallex](https://www.airwallex.com/app/)
2. **Navigasi** ke **Pengaturan > Kunci API**
3. **Klik** **Buat Kunci API**
4. **Masukkan deskripsi**: "Spwig Affiliate Payouts"
5. **Pilih izin**: Aktifkan **Payouts** (baca dan tulis)
6. **Klik** **Buat**
7. **Salin Kunci API** — Ditampilkan hanya sekali
8. **Salin ID Klien** — Ditampilkan bersama dengan kunci

### Langkah 2: Catat Lingkungan Anda

Airwallex menyediakan dua lingkungan:

- **Demo**: Untuk pengujian dengan transaksi palsu
- **Produksi**: Untuk transfer uang nyata

Pastikan Anda mengetahui lingkungan mana yang dimiliki kunci API Anda.

### Langkah 3: Tambahkan Penyedia di Spwig

Tambahkan akun Airwallex ke Spwig:

1. **Navigasi** ke **Pengaturan > Penyedia Pembayaran**
2. **Klik** **+ Tambahkan Akun Airwallex**
3. **Isi formulir**:
   - **Nama Akun**: Label deskriptif (misalnya, "Akun Airwallex EUR")
   - **Kunci API**: Salin dari dashboard Airwallex
   - **ID Klien**: Salin dari dashboard Airwallex
   - **Lingkungan**: Pilih Demo atau Produksi
   - **Apakah Aktif**: Centang untuk mengaktifkan
4. **Klik Simpan**

Spwig memvalidasi kredensial dengan menanyai saldo akun Anda.

### Langkah 4: Verifikasi Negara yang Didukung

Airwallex mendukung transfer ke banyak negara tetapi tidak semua. Periksa halaman [Cakupan Airwallex](https://www.airwallex.com/global-business-account/global-transfers) untuk memastikan negara afiliasi Anda didukung.

Negara yang umum didukung meliputi:
- Amerika Serikat
- Inggris Raya
- Negara-negara Uni Eropa
- Australia
- Kanada
- Singapura
- Hong Kong

### Langkah 5: Uji Transfer Bank

Uji integrasi Airwallex Anda:

1. Buat payout uji untuk afiliasi dengan detail rekening bank
2. Gunakan jumlah kecil ($1-$5) jika dalam mode Produksi
3. Proses dengan penyedia
4. Periksa dashboard Airwallex untuk transaksi
5. Tunggu konfirmasi webhook
6. Verifikasi payout selesai di Spwig

Mode Demo memproses secara instan. Mode Produksi memakan waktu 2-5 hari kerja.

## Logika Pemilihan Penyedia

Ketika Anda memproses payout, Spwig secara otomatis memilih penyedia yang sesuai berdasarkan metode pembayaran afiliasi.

### Alur Pemilihan

1. **Periksa metode pembayaran afiliasi**:
   - Jika `payment_email` disetel → Afiliasi memilih PayPal
   - Jika detail rekening disetel → Afiliasi memilih transfer bank
2. **cocokkan dengan penyedia**:
   - Email PayPal → Gunakan akun penyedia PayPal yang aktif
   - Detail rekening → Gunakan akun penyedia Airwallex yang aktif
3. **Jika penyedia yang dipilih tidak dikonfigurasikan, gunakan penyedia pertama yang tersedia**
4. **Tampilkan kesalahan** jika tidak ada penyedia yang cocok

### Akun Penyedia Banyak

Anda dapat mengonfigurasi banyak akun untuk penyedia yang sama (misalnya, dua akun PayPal untuk wilayah berbeda). Spwig memilih akun aktif pertama yang cocok dengan metode pembayaran. Untuk mengontrol akun yang digunakan, urutkan ulang mereka dalam daftar admin atau atur hanya satu sebagai aktif.

## Pengujian Integrasi Payout

Selalu uji integrasi penyedia Anda sebelum memproses pembayaran live ke afiliasi.

### Pengujian Mode Sandbox/Demo

1. **Atur penyedia ke mode sandbox** (PayPal Sandbox atau Airwallex Demo)
2. **Buat afiliasi uji** dengan detail pembayaran uji
3. **Buat komisi uji** dan persetujui mereka
4. **Buat payout uji** yang mencakup komisi tersebut
5. **Proses dengan penyedia** menggunakan menu aksi
6. **Pantau log Celery** untuk permintaan API
7. **Periksa dashboard penyedia** untuk transaksi
8. **Tunggu webhook** untuk memperbarui status payout
9. **Verifikasi komisi ditandai sebagai lunas**

### Pengujian Produksi

Sebelum meluncurkan:

1. **Beralih ke mode produksi** di pengaturan penyedia
2. **Buat payout uji kecil** ke diri Anda sendiri ($0,01-$1,00)
3. **Proses** dan tunggu hingga selesai
4. **Verifikasi dana diterima** di akun Anda sendiri
5. **Periksa webhook yang ditembakkan** dan status yang diperbarui
6. **Periksa biaya transaksi penyedia**

### Masalah Uji Umum

| Masalah | Penyebab | Solusi |
|-------|-------|----------|
| "Kredensial tidak valid" | Kunci API salah atau ketidakcocokan mode | Periksa ulang kredensial, verifikasi sandbox vs produksi |
| Webhook tidak pernah ditembakkan | URL tidak dikonfigurasikan di penyedia | Tambahkan URL webhook di dashboard penyedia |
| Payout tetap dalam proses | Tanda tangan webhook gagal | Periksa apakah rahasia webhook cocok |
| Tidak ada penyedia yang tersedia | Tidak ada penyedia aktif untuk metode pembayaran | Aktifkan setidaknya satu akun penyedia |

## Pemrosesan Batch (PayPal)

PayPal mendukung pemrosesan batch untuk efisiensi dan penghematan biaya.

### Cara Pemrosesan Batch Bekerja

Ketika Anda memilih beberapa payout dan mengklik **Proses dengan Penyedia**:

1. Spwig mengelompokkan semua payout PayPal ke dalam satu batch
2. Sistem mengirim satu permintaan API dengan semua detail payout (hingga 15.000)
3. PayPal memproses seluruh batch sebagai satu transaksi
4. Webhook mengembalikan hasil batch
5. Spwig memperbarui semua payout berdasarkan respons batch

### Keuntungan Batch

- **Pengurangan panggilan API** — Satu permintaan untuk ratusan payout
- **Biaya lebih rendah** — Beberapa struktur biaya PayPal lebih menguntungkan pemrosesan batch
- **Pemrosesan lebih cepat** — Eksekusi paralel untuk seluruh batch
- **Satu webhook** — Lebih mudah pemantauan dan log

### Batasan Batch

PayPal menerapkan batasan berikut:
- Maksimal 15.000 penerima per batch
- Maksimal $100.000 total per batch
- Pemrosesan biasanya selesai dalam beberapa menit

Jika Anda melebihi 15.000 payout, Spwig secara otomatis membagi menjadi beberapa batch.

## Pemrosesan Individual (Airwallex)

Airwallex memproses payout satu per satu, yang memberikan tradeoff berbeda.

### Cara Pemrosesan Individual Bekerja

Ketika Anda memproses payout Airwallex:

1. Sistem mengirim permintaan API terpisah untuk setiap payout
2. Airwallex mengantre transfer secara individual
3. Setiap transfer selesai secara independen (2-5 hari)
4. Webhook individual ditembakkan ketika setiap transfer selesai
5. Spwig memperbarui payout saat webhook tiba

### Keuntungan Pemrosesan Individual

- **Isolasi kesalahan yang lebih baik** — Gagal satu tidak menghambat yang lain
- **Pelacakan per-payout** — ID transaksi per individu
- **Lebih banyak detail pembayaran** — Informasi spesifik bank per transfer
- **Waktu fleksibel** — Transfer selesai pada tingkat yang berbeda

### Waktu Pemrosesan

Berbeda dengan pemrosesan batch instan PayPal, transfer Airwallex memakan waktu lebih lama:
- Transfer domestik: 1-2 hari kerja
- Transfer internasional: 3-5 hari kerja
- Beberapa negara: Hingga 7 hari kerja

Atur ekspektasi afiliasi sesuai dengan ketentuan program Anda.

## Konfigurasi Webhook

Webhook memungkinkan pembaruan status payout otomatis ketika penyedia menyelesaikan transaksi.

### Format URL Webhook

Konfigurasikan URL ini di dashboard penyedia Anda:

```
https://yourdomain.com/api/payout-providers/{provider}/webhook/
```

Ganti `{provider}` dengan:
- `paypal` untuk webhook PayPal
- `airwallex` untuk webhook Airwallex

Contoh:
- `https://shop.example.com/api/payout-providers/paypal/webhook/`
- `https://shop.example.com/api/payout-providers/airwallex/webhook/`

### Pengaturan Webhook PayPal

1. **Navigasi** ke [Dashboard Pengembang PayPal](https://developer.paypal.com/dashboard/)
2. **Klik** nama aplikasi Anda
3. **Gulir** ke bagian **Webhook**
4. **Klik** **Tambahkan Webhook**
5. **Masukkan URL webhook** (format di atas)
6. **Pilih acara**:
   - `PAYMENT.PAYOUTSBATCH.SUCCESS`
   - `PAYMENT.PAYOUTSBATCH.DENIED`
   - `PAYMENT.PAYOUTS-ITEM.SUCCEEDED`
   - `PAYMENT.PAYOUTS-ITEM.FAILED`
7. **Klik Simpan**

PayPal menyediakan kunci tanda tangan webhook. Spwig menggunakan ini untuk memverifikasi keaslian webhook.

### Pengaturan Webhook Airwallex

1. **Navigasi** ke [Dashboard Airwallex](https://www.airwallex.com/app/)
2. **Pergi ke** **Pengaturan > Webhook**
3. **Klik** **Buat Webhook**
4. **Masukkan URL webhook** (format di atas)
5. **Pilih acara**:
   - `transfer.created`
   - `transfer.completed`
   - `transfer.failed`
6. **Klik Buat**

Airwallex menandatangani webhook dengan rahasia API Anda.

### Keamanan Webhook

Webhook divalidasi menggunakan mekanisme berikut:

- **Verifikasi tanda tangan** — Penyedia menandatangani payload webhook dengan kunci rahasia
- **Pemeriksaan timestamp** — Menolak webhook lama (mencegah serangan ulang)
- **Daftar IP yang diizinkan** (opsional) — Batasi ke rentang IP penyedia
- **HTTPS diperlukan** — Webhook hanya berfungsi melalui SSL

Jangan pernah menonaktifkan verifikasi tanda tangan di produksi.

### Pengujian Webhook

Sebagian besar penyedia menyediakan alat pengujian webhook:

**PayPal**: Gunakan "Simulator" di Dashboard Pengembang untuk menembakkan webhook pengujian

**Airwallex**: Buat transfer uji di mode Demo dan pantau webhook

Anda juga dapat memeriksa log webhook di Spwig di **Pengaturan > Log Sistem** (jika logging diaktifkan).

## Penyelesaian Masalah

### Kesalahan Kredensial Tidak Valid

**Gejala**: "Autentikasi gagal" saat menyimpan akun penyedia

**Penyebab**:
- ID Klien atau Rahasia salah
- Kredensial Sandbox digunakan dalam mode Produksi (atau sebaliknya)
- Kunci API kedaluwarsa atau dicabut
- Akun tidak diverifikasi

**Solusi**:
- Salin ulang kredensial dari dashboard penyedia
- Verifikasi mode cocok (sandbox vs produksi)
- Regenerasi kunci API
- Hubungi dukungan penyedia untuk memverifikasi status akun

### Webhook Tidak Diterima

**Gejala**: Payout terjebak dalam status "Processing" selamanya

**Penyebab**:
- URL webhook tidak dikonfigurasikan di dashboard penyedia
- Sertifikat HTTPS tidak valid
- Firewall memblokir IP penyedia
- Validasi tanda tangan webhook gagal

**Solusi**:
- Periksa ulang URL webhook di pengaturan penyedia
- Verifikasi sertifikat SSL valid
- Izinkan rentang IP penyedia di firewall
- Periksa log Celery untuk kesalahan tanda tangan
- Uji webhook dengan alat simulator penyedia

### Payout Gagal

**Gejala**: Status payout berubah menjadi "Gagal" dengan pesan kesalahan

**Penyebab**:
- Detail pembayaran afiliasi tidak valid (email atau rekening bank salah)
- Saldo tidak cukup di akun penyedia
- Rekening penerima tidak dapat menerima pembayaran
- Negara tidak didukung (Airwallex)
- Payout melebihi batas penyedia

**Solusi**:
- Periksa pesan kesalahan di bidang **Respons Penyedia**
- Verifikasi detail pembayaran afiliasi benar
- Tambahkan dana ke akun penyedia
- Minta afiliasi memeriksa status akun mereka
- Periksa dukungan negara dan mata uang penyedia
- Bagi payout besar jika melebihi batas

### Ketidakcocokan Mode

**Gejala**: Payout uji bekerja tetapi payout produksi gagal

**Penyebab**:
- Penyedia diatur ke mode Sandbox tetapi menggunakan akun afiliasi produksi
- Kredensial API dari lingkungan yang salah

**Solusi**:
- Ubah mode penyedia ke Produksi
- Regenerasi kredensial API produksi
- Verifikasi URL webhook mengarah ke domain produksi

## Praktik Keamanan Terbaik

Lindungi integrasi payout Anda dengan langkah-langkah keamanan berikut:

### Penyimpanan Kredensial

- **Jangan commit kredensial ke kontrol versi** — Gunakan variabel lingkungan atau penyimpanan aman
- **Putar ulang kunci API setiap kuartal** — Buat kunci baru setiap 3 bulan
- **Gunakan kunci terpisah untuk sandbox dan produksi** — Jangan campur lingkungan
- **Batasi izin API** — Hanya berikan akses Payouts, bukan kontrol akun penuh

Spwig menyimpan kredensial penyedia secara terenkripsi di database. Jaga cadangan database Anda aman.

### Keamanan Webhook

- **Selalu verifikasi tanda tangan** — Jangan lewati validasi tanda tangan
- **Gunakan HTTPS secara eksklusif** — Webhook HTTP tidak didukung
- **Implementasikan daftar IP yang diizinkan** — Batasi webhook ke rentang IP penyedia
- **Log semua webhook** — Pantau aktivitas mencurigakan
- **Batasi laju webhook endpoint** — Mencegah penyalahgunaan

### Kontrol Akses

- **Batasi akses staf** — Hanya staf yang dipercayai yang harus memproses payout
- **Gunakan otentikasi dua faktor** — Haruskan 2FA untuk akun staf
- **Audit tindakan payout** — Periksa siapa yang memproses payout apa
- **Pisahkan tugas** — Staf berbeda untuk persetujuan vs pemrosesan

### Pemantauan

- **Periksa payout yang gagal setiap hari** — Selesaikan masalah secara cepat
- **Pantau saldo akun penyedia** — Pastikan ada dana yang cukup
- **Periksa log transaksi setiap minggu** — Tangkap anomali sejak dini
- **Atur peringatan** — Notifikasi email untuk payout besar atau gagal

## Tips

- Uji integrasi Anda secara menyeluruh dalam mode sandbox sebelum beralih ke produksi — tangkap masalah dengan uang palsu.
- Konfigurasikan PayPal dan Airwallex untuk memberi afiliasi pilihan pembayaran — afiliasi berbeda memilih metode berbeda.
- Atur URL webhook selama pengaturan awal dan verifikasi mereka ditembakkan dengan benar — webhook kritis untuk otomatisasi.
- Pastikan saldo akun penyedia Anda selalu terisi untuk menghindari payout gagal selama pemrosesan batch.
- Gunakan nama akun deskriptif jika mengonfigurasikan beberapa penyedia (misalnya, "PayPal USD", "PayPal EUR").
- Putar ulang kredensial API setiap kuartal sebagai praktik keamanan terbaik.
- Dokumentasikan URL webhook dan kredensial Anda di manajer kata sandi yang aman yang dibagikan dengan tim Anda.
- Pantau payout yang gagal segera — penundaan menyebabkan kekecewaan afiliasi dan merusak reputasi program.
- Selalu gunakan HTTPS untuk instalasi Spwig Anda — webhook memerlukan sertifikat SSL.
- Hubungi dukungan penyedia jika Anda mengalami kesalahan yang berkelanjutan — mereka dapat memverifikasi status akun dan izin Anda.