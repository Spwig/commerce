---
title: Audiences
---

Sebuah **Segment** adalah daftar audiens yang disimpan yang dapat Anda tuju dengan kampanye, perjalanan, atau uji coba A/B — daftar Segment khas Campaign Studio menyebutnya sebagai 'Audien yang ditargetkan', dan panduan ini menggunakan kedua kata tersebut untuk hal yang sama. Setiap segment bisa berupa **dinamis**, yang didefinisikan oleh aturan yang Spwig evaluasi ulang setiap kali digunakan, atau **statis**, daftar pelanggan yang Anda pilih secara manual.

Panduan ini mencakup pembuatan aturan segment dinamis — termasuk bidang-bidang terbaru yang menargetkan bucket nilai pelanggan toko Anda sendiri, program loyalitas, dan afiliasi — serta tombol **Tambahkan audiens awal** satu klik yang membangun sekumpulan segment siap pakai dari data apa pun yang sudah dimiliki toko Anda.

## Segment Dinamis vs. Statis

| Jenis | Bagaimana cara kerjanya | Paling cocok untuk |
|---|---|---|
| **Dinamis (aturan)** | Anda menentukan kondisi — misalnya, "Total pengeluaran minimal $500." Spwig menghitung ulang siapa yang sesuai setiap kali segment digunakan, sehingga keanggotaan berubah secara otomatis seiring perubahan pelanggan Anda. | Audiens berkelanjutan yang selalu mutakhir, seperti "Pelanggan VIP" atau "Belum memesan dalam 90 hari." |
| **Statis (daftar tetap)** | Daftar eksplisit pelanggan yang Anda tambahkan atau hapus secara manual. Keanggotaan tidak pernah berubah kecuali Anda yang mengubahnya. | Daftar satu kali — semua dari acara tertentu, atau kelompok yang dipilih secara manual untuk pengiriman satu kali. |

Pilih jenis dengan bidang **Jenis** saat Anda membuat segment. Sisanya dari panduan ini tentang segment dinamis — yang statis hanyalah daftar anggota dengan tidak ada aturan yang perlu dikonfigurasi.

## Membangun segment dinamis

Buka **Campaign Studio > Segmen**, lalu klik **+ Buat Segment Baru** (atau buka segment dinamis yang sudah ada) untuk sampai ke **pengatur aturan audiens**. Klik **+ Tambahkan kondisi** untuk menambahkan aturan, pilih apa yang akan dicek dan bagaimana, lalu atur apakah seorang pelanggan harus memenuhi **semua** atau **salah satu** dari kondisi Anda. Hitungan hidup di sudut kanan atas — misalnya, "8 pelanggan yang sesuai" — akan diperbarui segera setelah setiap perubahan, sehingga Anda dapat melihat siapa saja yang memenuhi syarat sebelum menyimpannya.

![Pembuat aturan audiens dengan kondisi segment pelanggan, tingkat loyalitas, nilai seumur hidup, dan afiliasi diatur, serta hitungan pelanggan yang sesuai secara langsung](/static/core/admin/img/help/audiences/rule-builder-new-fields.webp)

Sebuah kondisi dengan pemeriksaan **is true** yang tetap — **Sudah memesan**, **Mengizinkan pemasaran**, **Anggota loyalitas**, **Afiliasi** — tidak memerlukan apa pun selain memilih bidang itu sendiri; tidak ada operator atau nilai yang perlu diatur.

## Apa yang bisa ditargetkan

