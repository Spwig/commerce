---
title: Log Pengiriman Webhook
---

Setiap kali toko Anda mencoba mengirim webhook, sebuah entri log pengiriman akan dibuat. Log-log ini memungkinkan Anda melihat secara tepat apa yang dikirim, apakah berhasil, dan apa yang terjadi selama upaya pengiriman ulang. Panduan ini menjelaskan cara membaca log pengiriman dan men-debug masalah ketika pengiriman gagal.

## Melihat log pengiriman

Navigasikan ke **Integrations > Webhook Deliveries** untuk melihat riwayat lengkap dari semua upaya pengiriman webhook di semua endpoint Anda.

![Webhook delivery logs](/static/core/admin/img/help/webhook-deliveries/delivery-list.webp)

Daftar ini menampilkan nama endpoint, jenis acara, status, kode respons HTTP, waktu respons, dan jumlah upaya yang telah dilakukan untuk setiap pengiriman.

Log pengiriman hanya bisa dibaca — mereka dibuat secara otomatis ketika acara terjadi dan tidak dapat diedit.

## Status pengiriman

Setiap pengiriman memiliki salah satu dari status berikut:

| Status | Artinya |
|--------|---------------|
| **Pending** | Pengiriman sedang dalam antrian dan belum dicoba |
| **Success** | Server penerima merespons dengan kode status HTTP 2xx — pengiriman dikonfirmasi |
| **Failed** | Semua upaya pengiriman telah habis — pengiriman tidak akan dicoba lagi |
| **Retrying** | Upaya terbaru gagal, tetapi sistem akan mencoba lagi pada waktu ulang yang dijadwalkan |
| **Sandbox Blocked** | Pengiriman diblokir karena URL endpoint tidak dapat diakses di lingkungan saat ini |

Pengiriman dianggap berhasil ketika server penerima mengembalikan kode respons HTTP 2xx (200, 201, 202, dll.). Setiap respons lainnya — termasuk 3xx redirect atau kesalahan 4xx/5xx — dianggap sebagai kegagalan.

## Memfilter pengiriman

Gunakan panel filter di sebelah kanan untuk menyempitkan daftar:

- **Status** — Lihat hanya pengiriman yang gagal, sedang dicoba ulang, atau berhasil
- **Event Type** — Lihat semua pengiriman untuk acara tertentu (misalnya, semua pengiriman `order.created`)
- **Endpoint** — Lihat pengiriman untuk endpoint tertentu
- **Created At** — Filter berdasarkan rentang tanggal

Gunakan bilah pencarian untuk mencari berdasarkan jenis acara atau nama endpoint, atau untuk menemukan pengiriman tertentu berdasarkan ID-nya.

## Membaca detail pengiriman

Klik pada pengiriman apa pun untuk melihat detail lengkapnya. Rekam pengiriman hanya bisa dibaca.

### Ringkasan

- **ID** — Pengidentifikasi unik untuk upaya pengiriman ini
- **Endpoint** — Endpoint webhook mana yang pengiriman ini dikirimkan (tautan ke catatan endpoint)
- **Event Type** — Acara yang memicu pengiriman ini (misalnya, `order.paid`)
- **Status** — Status pengiriman saat ini

### Payload

Bagian **Payload** menampilkan data JSON yang tepat yang dikirim ke endpoint Anda. Ini mencakup jenis acara, tanda waktu, dan data acara lengkap. Gunakan ini untuk memverifikasi bahwa server penerima Anda menerima struktur data yang benar.

### Respons

Bagian **Respons** menampilkan apa yang dikembalikan server Anda:

- **Response Status Code** — Kode status HTTP yang dikembalikan oleh server Anda. Dikodekan berwarna: hijau untuk 2xx (sukses), kuning untuk 4xx (kesalahan klien), merah untuk 5xx (kesalahan server).
- **Response Time** — Berapa lama server Anda membutuhkan waktu untuk merespons dalam milidetik. Dikodekan berwarna: hijau di bawah 500ms, kuning hingga 2 detik, merah di atas 2 detik.
- **Response Body** — Tubuh respons dari server Anda (dipotong hingga 1.000 karakter). Ini dapat membantu mengidentifikasi mengapa server Anda menolak webhook.
- **Response Headers** — Header yang dikembalikan oleh server Anda.

