import streamlit as st

st.title("⚡ Voltage Divider Calculator (Advanced)")

st.write("R1, R2 aur Input Voltage enter karo aur unit select karo")

# Unit conversion function
def convert_to_ohm(value, unit):
    if unit == "Ω":
        return value
    elif unit == "kΩ":
        return value * 1000
    elif unit == "MΩ":
        return value * 1000000

# Input Voltage
vin = st.number_input("Input Voltage (Vin)", value=12.0)

st.subheader("R1")
r1_value = st.number_input("R1 Value", value=1.0)
r1_unit = st.selectbox("R1 Unit", ["Ω", "kΩ", "MΩ"])

st.subheader("R2")
r2_value = st.number_input("R2 Value", value=1.0)
r2_unit = st.selectbox("R2 Unit", ["Ω", "kΩ", "MΩ"])

# Convert to ohms
r1 = convert_to_ohm(r1_value, r1_unit)
r2 = convert_to_ohm(r2_value, r2_unit)

# Calculation
if r1 > 0 and r2 > 0:
    vout = vin * (r2 / (r1 + r2))

    st.success(f"Output Voltage (Vout): {vout:.2f} V")

    st.latex(r"V_{out} = V_{in} \times \frac{R_2}{R_1 + R_2}")

    st.write("### Converted Values")
    st.write(f"R1 = {r1} Ω")
    st.write(f"R2 = {r2} Ω")

else:
    st.error("R1 aur R2 zero se zyada hone chahiye")
