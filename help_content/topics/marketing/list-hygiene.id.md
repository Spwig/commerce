---
title: Kebersihan Daftar dan Penekanan
---

Setiap alamat email yang mengalami pantulan keras (hard-bounce), menandai email Anda sebagai spam, atau berulang kali gagal menerima pesan Anda menempatkan sisa daftar Anda pada risiko — penyedia kotak surat menilai reputasi pengirim Anda berdasarkan seberapa bersih pengiriman Anda, dan daftar yang kotor berarti lebih banyak *setiap* kampanye yang mendarat di spam. Campaign Studio melindungi Anda dari hal ini secara otomatis dengan **kebersihan daftar**: ia memantau alamat yang tidak dapat dikirim dan yang mengeluh, serta menghentikan pengiriman email pemasaran kepada mereka, tanpa perlu pengaturan apa pun dari sisi Anda.

Ini berbeda dari pembatalan berlangganan (unsubscribe). Alamat yang telah membatalkan berlangganan telah menarik persetujuan; alamat yang **ditekan (suppressed)** adalah alamat yang telah dipelajari oleh Spwig sebagai tidak aman atau tidak mungkin untuk terus dikirimkan, terlepas dari persetujuannya.

## Bagaimana alamat ditekan

Spwig menambahkan alamat ke **Daftar Penekanan (Suppression list)** secara otomatis ketika:

| Pemicu | Artinya |
|---------|---------------|
| **Pantulan keras (Hard bounce)** | Alamat tidak ada, atau domain menolak menerima email untuknya — tidak dapat dikirim secara permanen. |
| **Keluhan spam** | Penerima menandai email Anda sebagai spam atau sampah. |
| **Pantulan lunak berulang (Repeated soft bounces)** | Alamat mengalami pantulan lunak (kotak surat penuh, server sementara tidak tersedia) 5 kali dalam jendela 30 hari berjalan. Satu pantulan lunak diperlakukan sebagai gangguan sementara dan diabaikan — hanya pola kegagalan berulang yang memicu penekanan. |
| **Diblokir secara manual** | Anda menambahkan alamat tersebut sendiri. |

Setelah sebuah alamat ditekan, Spwig segera menghentikan pengiriman **kampanye** atau email **perjalanan (journey)** lebih lanjut ke alamat tersebut — tidak ada tindakan lain yang diperlukan dari Anda.

## Dari mana sinyal berasal

Spwig dapat mengetahui tentang pantulan atau keluhan dari beberapa tempat yang berbeda, yang ditampilkan sebagai **Sumber (Source)** pada setiap alamat yang ditekan:

- **Ditolak saat pengiriman** — server email Anda menolak alamat tersebut segera ketika Spwig mencoba mengirim ke sana.
- **Webhook penyedia** — jika Anda telah menghubungkan penyedia email (seperti SendGrid, Amazon SES, Mailgun, atau Postmark), penyedia tersebut melaporkan pantulan dan keluhan kembali ke Spwig saat terjadi.
- **Gerbang email (Mail gateway)** — jika toko Anda mengirim melalui gerbang email yang di-hosting oleh Spwig, Spwig menarik laporan pantulan dari gerbang tersebut atas nama Anda.
- **Ditambahkan secara manual** — Anda memasukkan alamat tersebut sendiri dari admin.

Anda tidak perlu mengonfigurasi apa pun untuk mendapatkan manfaat dari ini — dengan cara apa pun Anda mengirim email, Spwig memantau kegagalan dan menjaga daftar Anda tetap bersih.

## Dasbor Campaign Studio

Buka **Campaign Studio** dan cari kartu **Alamat yang ditekan (Suppressed addresses)**. Kartu ini menunjukkan total jumlah alamat yang saat ini ditekan, plus berapa banyak yang baru dalam 30 hari terakhir. Klik kartu untuk membuka daftar Penekanan (Suppressions) lengkap.

![Kartu statistik Alamat yang ditekan di dasbor Campaign Studio, menampilkan total dan jumlah "baru dalam 30 hari terakhir"](/static/core/admin/img/help/list-hygiene/dashboard-suppressed-card.webp)

Jumlah yang terus meningkat adalah hal yang normal — setiap daftar mengakumulasi beberapa alamat buruk seiring waktu karena orang-orang berganti pekerjaan, menutup akun, atau meninggalkan kotak masuk. Lonjakan tiba-tiba layak diselidiki; lihat [Email Outbox](email-outbox) untuk memeriksa apakah pengiriman tertentu mengalami jumlah kegagalan yang tidak biasa.

## Daftar Penekanan (Suppressions)

