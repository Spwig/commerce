---
title: Pengujian A/B
---

Fitur **pengujian A/B** di Campaign Studio memungkinkan Anda mencoba dua hingga empat **varian** — versi berbeda dari kampanye yang sama — pada sebagian audiens Anda sebelum mengirim ke seluruh daftar. Anda hanya perlu mengubah baris subjek, atau merancang konten yang sepenuhnya berbeda untuk setiap varian. Spwig membagi sampel daftar Anda secara merata di antara varian-varian, memantau kinerja masing-masing, dan secara otomatis mengirim varian dengan kinerja terbaik kepada semua orang yang tidak melihat pengujian tersebut.

## Menyiapkan pengujian

Buat kampanye Anda seperti biasa di pembuat visual Campaign Studio terlebih dahulu — tulis baris subjek, rancang konten Anda, dan pilih **Segmen** yang ingin Anda jangkau. Kampanye tersebut menjadi **wadah** pengujian. Setelah Anda melampirkan pengujian A/B ke kampanye itu, wadah itu sendiri tidak pernah dikirim secara langsung — tugasnya adalah menyimpan pengaturan, dan audiens yang diatur untuk dijangkau adalah persis kumpulan yang menjadi sasaran pengujian.

Dua tempat membuka asisten pengujian A/B:

- Tombol **Pengujian A/B** di bilah alat pembuat visual.
- Ikon **Pengujian A/B** pada kartu kampanye di **Campaign Studio > Kampanye**.

Setelah pengujian ada pada kampanye, tombol yang sama akan membawa Anda langsung ke hasilnya, bukan ke asisten, dan kartu kampanye akan menampilkan lencana kecil **A/B** sehingga Anda dapat melihatnya sekilas dalam daftar.

## Apa yang akan diuji

Langkah pertama asisten menanyakan apa yang harus berbeda di antara varian:

| Opsi | Yang berubah | Diukur oleh |
|--------|--------------|-------------|
| **Baris subjek** | Setiap varian mengirim konten yang persis sama — hanya baris subjeknya yang berbeda. Pengujian yang paling umum. | Tingkat pembukaan |
| **Konten** | Setiap varian adalah desain terpisah yang Anda bangun sendiri di pembuat visual. | Tingkat klik |

![Langkah "Apa yang ingin Anda uji?", dengan Baris subjek dipilih](/static/core/admin/img/help/ab-testing/ab-test-what-to-test.webp)

## Memilih varian Anda

Yang Anda masukkan selanjutnya tergantung pada apa yang Anda pilih:

- **Baris subjek** — ketik subjek untuk setiap varian (2–4). Dua baris ditampilkan pada awalnya; klik **Tambah subjek lain** untuk yang ketiga atau keempat.
- **Konten** — cukup pilih berapa banyak varian yang Anda inginkan (2–4). Setiap varian dimulai sebagai salinan persis dari desain saat ini wadah Anda, sehingga Anda hanya perlu mengubah apa yang sedang Anda uji.

Dalam hal apa pun, Spwig memberi label varian sebagai **A**, **B**, **C**, dan **D** sesuai urutan Anda memasukkannya — Anda akan melihatnya sebagai "Varian A", "Varian B", dan seterusnya dari sini.

![Langkah Varian dengan tiga baris subjek yang dimasukkan untuk varian A, B, dan C](/static/core/admin/img/help/ab-testing/ab-test-variants.webp)

Untuk pengujian konten, Anda tidak merancang varian di dalam asisten itu sendiri — setelah Anda membuat pengujian, kartu setiap varian di pusat hasil mendapatkan ikon pensil kecil yang membukanya di pembuat visual yang sama yang Anda gunakan untuk wadah. Ini hanya tersedia selama pengujian masih dalam **Draf**; begitu Anda memulai pengujian, desain dikunci sehingga apa yang Anda ukur tidak berubah di tengah pengujian.

## Pengaturan pengujian

Langkah terakhir asisten mencakup cara pengujian dijalankan dan diputuskan:

