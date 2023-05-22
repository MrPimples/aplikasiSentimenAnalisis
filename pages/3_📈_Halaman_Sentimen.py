import streamlit as st
import pandas as pd
import module.hasilSentimen as hs
import plotly.express as px

st.set_page_config(page_title="Halaman Sentimen", page_icon="📈")

st.title("📈Halaman Sentimen")
st.write(
    """Halaman ini berfungsi untuk menampilkan jumlah sentimen positif dari setiap bakal calon yang tersedia.
    Data yang digunakan diambil dari bulan Desember 2022, Januari 2023 dan Februari 2023. Untuk jumlah data tiap satu bakal calon 
    diambil sebanyak 4000 per bulan dan dibagi dalam bentuk 1000 per minggu dan hasil sentimen positif yang ditampilkan dibagi ke 4 minggu"""
)

namaCalon = ['Agus Harimurti Yudhono', 'Anies Baswedan', 'Ganjar Pranowo', 'Prabowo Subianto', 'Puan Maharani', 'Ridwan Kamil']
listBulan = ['Desember 2022', 'Januari 2023', 'Februari 2023']
kolomChart = ['Minggu']

pilihanCalon = st.multiselect('Pilih Nama Bakal Calon', namaCalon)

pilihanBulan = st.selectbox('Pilih Waktu yang akan ditampilkan', listBulan)

if(len(pilihanCalon) > 0):
    if st.button('Lihat Sentimen'):
        with st.spinner('Sedang memproses....'):
            hasil = hs.tampilSentimen(pilihanCalon,pilihanBulan)
        tab1, tab2, tab3 = st.tabs(["📈Grafik Garis", "📊Grafik Batang",'📅Tabel Hasil'])
        kolomChart.extend(pilihanCalon)
        
        dataPolaritas = hasil

        dataTampil = pd.DataFrame(
            dataPolaritas,
            columns=kolomChart)
        
        with tab1:
            st.write("Tab ini menampilkan total sentimen positif dalam bentuk grafik garis dari tiap bakal calon dengan rentang nilai 0-1000 dan menggunakan model dengan tingkat kepercayaan atau accuracy sebesar 98.25%")
            st.write('#### Hasil Sentimen Bulan', pilihanBulan)
            
            st.line_chart(dataTampil,x='Minggu')
        with tab2:
            st.write("Tab ini menampilkan total sentimen positif dalam bentuk grafik batang dari tiap bakal calon dengan rentang nilai 0-1000 dan menggunakan model dengan tingkat kepercayaan atau accuracy sebesar 98.25%")
            st.write('#### Hasil Sentimen Bulan', pilihanBulan)

            fig = px.bar(dataTampil, x="Minggu", y=pilihanCalon, barmode='group', height=400)

            st.plotly_chart(fig)
        with tab3:
            st.write("Tab ini menampilkan total sentimen positif dalam bentuk tabel dari tiap bakal calon dengan rentang nilai 0-1000 dan menggunakan model dengan tingkat kepercayaan atau accuracy sebesar 98.25%")
            st.write('#### Hasil Sentimen Bulan', pilihanBulan)
        
            hide_table_row_index = """
                        <style>
                        thead tr th:first-child {display:none}
                        tbody th {display:none}
                        </style>
                        """

            st.markdown(hide_table_row_index, unsafe_allow_html=True)

            st.table(dataTampil)
