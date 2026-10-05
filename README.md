# Proyek PBP — myportofolio

**Nama:** Razan Muhammad Fathin Lesmana  
**NPM:** 2506603646  
**Kelas:** PBP A

**Link PWS:** https://razan-muhammad51-myportofolio.pws.cs.ui.ac.id/  
**Repository:** https://github.com/RazanLesmana/myportofolio

---

## Deskripsi Proyek

Website portofolio pribadi ini menampilkan profil, pengalaman, penghargaan, proyek, dan halaman "contact me". Proyek ini juga mengintegrasikan siapa Razan di luar pengalaman dan pekerjaannya lewat elemen tambahan seperti foto.

Proyek ini dibangun dengan Django sebagai fullstack framework (menangani routing, tempating, dan (nanti?) persistence). Tampilan dibangun manual dengan HTML + CSS.

**Status saat ini:** Selesai Tugas 1

---

## Setup

```bash
# 1. Clone repositori
git clone https://github.com/RazanLesmana/myportofolio.git
cd myportofolio

# 2. Buat & aktifkan virtual environment
python -m venv env
source env/bin/activate      # macOS / Linux
env\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Siapkan environment variables
#    Buat berkas .env di root proyek berisi:
#    PRODUCTION=False

# 5. Jalankan migrasi & server
python manage.py migrate
python manage.py runserver
```

Data contoh Outside Work masuk otomatis lewat data migration, jadi tidak perlu diisi manual.

Buka http://localhost:8000/

---

## Progress Mingguan

### Minggu 0

- Setup sesuai Tutorial 0

### Minggu 1

- Setup sesuai Tutorial 1
- Merevisi warna yang digunakan dan struktur hero section
- Mengganti foto menjadi polaroid bertumpuk
- Menambahkan page "Experience"
- Menambahkan placeholder page "Achievement", "Projects", dan "Contact Me"

### Minggu 2

- Setup sesuai Tutorial 2
- Memindahkan data profil (nama, NPM, program studi, bio) dari HTML ke context view
- Mengonfigurasi routing dengan namespace `main` dan menghubungkan navigasi antarhalaman
- Menambahkan page "Outside Work" berisi section Photography, Travel, dan Runs
- Membuat model `OutsidePhoto` untuk menyimpan foto, album, dan section
- Membuat hero full-screen dengan gradasi dan judul yang menumpuk di atas foto
- Menyusun galeri grid yang dikelompokkan per album menggunakan `{% regroup %}`
- Menambahkan tampilan kondisi kosong untuk section Travel dan Runs
- Menyeragamkan navbar dan footer di ketiga halaman menggunakan tag `{% url %}`
- Membuat data migration agar data contoh ikut terisi saat deploy ke PWS
- Menambahkan unit test untuk halaman Outside Work


### Minggu 3

- Setup sesuai tutorial 3
- Refactor struktur file-file pada templates untuk extend base.html
- Menambahkan opsi add dan delete pada Experience dan Projects
- Menambahkan fitur pencarian projek berdasarkan judul
- Mengubah view daftar agar mengambil data lewat JSON lalu melakukan deserialisasi
- Mengubah field ended_at dari DateTimeField menjadi Charfield agar input sesuai dengan tampilan yang diinginkan

### Minggu 4
- Setup sesuai Tutorial 4 (registrasi, login, logout, cookie `last_login`)
- Menambahkan relasi `ManyToManyField` ke `User` pada model `Experience` untuk fitur star
- Membuat view `toggle_star_experience` dengan metode POST dan `{% csrf_token %}`, satu star per pengguna
- Menampilkan jumlah star dan status star pengguna pada tiap kartu Experience
- Menambahkan view `edit_experience` untuk mengubah data lewat form
- Menerapkan pembatasan hak akses di sisi server pada create, update, dan delete Experience
- Membuat peran **Editor** lewat Django Group dan memeriksanya dengan `user.groups.filter(name="Editor")`
- Menyembunyikan tombol tambah, edit, dan hapus bagi pengguna yang tidak berhak
- Memastikan endpoint JSON tetap berfungsi tanpa membocorkan data pengguna
---