Klik untuk masuk ke **Penekanan (Suppressions)** untuk melihat setiap alamat yang ditekan, mengapa ia ditekan, dan dari mana sinyal berasal.

![Daftar Penekanan yang menampilkan alamat yang ditekan dengan kolom Alasan dan Sumber](/static/core/admin/img/help/list-hygiene/suppressions-list.webp)

Gunakan filter di sebelah kanan untuk menyaring daftar berdasarkan **Alasan (Reason)** atau **Sumber (Source)** — misalnya, untuk meninjau setiap alamat yang diblokir secara manual, atau semua yang masuk melalui webhook penyedia.

## Menambahkan alamat secara manual

Untuk memblokir alamat sendiri — alamat penyalahgunaan yang diketahui, pesaing yang menambang newsletter Anda, atau apa pun yang ingin Anda jauhkan dari daftar Anda — klik **+ Tambahkan alamat yang ditekan** dan isi:

- **Email** — alamat yang akan diblokir
- **Reason** — pilih **Manually blocked** untuk entri yang ditambahkan sendiri
- **Source** — pilih **Added manually**
- **Detail** — catatan opsional yang menjelaskan alasannya (berguna untuk catatan Anda sendiri, dan untuk staf mana pun yang meninjau daftar nanti)

Simpan entri tersebut dan Spwig akan segera berhenti mengirim email kampanye atau journey ke alamat tersebut.

## Kapan saya harus melepaskan alamat?

Melepaskan (menghapus penekanan) sebuah alamat harus dilakukan secara jarang dan sengaja. Hanya lakukan ini ketika Anda yakin masalah dasarnya benar-benar sudah diperbaiki — misalnya:

- Pelanggan memberi tahu Anda bahwa kotak masuk mereka penuh dan sudah dibersihkan.
- Sebuah alamat ditekan oleh rangkaian soft-bounce yang Anda ketahui disebabkan oleh gangguan sementara di penyedia email mereka, bukan kotak masuk yang tidak aktif.
- Anda memblokir alamat secara manual dan kemudian memutuskan bahwa blokir tersebut adalah kesalahan.

Untuk melepaskan alamat, buka alamat tersebut di daftar Suppressions dan hapus entri — ini akan mengangkat blokir sehingga alamat tersebut dapat menerima email lagi. Jangan melepaskan alamat yang hard-bounce hanya karena tidak nyaman kehilangan pelanggan; alamat tersebut tidak ada, dan mengirim ke sana lagi hanya akan memantul dan merugikan reputasi Anda untuk kedua kalinya. Demikian pula, melepaskan alamat yang memiliki keluhan spam jarang membantu — penerima tersebut telah memberi tahu penyedia kotak masuk mereka bahwa mereka tidak ingin menerima email Anda, dan mengirim ke mereka lagi berisiko menimbulkan keluhan lain.

## Apa yang tidak terpengaruh

Suppression hanya berlaku untuk **kampanye pemasaran dan journey** yang dikirim melalui Campaign Studio. Hal ini tidak memengaruhi **email transaksional** — konfirmasi pesanan, pembaruan pengiriman, reset kata sandi, dan email lain yang dikirim toko Anda sebagai bagian dari tindakan pesanan atau akun selalu dikirim, bahkan ke alamat yang ditekan. Suppression ada untuk melindungi reputasi pengirim pemasaran Anda; ini bukan daftar blokir email umum untuk toko Anda.

## Tips

- Jangan melawan sistem dengan secara manual melepaskan setiap hard bounce yang Anda lihat — hard bounce berarti alamatnya sudah hilang, dan menambahkan kembali ke pengiriman Anda hanya akan memantul lagi.
- Periksa daftar Suppressions setelah pengiriman besar jika tingkat pembukaan Anda terlihat tidak biasa rendah — gelombang soft bounce pada domain bersama (misalnya, server email perusahaan yang bermasalah) bisa menjadi tanda masalah pengiriman sementara yang layak diselidiki dengan penyedia Anda.
- Jika Anda berpindah ke Spwig dari platform lain, jangan mengimpor seluruh daftar blokir lama Anda secara manual sebagai suppressions — biarkan Spwig belajar dari pantulan dan keluhan nyata pada daftar ini, sehingga Anda tidak secara tidak sengaja memblokir alamat yang sebenarnya akan terkirim dengan baik.
- Tinjau kolom **Source** sesekali — banyak entri **Provider webhook** mengonfirmasi bahwa pelaporan pantulan penyedia email Anda terhubung dan berfungsi.
- Jaga agar field **Detail** bermakna saat menambahkan blokir manual; ini adalah satu-satunya catatan mengapa keputusan tersebut dibuat setelah waktu berlalu.