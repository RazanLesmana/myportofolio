Proyek PBP myportofolio

Nama: Razan Muhammad Fathin Lesmana
NPM: 2506603646
Kelas: PBP A

Link PWS: https://razan-muhammad51-myportofolio.pws.cs.ui.ac.id/
Repository: https://github.com/RazanLesmana/myportofolio

=====DESKRIPSI PROYEK=====
Website portofolio pribadi ini menampilkan profil, pengalaman, penghargaan, proyek, dan halaman "contact me". Proyek ini juga mengintegrasikan siapa Razan di luar pengalaman dan pekerjaannya lewat elemen tambahan seperti foto. 

Proyek ini dibangun dengan Django sebagai fullstack framework (menangani routing, tempating, dan (nanti?) persistence). Tampilan dibangun manual dengan HTML + CSS.

Status saat ini: Selesai Tugas 1

===== SETUP MINGGU PERTAMA=====
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


===== PERTANYAAN REFLEKTIF =====
# Tugas 1: 
1. Saya tidak menggunakan elemen <article> dan <aside>, tetapi menggunakan <section>. <section> ini saya gunakan untuk membuat section experience. Saya rasa tanpa <article> dan <aside>, seluruh kebutuhan desain saya sudah terpenuhi dengan <section> dan <div> untuk membagi design menjadi beberapa bagian. 

2. Tantangan terberat saya adalah mengatur jarak antar elemen pada header. Saya mengevaluasinya dengan mencoba-coba mengedit ukuran di css dan jika belum berhasil saya bertanya kepada AI. Akhirnya, saya menemukan masalahnya adalah header dibagi menjadi 4 grid, sehingga ada jarak antar grid. 

Untuk saat ini, saya mengatur responsiveness lewat ukuran container, dan saya rasa hanya h1 yang benar2 memiliki ukuran responsif. Ini akan saya improve seiring saya belajar lebih jauh tentang cara2 membuat website responsive. 

3. Yang sangat saya rasakan adalah saya tidak bisa membuat polaroid foto bertumpuk saya bertukar tempat dengan foto yang lain. Berdasarkan itu, saya ingin menyiapkan cara untuk membuat elemen saling bertukar tempat pada iterasi proyek selanjutnya. 


===== AI DISCLOSURE =====
Saya menggunakan AI untuk membantu saya memahami struktur kode dan bagaimana cara serta syntax untuk membuat perubahan yang ingin saya ubah. 

Untuk menjamin pemahaman, saya tidak melakukan copy-paste kode, dan memastikan AI untuk menjelaskan tiap baris dari kode yang diberikan (jika saya belum paham). 

Tools yang digunakan: ChatGPT dan Claude web

# Strategi prompting: 
Saya akan mengirim kode kepada AI, lalu bertanya "di bagian mana yang mengatur fitur/tampilan XXXX", lalu bertanya bagaimana mengaplikasikan perubahan yang saya mau pada bagian tersebut. Untuk memastikan pemahaman, saya meminta AI untuk menjelaskan tiap baris kode yang ia berikan 

# Batasan AI
1. [Mengikut batasan dari instruksi]: Saat saya bertanya tentang cara menukar-nukar foto polaroid bertumbuk, AI memberikan solusi dengan Javascript, padahal ini belum masuk scope dari tugas 1 ini
2. Saat ini saya baru menemukan batasan tersebut pada penggunaan AI saya

# Link prompt 
Selama mengerjakan tugas 1, saya membuka chat baru setiap kali ingin menanyakan sesuatu ke AI, jadi prompt sangat tersebar ke room chat AI yang berbeda, pada AI yang berbeda (ada yang di claude, ada yang di chatGPT)