| Pengaturan | Apa yang dilakukannya |
|---------|--------------|
| **Sampel pengujian** | Bagian dari audiens Anda yang digunakan untuk pengujian, dibagi merata di antara varian: 20%, 30%, 50%, atau 100%. Sisanya — **holdout** — menerima pemenang setelahnya. Memilih 100% menguji seluruh daftar Anda sekaligus, sehingga tidak ada holdout yang tersisa untuk mengirim pemenang. |
| **Pemenang ditentukan oleh** | **Tingkat pembukaan** atau **Tingkat klik**. Bawaan adalah tingkat pembukaan untuk pengujian baris subjek dan tingkat klik untuk pengujian konten, karena itulah yang sebenarnya diukur masing-masing — tetapi Anda dapat mengubahnya ke arah mana pun. |
| **Jendela pengujian (jam)** | Berapa lama untuk mengumpulkan pembukaan dan klik sebelum memilih pemenang, dari 1 hingga 168 jam (satu minggu penuh). |
| **Kirim pemenang secara otomatis ke sisa audiens** | Aktif secara bawaan. Saat dicentang, Spwig mengirim email varian pemenang ke holdout segera setelah jendela berakhir, tanpa tindakan lebih lanjut dari Anda. |

Kartu ringkasan singkat di bagian bawah merangkum pilihan Anda sebelum Anda mengonfirmasi.

![Langkah Pengaturan dengan opsi sampel, metrik, jendela, dan kirim otomatis yang diatur, serta kartu tinjauan](/static/core/admin/img/help/ab-testing/ab-test-settings.webp)

## Memulai tes

Klik **Buat tes** untuk menyimpan pengaturan — ini belum mengirim apa pun. Anda akan berada di pusat hasil tes dengan status **Draft**, menampilkan setiap varian dengan nol penerima sejauh ini dan dua tombol: **Mulai tes** dan **Batal tes**.

![Tes yang baru dibuat dalam status Draft, menampilkan tiga varian yang siap dimulai](/static/core/admin/img/help/ab-testing/ab-test-draft.webp)

Klik **Mulai tes** ketika Anda siap. Spwig membagi sampel tes Anda secara merata di antara varian dan mengirim email ke masing-masing segera — Anda tidak perlu melakukan apa pun lagi; tugas latar belakang akan memeriksa setelah jendela tes berakhir dan menentukan pemenangnya secara otomatis. Status kampanye kontainer itu sendiri tetap **Draft** selama seluruh proses ini — itu wajar, karena varian (dan kemudian pemenangnya) yang sebenarnya dikirim, bukan kontainernya.

Audiens Anda harus cukup besar agar setiap varian mendapatkan jumlah penerima yang bermakna. Spwig akan memblokir memulai tes jika ada varian yang berakhir dengan nol orang, tetapi tes yang benar-benar layak dibaca membutuhkan lebih dari sekadar minimum — usahakan beberapa ratus penerima atau lebih sebelum mengandalkan hasilnya.

## Selama tes berjalan

Setelah dimulai, pusat beralih ke **Testing** dan menampilkan "Tes berjalan — pemenang ditentukan secara otomatis sekitar" tanggal dan waktu jendela berakhir. Jumlah penerima dan tingkat buka/klik langsung diperbarui setiap kali Anda mengunjungi, disertai grafik batang yang membandingkan tingkat buka dan tingkat klik setiap varian berdampingan — bukan hanya metrik yang Anda pilih untuk menentukan pemenang.

![Tes yang sedang berjalan menampilkan jumlah penerima langsung, tingkat buka/klik, dan grafik perbandingan](/static/core/admin/img/help/ab-testing/ab-test-running.webp)

Anda juga dapat memantau setiap tes dari **Dasbor Campaign Studio**: panel *Tes A/B Terbaru*-nya mencantumkan tes Anda yang sedang berjalan dan baru saja ditentukan — masing-masing dengan tingkat kepercayaannya sekilas — dan tautan langsung ke hasilnya, berdampingan dengan kartu yang menghitung berapa banyak tes yang sedang berjalan dan berapa banyak yang ditentukan dalam 30 hari terakhir.

## Membaca hasil

Ketika jendela tes berakhir, Spwig memilih varian dengan tingkat tertinggi pada metrik yang Anda pilih, menandai tes **Complete**, dan — jika **Kirim pemenang secara otomatis** dicentang dan ada holdout untuk dikirim — mengirim email varian tersebut ke semua orang yang bukan bagian dari tes. Kartu varian pemenang diberi garis luar dan membawa lencana **Winner**; grafik perbandingan tetap di tempatnya sehingga Anda dapat melihat bagaimana varian dibandingkan.

![Tes yang selesai dengan varian pemenang yang disorot dan lencana Winner](/static/core/admin/img/help/ab-testing/ab-test-complete.webp)

