---
title: Tindakan Persediaan Secara Massal
---

Selain penyesuaian satu kali, Spwig memberi Anda tiga tindakan massal pada daftar **Item Persediaan** untuk pekerjaan inventaris yang terjadi pada banyak produk sekaligus: memindahkan persediaan antar gudang, menulis ulang unit yang rusak atau hilang, dan menyeimbangkan persediaan setelah penghitungan fisik. Ketiga tindakan ini dijalankan dari dropdown **Tindakan** yang sama, menerapkan jumlah yang sama pada setiap item persediaan yang Anda pilih, dan sepenuhnya direkam dalam jejak audit pergerakan persediaan.

Navigasi ke **Produk > Item Persediaan** untuk menggunakannya.

## Menjalankan tindakan persediaan secara massal

1. Di daftar **Item Persediaan**, gunakan filter atau pencarian untuk menemukan item yang ingin Anda perbarui
2. Centang kotak di sebelah setiap item persediaan untuk memasukkan (atau gunakan kotak centang bagian atas untuk memilih semua item di halaman ini)
3. Pilih salah satu dari tiga tindakan dari dropdown **Tindakan**:
   - **Alihkan persediaan ke gudang**
   - **Catat persediaan yang rusak/hilang**
   - **Hitung ulang persediaan (penghitungan fisik)**
4. Klik **Jalankan**
5. Tinjau halaman konfirmasi — halaman ini mendaftar setiap item persediaan yang dipilih dengan jumlah **tersedia**, **dialokasikan**, dan **tersedia** saat ini sehingga Anda dapat memeriksa kembali apakah Anda memilih item yang benar
6. Isi formulir tindakan tersebut (lihat di bawah ini) dan klik tombol kirim untuk menerapkan

![Daftar Item Persediaan dengan dropdown Tindakan Massal terbuka, menunjukkan Alihkan persediaan ke gudang, Catat persediaan yang rusak/hilang, dan Hitung ulang persediaan (penghitungan fisik) bersama tindakan lainnya](/static/core/admin/img/help/stock-bulk-actions/stock-items-actions-dropdown.webp)

Jumlah yang Anda masukkan sama-sama diterapkan pada **setiap** item yang dipilih — ini dirancang untuk memindahkan, menulis ulang, atau menghitung ulang jumlah unit yang sama di banyak SKU sekaligus (misalnya, memindahkan 10 unit beberapa produk ke lokasi toko baru). Untuk satu item dengan jumlah yang berbeda, jalankan tindakan tersebut kembali dengan hanya item tersebut yang dipilih, atau gunakan ** Sesuaikan tingkat persediaan** sebagai gantinya.

## Alihkan persediaan ke gudang

Gunakan ini untuk memindahkan persediaan yang tersedia dari masing-masing item ke gudang yang berbeda — misalnya, restok toko ritel baru dari gudang utama Anda, atau menyeimbangkan kembali persediaan antar pusat pemenuhan regional.

Di halaman konfirmasi, isi:

| Kolom | Keterangan |
|-------|-------------|
| **Gudang tujuan** | Di mana persediaan harus dipindahkan. Hanya gudang aktif yang muncul dalam daftar ini. |
| **Jumlah per item** | Unit yang akan dipindahkan dari gudang saat ini masing-masing item yang dipilih. |
| **Alasan** | Catatan opsional, misalnya "Restok toko Auckland baru". |

Klik **Alihkan Persediaan** untuk menerapkan.

![Halaman konfirmasi Alihkan Persediaan: kartu Item Persediaan yang Dipilih yang mendaftar tiga item dengan angka tersedia/teralokir/tersedia, dan formulir Detail Alihkan dengan gudang tujuan, jumlah, dan alasan yang diisi](/static/core/admin/img/help/stock-bulk-actions/transfer-stock-confirmation.webp)

**Hanya persediaan yang tidak terpakai yang bisa dipindahkan.** Spwig mengalihkan dari persediaan *tersedia* (tersedia dikurangi unit yang dialokasikan untuk pesanan terbuka) — unit yang sudah dipesan pelanggan tetap berada di gudang sumber sehingga pesanan tersebut tetap dapat dipenuhi. Jika suatu item yang dipilih tidak memiliki persediaan tersedia yang cukup untuk menutupi jumlah yang Anda masukkan, item tersebut akan dilewati dan pesan kesalahan menjelaskan alasannya; bagian lain dari pilihan tetap dipindahkan.

Jika suatu item yang dipilih sudah tersedia di gudang tujuan yang Anda pilih, itu akan dilewati secara otomatis (tidak ada yang perlu dipindahkan ke dirinya sendiri), dan Anda akan melihat pesan yang memberi tahu Anda berapa banyak item yang dilewati karena alasan ini.

Setiap transfer menulis pasangan gerakan ke jejak audit — entri negatif **Pergeseran Gudang** di sumber dan yang positif yang sesuai di tujuan — sehingga jejak lengkap menunjukkan secara tepat dari mana persediaan itu berasal dan ke mana ia pergi.

## Catat persediaan yang rusak/hilang

