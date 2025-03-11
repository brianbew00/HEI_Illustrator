import streamlit as st
import pandas as pd
from fpdf import FPDF

st.title("Home Equity Investment (HEI) Calculator")

# User inputs
home_value = st.number_input("Home Value ($)", value=1000000, step=10000)
home_price_appreciation = st.number_input("Appreciation (%)", value=2.0, step=0.1) / 100
premium_percentage = st.number_input("Premium Percentage (%)", value=20.0, step=0.1) / 100
hei_multiplier = st.number_input("HEI Multiplier", value=2.0, step=0.1)
investor_cap = st.number_input("Investor Cap (%)", value=20.0, step=0.1) / 100

# Derived calculations
premium_amount = home_value * premium_percentage
investor_percentage = hei_multiplier * premium_percentage

st.write("**Premium Amount:**", f"${premium_amount:,.0f}")
st.write("**Investor Percentage:**", f"{investor_percentage*100:.0f}%")

# Initialize lists for yearly values
years = []
home_values = []
hei_caps = []
hei_intrinsic_values = []
settlement_values = []

# Year 0 calculations
years.append(0)
home_values.append(home_value)
current_hei_cap = premium_amount
hei_caps.append(current_hei_cap)
hei_intrinsic = investor_percentage * home_value
hei_intrinsic_values.append(hei_intrinsic)
settlement_values.append(min(current_hei_cap, hei_intrinsic))

# Calculate values for years 1 to 10
current_home_value = home_value
for year in range(1, 11):
    current_hei_cap *= (1 + investor_cap)
    current_home_value *= (1 + home_price_appreciation)
    hei_intrinsic = investor_percentage * current_home_value
    settlement = min(current_hei_cap, hei_intrinsic)
    
    years.append(year)
    home_values.append(current_home_value)
    hei_caps.append(current_hei_cap)
    hei_intrinsic_values.append(hei_intrinsic)
    settlement_values.append(settlement)

# Create a DataFrame to display the results
df = pd.DataFrame({
    "Year": years,
    "Home Value": [round(val) for val in home_values],
    "HEI Cap": [round(val) for val in hei_caps],
    "HEI Intrinsic Value": [round(val) for val in hei_intrinsic_values],
    "Settlement Value": [round(val) for val in settlement_values],
})
st.subheader("Calculation Results")
st.table(df)

# Plot the results as a line chart
chart_data = df.set_index("Year")
st.subheader("HEI Calculator Chart")
st.line_chart(chart_data)

# Function to generate a PDF from the table data
def generate_pdf(dataframe):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "HEI Calculator Report", ln=1, align="C")
    pdf.ln(10)
    
    # Table header
    pdf.set_font("Arial", 'B', 12)
    col_width = pdf.w / 5  # Divide page width equally among columns
    headers = list(dataframe.columns)
    for header in headers:
        pdf.cell(col_width, 10, header, border=1)
    pdf.ln(10)
    
    # Table rows
    pdf.set_font("Arial", '', 12)
    for _, row in dataframe.iterrows():
        pdf.cell(col_width, 10, str(row["Year"]), border=1)
        pdf.cell(col_width, 10, f'${row["Home Value"]:,}', border=1)
        pdf.cell(col_width, 10, f'${row["HEI Cap"]:,}', border=1)
        pdf.cell(col_width, 10, f'${row["HEI Intrinsic Value"]:,}', border=1)
        pdf.cell(col_width, 10, f'${row["Settlement Value"]:,}', border=1)
        pdf.ln(10)
    
    # Return PDF as bytes
    return pdf.output(dest="S").encode("latin1")

# Generate PDF and create a download button
pdf_bytes = generate_pdf(df)
st.download_button(
    label="Download PDF",
    data=pdf_bytes,
    file_name="HEI_Calculator_Report.pdf",
    mime="application/pdf"
)
