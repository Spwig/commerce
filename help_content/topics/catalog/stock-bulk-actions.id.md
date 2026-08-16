---
title: Tindakan Persediaan Secara Massal
---

Selain penyesuaian satu kali, Spwig memberi Anda tiga tindakan massal pada daftar **Barang Persediaan** untuk pekerjaan inventaris yang terjadi pada banyak produk sekaligus: memindahkan persediaan antar gudang, menulis ulang unit yang rusak atau hilang, dan menyeimbangkan persediaan setelah penghitungan fisik. Ketiga tindakan ini dijalankan dari dropdown **Tindakan** yang sama, menerapkan jumlah yang sama pada setiap item persediaan yang Anda pilih, dan sepenuhnya direkam dalam jejak audit pergerakan persediaan.

Navigasi ke **Produk > Barang Persediaan** untuk menggunakannya.

## Menjalankan tindakan persediaan secara massal

1. Di daftar **Barang Persediaan**, gunakan filter atau pencarian untuk menemukan item yang ingin Anda perbarui
2. Centang kotak di sebelah setiap item persediaan untuk memasukkan (atau gunakan kotak centang bagian atas untuk memilih semua item di halaman ini)
3. Pilih salah satu dari tiga tindakan dari dropdown **Tindakan**:
   - **Alihkan persediaan ke gudang**
   - **Catat persediaan yang rusak/hilang**
   - **Hitung ulang persediaan (penghitungan fisik)**
4. Klik **Pergi**
5. Tinjau halaman konfirmasi — halaman ini mendaftar setiap item persediaan yang dipilih dengan jumlah **tersedia**, **dialokasikan**, dan **tersedia** saat ini sehingga Anda dapat memeriksa kembali apakah Anda memilih item yang benar
6. Isi formulir tindakan tersebut (lihat di bawah ini) dan klik tombol kirim untuk menerapkannya

![Daftar Barang Persediaan dengan dropdown Tindakan Massal terbuka, menunjukkan Alihkan persediaan ke gudang, Catat persediaan yang rusak/hilang, dan Hitung ulang persediaan (penghitungan fisik) bersama tindakan lainnya](/static/core/admin/img/help/stock-bulk-actions/stock-items-actions-dropdown.webp)

Jumlah yang Anda masukkan sama-sama diterapkan pada **setiap** item yang dipilih — ini dirancang untuk memindahkan, menulis ulang, atau menghitung ulang jumlah unit yang sama di banyak SKU sekaligus (misalnya, memindahkan 10 unit beberapa produk ke lokasi toko baru). Untuk satu item dengan jumlah yang berbeda, jalankan tindakan tersebut kembali dengan hanya item tersebut yang dipilih, atau gunakan ** Sesuaikan tingkat persediaan** sebagai gantinya.

## Alihkan persediaan ke gudang

Gunakan ini untuk memindahkan persediaan yang tersedia dari masing-masing item ke gudang yang berbeda — misalnya, restok toko ritel baru dari gudang utama Anda, atau menyeimbangkan inventaris antar pusat pemenuhan regional.

Di halaman konfirmasi, isi:

| Kolom | Keterangan |
|-------|-------------|
| **Gudang tujuan** | Di mana persediaan harus dipindahkan. Hanya gudang aktif yang ditampilkan dalam daftar ini. |
| **Jumlah per item** | Unit yang akan dipindahkan dari gudang saat ini masing-masing item yang dipilih. |
| **Alasan** | Catatan opsional, misalnya "Restok toko Auckland baru". |

Klik **Alihkan Persediaan** untuk menerapkan.

![Halaman konfirmasi Alihkan Persediaan: kartu Barang Persediaan yang Dipilih yang mendaftar tiga item dengan angka tersedia/teralokir/tersedia, dan formulir Detail Alihkan dengan gudang tujuan, jumlah, dan alasan yang diisi](/static/core/admin/img/help/stock-bulk-actions/transfer-stock-confirmation.webp)

**Hanya persediaan yang tidak terpakai yang bisa dipindahkan.** Spwig mengalihkan dari persediaan *tersedia* (tersedia dikurangi unit yang dialokasikan untuk pesanan terbuka) — unit yang sudah dipesan pelanggan tetap berada di gudang sumber sehingga pesanan tersebut tetap dapat dipenuhi. Jika suatu item yang dipilih tidak memiliki persediaan tersedia yang cukup untuk menutupi jumlah yang Anda masukkan, item tersebut akan dilewati dan pesan kesalahan yang menjelaskan alasannya; bagian lain dari pilihan tetap dipindahkan.

Jika suatu item yang dipilih sudah tersedia di gudang tujuan yang Anda pilih, itu akan dilewati secara otomatis (tidak ada yang perlu dipindahkan ke dirinya sendiri), dan Anda akan melihat pesan yang memberi tahu Anda berapa banyak item yang dilewati karena alasan ini.

Setiap transfer menulis pasangan gerakan ke jejak audit — entri negatif **Pergeseran Gudang** di sumber dan yang positif yang sesuai di tujuan — sehingga jejak lengkap menunjukkan secara tepat dari mana persediaan itu berasal dan ke mana ia pergi.

## Catat persediaan yang rusak/hilang

Gunakan ini untuk menulis ulang unit yang rusak, rusak, atau hilang — misalnya, setelah menemukan barang rusak dalam pengiriman atau menyelidiki ketidaksesuaian.

Di halaman konfirmasi, isi:

