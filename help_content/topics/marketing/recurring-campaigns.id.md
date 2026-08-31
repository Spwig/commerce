---
title: Campaign Berkala
---

Fitur **Campaign Berkala** dari Campaign Studio memungkinkan Anda membuat sebuah newsletter sekali — misalnya ringkasan produk mingguan, atau ringkasan blog bulanan — dan membiarkan Spwig mengirimkannya secara otomatis pada jadwal berulang, alih-alih Anda membuat dan mengirim kampanye baru secara manual setiap kali.

## Perbedaan antara Penyebaran dan Berkala

Setiap kampanye di Campaign Studio memiliki **Jenis Kampanye**:

| Jenis | Perilaku |
|------|-----------|
| **Penyebaran** | Dikirim sekali — secara langsung atau pada tanggal dan waktu yang dijadwalkan. Gunakan ini untuk pengumuman, penawaran, atau email peluncuran produk yang bersifat satu kali. |
| **Berkala** | Bertindak sebagai template yang dikirim berdasarkan jadwal berulang. Setiap pengiriman adalah salinan yang diberi tanggal baru yang disebut sebagai **kejadian** — template itu sendiri tidak pernah "dikirim" secara langsung. |

Untuk mengubah sebuah kampanye menjadi bentuk berkala, buka kampanye tersebut di **Campaign Studio > Kampanye** dan atur **Jenis Kampanye** menjadi **Berkala**, lalu simpan. Bagian **Jadwal** akan muncul pada kampanye tersebut setelah Anda membukanya kembali — hanya muncul untuk kampanye berkala.

![Jenis kampanye diatur menjadi Berkala](/static/core/admin/img/help/recurring-campaigns/campaign-type-selector.webp)

## Menyetel jadwal

Sekali kampanye tersebut menjadi berkala, bagian **Jadwal**-nya mengontrol kapan kampanye tersebut diaktifkan:

| Bidang | Keterangan |
|-------|-------------|
| **Aktif** | Mengaktifkan atau menonaktifkan pengulangan tanpa menghapus jadwal. |
| **Kadens** | **Harian**, **Mingguan**, atau **Bulanan**. |
| **Interval** | Kirim setiap N satuan kadens — misalnya interval `2` dengan kadens **Mingguan** berarti setiap 2 minggu. |
| **Hari Kerja** | Hari mana yang akan dikirimkan untuk kadens mingguan (`0` = Senin ... `6` = Minggu). |
| **Hari Bulan** | Hari mana yang akan dikirimkan untuk kadens bulanan (`1`–`28`, sehingga setiap bulan memiliki hari tersebut). |
| **Waktu Pengiriman** | Waktu sehari kapan kampanye dikirimkan. |
| **Zona Waktu** | Nama zona IANA, misalnya `Europe/London` atau `America/New_York` — waktu pengiriman diinterpretasikan dalam zona ini, bukan zona server. |

![Bagian jadwal mingguan pada kampanye berkala](/static/core/admin/img/help/recurring-campaigns/schedule-section.webp)

Segera setelah Anda menyimpan jadwal yang aktif, jadwal tersebut **mengaktifkan dirinya sendiri** — Spwig menghitung waktu berikutnya dan menampilkannya di **Waktu Berikutnya**. Anda tidak perlu memicu sesuatu secara manual; tugas latar belakang memeriksa jadwal yang jatuh tempo dan mengirimkan kejadian ketika waktunya tiba. **Waktu Terakhir Dikirim** dan **Jumlah Kejadian yang Dikirim** diperbarui secara otomatis setelah setiap pengiriman sehingga Anda dapat melihat apakah jadwal tersebut aktif.

## Kebijakan Tidak Ada Konten Baru

Newsletter berkala sering kali memiliki konten dinamis — yang paling umum adalah blok **Postingan Blog** (atau **Grid Produk**) yang diatur menjadi **Baru sejak pengiriman terakhir** dalam pembuat visual, yang hanya menampilkan postingan yang diterbitkan — atau produk yang ditambahkan — sejak pengiriman kampanye sebelumnya. Hal ini menimbulkan pertanyaan yang jelas: apa yang terjadi jika pengiriman yang dijadwalkan tiba dan tidak ada konten baru yang bisa ditampilkan?

Spwig menjawab pertanyaan ini dengan **Kebijakan Tidak Ada Konten Baru**:

| Kebijakan | Apa yang terjadi | Paling cocok untuk |
|--------|---------------|----------|
| **Lewati pengiriman ini** *(default)* | Kejadian ini sepenuhnya dilewati — tidak ada yang dikirim. Jadwal langsung bergerak ke putaran berikutnya yang dijadwalkan. | Sebuah blog atau ringkasan produk, sehingga pelanggan tidak permai diberi tahu email yang hanya mengulang apa yang sudah mereka lihat. |
| **Kirim saja (lewatkan blok kosong)** | Email dikirim sesuai jadwal. Setiap blok yang tidak memiliki konten baru — seperti blok 

Halaman edit kampanye berulang mencantumkan **Riwayat kejadian** — kejadian-kejadian terbaru, masing-masing terhubung ke catatan kampanye dari kejadian tersebut sehingga Anda dapat meninjau persis apa yang dikirim dan bagaimana kinerjanya.

![Daftar riwayat kejadian pada kampanye berulang](/static/core/admin/img/help/recurring-campaigns/occurrence-history.webp)

## Tips

- Pasangkan kampanye berulang dengan blok **Blog Posts** yang diatur ke **Baru sejak pengiriman terakhir** untuk membuat ringkasan "posting baru minggu ini" yang terawat sendiri — Anda menulis posting, Spwig menangani pengirimannya.
- Mulai dengan **Lewati pengiriman ini** untuk ringkasan konten. Ini adalah default paling aman: pelanggan tidak pernah menerima pengulangan konten dari pengiriman sebelumnya.
- Hanya beralih ke **Kirim saja** jika template Anda memiliki konten lain yang layak dikirim secara mandiri, bahkan ketika blok dinamis kosong.
- Gunakan **Tahan dan kirim terlambat** ketika melewatkan satu ritme pengiriman sesekali tidak masalah, tetapi melewatkannya selama berminggu-minggu berturut-turut tidak — atur jendela tahan sesuai dengan durasi jeda yang Anda rasa nyaman.
- Periksa **Jalankan berikutnya pada** setelah menyimpan jadwal untuk memastikan jatuh pada hari dan waktu yang Anda harapkan, terutama ketika bekerja melintasi zona waktu.
- Tinjau **Riwayat kejadian** secara rutin — template yang terus melupakan pengiriman adalah tanda bahwa sumber konten dinamis Anda (misalnya blog) telah sepi.