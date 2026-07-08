---
title: Program Referensi
---

Program referensi memungkinkan pelanggan yang sudah ada berbagi tautan referensi unik dengan teman dan keluarga mereka. Ketika teman yang direferensikan membuat pembelian kualifikasi pertama mereka, baik pemberi referensi dan pelanggan baru dapat menerima hadiah — meningkatkan akuisisi pelanggan baru melalui mulut ke mulut.

## Cara program referensi bekerja

1. Seorang pelanggan berbagi tautan referensi unik (atau kode) dengan temannya.
2. Teman tersebut mengklik tautan dan dilacak melalui cookie hingga 30 hari (dapat dikonfigurasi).
3. Teman tersebut mendaftar dan membuat pesanan kualifikasi pertama.
4. Sistem membuat catatan atribusi referensi dan menjalankan pemeriksaan penipuan dan kelayakan.
5. Jika atribusi disetujui, hadiah diberikan kepada kedua pihak.

Toko Anda memiliki satu konfigurasi program referensi. Navigasikan ke **Pemasaran > Program Referensi** untuk mengatur.

## Mengatur program referensi Anda

### Status program

Program memiliki tiga status:

- **Draft** — Program sedang dikonfigurasi tetapi belum aktif. Tautan referensi tidak aktif.
- **Active** — Program sedang berjalan. Pelanggan dapat berbagi tautan dan memperoleh hadiah.
- **Paused** — Program sementara dihentikan. Atribusi yang sudah ada tetap diproses, tetapi tidak ada referensi baru yang dilacak.

Atur **Status** menjadi **Active** ketika Anda siap meluncurkan. Anda dapat menghentikannya kapan saja.

### Konfigurasi hadiah

Tentukan hadiah yang diberikan ketika referensi berhasil. Program mendukung **hadiah dua sisi** — artinya Anda dapat memberikan hadiah kepada pemberi referensi (pelanggan yang berbagi tautan) dan penerima referensi (pelanggan baru yang menggunakan tautan tersebut).

Konfigurasikan hadiah untuk setiap penerima di bidang **Konfigurasi Hadiah**. Jenis hadiah yang tersedia adalah:

| Jenis Hadiah | Deskripsi |
|-------------|-------------|
| **Kredit Toko** | Menambahkan kredit ke dompet pelanggan, dapat digunakan pada pesanan masa depan |
| **Kode Kupon** | Menghasilkan kode voucher diskon unik |
| **Diskon Persentase** | Memberikan diskon persentase untuk digunakan saat checkout |
| **Keuntungan Eksklusif** | Sebuah keuntungan khusus (misalnya, hadiah gratis, akses prioritas) — dijelaskan dalam bidang deskripsi hadiah |

**Contoh konfigurasi** — $10 kredit toko untuk pemberi referensi dan $10 diskon untuk pelanggan baru:

```json
{
  "referrer": {"kind": "credit", "amount": 10},
  "referee": {"kind": "discount", "amount": 10},
  "double_sided": true
}
```

Atur "double_sided": false jika Anda hanya ingin memberikan hadiah kepada pemberi referensi.

### Aturan kelayakan

Aturan kelayakan menentukan referensi mana yang memenuhi syarat untuk menerima hadiah. Konfigurasikan ini di bidang **Aturan Kelayakan**:

| Aturan | Apa yang dilakukannya |
|------|--------------|
| `new_customer_only` | Jika `true`, teman yang direferensikan harus menjadi pelanggan baru (tidak memiliki pesanan sebelumnya) |
| `min_order_value` | Nilai minimum pesanan (dalam mata uang toko Anda) yang harus dibelanjakan oleh teman yang direferensikan |
| `exclude_discounts` | Jika `true`, pesanan di mana pelanggan yang direferensikan menggunakan voucher tidak memenuhi syarat |
| `exclude_staff` | Jika `true`, akun staf tidak dapat menjadi pemberi referensi atau penerima referensi |

**Contoh** — hanya pelanggan baru, nilai pesanan minimum $40, staf dikecualikan:

```json
{
  "new_customer_only": true,
  "min_order_value": 40.0,
  "exclude_discounts": false,
  "exclude_staff": true
}
```

### Konfigurasi waktu

Bidang **Konfigurasi Waktu** mengontrol kapan hadiah diberikan setelah pesanan kualifikasi:

