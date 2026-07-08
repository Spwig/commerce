---
title: Aturan Bisnis Berbasis Lokasi
---

Aturan bisnis berbasis lokasi memungkinkan Anda secara otomatis melakukan tindakan ketika pengunjung datang dari negara, wilayah, atau jenis perangkat tertentu. Anda dapat menggunakan aturan untuk menetapkan mata uang bagi pelanggan dari wilayah tertentu, mengarahkan pengunjung ke halaman yang disesuaikan, menampilkan banner promosi, atau membatasi akses ke konten tertentu.

Aturan dievaluasi dalam urutan prioritas setiap kali sesi pengunjung dibuat. Ketika aturan cocok, tindakan yang dikonfigurasikan dieksekusi segera.

## Bagaimana aturan bisnis bekerja

Setiap aturan terdiri dari dua bagian:

- **Kondisi** — kriteria yang harus dipenuhi agar aturan berlaku (misalnya, "pengunjung berasal dari Jerman")
- **Tindakan** — apa yang terjadi ketika semua kondisi cocok (misalnya, "tetapkan mata uang ke EUR")

Kondisi dan tindakan disimpan sebagai objek JSON dalam formulir aturan. Spwig mengevaluasi semua aturan aktif dalam urutan prioritas (dengan angka terkecil terlebih dahulu) dan menerapkannya jika cocok.

## Navigasi ke aturan bisnis

Navigasikan ke **Pelanggan > Aturan Bisnis** untuk melihat semua aturan yang dikonfigurasikan. Daftar menampilkan nama, status, prioritas, jumlah kali aturan tersebut diaktifkan, dan kapan terakhir kali aturan tersebut berlaku.

Klik aturan apa pun untuk melihat atau mengeditnya, atau klik **+ Tambah Aturan Bisnis** untuk membuat aturan baru.

## Membuat aturan bisnis

### Langkah 1: informasi dasar

Isi detail identifikasi aturan:

- **Nama** — nama yang jelas dan deskriptif (misalnya, `Set EUR untuk Zona Euro`)
- **Deskripsi** — catatan opsional yang menjelaskan tujuan aturan
- **Aktif** — centang untuk mengaktifkan aturan; hilangkan centang untuk menghentikan aturan tanpa menghapusnya
- **Prioritas** — angka yang lebih rendah dieksekusi lebih dulu; gunakan `10`, `20`, `30` untuk meninggalkan ruang bagi aturan di masa depan

### Langkah 2: mendefinisikan kondisi

Di bidang **Kondisi**, masukkan objek JSON yang menggambarkan kapan aturan harus berlaku. Semua kondisi dalam objek harus benar agar aturan cocok.

#### Kunci kondisi yang tersedia

| Kondisi | Format | Contoh |
|-----------|--------|---------|
| `country_in` | Array kode negara ISO | `["DE", "FR", "IT"]` |
| `country_not_in` | Array kode negara ISO | `["US", "CA"]` |
| `region_in` | Array nama wilayah | `["Bavaria", "Catalonia"]` |
| `region_not_in` | Array nama wilayah | `["Quebec"]` |
| `is_mobile` | Boolean | `true` |
| `is_vpn` | Boolean | `false` |

#### Contoh kondisi

Pengunjung dari Jerman, Prancis, atau Italia:
```json
{
  "country_in": ["DE", "FR", "IT"]
}
```

Pengunjung dari Amerika Serikat yang menggunakan perangkat mobile:
```json
{
  "country_in": ["US"],
  "is_mobile": true
}
```

Pengunjung dari luar Uni Eropa:
```json
{
  "country_not_in": ["AT","BE","BG","CY","CZ","DE","DK","EE","ES","FI","FR","GR","HR","HU","IE","IT","LT","LU","LV","MT","NL","PL","PT","RO","SE","SI","SK"]
}
```

### Langkah 3: mendefinisikan tindakan

Di bidang **Tindakan**, masukkan objek JSON yang menggambarkan apa yang harus terjadi ketika aturan berlaku.

#### Kunci tindakan yang tersedia

