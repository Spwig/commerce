---
title: Pengaturan Multi-Mata Uang
---

Multi-mata uang memungkinkan pelanggan Anda untuk menjelajahi produk dan menyelesaikan checkout dalam mata uang yang mereka pilih. Harga secara otomatis dikonversi dari mata uang dasar Anda menggunakan tingkat pertukaran dari penyedia yang terhubung atau tingkat yang didefinisikan secara manual.

## Sebelum memulai

Sebelum mengaktifkan multi-mata uang, Anda memerlukan:

1. **Penyedia tingkat pertukaran yang aktif** - Pergi ke **Pengaturan > Tab Multi-Mata Uang > Dashboard Tingkat Pertukaran** dan hubungkan setidaknya satu penyedia (seperti Open Exchange Rates, Fixer.io, atau ExchangeRate-API). Penyedia harus aktif dan menyinkronkan tingkat.
2. **Setidaknya dua mata uang** - Mata uang dasar Anda ditambah satu atau lebih mata uang tambahan yang ingin Anda dukung.

## Mengaktifkan multi-mata uang

Navigasikan ke **Pengaturan > Multi-Mata Uang** dan centang **Aktifkan Multi-Mata Uang**. Setelah diaktifkan, konfigurasikan opsi berikut:

| Pengaturan | Deskripsi |
|---------|-------------|
| **Mode Pemilihan Mata Uang** | Cara pelanggan memilih mata uang mereka. *Otomatis* mendeteksi dari lokasi mereka, *Manual* memungkinkan mereka memilih dari pengubah, *Keduanya* menggabungkan kedua pendekatan. |
| **Tampilkan Pengubah Mata Uang** | Tampilkan pemilih mata uang di toko Anda sehingga pelanggan dapat mengubah mata uang secara manual. |
| **Posisi Pengubah** | Di mana pengubah mata uang muncul (header, footer, atau sidebar). |
| **Tampilkan Informasi Tingkat Pertukaran** | Tampilkan pemberitahuan kepada pelanggan bahwa harga adalah konversi pendekatan dari mata uang dasar Anda. |
| **Aktifkan Format Lokal** | Format angka dan simbol mata uang sesuai dengan setiap lokasi pelanggan (misalnya, 1.234,56 untuk format Eropa). |

## Mode checkout

Pilih cara multi-mata uang bekerja saat checkout:

| Mode | Deskripsi |
|------|-------------|
| **Multi-Mata Uang Penuh** | Pelanggan menjelajahi, menambahkan ke keranjang, dan membayar dalam mata uang yang mereka pilih. Tingkat pertukaran dikunci saat checkout dan dicatat dengan pesanan. Ini adalah default. |
| **Hanya Tampil** | Harga ditampilkan dalam mata uang pelanggan untuk kenyamanan, tetapi keranjang dan pembayaran selalu diproses dalam mata uang dasar Anda. Saat checkout, pelanggan melihat pemberitahuan yang menunjukkan jumlah konversi pendekatan bersama dengan jumlah tagihan aktual dalam mata uang dasar Anda. |

**Hanya Tampil** berguna ketika penyedia pembayaran Anda hanya mendukung mata uang dasar Anda, atau ketika Anda ingin menghindari risiko tingkat pertukaran sepenuhnya. Pelanggan masih melihat harga lokal saat menjelajahi, memberi mereka perasaan biaya dalam mata uang mereka sendiri.

## Interval sinkronisasi tingkat pertukaran

Kontrol seberapa sering toko Anda mengambil tingkat terbaru dari penyedia yang terhubung:

| Interval | Deskripsi |
|----------|-------------|
| **Real-time** | Setiap 15 menit. Terbaik untuk toko dengan penjualan internasional tinggi. |
| **Setiap jam** | Sekali per jam. Keseimbangan yang baik antara kebaruan dan penggunaan API. |
| **Setiap hari** | Sekali per hari. Cocok untuk sebagian besar toko. Ini adalah default. |
| **Setiap minggu** | Sekali per minggu. Untuk toko dengan harga stabil. |
| **Bulanan / Kuartalan** | Pembaruan yang kurang sering untuk toko yang jarang mengubah tingkat. |
| **Hanya Manual** | Tingkat tidak pernah diambil secara otomatis. Anda mengelola semua tingkat secara manual. |