### Minggu 5
- Setup sesuai Tutorial 5 (toast, AJAX, debouncing, modal, XSS)
- Mengubah halaman Experience agar hanya merender kerangka, lalu mengambil data lewat `fetch()` dari endpoint JSON
- Menyusun JSON secara manual di `get_experiences_json`, termasuk jumlah star dan status star pengguna yang sedang login
- Menambahkan kondisi loading, kosong, dan error
- Menambahkan pencarian berdasarkan jabatan dengan debouncing 300 ms
- Memindahkan form tambah Experience ke dalam modal (Popover API) dan mengirimnya lewat AJAX ke `create_experience_ajax` (201/400/403)
- Menampilkan toast untuk hasil berhasil dan gagal, termasuk pesan validasi dari server
- Menerapkan `escapeHtml` pada semua teks yang disisipkan lewat JavaScript dan `strip_tags` pada `clean_<field>` di `ExperienceForm`

## Pertanyaan Reflektif

### Tugas 1

**1.** Saya tidak menggunakan elemen `<article>` dan `<aside>`, tetapi menggunakan `<section>`. `<section>` ini saya gunakan untuk membuat section experience. Saya rasa tanpa `<article>` dan `<aside>`, seluruh kebutuhan desain saya sudah terpenuhi dengan `<section>` dan `<div>` untuk membagi design menjadi beberapa bagian.

**2.** Tantangan terberat saya adalah mengatur jarak antar elemen pada header. Saya mengevaluasinya dengan mencoba-coba mengedit ukuran di css dan jika belum berhasil saya bertanya kepada AI. Akhirnya, saya menemukan masalahnya adalah header dibagi menjadi 4 grid, sehingga ada jarak antar grid.

Untuk saat ini, saya mengatur responsiveness lewat ukuran container, dan saya rasa hanya `h1` yang benar2 memiliki ukuran responsif. Ini akan saya improve seiring saya belajar lebih jauh tentang cara2 membuat website responsive.

**3.** Yang sangat saya rasakan adalah saya tidak bisa membuat polaroid foto bertumpuk saya bertukar tempat dengan foto yang lain. Berdasarkan itu, saya ingin menyiapkan cara untuk membuat elemen saling bertukar tempat pada iterasi proyek selanjutnya.

### Tugas 2

**1.** Alur request sampai data muncul di browser:

1. Browser request `/outside-work/`
2. urls menentukan view
3. view mengambil data lewat Model/ORM
4. Data dimasukkan ke context
5. template mengubahnya menjadi HTML
6. HTML dikirim ke browser

```
URL → View → Model → Database → Template → Browser
```

**2.** Agar data dan tampilan terpisah. Data jadi bisa ditambah/diubah lewat datase tanpa mengubah HTML atau deploy ulang, dan bisa dipake berulang kali di section/halaman berbeda.

**3.** `makemigrations` hanya membuat file yang berisi rencana perubahan database, sementara `migrate` menjalankan perubahan tersebut ke database.

### Tugas 3

**1.** Mengapa menggunakan ModelForm dan {% csrf_token %}?

ModelForm digunakan untuk mengambil model dari Django. Tujuannya: 
1. tidak perlu menulis ulang field karena sudah digenerate langsung dari model
2. Validasi data otomatis
3. Langsung bisa form.save() untuk menyimpan data ke database
4. Sinkronisasi otomatis. Ketika kita menambah field di model, form ikut terupdate tanpa perlu mengubah file HTML. 

crsf_token digunakan untuk menghindari serangan CSRF dimana orang lain dapat mengirim request POST ke website kita dengan session/cookie user yang sedang login. Tag crsf_token menyisipkan token acak unik ke dalam form, sehingga saat POST masuk, Django akan membandingkan token di form dengan token di session. 

**2.** JSON lebih disukai dari ML karena lebih ringkas, native di Javascript.JSON, dan lebih mudah dibaca

**3.** Alur view mengembalikan portofolio dalam bentuk JSON: 

1. User membuka URL
2. main/urls.pyu mencocokkan URL dan meneruskannya ke view di main/views.py
3. Di vie,w, data diambil dari database lewat Product.objects.all() yang menhasilkan QuerySet (objecct Python)
4. Queryset itu di-serialize lewat serializers.serialize("json", data) untuk diubah menjadi string JSON
5. View mengembalikan HttpResponse 
6. Browser/client menerima respons berisi teks JSON, bukan HTML 

