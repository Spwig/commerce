---
title: 'Pengaturan SSO: Microsoft Entra ID'
---

Panduan ini akan membimbing Anda melalui proses menghubungkan Spwig ke Microsoft Entra ID (sebelumnya dikenal sebagai Azure Active Directory) untuk single sign-on (SSO) admin. Setelah dikonfigurasi, staf Anda dapat masuk ke panel admin Spwig menggunakan akun kerja Microsoft mereka.

**Catatan:** Microsoft mungkin akan memperbarui antarmuka pusat admin Entra dari waktu ke waktu. Petunjuk ini ditulis berdasarkan antarmuka seperti pada awal tahun 2026. Jika langkah-langkah ini berbeda dari apa yang Anda lihat, lihat dokumentasi resmi Microsoft tentang [mendaftarkan aplikasi dengan platform identitas Microsoft](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app).

## Prasyarat

- Langganan Azure dengan akses ke Microsoft Entra ID
- Peran **Application Administrator** atau **Global Administrator** di tenant Entra ID Anda
- URL toko Spwig Anda (misalnya, `https://your-store.com`)
- Alamat email staf harus sesuai dengan akun Microsoft mereka di Spwig

## Langkah 1: Mendaftarkan Aplikasi

1. Masuk ke [Microsoft Entra admin center](https://entra.microsoft.com)
2. Navigasi ke **Identity > Applications > App registrations**
3. Klik **New registration**
4. Konfigurasikan pendaftaran:

| Field | Value |
|-------|-------|
| **Name** | `Spwig Admin SSO` (atau nama apa pun yang Anda sukai) |
| **Supported account types** | **Accounts in this organizational directory only** (Single tenant) |
| **Redirect URI** | Platform: **Web**, URI: `https://your-store.com/oidc/callback/` |

5. Klik **Register**

**Penting:** URI redirect harus tepat sesuai dengan `https://your-store.com/oidc/callback/` — termasuk slash akhir. Ganti `your-store.com` dengan domain toko Anda yang sebenarnya.

## Langkah 2: Catat ID Aplikasi

Setelah pendaftaran, Anda akan melihat halaman **Overview** aplikasi. Catat dua nilai ini — Anda membutuhkannya nanti:

| Value | Where to Find It | What It's For |
|-------|-----------------|---------------|
| **Application (client) ID** | Overview page, top section | Masukkan sebagai **Client ID** di Spwig |
| **Directory (tenant) ID** | Overview page, top section | Digunakan untuk membangun URL Discovery |

## Langkah 3: Membuat Client Secret

1. Di pendaftaran aplikasi, navigasi ke **Certificates & secrets**
2. Klik **New client secret**
3. Masukkan deskripsi (misalnya, `Spwig SSO`) dan pilih periode kedaluwarsa
4. Klik **Add**
5. **Salin nilai segera** — nilai ini hanya ditampilkan sekali. Ini adalah client secret yang akan Anda masukkan ke Spwig.

**Jangan salin ID Secret** — Anda membutuhkan kolom **Value**, bukan kolom ID.

**Buat pengingat** untuk memutar ulang rahasia sebelum kedaluwarsa. Ketika sebuah rahasia kedaluwarsa, SSO akan berhenti bekerja sampai Anda membuat yang baru dan memperbarui di Spwig.

## Langkah 4: Konfigurasi Izin API

1. Navigasi ke **API permissions**
2. Pastikan **Microsoft Graph > User.Read** (delegated) terdaftar. Izin ini ditambahkan secara default.
3. Jika izin `openid`, `email`, dan `profile` tidak terdaftar, klik **Add a permission > Microsoft Graph > Delegated permissions** dan tambahkan mereka.
4. Klik **Grant admin consent for [your organization]** jika diminta.

## Langkah 5: Membangun URL Discovery

URL Discovery OIDC mengikuti format berikut:

```
https://login.microsoftonline.com/{tenant-id}/v2.0/.well-known/openid-configuration
```

Ganti `{tenant-id}` dengan **Directory (tenant) ID** dari Langkah 2.

Contoh: jika ID tenant Anda adalah `a1b2c3d4-e5f6-7890-abcd-ef1234567890`, URL Discovery adalah:

```
https://login.microsoftonline.com/a1b2c3d4-e5f6-7890-abcd-ef1234567890/v2.0/.well-known/openid-configuration
```

## Langkah 6: Konfigurasi Klaim Grup (Opsional)

Jika Anda ingin Spwig secara otomatis menetapkan status staf atau superuser berdasarkan keanggotaan grup Entra ID:

1. Di pendaftaran aplikasi, navigasi ke **Token configuration**
2. Klik **Add groups claim**
3. Pilih jenis grup yang ingin Anda sertakan (biasanya **Security groups**)
4. Di bawah **Customize token properties by type**, untuk token **ID**, pilih **Group ID**
5. Klik **Add**

**Penting:** Entra ID mengirimkan **Object IDs** (UUID seperti `a1b2c3d4-...`), bukan nama tampilan grup.

Ketika mengonfigurasi pemetaan peran di Spwig, Anda harus menggunakan Object IDs ini.

Untuk menemukan Object ID sebuah grup:
1. Di pusat administrasi Entra, pergi ke **Identity > Groups > All groups**
2. Klik grup
3. Salin **Object ID** dari halaman ringkasan grup

### Batas Grup

Microsoft Entra ID hanya mencakup maksimal **200 grup** dalam token. Jika pengguna termasuk lebih dari 200 grup, klaim grup diganti dengan tautan ke Microsoft Graph API. Untuk organisasi dengan banyak grup, pertimbangkan untuk membuat grup keamanan khusus untuk akses Spwig dan menggunakan [filter grup](https://learn.microsoft.com/en-us/entra/identity-platform/optional-claims-reference) untuk membatasi grup yang termasuk.

## Langkah 7: Konfigurasi di Spwig

1. Di admin Spwig, navigasikan ke **Enterprise SSO > SSO Provider Configuration**
2. Atur **Provider Name** menjadi `Microsoft Entra ID`
3. Tempelkan URL Penemuan dari Langkah 5 ke **OIDC Discovery URL**
4. Klik **Auto-Discover** — ini mengisi semua bidang akhir titik secara otomatis
5. Masukkan **Client ID** dari Langkah 2
6. Masukkan **Client Secret** (Nilai) dari Langkah 3
7. Jika Anda mengonfigurasi klaim grup di Langkah 6:
   - Atur **Groups Claim** menjadi `groups`
   - Di **Staff Groups**, masukkan Object ID grup yang anggotanya harus menjadi staf (dipisahkan dengan koma)
   - Di **Superuser Groups**, masukkan Object ID grup yang anggotanya harus menjadi superuser (dipisahkan dengan koma)
8. Klik **Save**

## Langkah 8: Aktifkan dan Uji

1. Navigasikan ke **Site Settings > Security** tab
2. Centang **Enable SSO for admin login**
3. Klik **Save**
4. Buka halaman login admin di **jendela pribadi/incognito**
5. Anda seharusnya melihat tombol **Sign in with Microsoft Entra ID**
6. Klik tombol tersebut — Anda seharusnya dialihkan ke halaman login Microsoft
7. Masuk dengan akun Microsoft yang alamat emailnya cocok dengan pengguna staf di Spwig
8. Anda seharusnya dialihkan kembali ke dashboard admin Spwig

## Masalah Umum

| Masalah | Penyebab | Solusi |
|---------|-------|----------|
| **AADSTS50011: URI redirect tidak cocok** | URI redirect di Entra tidak cocok secara tepat | Periksa URI redirect adalah `https://your-store.com/oidc/callback/` dengan slash akhir. Periksa kesalahan antara HTTP dan HTTPS. |
| **AADSTS700016: Aplikasi tidak ditemukan** | Client ID atau tenant salah | Periksa ulang Client ID dan pastikan URL Penemuan menggunakan ID tenant yang benar |
| **Login berhasil di Microsoft tetapi gagal di Spwig** | Tidak ada pengguna yang cocok di Spwig | Pastikan akun staf ada di Spwig dengan alamat email yang sama dengan akun Microsoft. Periksa bahwa pengguna memiliki status staf jika Restrict to Staff diaktifkan. |
| **Klaim grup kosong** | Klaim grup tidak dikonfigurasi | Ikuti Langkah 6 untuk menambahkan klaim grup ke konfigurasi token |
| **Klaim grup mengembalikan URL alih-alih ID** | Pengguna berada dalam lebih dari 200 grup | Gunakan filter grup untuk membatasi grup dalam token, atau tetapkan grup spesifik |
| **SSO berhenti bekerja setelah beberapa bulan** | Client secret telah kedaluwarsa | Buat client secret baru di Entra dan perbarui di konfigurasi SSO Provider Spwig |

## Tips

- **Gunakan grup keamanan** untuk pemetaan peran, bukan grup Microsoft 365 atau daftar distribusi.

Grup keamanan dirancang untuk kontrol akses dan bekerja paling andal dengan klaim OIDC.
- **Rekomendasi single tenant** — memilih "Akun di direktori organisasi ini saja" membatasi SSO hanya untuk pengguna organisasi Anda.

Konfigurasi multi-tenant memerlukan validasi tambahan.
- **Atur masa berlaku secret yang panjang** — pilih 24 bulan saat membuat client secret, dan tetapkan pengingat kalender pada 22 bulan untuk memperbarui.
- **Akses kondisional** — Anda dapat membuat kebijakan akses kondisional di Entra ID yang berlaku khusus untuk pendaftaran aplikasi Spwig.

Misalnya, memerlukan MFA, memblokir masuk dari lokasi yang tidak dapat dipercaya, atau memerlukan perangkat yang sesuai.
- **Uji dengan akun non-admin** — buat akun staf uji di Spwig untuk memverifikasi SSO berfungsi sebelum diterapkan ke seluruh tim Anda.