Interval sinkronisasi memengaruhi seberapa sering tugas latar belakang mengambil tingkat dari penyedia Anda. Antara sinkronisasi, tingkat yang disimpan digunakan. Jika Anda perlu memaksa sinkronisasi segera, gunakan tombol **Sinkronisasi Sekarang** di Dashboard Tingkat Pertukaran atau **Sinkronisasi dari Penyedia** di halaman Tingkat Pertukaran Manual.

## Tingkat pertukaran manual

Tingkat pertukaran manual memungkinkan Anda menetapkan tingkat konversi eksak untuk pasangan mata uang tertentu. Mereka mengambil prioritas atas tingkat yang diambil dari penyedia, memberi Anda kendali penuh atas harga.

Navigasikan ke **Tingkat Pertukaran > Tingkat Pertukaran Manual** untuk mengelolanya.

### Menetapkan tingkat secara manual

Klik **Tambahkan Tingkat** untuk membuat tingkat untuk pasangan mata uang. Tentukan mata uang dasar, mata uang target, dan tingkat. Misalnya, menetapkan USD/EUR ke 0,92 berarti 1 USD = 0,92 EUR.

### Sinkronisasi dari penyedia

Klik **Sinkronisasi dari Penyedia** untuk mengisi otomatis tingkat manual dari tingkat terbaru penyedia yang terhubung Anda.

Ini menciptakan tarif manual untuk semua mata uang yang didukung, memberi Anda titik awal untuk menyetel ulang secara lebih tepat.

Tarif terkunci akan dilewati selama sinkronisasi, sehingga tarif yang telah Anda atur secara manual tidak akan tertimpa.

### Mengunci tarif

Klik ikon kunci pada tarif mana pun untuk mencegahnya dari tertimpa selama sinkronisasi penyedia. Ini berguna ketika Anda telah menegosiasikan tarif tertentu atau ingin mempertahankan tarif tetap terlepas dari pergerakan pasar.

- **Tarif terkunci** menampilkan badge kunci dan tidak termasuk dalam sinkronisasi otomatis.
- **Tarif tidak terkunci** dapat diperbarui saat Anda mengklik Sinkronisasi dari Penyedia.

### Perbandingan penyedia

Setiap tarif manual menampilkan tarif penyedia saat ini di sebelahnya, beserta perbedaan persentase. Ini membantu Anda melihat secara cepat bagaimana tarif manual Anda dibandingkan dengan tarif pasar:

- Persentase **hijau** berarti tarif Anda lebih tinggi dari tarif penyedia.
- Persentase **merah** berarti tarif Anda lebih rendah dari tarif penyedia.

## Markup tarif pertukaran

Anda dapat menambahkan markup persentase ke tarif pertukaran untuk menutupi biaya konversi mata uang dan melindungi diri dari fluktuasi tarif antara saat pelanggan memesan dan saat Anda menerima pembayaran.

Sebagai contoh, markup 2% pada tarif USD/EUR 1.18 akan mengubahnya menjadi sekitar 1.20 USD/EUR. Buffer kecil ini membantu memastikan Anda tidak kehilangan uang dalam konversi mata uang.

## Strategi pemilihan tarif

Ketika Anda memiliki beberapa penyedia tarif pertukaran yang terhubung, Anda dapat memilih cara tarif dipilih:

- **Penyedia Utama** - Selalu menggunakan tarif dari penyedia utama yang ditentukan. Ini memastikan harga yang konsisten di seluruh toko Anda. Jika penyedia utama tidak memiliki data untuk pasangan mata uang tertentu, sistem akan beralih ke tarif terbaru yang tersedia dari penyedia mana pun.
- **Terbaru yang Tersedia** - Menggunakan tarif yang paling baru disinkronkan dari penyedia aktif mana pun. Ini memberi Anda data terbaru, tetapi tarif mungkin sedikit berbeda antar penyedia.

