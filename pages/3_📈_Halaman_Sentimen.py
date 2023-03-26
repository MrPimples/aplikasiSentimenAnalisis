import streamlit as st
import time
import pandas as pd
import numpy as np
import module.hasilSentimen as hs


st.set_page_config(page_title="Plotting Demo", page_icon="📈")

st.title("📈Halaman Sentimen")
st.write(
    """Halaman ini berfungsi untuk menampilkan jumlah sentimen positif dari setiap bakal calon yang tersedia.
    Data yang digunakan diambil dari bulan Desember 2022, Januari 2023 dan Februari 2023. Untuk jumlah data tiap satu bakal calon 
    diambil sebanyak 4000 per bulan dan dibagi dalam bentuk 1000 per minggu dan hasil sentimen positif yang ditampilkan dibagi ke 4 minggu"""
)

namaCalon = ['Agus Harimurti Yudhono', 'Anies Baswedan', 'Ganjar Pranowo', 'Prabowo Subianto', 'Puan Maharani', 'Ridwan Kamil']
listBulan = ['Desember 2022', 'Januari 2023', 'Februari 2023']

# pilihanCalon1 = st.selectbox('Pilih Nama Calon 1', namaCalon)
# pilihanCalon2 = st.selectbox('Pilih Nama Calon 2', namaCalon)

pilihanCalon = st.multiselect('Pilih Nama Bakal Calon', namaCalon)

pilihanBulan = st.selectbox('Pilih Waktu yang akan ditampilkan', listBulan)

if st.button('Lihat Sentimen'):
    with st.spinner('Wait for it...'):
        hasil = hs.tampilSentimen(pilihanCalon,pilihanBulan)
    tab1, tab2, tab3 = st.tabs(["📈Grafik Garis", "📊Grafik Batang",'📅Tabel Hasil'])
    pilihanCalon.insert(0, 'Minggu')
    with tab1:
        st.title('Grafik Garis')
        dataPolaritas = hasil

        chart_data = pd.DataFrame(
            dataPolaritas,
            columns=pilihanCalon)

        st.line_chart(chart_data,x='Minggu')
    with tab2:
        st.title('Grafik Batang')
        dataPolaritas = hasil

        chart_data = pd.DataFrame(
            dataPolaritas,
            columns=pilihanCalon)

        st.bar_chart(chart_data,x='Minggu')
    with tab3:
        st.title('Tabel Hasil')
        df = pd.DataFrame(
            dataPolaritas,
            columns=pilihanCalon)
    
        # CSS to inject contained in a string
        hide_table_row_index = """
                    <style>
                    thead tr th:first-child {display:none}
                    tbody th {display:none}
                    </style>
                    """

        # Inject CSS with Markdown
        st.markdown(hide_table_row_index, unsafe_allow_html=True)

        # Display a static table
        st.table(df)