### Detail kesalahan

Jika pengiriman gagal, bagian **Detail Kesalahan** menampilkan pesan kesalahan — contohnya, `Connection refused`, `Timeout after 30s`, atau kesalahan HTTP dari server Anda.

### Informasi ulang

- **Attempt Count** — Berapa banyak upaya pengiriman yang telah dilakukan (termasuk upaya pertama)
- **Next Retry At** — Kapan upaya ulang berikutnya akan dilakukan (hanya ditampilkan untuk pengiriman dengan status **Retrying**)

Ulangan mengikuti jadwal back-off eksponensial — jeda antara ulangan meningkat dengan setiap upaya untuk menghindari mengganggu server yang sementara tidak tersedia. Dengan maksimum 5 ulangan (default), jadwal ulangan mencakup beberapa jam.

## Mencoba pengiriman yang gagal secara manual

Jika Anda ingin segera mencoba kembali pengiriman tanpa menunggu jadwal otomatis:

1. Pilih kotak centang di sebelah pengiriman yang ingin Anda coba kembali
2. Dari dropdown **Action**, pilih **Retry selected deliveries**
3. Klik **Go**

Hanya pengiriman yang tidak berstatus **Success** yang akan diproses ulang. Pengiriman yang berhasil akan diabaikan.

Ini berguna ketika Anda telah memperbaiki masalah pada server penerima dan ingin memproses ulang kejadian yang gagal tanpa menunggu.

## Diagnosa kegagalan umum

### Kode respons HTTP 4xx

Respons 4xx dari server Anda biasanya berarti ada masalah dengan permintaan — otentikasi gagal, URL endpoint berubah, atau server Anda menolak format payload. Periksa:

- Apakah URL endpoint benar?
- Apakah server Anda memverifikasi tanda tangan HMAC dengan benar? Ketidakcocokan menyebabkan banyak server mengembalikan 401 atau 403.
- Apakah struktur payload berubah? Periksa payload dalam log pengiriman terhadap apa yang diharapkan oleh server Anda.

### Kode respons HTTP 5xx

Respons 5xx berarti server Anda mengalami kesalahan internal saat memproses webhook. Periksa log kesalahan server Anda sendiri untuk mendiagnosis masalah.

### Koneksi ditolak / Timeout

Kesalahan ini berarti Spwig sama sekali tidak dapat mencapai server Anda:

- Apakah server sedang berjalan dan dapat diakses secara publik?
- Apakah URL benar (termasuk protokol yang benar — http atau https)?
- Apakah firewall memblokir permintaan masuk?
- Apakah waktu respons server melebihi batas waktu yang dikonfigurasikan? Jika ya, tingkatkan pengaturan **Timeout** pada endpoint atau optimalkan penangani webhook server Anda untuk merespons dengan cepat (ideally dalam 5 detik).

### Sandbox Blocked

Pengiriman diblokir ke URL localhost atau alamat jaringan internal. Endpoint webhook harus dapat diakses secara publik. Gunakan alat seperti ngrok selama pengembangan untuk mengungkapkan server lokal secara publik.

## Tips

- Selesaikan pengiriman **Failed** segera — data acara masih ada dalam payload, dan Anda dapat mencoba kembali secara manual setelah masalah diperbaiki.
- Jika Anda melihat banyak pengiriman **Retrying** untuk satu endpoint, buka catatan endpoint dan periksa bagian **Health** — endpoint mungkin segera dinonaktifkan secara otomatis.
- Waktu respons penting: konfigurasikan penangani webhook Anda untuk merespons dengan cepat (dalam beberapa detik) dan proses payload secara asinkron di latar belakang. Penangani yang lambat menyebabkan kegagalan timeout bahkan jika logika Anda benar.
- Gunakan filter **Event Type** untuk memeriksa riwayat pengiriman untuk jenis acara tertentu saat menyelidiki apakah integrasi Anda menerima acara yang benar.
- Log pengiriman menumpuk seiring waktu. Gunakan filter tanggal untuk fokus pada pengiriman terbaru dan hindari menghadapi riwayat lama.