| Tindakan | Format | Deskripsi |
|--------|--------|-------------|
| `set_currency` | String kode mata uang | Tetapkan mata uang untuk pengunjung |
| `set_language` | String kode bahasa | Tetapkan bahasa tampilan |
| `show_banner` | Boolean | Memicu banner promosi |
| `redirect_to` | String jalur URL | Arahkan pengunjung ke URL yang berbeda |

#### Contoh tindakan

Tetapkan mata uang ke Euro:
```json
{
  "set_currency": "EUR"
}
```

Arahkan ke halaman landing yang disesuaikan:
```json
{
  "redirect_to": "/de/"
}
```

Tetapkan mata uang dan bahasa sekaligus:
```json
{
  "set_currency": "GBP",
  "set_language": "en"
}
```

## Contoh praktis

### Contoh: Aturan mata uang zona euro

**Skenario:** Secara otomatis tampilkan harga dalam Euro kepada pengunjung dari negara-negara zona euro.

| Field | Value |
|-------|-------|
| Name | `Eurozone — Set EUR` |
| Priority | `10` |
| Is Active | Checked |
| Conditions | `{"country_in": ["AT","BE","DE","ES","FI","FR","GR","IE","IT","LU","NL","PT"]}` |
| Actions | `{"set_currency": "EUR"}` |

### Contoh: Aturan harga Inggris

**Skenario:** Tampilkan harga dalam GBP kepada pengunjung dari Inggris Raya.

| Field | Value |
|-------|-------|
| Name | `UK — Set GBP` |
| Priority | `20` |
| Is Active | Checked |
| Conditions | `"{\"country_in\": [\"GB\"]}"` |
| Actions | `"{\"set_currency\": \"GBP\"}"` |

### Contoh: mengarahkan ke bagian toko yang dilokalisasi

**Skenario:** Arahkan pengunjung dari Australia ke halaman Australia yang dedikasikan.

| Field | Value |
|-------|-------|
| Name | `Australia — Redirect` |
| Priority | `30` |
| Is Active | Checked |
| Conditions | `"{\"country_in\": [\"AU\"]}"` |
| Actions | `"{\"redirect_to\": \/au\/}"` |

## Pengujian aturan

Anda dapat memverifikasi bahwa aturan cocok dengan profil pengunjung yang diharapkan tanpa menunggu lalu lintas nyata:

1. Dalam daftar Business Rules, pilih aturan menggunakan kotak centangnya
2. Buka dropdown **Action** dan pilih **Test selected rules**
3. Klik **Go**

Spwig akan mengevaluasi aturan terhadap profil pengunjung berbasis AS dan melaporkan apakah aturan cocok dan tindakan apa yang akan dipicu.

## Memantau aktivitas aturan

Kolom **Triggered** dalam daftar aturan menunjukkan seberapa banyak kali setiap aturan telah dipicu. Klik aturan untuk melihat **Last Triggered** timestamp di bagian Statistics.

Gunakan tindakan **Reset statistics** untuk mengatur ulang jumlah pencapaian menjadi nol jika Anda ingin memulai pengukuran dari tanggal tertentu setelah membuat perubahan pada aturan.

## Tips

- Tetapkan prioritas dengan celah (10, 20, 30) daripada angka berurutan (1, 2, 3) agar Anda dapat memasukkan aturan baru nanti tanpa perlu mengubah nomor semua
- Aturan berjalan dalam urutan prioritas dan semua aturan yang cocok diterapkan — jika dua aturan keduanya menetapkan mata uang, tindakan aturan dengan prioritas lebih rendah (nomor lebih tinggi) akan diterapkan terakhir
- Gunakan toggle **Is Active** untuk sementara menghentikan aturan selama promosi tanpa menghapus konfigurasinya
- Selalu uji aturan baru sebelum mengaktifkannya di lingkungan produksi untuk memastikan kondisinya benar
- Deteksi VPN (`"is_vpn": true`) tersedia jika Anda ingin menerapkan perlakuan berbeda untuk pengunjung yang menyembunyikan lokasi mereka, tetapi ingat bahwa beberapa pelanggan sah menggunakan VPN untuk privasi