| Pengaturan | Apa yang dilakukannya |
|---------|--------------|
| `issue_on` | Kapan hadiah diberikan: `signup` (segera setelah pendaftaran), `first_purchase` (segera setelah pesanan), atau `post_refund` (setelah jendela pengembalian berakhir) |
| `refund_window_days` | Berapa hari menunggu sebelum memberikan hadiah saat menggunakan `post_refund` (default: 14 hari) |

Menggunakan `post_refund` adalah pendekatan paling hati-hati — menunggu hingga jendela pengembalian berakhir sebelum memberikan hadiah, mengurangi risiko memberikan hadiah untuk pesanan yang kemudian dikembalikan.

### Batas dan batasan

Mencegah seorang pemberi referensi tunggal memperoleh hadiah tak terbatas dengan menetapkan batas di bidang **Batas & Batasan**:

| Pengaturan | Fungsi apa yang dilakukan |
|---------|--------------|
| `monthly_per_referrer` | Jumlah maksimum konversi rujukan yang berhasil diberi hadiah per bulan, per pemberi rujukan |
| `lifetime_per_referrer` | Total maksimum konversi rujukan yang berhasil diberi hadiah sepanjang masa, per pemberi rujukan |
| `max_reward_per_order` | Nilai hadiah maksimum (dalam mata uang toko Anda) yang diberikan untuk satu konversi rujukan |

**Contoh** — 20 rujukan per bulan, 200 sepanjang masa, $50 hadiah maksimum per konversi:

```json
{
  "monthly_per_referrer": 20,
  "lifetime_per_referrer": 200,
  "max_reward_per_order": 50
}
```

### Pengaturan pelacakan

Konfigurasikan cara tautan rujukan dilacak dalam bidang **Pengaturan Pelacakan**:

| Pengaturan | Fungsi apa yang dilakukan |
|---------|--------------|
| `cookie_ttl_days` | Berapa hari cookie pelacakan rujukan tetap aktif setelah teman mengklik tautan (default: 30) |
| `attribution` | Metode atribusi — saat ini `last_touch` (klik tautan rujukan terbaru yang diberi kredit) |

### Kebijakan penipuan

Sistem deteksi penipuan secara otomatis menilai setiap atribusi rujukan untuk risiko sebelum menyetujuinya. Konfigurasikan kebijakan dalam bidang **Kebijakan Penipuan**:

| Pengaturan | Fungsi apa yang dilakukan |
|---------|--------------|
| `policy` | Ketat secara keseluruhan: `strict`, `balanced`, atau `lenient` |
| `auto_reject_threshold` | Skor risiko (0–100) di atasnya atribusi secara otomatis ditolak (default: 80) |
| `auto_approve_threshold` | Skor risiko di bawahnya atribusi secara otomatis disetujui (default: 30) |
| `check_ip` | Jika `true`, memeriksa apakah pemberi rujukan dan pelanggan yang dirujuk berbagi alamat IP yang sama |
| `check_device` | Jika `true`, memeriksa apakah pemberi rujukan dan pelanggan yang dirujuk berbagi sidik jari perangkat |
| `check_velocity` | Jika `true`, memantau tingkat rujukan yang tidak biasa tinggi dari satu sumber |
| `velocity_window_hours` | Jendela waktu (dalam jam) untuk pemeriksaan kecepatan |
| `max_referrals_per_window` | Jumlah maksimum rujukan yang diperbolehkan dari satu sumber dalam jendela kecepatan |

Atribusi dengan skor risiko antara ambang batas penolakan otomatis dan persetujuan otomatis berada dalam status **Pending** dan memerlukan tinjauan manual.

### Ketentuan dan syarat

Masukkan ketentuan dan syarat hukum apa pun untuk program ini dalam bidang **Ketentuan & Syarat**. Teks ini ditampilkan kepada pelanggan saat mereka melihat program rujukan. Format markdown didukung.

## Melihat atribusi rujukan

Navigasikan ke **Marketing > Referral Attributions** untuk melihat semua kasus rujukan — hubungan antara pemberi rujukan dan pelanggan yang dirujuk.

![Daftar atribusi rujukan](/static/core/admin/img/help/referral-program/attribution-list.webp)

Setiap atribusi menampilkan pemberi rujukan, pelanggan yang dirujuk, pesanan pertama yang mereka tempatkan, status saat ini, dan skor risiko.

