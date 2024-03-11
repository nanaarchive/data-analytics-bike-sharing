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
hour_data = pd.read_csv("data/hour.csv")
day_data = pd.read_csv("data/day.csv")

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
    # Load data
    merged_data = pd.read_csv('dashboard/main_data.csv')

    # Konversi kolom 'dteday' ke tipe datetime
    merged_data['dteday'] = pd.to_datetime(merged_data['dteday'])

    # Mengelompokkan data peminjaman sepeda untuk setiap tiga bulan
    total_rentals_by_3_months = merged_data.resample('3M', on='dteday')['cnt_x'].sum().reset_index()

    # Membuat dataframe baru dengan total jumlah peminjaman sepeda untuk setiap kondisi cuaca pada setiap tiga bulan
    total_rentals_by_weather_3_months = merged_data.groupby([pd.Grouper(key='dteday', freq='3M'), 'weathersit_x'])['cnt_x'].sum().reset_index()

    # Menentukan palet warna yang sama untuk scatterplot dan lineplot
    palette = sns.color_palette('Set2', len(total_rentals_by_weather_3_months['weathersit_x'].unique()))

    # Plot the data
    fig, ax = plt.subplots(figsize=(10, 6))

    # Menambahkan informasi kondisi cuaca dengan warna yang berbeda
    sns.scatterplot(data=total_rentals_by_weather_3_months, x='dteday', y='cnt_x', hue='weathersit_x', palette=palette, legend=True, s=100)

    # Menghubungkan titik-titik cuaca dengan garis untuk tiap kondisi cuaca
    for _, group_data in total_rentals_by_weather_3_months.groupby('weathersit_x'):
        sns.lineplot(data=group_data, x='dteday', y='cnt_x', marker='o', linestyle='-')

    plt.title('Pola Peminjaman Sepeda setiap Tiga Bulan dengan Kondisi Cuaca')
    plt.xlabel('Tanggal')
    plt.ylabel('Jumlah Total Peminjaman Sepeda')

    plt.xticks(rotation=45)  # Label sumbu x sesuai dengan bulan

    plt.tight_layout()  # Memperbaiki tata letak agar tidak tumpang tindih

    # Display the plot in Streamlit
    st.pyplot(fig)

    st.write(
    """
    # Hasil Visualisasi No.2
    Bagaimana Pengaruh kondisi cuaca terhadap pola peminjaman sepeda?
    """)

    # Load data
    hour_data = pd.read_csv('data/hour.csv')

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

    # Load data
    hourly_data = pd.read_csv('data/hour.csv')

    # Konversi kolom 'dteday' ke tipe datetime
    hourly_data['dteday'] = pd.to_datetime(hourly_data['dteday'])

    # Ambil informasi hari dari tanggal
    hourly_data['day_of_week'] = hourly_data['dteday'].dt.day_name()

    # Hitung rata-rata jumlah peminjaman sepeda untuk setiap hari dalam seminggu
    average_rentals_by_day = hourly_data.groupby('day_of_week')['cnt'].mean()

    # Urutkan berdasarkan urutan hari dalam seminggu
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    average_rentals_by_day = average_rentals_by_day.reindex(days_of_week)

    # Plot the data using bar chart
    st.bar_chart(average_rentals_by_day)