Gunakan ini untuk menulis ulang unit yang rusak, rusak, atau hilang — misalnya, setelah menemukan barang rusak dalam pengiriman atau menyelidiki ketidaksesuaian.

Di halaman konfirmasi, isi:

| Field | Description |
|-------|-------------|
| **Quantity to write off (per item)** | Jumlah unit yang akan dihapus dari stok tersedia untuk setiap item yang dipilih. |
| **Reason** | Catatan opsional, misalnya "Kerusakan air selama penyimpanan". |

Klik **Record Write-off** untuk menerapkan.

**Stok yang dipesan tidak dapat dihapus.** Stok tersedia tidak pernah boleh turun di bawah jumlah yang saat ini dialokasikan untuk pesanan terbuka — Spwig memblokir penghapusan untuk item mana pun di mana jumlah yang Anda masukkan akan mengurangi stok yang dialokasikan, sehingga Anda tidak akan secara tidak sengaja meninggalkan pesanan yang sudah dibayar tanpa stok untuk melaksanakannya. Jika hal itu terjadi untuk suatu item, Anda akan melihat pesan kesalahan yang menyebutkan nama item dan berapa banyak unit yang tidak dipesan yang sebenarnya tersedia untuk dihapus.

Setiap penghapusan dicatat sebagai pergerakan **Damaged/Lost** pada item stok tersebut, dengan jumlah negatif.

## Recount stock (physical count)

Gunakan ini setelah penghitungan stok fisik untuk mengoreksi jumlah stok tersedia agar sesuai dengan yang sebenarnya Anda hitung — cara tercepat untuk menyelaraskan banyak item setelah audit gudang atau penghitungan siklus.

Di halaman konfirmasi, isi:

| Field | Description |
|-------|-------------|
| **Counted on-hand quantity (per item)** | Jumlah yang Anda hitung secara fisik. Stok tersedia diatur ke angka persis ini untuk setiap item yang dipilih — tidak ditambahkan atau dikurangkan. |
| **Reason** | Catatan opsional, misalnya "Penghitungan stok gudang Q3". |

Klik **Apply Recount** untuk menerapkan.

![The Recount Stock confirmation page: the Selected Stock Items card and a Recount Details form with the counted on-hand quantity and a reason filled in](/static/core/admin/img/help/stock-bulk-actions/recount-stock-confirmation.webp)

Berbeda dengan dua tindakan lainnya, recount dapat memindahkan stok ke arah mana pun — naik jika Anda menghitung lebih banyak dari yang diharapkan sistem, turun jika Anda menghitung lebih sedikit. Jika jumlah yang Anda masukkan lebih rendah dari jumlah yang saat ini dialokasikan untuk pesanan terbuka, Spwig tetap menerapkannya (penghitungan adalah fakta, bukan sesuatu yang bisa diperdebatkan), tetapi angka **Available** untuk item tersebut akan ditampilkan sebagai `0` pada daftar stok dan ikon statusnya akan berubah menjadi Out of Stock — perlakukan itu sebagai sinyal untuk memeriksa apakah pesanan yang terdampak masih dapat dipenuhi.

Setiap recount dicatat sebagai pergerakan **Physical Recount**, dengan jumlah yang menunjukkan koreksi (positif atau negatif) antara angka stok tersedia lama dan baru.

## Reviewing what changed

Setiap transfer, penghapusan, dan recount dicatat dengan cara yang sama seperti perubahan stok lainnya:

- Buka item stok dan gulir ke bagian **Stock Movements** untuk melihat riwayat lengkapnya
- Atau navigasi ke **Products > Stock Movements** untuk menelusuri pergerakan di semua item, dapat difilter berdasarkan tipe

Setiap entri mencatat tipe pergerakan, perubahan jumlah, angka stok tersedia sebelumnya dan baru, siapa yang melakukan perubahan, dan alasan yang Anda masukkan (jika ada) — sehingga transfer massal atau penghapusan sama telusurnya dengan penyesuaian manual tunggal.

## Tips

- Jalankan **Recount stock** segera setelah penghitungan stok fisik saat angka yang dihitung masih segar — lebih mudah menangkap kesalahan ketik di halaman konfirmasi daripada mengurai kemudian dari riwayat pergerakan.

- Selalu isi **Reason** untuk penghapusan dan recount. Enam bulan dari sekarang, "Kerusakan air selama penyimpanan" jauh lebih berguna dalam jejak audit daripada kolom kosong.

- Sebelum mentransfer stok, periksa kolom **Available** di halaman konfirmasi — ini sudah memperhitungkan unit yang dialokasikan, sehingga Anda akan segera tahu jika suatu jumlah terlalu tinggi untuk salah satu item yang Anda pilih.

- Tindakan ini menerapkan jumlah yang sama untuk setiap item yang dipilih. Kelompokkan pilihan Anda berdasarkan item yang benar-benar membutuhkan jumlah yang sama untuk dipindahkan, dihapus, atau dihitung ulang, dan tangani pengecualian satu per satu.

- Jika Anda menggunakan POS di lokasi ritel, ingat bahwa buffer stok gudang bukan bagian dari "available" untuk pesanan online — tetapi transfer massal dan penghapusan tetap bekerja terhadap total stok tersedia aktual gudang.