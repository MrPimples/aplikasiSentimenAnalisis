import streamlit as st
import time
import module.hasilModel as hm

st.title("🎭Halaman Hasil Model")
st.write("Halaman ini berfungsi untuk menampilkan hasil validasi dari model yang telah dibuat dan yang digunakan pada halaman sentimen."
         " Parameter validasi untuk modelnya berupa Accuracy, Precision, Recall dan F-Score")

if st.button('Lihat Hasil'):
    with st.spinner('Wait for it...'):
        time.sleep(1)
        outputModel = hm.hasilModel()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Accuracy", "{:.2f}%".format(outputModel['accuracy']))
    col2.metric("Precision", "{:.2f}%".format(outputModel['precision']))
    col3.metric("Recall", "{:.2f}%".format(outputModel['recall']))
    col4.metric("F-Score", "{:.2f}%".format(outputModel['fscore']))
    successDialog = st.empty()
    successDialog.success('Selesai!')
    time.sleep(2)
    successDialog.empty()

else:
    st.write('Silahkan Tekan Tombol Lihat Hasil')  