| Bidang | Apa yang dicek |
|---|---|
| **Total pengeluaran** | Total pesanan seumur hidup. |
| **Jumlah pesanan** | Jumlah pesanan yang selesai. |
| **Nilai seumur hidup** | Nilai seumur hidup yang dihitung pelanggan. |
| **Rata-rata nilai pesanan** | Jumlah rata-rata per pesanan yang selesai. |
| **Hari sejak pesanan terakhir** | Seberapa lama sejak pesanan terbaru pelanggan — targetkan 90+ hari untuk audiens yang ingin dikembalikan. |
| **Sudah memesan** | Apakah pelanggan memiliki setidaknya satu pesanan yang selesai. |
| **Mengizinkan pemasaran** | Apakah pelanggan telah menyetujui email pemasaran. |
| **Bahasa** | Bahasa yang tersimpan pelanggan. |
| **Sumber** | Bagaimana pelanggan bergabung — pendaftaran toko, impor, pesanan, ditambahkan secara manual, atau API. |
| **Bergabung setelah** | Pelanggan yang bergabung pada atau setelah tanggal tertentu. |
| **Membawa tag** | Apakah pelanggan memiliki [tag](/help/subscriber-tags) yang telah Anda buat. |
| **Segment pelanggan** | Apakah pelanggan termasuk ke dalam salah satu segment pelanggan yang diberi nama oleh toko Anda sendiri — Pelanggan Tamu, Pelanggan Baru, Pelanggan Rutin, Pembeli Frekuensi Tinggi, Pelanggan Nilai Tinggi, Pelanggan VIP, Pencari Diskon, Pelanggan yang Berisiko, atau Pelanggan Tidak Aktif. |
| **Anggota loyalitas** | Apakah pelanggan adalah anggota aktif dari program loyalitas Anda. |
| **Poin loyalitas** | Jumlah poin yang tersedia saat ini bagi anggota. |
| **Tingkat loyalitas** | Tingkat loyalitas mana yang saat ini dimiliki anggota. |
| **Afiliasi** | Apakah pelanggan adalah mitra afiliasi aktif Anda.

**Segment pelanggan**, dua bidang nilai **Loyalitas** ini, **Tingkat Loyalitas**, dan **Afiliasi** adalah penambahan yang lebih baru, dan masing-masing hanya muncul di pemilih kondisi sekali toko Anda benar-benar memiliki jenis data ini: bidang loyalitas muncul sekali program loyalitas Anda memiliki anggota dan setidaknya satu tingkat aktif, **Afiliasi** muncul sekali Anda memiliki setidaknya satu afiliasi, dan **Segment pelanggan** muncul sekali Anda memiliki setidaknya satu segment pelanggan aktif yang dikonfigurasi.

Anda tidak akan melihat opsi pada toko yang baru yang pasti tidak mungkin cocok dengan siapa pun.

Satu batasan saat ini yang perlu diketahui: untuk setiap kondisi dengan daftar pilihan — **Bahasa**, **Sumber**, **Memiliki tag**, **Segment pelanggan**, **Tingkat Loyalitas** — operator **adalah salah satu dari** masih hanya memungkinkan Anda memilih satu nilai pada satu waktu. Jika Anda ingin cocokkan beberapa (misalnya, pelanggan di VIP atau segment nilai tinggi), tambahkan satu kondisi per nilai dan atur **Match** menjadi **salah satu**.

## Tambahkan audiens awal

Membuat aturan dari nol untuk setiap audiens yang jelas — VIP Anda, anggota loyalitas, semua orang yang sudah bungkam — memakan waktu lama ketika Spwig sudah bisa melihat siapa pun yang memenuhi syarat. Di daftar Segment, klik **Tambahkan audiens awal** dan Spwig membuat sejumlah segment dinamis siap pakai, yang dapat diedit dari data pelanggan, loyalitas, dan afiliasi apa pun yang sudah dimiliki toko Anda.

![Daftar Segment dengan tombol New Segment dan Add starter audiences](/static/core/admin/img/help/audiences/segments-changelist.webp)

| Starter | Target | Kebutuhan |
|---|---|---|
| **Pelanggan VIP** | Segment pelanggan VIP Anda | Segment pelanggan VIP aktif |
| **Pelanggan bernilai tinggi** | Segment pelanggan VIP dan Nilai Tinggi Anda | Segment pelanggan VIP atau Nilai Tinggi aktif |
| **Pembeli berulang** | Segment pelanggan Frequent Buyer dan Regular Anda | Segment pelanggan Frequent Buyer atau Regular aktif |
| **Pelanggan baru** | Segment pelanggan baru Anda | Segment pelanggan baru aktif |
| **Pelanggan yang kehilangan minat** | Pelanggan yang pernah memesan tetapi tidak dalam 90 hari terakhir | Riwayat pesanan pelanggan apa pun |
| **Anggota loyalitas** | Semua orang yang aktif dalam program loyalitas Anda | Program loyalitas aktif dengan anggota |
| **Tingkat loyalitas teratas** | Anggota di tingkat loyalitas tertinggi Anda | Setidaknya satu tingkat loyalitas aktif |
| **Afiliasi** | Mitra afiliasi aktif Anda | Setidaknya satu afiliasi |