| Field | Description |
|-------|-------------|
| **Jumlah yang ditulis ulang (per item)** | Unit yang dikeluarkan dari stok on-hand untuk setiap item yang dipilih. |
| **Alasan** | Catatan opsional, misalnya "Kerusakan akibat air selama penyimpanan". |

Klik **Catat Penulisan Ulang** untuk menerapkan.

**Stok yang dialokasikan tidak bisa ditulis ulang.** Stok on-hand tidak per maih turun di bawah jumlah yang saat ini dialokasikan untuk pesanan terbuka — Spwig memblokir penulisan ulang untuk setiap item di mana jumlah yang Anda masukkan akan mengurangi stok yang dialokasikan, sehingga Anda tidak bisa secara tidak sengaja meninggalkan pesanan yang dibayar tanpa stok untuk memenuhinya. Jika terjadi demikian untuk suatu item, Anda akan melihat pesan kesalahan yang menyebutkan item tersebut dan berapa banyak unit yang sebenarnya tersedia untuk ditulis ulang.

Setiap penulisan ulang dicatat sebagai **Kerusakan/Kehilangan** pergerakan pada item stok tersebut, dengan jumlah negatif.

## Hitung ulang stok (hitungan fisik)

Gunakan ini setelah penghitungan stok fisik untuk menyesuaikan jumlah stok on-hand dengan apa yang baru saja Anda hitung — cara tercepat untuk menyelesaikan banyak item setelah audit gudang atau hitungan siklus.

Pada halaman konfirmasi, isi:

| Field | Deskripsi |
|-------|-------------|
| **Jumlah stok on-hand yang dihitung (per item)** | Jumlah yang baru saja Anda hitung secara fisik. On-hand diatur menjadi angka yang tepat untuk setiap item yang dipilih — tidak ditambah atau dikurangi. |
| **Alasan** | Catatan opsional, misalnya "Penghitungan stok gudang Q3". |

Klik **Terapkan Hitung Ulang** untuk menerapkan.

![Halaman konfirmasi Hitung Ulang Stok: kartu Selected Stock Items dan formulir Detail Hitung Ulang dengan jumlah stok on-hand yang dihitung dan alasan yang telah diisi](/static/core/admin/img/help/stock-bulk-actions/recount-stock-confirmation.webp)

Berbeda dengan tindakan lainnya, hitung ulang dapat memindahkan stok dalam kedua arah — naik jika Anda menghitung lebih banyak dari yang sistem harapkan, turun jika Anda menghitung lebih sedikit. Jika jumlah yang Anda masukkan lebih rendah dari jumlah yang saat ini dialokasikan untuk pesanan terbuka, Spwig tetap menerapkannya (hitungan adalah fakta, bukan sesuatu yang bisa diperdebatkan), tetapi angka **Tersedia** untuk item tersebut akan menunjukkan `0` pada daftar stok dan ikon statusnya akan berubah menjadi **Habis** — anggaplah ini sebagai tanda untuk memeriksa apakah pesanan yang terkena dampak masih bisa dipenuhi.

Setiap hitungan ulang dicatat sebagai **Penghitungan Fisik** pergerakan, dengan jumlah menunjukkan koreksi (positif atau negatif) antara angka on-hand lama dan baru.

## Melihat perubahan yang terjadi

Setiap transfer, penulisan ulang, dan penghitungan ulang dicatat dengan cara yang sama seperti perubahan stok lainnya:

- Buka item stok dan gulir ke bagian **Pergerakan Stok** untuk melihat riwayat lengkapnya
- Atau navigasi ke **Produk > Pergerakan Stok** untuk melihat pergerakan di seluruh item, yang dapat difilter berdasarkan jenisnya

Setiap entri mencatat jenis pergerakan, perubahan jumlah, angka on-hand sebelumnya dan baru, siapa yang melakukan perubahan, serta alasan yang Anda masukkan (jika ada) — jadi transfer atau penulisan ulang dalam jumlah besar sama-sama dapat dilacak seperti penyesuaian manual tunggal.

## Tips

- Jalankan **Hitung Ulang Stok** tepat setelah penghitungan stok fisik sementara angka yang dihitung masih segar — lebih mudah menangkap kesalahan ketik di halaman konfirmasi daripada menyelesaikannya nanti dari riwayat pergerakan.
- Isi selalu **Alasan** untuk penulisan ulang dan penghitungan ulang. Enam bulan dari sekarang, "Kerusakan akibat air selama penyimpanan" jauh lebih berguna dalam jejak audit daripada bidang yang kosong.
- Sebelum mentransfer stok, periksa kolom **Tersedia** pada halaman konfirmasi — sudah termasuk unit yang dialokasikan, jadi Anda akan langsung tahu apakah jumlah tertentu terlalu tinggi untuk salah satu item yang baru saja Anda pilih.
- Tindakan ini menerapkan jumlah yang sama untuk setiap item yang dipilih. Kelompokkan pemilihan Anda berdasarkan item yang benar-benar membutuhkan jumlah yang sama dipindahkan, ditulis ulang, atau dihitung ulang, dan selesaikan pengecualian satu per satu.
- Jika Anda menggunakan POS di lokasi ritel, ingatlah bahwa buffer stok gudang bukan bagian dari "tersedia" untuk pesanan online — tetapi transfer dalam jumlah besar dan penulisan ulang tetap bekerja terhadap total on-hand nyata gudang tersebut.