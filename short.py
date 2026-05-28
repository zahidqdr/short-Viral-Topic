import streamlit as st

st.title("⚡ Voltage Divider Calculator")

st.write("R1, R2 aur Input Voltage enter karo aur output voltage calculate karo")

# Inputs
vin = st.number_input("Input Voltage (Vin)", value=12.0)
r1 = st.number_input("Resistor R1 (Ohms)", value=1000.0)
r2 = st.number_input("Resistor R2 (Ohms)", value=1000.0)

# Formula
if r1 > 0 and r2 > 0:
    vout = vin * (r2 / (r1 + r2))

    st.success(f"Output Voltage (Vout): {vout:.2f} V")

    st.latex(r"V_{out} = V_{in} \times \frac{R_2}{R_1 + R_2}")

else:
    st.error("R1 aur R2 zero se zyada hone chahiye")
