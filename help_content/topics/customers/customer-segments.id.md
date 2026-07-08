---
title: Segment Pelanggan
---

Segment pelanggan memungkinkan Anda secara otomatis mengklasifikasikan pelanggan Anda ke dalam kelompok yang bermakna berdasarkan perilaku pembelian mereka. Setelah pelanggan dikategorikan, Anda dapat menggunakan kelompok tersebut untuk fokus pada upaya pemasaran Anda — contohnya, menawarkan hadiah loyalitas kepada pelanggan VIP atau mengirimkan kampanye pemulihan kepada pelanggan yang sudah lama tidak berbelanja.

Spwig mengevaluasi kriteria segment terhadap metrik setiap pelanggan dan menetapkan mereka ke segment dengan prioritas tertinggi yang mereka penuhi. Hal ini terjadi secara otomatis saat data pelanggan diperbarui.

## Jenis segment yang tersedia

Spwig dilengkapi dengan himpunan jenis segment bawaan. Setiap jenis segment memiliki identifikasi internal tetap, tetapi Anda dapat menyesuaikan nama tampilan, deskripsi, kriteria, dan warna sesuai dengan cara Anda memandang pelanggan Anda.

| Jenis Segment | Penggunaan Tipe |
|---|---|
| **Pelanggan Tamu** | Pelanggan yang menyelesaikan pembelian tanpa membuat akun |
| **Pelanggan Baru** | Pelanggan yang baru saja membuat pembelian pertama mereka |
| **Pelanggan Rutin** | Pelanggan dengan riwayat pembelian yang konsisten |
| **Pembeli Sering** | Pelanggan yang sering membeli (waktu antar pesanan pendek) |
| **Nilai Tinggi** | Pelanggan dengan total pengeluaran yang tinggi |
| **Pelanggan VIP** | Pelanggan paling bernilai dan loyal Anda |
| **Pemburu Diskon** | Pelanggan yang cenderung membeli selama promo |
| **Berisiko** | Pelanggan yang sudah lama tidak berbelanja |
| **Tidak Aktif** | Pelanggan yang sudah absen selama periode yang lama |

## Memahami kriteria segment

Setiap segment didefinisikan oleh kombinasi kriteria. Spwig memeriksa kriteria ini terhadap metrik yang disimpan untuk setiap pelanggan. Semua kriteria dalam sebuah segment dikombinasikan — pelanggan harus memenuhi setiap kondisi yang ditetapkan untuk memenuhi syarat.

### Kriteria pengeluaran

- **Min Total Spent** — pelanggan harus menghabiskan setidaknya jumlah ini di semua pesanan yang selesai
- **Max Total Spent** — pelanggan tidak boleh menghabiskan lebih dari jumlah ini

Gunakan rentang pengeluaran untuk mengidentifikasi tingkat tertentu. Contohnya, menetapkan Min ke $500 dan Max ke $2.000 akan menargetkan pelanggan tingkat menengah.

### Kriteria jumlah pesanan

- **Min Orders** — pelanggan harus memiliki setidaknya jumlah pesanan selesai ini
- **Max Orders** — pelanggan tidak boleh memiliki lebih dari jumlah pesanan selesai ini

Menggabungkan Min Orders dengan minimum pengeluaran adalah cara andal untuk mendefinisikan pelanggan VIP: mereka membeli sering *dan* menghabiskan secara dermawan.

### Kriteria kebaruan

- **Min Days Since Last Purchase** — pesanan terbaru pelanggan harus setidaknya sebanyak hari ini yang lalu
- **Max Days Since Last Purchase** — pesanan terbaru pelanggan harus dalam jangka hari ini

Kriteria kebaruan sangat penting untuk segment berisiko dan tidak aktif. Contohnya, menetapkan Min Days ke 90 dan Max Days ke 365 mengidentifikasi pelanggan yang sudah diam tetapi belum sepenuhnya hilang.

## Prioritas segment

Ketika pelanggan memenuhi lebih dari satu segment, segment dengan nilai **prioritas tertinggi** yang menang. Anda dapat menetapkan prioritas untuk setiap segment di bagian **Display Settings** dari formulir segment.

Segment **Pelanggan Tamu** selalu dievaluasi terlebih dahulu, secara independen dari urutan prioritas, karena status tamu ditentukan oleh jenis akun, bukan kriteria pembelian.

## Melihat dan mengelola segment

Navigasikan ke **Customers > Customer Segments** untuk melihat semua segment yang dikonfigurasikan. Daftar menampilkan nama tampilan setiap segment, jenis internal, warna yang ditetapkan, prioritas, jumlah pelanggan yang cocok saat ini, dan apakah segment aktif.

