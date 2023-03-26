import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Aplikasi Sentimen Analisis", page_icon="🎭")

st.title("🎭Aplikasi Sentimen Analisis Bakal Calon Presiden Indonesia 2024")

st.markdown(
    """
    Selamat Datang di Aplikasi Sentimen Analisis Bakal Calon Presiden Indonesia 2024. Aplikasi ini dibuat menggunakan
    bahasa pemrograman Python🐍 dan menggunakan framework GUI berupa Streamlit. Data yang digunakan saya ambil dari Twitter mulai dari bulan
    Desember 2022 sampai dengan Februari 2023.
    ### Aplikasi ini memiliki 2 menu
    - Menu pertama adalah menu untuk menampilkan hasil model yang telah dibuat sebelumnya berupa Accuracy, Precision, Recall dan F-Score.
    - Menu kedua berfungsi untuk menampilkan jumlah sentimen positif dari tiap bakal calon. Ada total 6 bakal calon
    ### Total terdapat 6 nama bakal calon yang tersedia
    - Bapak Agus Harimurti Yudhono
    - Bapak Anies Baswedan
    - Bapak Ganjar Pranowo
    - Bapak Prabowo Subianto
    - Ibu Puan Maharani
    - Bapak Ridwan Kamil
    
    #### Disclaimer
    Aplikasi ini merupakan bagian dari penelitian tugas akhir saya, saya tidak bermaksud untuk menjatuhkan pihak manapun dan saya juga tidak memihak pihak manapun. 
    Aplikasi ini saya buat murni untuk kebutuhan penelitian tugas akhir saya.
    
    -Dimas Rizky Sanjaya
"""
)