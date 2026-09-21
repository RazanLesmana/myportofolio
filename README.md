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

---

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

---

## AI Disclosure

Saya menggunakan AI untuk membantu memahami struktur kode Django dan syntax untuk perubahan yang ingin saya buat. Untuk menjamin pemahaman, saya tidak melakukan copy-paste kode secara buta, dan meminta AI menjelaskan tiap baris dari kode yang diberikan jika saya belum paham.

**Tools yang digunakan:** Claude

### Strategi prompting

Untuk Tugas 3 saya mengubah pendekatan di tengah jalan. Di awal saya masih meminta AI memberi kode per langkah seperti Tugas 2, tetapi setelah beberapa kali salah tempel berkas saya berhenti dan memutuskan menulis sendiri seluruh kodenya, lalu memakai AI hanya untuk menjelaskan konsep dan mengoreksi kesalahan saya.

Jadi selama mengerjakan tugas 3, saya hanya menggunakan AI untuk mengoreksi kesalahan dan membantu mempercepat proses penggantian nama variable pada CSS.

Konsep yang saya tanyakan sampai paham: perbedaan `Project`, `project`, dan `projects`; alasan `{% extends %}` membuang konten di luar `{% block %}` tanpa error; kenapa `serialize` lalu `deserialize` di satu view terlihat redundan tetapi tetap diminta; serta hubungan antara path URL, nama route, nama fungsi view, dan nama berkas template yang ternyata sama sekali tidak saling terikat.

### Batasan AI

1. **Menebak isi tutorial sebelum membacanya.** Di awal AI langsung mengimplementasikan empat view data delivery (`show_xml`, `show_json`, `show_xml_by_id`, `show_json_by_id`) berdasarkan asumsi pola PBP tahun sebelumnya. Setelah PDF Tutorial 3 benar-benar dibaca, ternyata yang diminta adalah satu endpoint `get_projects_json` dengan filter `?title=`. Keempat view tersebut harus saya hapus karena tidak diminta dan menduplikasi fungsi yang sudah ada.

2. **Instruksi yang ambigu merusak tampilan.** Saat membuat komponen modal hapus untuk Experience, AI menyuruh saya "salin polanya, ganti semua `project` jadi `experience`". Saya ikuti, termasuk mengganti nama class CSS-nya, sehingga `class="project-delete-modal"` berubah dan tidak ada aturan CSS yang cocok — modalnya muncul tanpa gaya sama sekali. AI baru menjelaskan bahwa nama class CSS adalah nama gaya, bukan nama data, dan tidak boleh ikut diganti, setelah saya mengeluh tampilannya jelek.

Kesimpulan saya: pola kegagalan AI di Tugas 3 sama dengan Tugas 2, yaitu menebak sebelum punya informasi yang cukup, tapi kali ini yang ditebak bukan bug, melainkan isi instruksi tugas. Karena itu saya belajar memaksa AI membaca sumber aslinya dulu, dan memverifikasi setiap klaimnya lewat perintah yang menampilkan kondisi berkas apa adanya, bukan lewat deskripsi.

### Link prompt

Sama seperti Tugas 2, saya menggunakan satu chat dari awal sampai akhir sehingga log lengkapnya bisa ditelusuri berurutan: https://claude.ai/cowork/cse_013MtGmYPeekJfgQk582XwLH