Spwig hanya membuat starter yang benar-benar memiliki data untuknya — toko yang tidak memiliki program loyalitas sama sekali tidak akan mendapatkan starter **Anggota loyalitas**, melainkan yang kosong yang tidak per mai akan cocok dengan siapa pun. Spwig memastikan tepat apa yang ditambahkannya, misalnya: "Menambahkan 7 audiens starter: Pelanggan bernilai tinggi, Pembeli berulang, Pelanggan baru, Pelanggan yang kehilangan minat, Anggota loyalitas, Tingkat loyalitas teratas, Afiliasi."

![Pesan keberhasilan yang memastikan audiens starter mana yang baru saja ditambahkan](/static/core/admin/img/help/audiences/starter-audiences-added.webp)

Aman untuk mengklik **Tambahkan audiens awal** lebih dari sekali. Spwig tidak per mai membuat duplikat starter yang sudah ada, jadi mengkliknya lagi setelah menyiapkan (misalnya) program loyalitas Anda yang pertama hanya menambahkan apa pun yang baru tersedia — jika semuanya sudah disiapkan, itu hanya akan mengatakannya.

![Pesan informasi yang ditampilkan ketika setiap audiens starter sudah ada](/static/core/admin/img/help/audiences/starter-audiences-already-set-up.webp)

Jika Anda menghapus starter yang tidak diinginkan, mengklik **Tambahkan audiens awal** lagi tidak akan mengembalikannya — Spwig menganggapnya sebagai segment yang sengaja Anda hapus, bukan yang akan dibuat ulang.

Sesudah disemai, sebuah starter adalah segment dinamis biasa: buka dari daftar untuk meninjau atau menyesuaikan aturannya, ganti namanya, atau hapus, persis seperti segment yang Anda buat sendiri.

## Siapa saja yang sebenarnya dicakup oleh audiens ini

Kondisi pelanggan, loyalitas, dan afiliasi di atas hanya cocok dengan pelanggan yang emailnya terhubung ke akun pelanggan — pendaftaran newsletter anonim tidak akan cocok dengan kondisi **Anggota loyalitas** atau **VIP**, bahkan secara benar, karena Spwig tidak memiliki riwayat pesanan atau loyalitas untuk mencocokkannya.

Jika banyak pelanggan Anda memiliki akun tetapi belum berlangganan, minta siapa pun yang mengelola instalasi Spwig Anda untuk menjalankan sinkronisasi pelanggan — ini membuat rekaman Pelanggan untuk setiap akun pelanggan yang ada dalam satu langkah, sehingga audiens ini memiliki orang-orang nyata untuk dicocokkan.

Berapa pun jumlah pelanggan yang dihitung oleh segmen, angka tersebut menggambarkan siapa yang *bisa* menerima kampanye, bukan siapa yang akan menerimanya. Setiap pengiriman tetap memeriksa persetujuan pemasaran masing-masing pelanggan terlebih dahulu, sehingga segmen tidak pernah menjadi cara untuk mengabaikannya.

## Tips

- Mulai dari audiens awal dan sesuaikan alih-alih membangun aturan yang sama secara manual — setelah dibuat, audiens awal tidak berbeda dari segmen mana pun yang Anda buat sendiri.
- Kondisi boolean seperti **Anggota loyalitas**, **Afiliasi**, dan **Pernah memesan** tidak memerlukan operator atau nilai — cukup tambahkan kondisinya dan Anda selesai.
- Gabungkan bidang yang lebih baru dengan yang asli untuk penargetan yang lebih ketat, misalnya **Anggota loyalitas** ditambah **Bergabung dengan pemasaran**, alih-alih mengandalkan satu kondisi saja.
- Jika aturan segmen merujuk pada sesuatu yang telah dihapus — segmen pelanggan yang dihapus, tag yang dikosongkan, dan sebagainya — Spwig memperlakukannya sebagai tidak cocok dengan siapa pun alih-alih kembali ke daftar pelanggan Anda secara keseluruhan. Penargetan yang rusak mengurangi pengiriman; tidak pernah mengirim ke semua orang secara tidak sengaja.
- Jika jumlah anggota segmen terlihat kedaluwarsa, buka dan simpan lagi, atau gunakan tindakan massal **Bangun ulang jumlah anggota** dari daftar Segmen, untuk menghitungnya kembali segera.
- Perhatikan jumlah "pelanggan yang cocok" secara langsung saat Anda membangun aturan — ini adalah cara tercepat untuk menangkap kondisi yang lebih sempit (atau lebih luas) dari yang Anda maksud sebelum Anda menyimpan.