jadi, harus di-serialize dulu karena object Django adalah object Python yang tidak dapat langsung dikirim protokol HTTP. Oleh karena itu, serialization mengubah object itu jadi format teks standar (JSON) yang bisa dikirim lewat jaringan dan dibaca ulang oleh bahasa apapun


### Tugas 5

**1.** Debouncing = nunda fungsi sampai user berhenti ngetik sebentar.
- Tiap ketikan: timer lama dibatalkan (`clearTimeout`), timer baru dipasang (`setTimeout` 300 ms).
- Request baru dikirim kalau 300 ms lewat tanpa ketikan baru.
- Penting karena tanpa debounce, tiap huruf = 1 request ("Django" = 6 request). Server jadi berat dan hasil lama bisa nimpa hasil baru.

**2.** `await` = tunggu `fetch()` selesai dulu, baru lanjut ke baris berikutnya.
- `fetch()` cuma ngasih Promise ("janji, hasilnya nyusul"), bukan data.
- Tanpa `await`, variabelnya masih Promise yang belum selesai. `response.ok` jadi `undefined` dan `response.json()` error, karena datanya belum datang.

**3.** XSS = penyerang nyelipin JavaScript ke halaman kita, lalu kode itu jalan di browser orang lain.
- Template Django otomatis nge-escape `{{ variabel }}`, jadi tag HTML tampil sebagai teks biasa.
- Lewat AJAX, data JSON dimasukin ke HTML pakai `innerHTML` tanpa escape otomatis, jadi browser bisa ngejalanin tag seperti `<img onerror="...">`.
- Solusinya: `escapeHtml` di JavaScript + `strip_tags` di `clean_<field>` pada form.
---

## AI Disclosure

Saya menggunakan AI untuk membantu memahami struktur kode Django dan syntax untuk perubahan yang ingin saya buat. Untuk menjamin pemahaman, saya tidak melakukan copy-paste kode secara buta, dan meminta AI menjelaskan tiap baris dari kode yang diberikan jika saya belum paham.

**Tools yang digunakan:** Claude

## AI Disclosure

Saya menggunakan AI untuk memahami alur AJAX, debouncing, modal, dan perlindungan XSS, lalu menerapkannya ke halaman Experience. Sebagian kode template dan JavaScript saya salin dari AI karena waktu mendekati tenggat, dan akan saya kerjakan ulang sendiri sebagai persiapan kuis.

**Tools yang digunakan:** Claude

### Strategi prompting

- Mengunggah PDF Tutorial 5 dan Tugas 5, lalu meminta penjelasan alur besar dulu (browser ↔ server) sebelum masuk kode.
- Meminta halaman belajar interaktif: tiap bagian berisi penjelasan cara kerja dan hubungan antarfile, pertanyaan yang harus saya jawab sendiri, baru kunci jawaban dan kode terbuka.
- Mengirim isi `main/views.py`, `main/models.py`, `main/forms.py`, dan template saya supaya kode disesuaikan dengan proyek saya, bukan contoh tutorial.
- Mengecek tiap perubahan dengan `python manage.py runserver` dan mengirim pesan error ke AI saat gagal.

### Batasan AI

1. **AI tidak tahu ketergantungan di kode saya.** `show_experiences` lama memanggil `get_experiences_json` lalu melakukan deserialisasi, sehingga perubahan format JSON akan membuat halaman crash. Ini baru ketahuan setelah saya mengirim isi `main/views.py`.
2. **Kode yang benar tetap bisa salah saat ditempel.** Saya sempat menaruh method `clean_*` di `main/models.py` (seharusnya di `main/forms.py`) dan membuat `return` masuk ke dalam loop di `get_experiences_json`. Keduanya saya perbaiki manual setelah melihat warning editor dan error server.

### Link prompt

Sama seperti Tugas 3, saya menggunakan satu chat dari awal sampai akhir sehingga log lengkapnya bisa ditelusuri berurutan: https://claude.ai/cowork/cse_013MtGmYPeekJfgQk582XwLH