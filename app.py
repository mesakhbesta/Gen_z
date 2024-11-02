import gdown
import pandas as pd
import streamlit as st
import os

# Nama file untuk disimpan
file_name = 'FINAL_CLUSTER.csv'

# Periksa apakah file sudah ada di direktori lokal
if not os.path.exists(file_name):
    # Link untuk mengunduh file dari Google Drive
    gdown.download('https://drive.google.com/uc?id=1VQH8OEgBZcZTTks0ZfeB0RLrFiZbyllo', file_name, quiet=False)

# Baca file CSV
data = pd.read_csv(file_name, sep="*")

# Header untuk aplikasi
st.markdown("<h1 style='text-align: center; color: #6A0DAD;'>🌟 Toko Gen-Z 🌟</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #333333;'>Temukan Rekomendasi Produk Terbaik dengan Harga Terjangkau!</h4>", unsafe_allow_html=True)

# Pilih kategori produk
selected_cluster = st.selectbox('💼 **Pilih Kategori Produk**', data['nama_cluster'].unique())

# Filter data berdasarkan kategori
filtered_data = data[data['nama_cluster'] == selected_cluster]

# Filter berdasarkan lokasi
locations = filtered_data['location'].unique()
selected_location = st.selectbox('📍 **Pilih Lokasi**', locations)

# Filter data berdasarkan lokasi
filtered_data = filtered_data[filtered_data['location'] == selected_location]

# Pilih kategori harga
selected_price_cluster = st.selectbox('💰 **Pilih Kategori Harga**', filtered_data['cluster_harga'].unique())
final_recommendations = filtered_data[filtered_data['cluster_harga'] == selected_price_cluster]

# Tentukan jumlah produk yang ditampilkan
max_display = st.number_input('📋 **Jumlah Produk yang Ditampilkan**', min_value=1, max_value=len(final_recommendations), value=5)

# Tombol cari produk
if st.button('🔍 **Cari Produk**'):
    # Buat tab menu
    tab1, tab2, tab3 = st.tabs(["Rekomendasi Produk", "Statistik Produk", "Produk Paling Populer"])

    # Tab 1: Rekomendasi Produk
    with tab1:
        st.subheader('🎁 **Rekomendasi Produk Terbaik**')
        
        # Prioritaskan produk dengan rating 5
        five_star_products = final_recommendations[final_recommendations['rating'] == 5]
        other_products = final_recommendations[final_recommendations['rating'] < 5]

        top_products = pd.concat([five_star_products, other_products])  # Menggabungkan menggunakan pd.concat

        if not top_products.empty:
            for index, row in top_products.head(max_display).iterrows():
                sold_formatted = f"{int(row['sold']):,.0f}".replace(",", ".")
                st.markdown(
                    f"""
                    <div style="border: 2px solid #DDA0DD; border-radius: 10px; padding: 15px; margin: 10px 0; background-color: #F9F0FF;">
                        <h4 style="color: #4B0082;">🛍️ Nama Produk: <span style="color: #8A2BE2;">{row['clean_name']}</span></h4>
                        <p style="color: #5F9EA0;">📍 Lokasi: <strong>{row['location']}</strong></p>
                        <p style="color: #5F9EA0;">⭐ Rating: <strong>{row['rating']}</strong> | Terjual: <strong>{sold_formatted}</strong></p>
                        <p style="color: #8B4513;">💸 Harga: <strong>Rp{int(row['price']):,.0f}</strong></p>
                    </div>
                    """, unsafe_allow_html=True
                )
        else:
            st.markdown("<p style='color: #DC143C;'>Tidak ada produk yang ditemukan untuk kategori ini.</p>", unsafe_allow_html=True)

    # Tab 2: Statistik Produk
    with tab2:
        st.subheader("📊 Statistik Produk")
        st.markdown("Tampilkan statistik singkat mengenai produk berdasarkan kategori dan harga.")
        
        # Statistik sederhana
        st.write("Total Produk:", len(filtered_data))
        st.write("Rata-rata Harga:", f"Rp{filtered_data['price'].mean():,.0f}".replace(",", "."))
        st.write("Rata-rata Rating:", f"{filtered_data['rating'].mean():.2f}")

    # Tab 3: Produk Paling Populer
    with tab3:
        st.subheader("🔥 **Produk Paling Populer**")
        
        # Menghitung produk paling terjual
        popular_products = filtered_data.sort_values(by='sold', ascending=False).head(10)

        if not popular_products.empty:
            for index, row in popular_products.iterrows():
                sold_formatted = f"{int(row['sold']):,.0f}".replace(",", ".")
                st.markdown(
                    f"""
                    <div style="border: 2px solid #DDA0DD; border-radius: 10px; padding: 15px; margin: 10px 0; background-color: #F9F0FF;">
                        <h4 style="color: #4B0082;">🛍️ Nama Produk: <span style="color: #8A2BE2;">{row['clean_name']}</span></h4>
                        <p style="color: #5F9EA0;">⭐ Rating: <strong>{row['rating']}</strong> | Terjual: <strong>{sold_formatted}</strong></p>
                        <p style="color: #8B4513;">💸 Harga: <strong>Rp{int(row['price']):,.0f}</strong></p>
                    </div>
                    """, unsafe_allow_html=True
                )
        else:
            st.markdown("<p style='color: #DC143C;'>Tidak ada produk yang ditemukan untuk kategori ini.</p>", unsafe_allow_html=True)

# Menambahkan footer
st.markdown("<footer style='text-align: center; color: #333333;'>Terima kasih telah mengunjungi Toko Gen-Z! 🛒</footer>", unsafe_allow_html=True)