### Status atribusi

| Status | Artinya |
|--------|---------------|
| **Pending** | Menunggu tinjauan — skor risiko berada dalam rentang tinjauan manual |
| **Approved** | Rujukan valid — hadiah telah atau akan diberikan |
| **Rejected** | Rujukan tidak memenuhi syarat atau ditandai sebagai penipuan |
| **Expired** | Rujukan tidak dikonversi dalam jendela pelacakan |

### Menyetujui atau menolak atribusi secara manual

Untuk atribusi dalam status **Pending**, Anda dapat menyetujui atau menolak secara manual dengan membuka catatan atribusi dan menggunakan tombol aksi. Saat menolak, pilih **Alasan Penolakan**:

- Rujukan Diri Sendiri
- Bukan Pelanggan Baru
- Nilai Pesanan di Bawah Minimum
- Email Sementara
- Batas Terlampaui
- Risiko Penipuan
- Pesanan Dikembalikan atau Dibatalkan
- Penolakan Manual

Anda juga dapat menambahkan **Catatan Penolakan** untuk catatan Anda sendiri.

### Memfilter berdasarkan tingkat risiko

Gunakan filter **Tingkat Risiko** di bilah samping untuk fokus pada atribusi berisiko tinggi yang memerlukan tinjauan:

- Risiko Rendah (skor 0–30) — Disetujui otomatis
- Risiko Sedang (skor 31–70) — Tinjauan manual
- Risiko Tinggi (skor 71–89) — Tinjauan manual, perlakukan dengan hati-hati
- Risiko Sangat Tinggi (skor 90+) — Ditolak otomatis

## Melihat hadiah yang diberikan

Navigasi ke **Pemasaran > Hadiah yang Diberikan** untuk melihat semua hadiah yang telah diberikan sebagai hasil dari atribusi yang disetujui.

Setiap entri hadiah menampilkan pelanggan, apakah mereka adalah pengirim atau penerima, jenis dan jumlah hadiah, serta status pemakaian saat ini.

### Status Hadiah

| Status | Artinya |
|--------|---------|
| **Menunggu** | Hadiah telah dibuat tetapi belum diberikan kepada pelanggan |
| **Diberikan** | Hadiah aktif dan tersedia untuk digunakan oleh pelanggan |
| **Diklaim** | Pelanggan telah menggunakan hadiah |
| **Kadaluarsa** | Hadiah telah melebihi tanggal kedaluarsa tanpa digunakan |
| **Dibatalkan** | Hadiah dibatalkan secara manual (misalnya, jika pesanan asli dikembalikan setelah hadiah diberikan) |

### Membatalkan Hadiah

Jika hadiah perlu dibatalkan — misalnya, pesanan yang memenuhi syarat dikembalikan — buka catatan hadiah dan gunakan tindakan **Batalkan**. Tambahkan catatan yang menjelaskan mengapa hadiah tersebut dibatalkan untuk catatan Anda.

## Tips

- Mulailah dengan pengaturan waktu `post_refund`. Menunggu hingga jendela pengembalian berakhir sebelum memberikan hadiah mencegah pemberian hadiah untuk pesanan yang akhirnya dikembalikan.
- Kebijakan penipisan `balanced` adalah pilihan default yang baik untuk sebagian besar toko. Beralih ke `strict` jika Anda melihat lonjakan tidak biasa dalam jumlah rujukan dari sejumlah akun kecil.
- Tetapkan batas bulanan dan seumur hidup yang realistis. Jika nilai hadiah Anda tinggi, batas 10–20 per bulan per pengirim adalah wajar untuk mencegah penyalahgunaan.
- Tinjau **Menunggu** atribusi secara mingguan. Membiarkan mereka tidak ditinjau terlalu lama dapat menyebabkan frustrasi bagi pengirim yang sah yang menunggu hadiah mereka.
- Gunakan filter **Tingkat Risiko** untuk memprioritaskan antrian tinjauan manual Anda — mulailah dengan atribusi berisiko sangat tinggi sebelum beralih ke risiko sedang.
- Pertahankan Kondisi & Ketentuan Anda singkat dan dalam bahasa sederhana. Pelanggan lebih mungkin berpartisipasi ketika mereka memahami aturan secara jelas.