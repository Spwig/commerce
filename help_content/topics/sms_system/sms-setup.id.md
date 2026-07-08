---
title: Pengaturan Pemasok SMS
---

Pemberitahuan SMS menjaga pelanggan Anda tetap diberitahu di setiap langkah pesanan mereka — dari konfirmasi hingga pengiriman. Untuk mengirim pesan SMS atau WhatsApp dari toko Anda, Anda perlu menghubungkan akun pemasok SMS dengan kredensial Anda. Setelah terhubung, Spwig menggunakan akun tersebut untuk mengirim semua pesan teks yang keluar.

Navigasikan ke **Sistem SMS > Akun Pemasok SMS** untuk mengelola pemasok SMS Anda.

![Daftar akun pemasok SMS](/static/core/admin/img/help/sms-setup/provider-list.webp)

## Menambahkan pemasok SMS

Anda dapat menambahkan pemasok menggunakan **Wizard Setup** (dianjurkan untuk pengaturan pertama) atau formulir manual.

### Menggunakan wizard setup

1. Navigasikan ke **Sistem SMS > Akun Pemasok SMS**
2. Klik **Wizard Setup** di toolbar
3. Ikuti langkah-langkah yang diarahkan:
   - **Langkah 1**: Pilih pemasok Anda dari daftar pemasok yang tersedia
   - **Langkah 2**: Masukkan kredensial pemasok Anda (kunci API, SID Akun, dll.)
   - **Langkah 3**: Tetapkan nama tampilan dan pengaturan default, lalu simpan
4. Wizard menguji koneksi secara otomatis sebelum disimpan

### Menambahkan pemasok secara manual

1. Navigasikan ke **Sistem SMS > Akun Pemasok SMS**
2. Klik **Lihat Pemasok** untuk menjelajahi pemasok SMS yang tersedia, atau klik **+ Tambah Akun Pemasok SMS** secara langsung
3. Di bidang **Pemasok**, pilih pemasok SMS Anda dari dropdown
4. Setelah Anda memilih pemasok, bidang kredensial akan muncul secara otomatis berdasarkan apa yang diperlukan oleh pemasok tersebut
5. Isi bidang kredensial yang diperlukan (ini bervariasi tergantung pemasok — lihat bagian di bawah untuk pemasok umum)
6. Masukkan **Nama Tampilan** untuk mengidentifikasi akun ini (misalnya, `Twilio — Utama`)
7. Tetapkan **Pengaturan Default** (lihat di bawah)
8. Klik **Simpan**

## Kredensial Pemasok

### Twilio

| Bidang | Di mana menemukannya |
|-------|-----------------|
| Account SID | Konsol Twilio → Dashboard |
| Auth Token | Konsol Twilio → Dashboard |
| From Number | Nomor telepon Twilio Anda dalam format E.164 (misalnya, `+15551234567`) |

### Pemasok lain

Komponen pemasok SMS lain yang terinstal akan menampilkan bidang kredensial mereka sendiri saat dipilih. Lihat dokumentasi pemasok Anda untuk nilai yang tepat — biasanya sebuah kunci API atau token akses dan identifikasi pengirim.

## Pengaturan Default

Setelah memasukkan kredensial, konfigurasikan cara akun ini digunakan:

- **Aktif** — aktifkan atau nonaktifkan akun ini. Akun yang tidak aktif tidak akan digunakan untuk mengirim, bahkan jika diatur sebagai default
- **Akun SMS Default** — saat dicentang, semua pemberitahuan SMS dari toko Anda menggunakan akun ini. Hanya satu akun yang dapat menjadi akun SMS default pada satu waktu
- **Akun WhatsApp Default** — jika pemasok ini mendukung WhatsApp (misalnya, Twilio melalui WhatsApp Business API), centang ini untuk menggunakan akun ini sebagai default untuk pesan WhatsApp

## Menguji koneksi

Setelah menyimpan akun pemasok, uji apakah kredensial bekerja:

1. Navigasikan ke **Sistem SMS > Akun Pemasok SMS**
2. Klik akun pemasok Anda untuk membukanya
3. Klik tombol **Uji Koneksi**
4. Spwig mengirim permintaan uji ke pemasok dan memperbarui bidang **Status Koneksi**

| Status | Arti |
|--------|---------|
| Terhubung | Kredensial valid dan pemasok dapat dijangkau |
| Koneksi Gagal | Kredensial salah atau pemasok tidak dapat dijangkau |
| Belum Diuji | Koneksi belum diuji |

Jika uji gagal, periksa kembali kredensial Anda dan pastikan akun Anda memiliki izin yang diperlukan di dashboard pemasok.

## Kolom Status Koneksi

Daftar Akun Pemasok SMS menampilkan badge **Koneksi** yang dikodekan berdasarkan warna untuk setiap akun:

- **Terhubung** (hijau) — akun berfungsi dengan baik
- **Koneksi Gagal** (merah) — kredensial gagal — perbarui kredensial
- **Belum Diuji** (abu-abu) — akun belum diuji

## Tips

- Gunakan Wizard Setup untuk pemasok pertama Anda — ia memandu Anda melalui setiap bidang dan menguji koneksi sebelum disimpan
- Hanya satu akun yang dapat menjadi Akun SMS Default pada satu waktu.

Jika Anda menambahkan akun kedua dan menandainya sebagai default, akun default sebelumnya secara otomatis tidak aktif
- Catat kredensial API penyedia Anda di tempat yang aman.

Jika kredensial berubah, perbarui di sini segera untuk menghindari notifikasi yang gagal
- Akun tidak aktif tetap ada dalam daftar tetapi tidak digunakan untuk mengirim — berguna untuk menyimpan kredensial cadangan tanpa mengaktifkannya
- Kebanyakan penyedia membebankan biaya per pesan yang dikirim — pantau penggunaan di dashboard penyedia untuk menghindari tagihan yang tidak terduga