Perhatikan bahwa angka di halaman ini selalu untuk sampel tes, bukan seluruh daftar Anda — dengan sampel 20%, Anda membaca bagaimana seperlima audiens Anda merespons, bukan semua orang.

## Seberapa yakin hasilnya?

Tingkat buka atau klik yang lebih tinggi tidak selalu berarti sebuah varian benar-benar lebih baik — dengan audiens kecil, satu varian bisa keluar sebagai pemenang murni karena kebetulan. Jadi di samping pemenang, Spwig menunjukkan **seberapa yakin bahwa hasilnya nyata**, berdasarkan besarnya selisih dan jumlah penerima. Anda akan melihat salah satu dari tiga pembacaan:

- **Hasil yang jelas** — Spwig setidaknya 95% yakin bahwa varian yang memimpin benar-benar mengalahkan yang lain. Ini adalah hasil yang dapat Anda tindak lanjuti.
- **Terlalu ketat untuk ditentukan** — ada pemimpin, tetapi selisihnya cukup kecil sehingga bisa jadi kebetulan. Persentase yang ditampilkan adalah seberapa yakin Spwig, di bawah ambang 95%. Pertimbangkan untuk menjalankan ulang dengan audiens yang lebih besar atau jendela tes yang lebih lama sebelum menarik kesimpulan.
- **Belum cukup data** — terlalu sedikit penerima (atau terlalu sedikit buka dan klik) untuk membedakan varian sama sekali. Ini umum terjadi pada daftar kecil; kembangkan audiens atau biarkan tes berjalan lebih lama.


[![Hasil uji coba yang selesai menunjukkan hasil yang jelas — variasi pemenang memiliki badge kepercayaan dan ringkasan membaca "jelas secara statistik"](/static/core/admin/img/help/ab-testing/ab-test-confidence.webp)

Bacaan yang sama muncul saat uji coba sedang berlangsung, sehingga Anda dapat memantau hasilnya menjadi lebih pasti — atau tidak — sebelum jendela berakhir. Karena kepercayaan sangat bergantung pada ukuran audiens, inilah alasan praktis untuk menargetkan beberapa ratus atau lebih penerima per uji coba: pada daftar yang sangat kecil, bahkan perbedaan yang terlihat besar biasanya akan terbaca sebagai "terlalu dekat untuk diputuskan".

Catatan bahwa ketika pengiriman otomatis aktif, Spwig tetap mengirimkan variasi dengan tingkat tertinggi kepada sisa audiens Anda bahkan jika hasilnya tidak menentu — pembacaan kepercayaan ada untuk memberi tahu Anda seberapa besar kepercayaan Anda terhadap hasilnya, bukan untuk menghentikan pengiriman.

## Membatalkan uji coba

**Batalkan uji coba** tersedia saat uji coba dalam status **Draf** atau **Pengujian**, dan menghentikannya tanpa ada pemenang yang pernah dikirimkan. Tersedia untuk situasi ketika Anda berubah pikiran atau membuat kesalahan dalam pengaturan — bukan sesuatu yang digunakan secara sembarangan, karena sekali uji coba dibatalkan (atau selesai secara normal), tidak ada tombol untuk membuat yang baru pada kampanye yang sama. Jika Anda ingin melakukan perbandingan lain di masa depan, buat kampanye baru.

## Tips

- Mulailah dengan uji coba **Subjek** — ini yang paling mudah dibuat dan alasan paling umum untuk melakukan A/B test.
- Gunakan uji coba **Konten** ketika Anda ingin membandingkan desain atau tawaran yang benar-benar berbeda, bukan hanya perbedaan kata-kata pada subjek.
- Selesaikan desain setiap variasi dari uji coba konten — dengan menggunakan ikon pensil pada setiap kartu — sebelum mengklik **Mulai Uji Coba**. Anda tidak bisa mengedit desain variasi setelah uji coba berjalan.
- Pertahankan **Contoh Uji Coba** di bawah 100% jika Anda ingin Spwig secara otomatis mengirimkan pemenang kepada sisa daftar setelahnya — pada 100% tidak ada kelompok yang ditahan untuk dijangkau.
- Beri waktu jendela uji coba cukup agar mencakup kebiasaan membaca pelanggan Anda (24 jam secara nyaman mencakup satu hari penuh zona waktu dan kotak masuk) daripada menentukan pemenang hanya dari satu atau dua jam pertama.