![Customer Segments List](/static/core/admin/img/help/customer-segments/segments-list.webp)

### Membuat atau mengedit segment

1.

Navigasikan ke **Customers > Customer Segments**
2.

Klik segment yang ada untuk mengeditnya, atau klik **+ Add Customer Segment** untuk membuat yang baru
3.



Isi tab **Segment Information**:
   - **Name** — pilih jenis segment internal dari dropdown
   - **Display Name** — nama yang dapat dibaca manusia yang ditampilkan di admin (misalnya, "VIP Customers")
   - **Description** — catatan internal singkat yang menjelaskan apa yang dimaksud dengan segment ini
4.

Tetapkan kriteria di tab yang relevan:
   - **Criteria - Spending** — jumlah pengeluaran minimum dan maksimum total
   - **Criteria - Orders** — jumlah pesanan minimum dan maksimum
   - **Criteria - Recency** — jumlah hari minimum dan maksimum sejak pembelian terakhir
5.

Konfigurasikan **Display Settings**:
   - **Color** — warna heksadesimal yang digunakan untuk mengidentifikasi segment ini secara visual dalam daftar
   - **Priority** — angka yang lebih tinggi berarti segment ini dievaluasi terlebih dahulu
   - **Is Active** — hilangkan centang untuk menonaktifkan segment tanpa menghapusnya
6.

Klik **Save** untuk menerapkan perubahan

### Contoh: Mengonfigurasi segment VIP

Berikut adalah contoh nyata untuk segment VIP bernilai tinggi:

| Field | Value |
|---|---|
| Name | `vip` |
| Display Name | VIP Customers |
| Min Total Spent | $1,000 |
| Min Orders | 5 |
| Max Days Since Last Purchase | 180 |
| Priority | 90 |
| Color | `#FFD700` |

Ini berarti: seorang pelanggan memenuhi syarat sebagai VIP jika mereka telah menghabiskan setidaknya $1,000, memesan setidaknya 5 pesanan, dan melakukan pembelian dalam 6 bulan terakhir.

### Contoh: Mengonfigurasi segment At Risk

| Field | Value |
|---|---|
| Name | `at_risk` |
| Display Name | At Risk |
| Min Days Since Last Purchase | 60 |
| Max Days Since Last Purchase | 180 |
| Priority | 30 |
| Color | `#FF6B35` |

## Menggunakan segment untuk pemasaran yang ditargetkan

Segment ditampilkan di profil pelanggan di seluruh admin, sehingga tim Anda segera mengetahui tingkatan mana setiap pelanggan termasuk. Gunakan informasi ini untuk:

- **Menjalankan kampanye voucher yang ditargetkan** — buat voucher yang dibatasi untuk pelanggan dalam segment tertentu, lalu gunakan sistem email Anda untuk mengirimkannya hanya ke kelompok tersebut
- **Meningkatkan prioritas dukungan** — tandai pelanggan VIP atau bernilai tinggi sehingga tim Anda dapat memberikan layanan prioritas
- **Merencanakan re-engagement** — tinjau segment At Risk dan Inactive secara berkala untuk mengidentifikasi pelanggan yang membutuhkan email win-back atau penawaran khusus
- **Menyesuaikan pengeluaran pemasaran** — fokuskan anggaran akuisisi pada saluran yang membawa pelanggan bernilai tinggi dengan menganalisis segment mana yang mereka konversi

## Tips

- Mulailah dengan jenis segment bawaan sebelum membuat kriteria kustom — mereka menutupi kebutuhan segmentasi yang paling umum secara bawaan
- Tinjau jumlah pelanggan di setiap segment secara berkala; segment VIP dengan nol pelanggan atau segment At Risk yang tumbuh pesat keduanya layak untuk diselidiki
- Gunakan bidang **Priority** secara sengaja — jika kriteria Anda tumpang tindih antar segment (misalnya, seorang pelanggan memenuhi syarat untuk kedua Frequent Buyer dan High Value), segment dengan prioritas yang lebih tinggi menang
- Nonaktifkan segment yang saat ini tidak digunakan alih-alih menghapusnya — Anda dapat mengaktifkannya kembali nanti tanpa mengonfigurasikan ulang kriteria
- Kriteria segment diperiksa terhadap metrik pelanggan yang disimpan, yang dihitung ulang secara otomatis. Jika jumlah segment terlihat ketinggalan, metrik dapat dihitung ulang dari bagian Customer Metrics di admin