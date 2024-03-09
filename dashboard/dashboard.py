# Import library
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import base64

# Load data
day_df = pd.read_csv("data/day.csv")
hour_df = pd.read_csv("data/hour.csv")


# Define title and styling
st.write('<h1 style="text-align: center;">Analisis Data Bike Sharing</h1>', unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Dashboard")
selected_option = st.sidebar.selectbox("Pilih Tampilan", ["Tabel", "Data Visual"])

# Load your CSV data
hour_data = pd.read_csv("hour.csv")
day_data = pd.read_csv("day.csv")

# Sidebar
st.sidebar.title("Download Data")


# Add button to download the main data CSV file in the sidebar
if st.sidebar.button("Download Main Data CSV"):
    csv = all_df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # Some encoding
    href = f'<a href="data:file/csv;base64,{b64}" download="main_data.csv">Download Main Data CSV</a>'
    st.sidebar.markdown(href, unsafe_allow_html=True)

# Main content
if selected_option == "Tabel":
    st.subheader("Tabel Data")
    st.write("### Day Dataset")
    st.write(day_df.describe())
    st.write("### Hour Dataset")
    st.write(hour_df.describe())

elif selected_option == "Data Visual":
    # Data Visual jumlah peminjaman sepeda berdasarkan hari dalam seminggu
    # Visualisasi pengaruh kondisi cuaca terhadap jumlah peminjaman sepeda menggunakan line plot

    st.write(
    """
    # Hasil Visualisasi No.1
    Bagaimana Pengaruh kondisi cuaca terhadap pola peminjaman sepeda?
    """)

    merged_data = pd.merge(hour_data, day_data, on='dteday')

    plt.figure(figsize=(10, 6))
    sns.lineplot(x='dteday', y='cnt_x', hue='weathersit_x', data=merged_data, estimator=sum)
    plt.title('Perubahan Jumlah Peminjaman Sepeda berdasarkan Kondisi Cuaca')
    plt.xlabel('Tanggal')
    plt.ylabel('Jumlah Peminjaman Sepeda')
    plt.legend(title='Kondisi Cuaca')
    # Get the current figure and pass it to st.pyplot()
    fig = plt.gcf()
    st.pyplot(fig)
    
    st.write(
    """
    # Hasil Visualisasi No.2 
    Kira-kira berapa jumlah peminjaman sepeda berdasarkan Jam?
    """)

    # Load data
    hour_data = pd.read_csv('D:\Semester 6\Bangkit\Dicoding\Analisis_Data_Nadya\data\hour.csv')

    # Hitung rata-rata jumlah peminjaman sepeda untuk setiap jam
    average_rentals_by_hour = hour_data.groupby('hr')['cnt'].mean()

    # Plot jumlah rata-rata peminjaman sepeda berdasarkan jam dalam satu hari
    plt.figure(figsize=(10, 6))
    plt.plot(average_rentals_by_hour.index, average_rentals_by_hour.values, marker='o')
    plt.title('Rata-Rata Jumlah Peminjaman Sepeda per Jam dalam Satu Hari')
    plt.xlabel('Jam (1-24)')
    plt.ylabel('Rata-Rata Jumlah Peminjaman')
    plt.xticks(range(0, 24))  # Mengatur label sumbu x mulai dari jam 1 hingga 24
    plt.grid(True)
    # Get the current figure and pass it to st.pyplot()
    fig = plt.gcf()
    st.pyplot(fig)

    st.write(
    """
    Kira-kira berapa jumlah peminjaman sepeda berdasarkan Hari?
    """)

        # Ubah tipe data kolom 'dteday' menjadi datetime
    merged_data['dteday'] = pd.to_datetime(merged_data['dteday'])

    # Hitung rata-rata jumlah peminjaman sepeda berdasarkan hari dalam satu minggu
    average_rentals_by_weekday = merged_data.groupby(merged_data['dteday'].dt.dayofweek)['cnt_x'].mean()

    # Plot untuk rata-rata jumlah peminjaman sepeda berdasarkan hari dalam satu minggu
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(average_rentals_by_weekday.index, average_rentals_by_weekday.values)
    ax.set_title('Rata-Rata Jumlah Peminjaman Sepeda berdasarkan Hari dalam Satu Minggu')
    ax.set_xlabel('Hari')
    ax.set_ylabel('Rata-Rata Jumlah Peminjaman')

    # Tampilkan plot menggunakan st.pyplot() dengan menyertakan objek figure
    st.pyplot(fig)
