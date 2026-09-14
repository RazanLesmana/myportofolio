Proyek PBP myportofolio

Nama: Razan Muhammad Fathin Lesmana
NPM: 2506603646
Kelas: PBP A

Link PWS: https://razan-muhammad51-myportofolio.pws.cs.ui.ac.id/
Repository: https://github.com/RazanLesmana/myportofolio

## DESKRIPSI PROYEK
Website portofolio pribadi ini menampilkan profil, pengalaman, penghargaan, proyek, dan halaman "contact me". Proyek ini juga mengintegrasikan siapa Razan di luar pengalaman dan pekerjaannya lewat elemen tambahan seperti foto. 

Proyek ini dibangun dengan Django sebagai fullstack framework (menangani routing, tempating, dan (nanti?) persistence). Tampilan dibangun manual dengan HTML + CSS.

Status saat ini: Selesai Tugas 1

## SETUP MINGGU PERTAMA
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

Data contoh Outside Work masuk otomatis lewat data migration,
jadi tidak perlu diisi manual.

Buka http://localhost:8000/

=====PROGRESS MINGGUAN=====
# Minggu 0:
- Setup Sesuai Tutorial 0 

# Minggu 1: 
- Setup sesuai tutorial 1
- Merevisi warna yang digunakan dan struktur hero section
- Mengganti foto menjadi polaroid bertumpuk
- Menambahkan page "Experience" 
- Menambahkan placeholder page "Achievement", "Projects", dan "Contact Me" 

# Minggu 2:
- Setup sesuai tutorial 2
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


===== PERTANYAAN REFLEKTIF =====
## Tugas 1: 
1. Saya tidak menggunakan elemen <article> dan <aside>, tetapi menggunakan <section>. <section> ini saya gunakan untuk membuat section experience. Saya rasa tanpa <article> dan <aside>, seluruh kebutuhan desain saya sudah terpenuhi dengan <section> dan <div> untuk membagi design menjadi beberapa bagian. 

2. Tantangan terberat saya adalah mengatur jarak antar elemen pada header. Saya mengevaluasinya dengan mencoba-coba mengedit ukuran di css dan jika belum berhasil saya bertanya kepada AI. Akhirnya, saya menemukan masalahnya adalah header dibagi menjadi 4 grid, sehingga ada jarak antar grid. 

Untuk saat ini, saya mengatur responsiveness lewat ukuran container, dan saya rasa hanya h1 yang benar2 memiliki ukuran responsif. Ini akan saya improve seiring saya belajar lebih jauh tentang cara2 membuat website responsive. 

3. Yang sangat saya rasakan adalah saya tidak bisa membuat polaroid foto bertumpuk saya bertukar tempat dengan foto yang lain. Berdasarkan itu, saya ingin menyiapkan cara untuk membuat elemen saling bertukar tempat pada iterasi proyek selanjutnya. 

## Tugas 2
1. alur request sampai data muncul di browser: 
   1. Browser request /outside-work/ 
   2. urls menentukan view
   3. view mengambil data lewat Model/ORM
   4. Data dimasukkan ke context
   5. template mengubahnya menjadi HTML 
   6. HTML dikirim ke browser 
   URL -> View -> Model -> Database -> Template -> Browser
2. Agar data dan tampilan terpisah. Data jadi bisa ditambah/diubah lewat datase tanpa mengubah HTML atau deploy ulang, dan bisa dipake berulang kali di section/halaman berbeda. 
3. makemigrations hanya membuat file yang berisi rencana perubahan database, sementara migrate menjalankan perubahan tersebut ke database. 


## AI Disclosure

Saya menggunakan AI untuk membantu memahami struktur kode Django dan syntax
untuk perubahan yang ingin saya buat. Untuk menjamin pemahaman, saya tidak
melakukan copy-paste kode secara buta, dan meminta AI menjelaskan tiap baris
dari kode yang diberikan jika saya belum paham.

**Tools yang digunakan:** Claude

### Strategi prompting

Berbeda dari Tugas 1, kali ini saya meminta AI memecah pekerjaan menjadi
langkah-langkah bernomor terlebih dahulu, lalu mengerjakannya satu per satu.
Untuk tiap langkah saya minta tiga hal: kode, penjelasan kenapa kodenya seperti
itu, dan cara memverifikasi bahwa langkah tersebut sudah benar sebelum lanjut
ke langkah berikutnya.

Saya juga berhenti bertanya konsep setiap kali menemui syntax yang belum saya
pahami — misalnya fungsi `{% endif %}` dan `{% endfor %}`, kegunaan
`{% load static %}`, cara kerja `@media`, dan arti `&copy;`. Ketika AI memberi
saran, saya menanyakan alasannya sebelum menerapkan, bukan langsung menempel.

### Batasan AI

1. **Diagnosis yang salah.** Ketika judul section "Photography" tidak muncul di
   layar lebar, AI menduga penyebabnya aturan CSS yang terduplikasi dan meminta
   saya menghitung kemunculan tiap selektor. Ternyata tidak ada duplikat sama
   sekali. Penyebab aslinya baru ketemu setelah saya mengirim seluruh isi
   `style.css`: satuan `height: 100%vh` yang tidak valid, yang membuat foto hero
   meluber keluar dan menutupi judul di bawahnya.

2. **Saran yang tidak perlu.** AI memberi blok CSS baru untuk navbar, padahal
   aturan `.site-header nav a` sudah ada di berkas saya sejak Tugas 1. Saya
   menolak saran tersebut karena hanya akan menghasilkan aturan kembar dan
   menutupi masalah yang sebenarnya.

3. **Struktur data yang tidak konsisten.** AI menyarankan foto sampul halaman
   diberi `album = "Singapore, 2024"`, padahal perannya adalah sampul untuk
   seluruh halaman yang mencakup tiga section, bukan anggota album Singapura.
   Setelah saya tanyakan, strukturnya diperbaiki menjadi album kosong.

Kesimpulan saya: AI cukup diandalkan untuk menjelaskan konsep dan memberi
kerangka kode, tetapi tidak bisa dipercaya untuk mendiagnosis bug tanpa melihat
kode yang lengkap. Beberapa kali AI menebak sebelum punya informasi yang cukup,
dan saya perlu memverifikasi sendiri lewat DevTools.

### Link prompt

Berbeda dari Tugas 1 yang promptnya tersebar di banyak chat dan dua AI berbeda,
untuk Tugas 2 saya menggunakan satu chat dari awal sampai akhir, sehingga log
lengkapnya bisa ditelusuri berurutan: 