Untuk sebagian besar toko, **Penyedia Utama** adalah pilihan yang disarankan karena memberikan harga yang paling dapat diprediksi.

## Mata uang yang didukung

Gunakan manajer mata uang drag-and-drop untuk memilih mata uang yang didukung oleh toko Anda:

1. **Mata Uang Tersedia** (kolom kiri) menampilkan semua mata uang yang dapat Anda aktifkan.
2. **Mata Uang Aktif** (kolom kanan) menampilkan mata uang yang saat ini aktif di toko Anda.
3. Drag mata uang antar kolom untuk mengaktifkan atau menonaktifkan mereka.
4. Drag dalam kolom Aktif untuk mengurutkan cara mata uang muncul di pengganti.
5. Klik **Simpan Konfigurasi Mata Uang** untuk menerapkan perubahan Anda.

Mata uang dasar Anda selalu aktif dan tidak dapat dihapus.

## Bagaimana tarif pertukaran diselesaikan

Ketika harga perlu dikonversi, sistem memeriksa tarif dalam urutan ini:

1. **Tarif pertukaran manual** - Jika ada tarif manual aktif untuk pasangan mata uang, tarif ini selalu digunakan terlebih dahulu.
2. **Tarif penyedia** - Jika tidak ada tarif manual, tarif terbaru dari penyedia terhubung Anda digunakan.

Ini berarti Anda dapat menggunakan penyedia untuk sebagian besar mata uang dan mengganti pasangan tertentu dengan tarif manual di mana Anda memerlukan kontrol yang tepat.

## Penting: Pengaturan ini permanen

Setelah multi-mata uang diaktifkan dan pelanggan memesan dalam mata uang asing, pengaturan ini **tidak dapat dinonaktifkan**. Ini karena:

- Pesanan secara permanen menyimpan mata uang yang dipilih oleh pelanggan dan tarif pertukaran yang digunakan saat pembelian.
- Laporan keuangan dan perhitungan pengembalian uang bergantung pada data mata uang historis ini.
- Menonaktifkan multi-mata uang akan meninggalkan pesanan multi-mata uang yang sudah ada dalam keadaan yang tidak konsisten.

Jika tidak ada pesanan yang ditempatkan dalam mata uang asing, Anda masih dapat menonaktifkan multi-mata uang.

## Tips

Jaga semua format markdown, jalur gambar, blok kode, dan istilah teknis.

- **Uji coba dengan pesanan kecil terlebih dahulu** - Plasihkan pesanan uji dalam mata uang asing untuk memverifikasi alur checkout dan memastikan tingkat pertukaran diterapkan dengan benar.
- **Pantau tingkat pertukaran secara berkala** - Periksa Dashboard Tingkat Pertukaran secara berkala untuk memastikan penyedia Anda menyinkronkan tingkat dan terlihat masuk akal.
- **Pertimbangkan markup untuk mata uang yang volatil** - Jika Anda mendukung mata uang dengan volatilitas tinggi, markup sedikit lebih tinggi (2-3%) dapat melindungi margin Anda.
- **Mulai dengan mata uang utama** - Mulailah dengan mata uang yang umum digunakan (EUR, GBP, JPY, CAD, AUD) dan perluas berdasarkan permintaan pelanggan.
- **Periksa kompatibilitas penyedia pembayaran** - Tidak semua penyedia pembayaran mendukung semua mata uang.

Periksa dokumentasi penyedia pembayaran Anda untuk memastikan mata uang mana yang mereka proses.
- **Gunakan mode Tampilan Saja jika ragu** - Jika Anda tidak yakin apakah penyedia pembayaran Anda menangani checkout multi-mata uang, mulailah dengan mode Tampilan Saja.

Anda dapat beralih ke Multi-Mata Uang Penuh nanti.
- **Kunci tingkat sebelum periode promosi** - Jika Anda menjalankan penjualan, kunci tingkat pertukaran Anda sebelumnya untuk memastikan harga konsisten sepanjang promosi.