# Deadlock Detection and Prevention (Banker's Algorithm)

Aplikasi GUI interaktif berbasis **Python (Tkinter)** untuk mendeteksi dan mencegah **deadlock** pada sistem multiproses menggunakan **Banker's Algorithm**.  
Dirancang sebagai alat edukasi dan simulasi untuk memahami konsep deadlock, safe state, dan urutan aman (safe sequence).

---

## Nama Aplikasi

**Deadlock Detection and Prevention (Banker's Algorithm)**

## Creator

**Nama:** Ragil Amirzaky (alias Tenzly)
**Email / Kontak:** [lapness21@gmail.com / GitHub]  
**Tahun:** 2025

---

## Deskripsi Singkat

Aplikasi ini memungkinkan pengguna memasukkan jumlah proses dan jenis sumber daya, kemudian mengisi:

- Matriks **Allocation** (alokasi saat ini),
- Matriks **Max Need** atau **Need** (pilihan mode),
- Vektor **Available** (sumber daya yang tersedia).

Aplikasi akan mensimulasikan langkah-langkah Algoritma Bankir dan menampilkan apakah sistem berada pada **safe state** atau terjadi **deadlock**, lengkap dengan log langkah demi langkah dan safe sequence bila ada.

---

## Fitur

- Antarmuka GUI modern menggunakan **Tkinter** dengan custom widget (Rounded buttons & entries).
- Dua mode input:
  - **Max Need Matrix** → otomatis menghitung `Need = MaxNeed - Allocation`
  - **Need Matrix** → pengguna memasukkan Need secara langsung
- Validasi input (cek integer, tidak kosong, validitas Need jika MaxNeed dipakai)
- Log langkah demi langkah Algoritma Bankir pada panel kanan
- Popup hasil akhir: safe state + safe sequence atau deadlock detected
- Cocok untuk penggunaan pembelajaran, praktikum OS, atau demo konsep

---

## Prasyarat

- Python 3.8+
- Paket:
  - `numpy`

Install dependensi:

```bash
pip install numpy
```

---

## Struktur Proyek (contoh)

```
project-root/
├─ main.py          # file utama aplikasi (tkinter + banker algorithm)
├─ README.md        # dokumentasi (file ini)
└─ assets/          # (opsional) gambar / ikon
```

> Catatan: file utama pada contoh ini diberi nama `main.py`. Sesuaikan dengan nama file program Anda.

---

## Cara Kerja (ringkas)

1. Pengguna memasukkan jumlah proses (N) dan jumlah jenis resource (M).
2. Program membuat input matriks sesuai N dan M: Allocation, MaxNeed/Need, dan Available.
3. Jika mode `Max Need` dipilih: program menghitung `Need = MaxNeed - Allocation` (validasi: Need >= 0).
4. Jalankan Algoritma Bankir:
   - Inisialisasi `Work = Available`, `Finish[i] = False` untuk semua proses.
   - Cari proses i dengan `Finish[i] == False` dan `Need[i] <= Work`.
   - Jika ditemukan, jalankan proses tersebut (anggap selesai) dan `Work += Allocation[i]`, tandai `Finish[i] = True`.
   - Ulangi hingga semua selesai atau tidak ada proses yang bisa dieksekusi.
5. Jika semua `Finish[i] == True` → **Safe State** + tampilkan safe sequence.
6. Jika tidak semuanya selesai → **Deadlock detected**.

---

## Cara Pakai (step-by-step)

1. Pastikan dependensi sudah terpasang (`numpy`).
2. Jalankan aplikasi:

```bash
python main.py
```

3. Isi nilai:
   - `Number of Processes (N)`
   - `Number of Resources (M)`
   - Klik **Next**
4. Pilih mode input:
   - **Max Need Matrix** atau **Need Matrix**
5. Isi:
   - **Allocation Matrix** (N x M)
   - **Max Need / Need Matrix** (N x M)
   - **Available Vector** (1 x M)
6. Klik **Detect Deadlock (Banker's)**
7. Lihat log langkah demi langkah pada panel kanan dan popup hasil akhir.

---

## Contoh Input & Output (ilustrasi)

**Contoh input singkat (N=3, M=3)**  
Allocation:

```
0 1 0
2 0 0
3 0 2
```

MaxNeed:

```
7 5 3
3 2 2
9 0 2
```

Available:

```
3 3 2
```

**Contoh output (log)**:

```
--- Memulai Algoritma Banker's ---
Mode Input: Max Need
Allocation Matrix:
[[0 1 0]
 [2 0 0]
 [3 0 2]]
Need Matrix:
[[7 4 3]
 [1 2 2]
 [6 0 0]]
Initial Available (Work): [3 3 2]
ITERASI 1: ...
✅ P1 selesai. Work baru = [...]
...
✅ TIDAK ADA DEADLOCK TERDETEKSI.
SAFE SEQUENCE: ['P1', 'P0', 'P2']
```

---

## Validasi dan Penanganan Error

- Semua input harus integer. Jika ada field kosong atau bukan integer, aplikasi menampilkan error.
- Jika mode `Max Need` menghasilkan nilai `Need < 0` (MaxNeed < Allocation), aplikasi menampilkan error dan meminta koreksi.

---

## Keterbatasan

- Aplikasi ini bersifat edukatif/simulasi; **tidak** ditujukan untuk penggunaan produksi.
- UI berbasis Tkinter sederhana—penyempurnaan UX/UI masih dapat dilakukan.
- Belum ada fitur simpan/unggah (save/load) konfigurasi secara default.

---

## Kontribusi

Kontribusi dipersilakan (bugfix, fitur baru, perbaikan UI). Silakan fork repository dan ajukan pull request.

---

## Lisensi

Lisensi MIT — gunakan, modifikasi, dan distribusikan kembali dengan menyertakan atribusi.

Contoh singkat header MIT:

```
MIT License

Copyright (c) 2025 [\[Ragil Amirzaky\]](https://github.com/Lapnes

Permission is hereby granted, free of charge, to any person obtaining a copy...
```

---

## Credit

- Dikembangkan dari: saransridatha(Banker's Algorithm)
- Dokumentasi & bantuan pembuatan README: ChatGPT (asisten dokumentasi)
- Referensi konsep Algoritma Bankir: buku teks OS, CSCI-442, dan sumber akademik (By ChatGPT ReSearch)

---

## Kontak

Untuk pertanyaan, saran, atau kontribusi, hubungi:  
**Email:** lapness21@gmail.com
**GitHub:** [\[Lapnes\]](https://github.com/Lapnes)
