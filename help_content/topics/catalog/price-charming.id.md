---
title: Aturan Harga Menarik
---

Harga menarik (juga disebut penentuan harga psikologis) secara otomatis menyesuaikan harga produk Anda agar berakhir dengan digit tertentu yang terasa lebih menarik bagi pelanggan. Misalnya, alih-alih menampilkan harga $20.00, harga menarik dapat menampilkan $19.99 — teknik yang luas digunakan yang membuat harga terlihat lebih rendah secara sekilas.

Spwig menerapkan aturan harga menarik secara otomatis di seluruh toko Anda, per mata uang, sehingga Anda hanya perlu menetapkan setiap aturan sekali saja.

## Cara harga menarik bekerja

Ketika harga produk dihitung (termasuk setelah promosi atau diskon), Spwig memeriksa apakah ada aturan harga menarik yang aktif untuk mata uang tersebut. Jika ada, harga akan disesuaikan sebelum ditampilkan kepada pelanggan. Penyesuaian ini berlaku untuk harga di atas ambang batas minimum yang Anda pilih.

Anda dapat mengonfigurasi aturan terpisah untuk setiap mata uang yang diterima toko Anda. Misalnya, Anda mungkin menggunakan akhiran `.99` untuk USD tetapi membulatkan ke `¥10` terdekat untuk JPY.

## Membuat aturan harga menarik

1. Navigasikan ke **Katalog > Aturan Harga Menarik**
2. Klik **+ Tambah Aturan Harga Menarik**
3. Pilih **Mata Uang** yang berlaku untuk aturan ini (misalnya, `USD`, `EUR`, `NZD`)
4. Pilih **Jenis Aturan** (lihat tabel di bawah ini)
5. Secara opsional, tetapkan **Ambang Batas Harga Minimum** untuk mengecualikan harga yang sangat rendah
6. Centang **Terapkan pada Harga Diskon** jika Anda juga ingin harga menarik diterapkan saat barang sedang diskon
7. Pastikan **Aktif** dicentang
8. Klik **Simpan**

Hanya satu aturan yang dapat ada per mata uang. Jika Anda perlu mengubah aturan, edit aturan yang sudah ada.

## Jenis aturan

| Jenis Aturan | Contoh | Terbaik untuk |
|-----------|---------|----------|
| **Harga Menarik Akhiran .99** | $20.50 → $19.99 | Produk ritel umum — harga psikologis klasik |
| **Harga Menarik Akhiran .95** | $20.50 → $19.95 | Alternatif sedikit lebih lembut dari .99 |
| **Harga Menarik Akhiran .90** | $20.50 → $19.90 | Terasa bulat tetapi masih di bawah dolar berikutnya |
| **Bulatkan ke Bawah** | $19.50 → $19.00 | Toko yang lebih suka angka bulat |
| **Bulatkan ke Atas** | $19.50 → $20.00 | Bulatkan sedikit untuk tampilan bersih |
| **Bulatkan ke 5 Terdekat** | $23.00 → $25.00 | Toko ritel dan pasar dengan lalu lintas tinggi |
| **Bulatkan ke 10 Terdekat** | $23.00 → $20.00 | Barang berharga tinggi seperti peralatan rumah tangga |
| **Bulatkan ke 100 Terdekat** | $1,234 → $1,200 | Barang bernilai tinggi seperti furnitur atau elektronik |
| **Akhiran Khusus** | Sembarang — tentukan di bawah | Ketika merek Anda menggunakan akhiran tertentu seperti `.88` |

### Akhiran Khusus

Jika Anda memilih **Akhiran Khusus**, masukkan nilai akhiran di bidang **Akhiran Khusus**. Misalnya, masukkan `0.88` untuk membuat semua harga berakhir dengan `.88` (umum di beberapa pasar Asia).

## Ambang batas harga minimum

Gunakan bidang **Ambang Batas Harga Minimum** untuk melewatkan harga menarik untuk item berharga sangat rendah di mana penyesuaian akan terlihat aneh. Misalnya, menetapkan ambang batas `5.00` berarti produk yang harganya di bawah $5 akan ditampilkan dengan harga yang dihitung sebenarnya tanpa penerapan harga menarik.

Biarkan tetap pada `0` untuk menerapkan harga menarik pada semua harga.

## Harga diskon

Secara default, harga menarik diterapkan pada harga normal dan harga diskon. Jika Anda ingin harga diskon Anda menampilkan nilai yang dihitung secara eksak (berguna untuk harga promosi terbatas waktu di mana angka eksak penting), hilangkan centang **Terapkan pada Harga Diskon**.

## Menonaktifkan aturan

Untuk sementara menghentikan harga menarik tanpa menghapus aturan, hilangkan centang **Aktif** dan simpan. Aturan tetap disimpan dan dapat diaktifkan kembali kapan saja.

## Tips

Jaga semua format markdown, jalur gambar, blok kode, dan istilah teknis.

- Mulai dengan akhiran .99 jika Anda tidak yakin — ini adalah teknik penentuan harga psikologis yang paling dikenal dan bekerja dengan baik untuk sebagian besar jenis produk.
- Tetapkan ambang batas minimum jika Anda menjual barang berharga rendah (di bawah $5) agar barang seharga $3.50 tidak turun menjadi $2.99.
- Periksa harga Anda setelah mengaktifkan aturan baru dengan melihat produk di toko online — harga yang telah diubah akan ditampilkan secara real time.
- Yen Jepang dan mata uang bulat serupa bekerja terbaik dengan **Bulatkan ke 10 terdekat** atau **Bulatkan ke 100 terdekat**, karena akhiran desimal terlihat tidak biasa.
- Penyesuaian harga dilakukan setelah semua diskon dan promosi, sehingga harga diskon Anda juga akan terlihat telah diubah kecuali Anda menghilangkan centang pada **Terapkan ke Harga Diskon**.
- Anda dapat memiliki jenis aturan yang berbeda untuk mata uang yang berbeda, yang berguna jika Anda menjual ke pasar dengan konvensi harga yang berbeda.