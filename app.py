import streamlit as st
from scipy.optimize import linprog
import math

st.set_page_config(page_title="Aplikasi Industri", layout="centered")

menu = st.sidebar.selectbox("Pilih Menu", [
    "Optimasi Produksi (LP)",
    "Model Persediaan (EOQ)",
    "Model Antrian (M/M/1)",
    "Break Even Point"
])

# --- 1. Linear Programming ---
if menu == "Optimasi Produksi (LP)":
    st.header("Optimasi Produksi - Linear Programming")
    
    st.markdown("Contoh: Maksimalkan Z = 40x + 30y dengan kendala:")
    st.latex(r'''
    \begin{align*}
    2x + y &\leq 40 \\
    x + 2y &\leq 50 \\
    x, y &\geq 0
    \end{align*}
    ''')

    if st.button("Hitung Optimasi"):
        # Maks: 40x + 30y → Min: -40x -30y
        c = [-40, -30]
        A = [[2, 1], [1, 2]]
        b = [40, 50]
        x_bounds = (0, None)
        y_bounds = (0, None)

        res = linprog(c, A_ub=A, b_ub=b, bounds=[x_bounds, y_bounds], method='highs')

        if res.success:
            st.success("Solusi optimal ditemukan!")
            st.write(f"x = {res.x[0]:.2f}")
            st.write(f"y = {res.x[1]:.2f}")
            st.write(f"Maksimum Z = {-res.fun:.2f}")
        else:
            st.error("Tidak ditemukan solusi.")

# --- 2. EOQ ---
elif menu == "Model Persediaan (EOQ)":
    st.header("Model Persediaan - EOQ")
    D = st.number_input("Permintaan tahunan (D)", min_value=1.0, value=1000.0)
    S = st.number_input("Biaya pemesanan per pesanan (S)", min_value=1.0, value=500.0)
    H = st.number_input("Biaya penyimpanan per unit per tahun (H)", min_value=1.0, value=2.0)

    if st.button("Hitung EOQ"):
        EOQ = math.sqrt((2 * D * S) / H)
        st.success(f"EOQ = {EOQ:.2f} unit per pesanan")

# --- 3. Antrian M/M/1 ---
elif menu == "Model Antrian (M/M/1)":
    st.header("Model Antrian - M/M/1")
    λ = st.number_input("Rata-rata kedatangan (λ)", min_value=0.01, value=5.0)
    μ = st.number_input("Rata-rata layanan (μ)", min_value=0.01, value=8.0)

    if st.button("Hitung Antrian"):
        if λ >= μ:
            st.error("Sistem tidak stabil: λ ≥ μ")
        else:
            ρ = λ / μ
            L = ρ / (1 - ρ)
            Lq = ρ**2 / (1 - ρ)
            W = 1 / (μ - λ)
            Wq = ρ / (μ - λ)

            st.write(f"Utilisasi server (ρ) = {ρ:.2f}")
            st.write(f"Jumlah rata-rata pelanggan dalam sistem (L) = {L:.2f}")
            st.write(f"Jumlah rata-rata dalam antrian (Lq) = {Lq:.2f}")
            st.write(f"Waktu rata-rata dalam sistem (W) = {W:.2f}")
            st.write(f"Waktu rata-rata dalam antrian (Wq) = {Wq:.2f}")

# --- 4. Break Even Point ---
elif menu == "Break Even Point":
    st.header("Analisis Titik Impas (Break Even Point)")
    FC = st.number_input("Biaya Tetap (Fixed Cost)", min_value=0.0, value=10000.0)
    P = st.number_input("Harga Jual per Unit", min_value=0.01, value=100.0)
    VC = st.number_input("Biaya Variabel per Unit", min_value=0.01, value=60.0)

    if st.button("Hitung BEP"):
        if P <= VC:
            st.error("Harga jual harus lebih tinggi dari biaya variabel.")
        else:
            BEP_unit = FC / (P - VC)
            BEP_revenue = BEP_unit * P
            st.write(f"BEP (unit) = {BEP_unit:.2f} unit")
            st.write(f"BEP (pendapatan) = Rp {BEP_revenue:,.2f}")

