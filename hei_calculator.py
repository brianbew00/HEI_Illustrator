import streamlit as st
import pandas as pd
import numpy as np

st.title("Home Equity Investment (HEI) Calculator")

# Input Fields
home_value = st.number_input("Home Value ($)", value=1000000, step=10000)
home_appreciation = st.number_input("Home Price Appreciation (%)", value=2.0, format="%.2f") / 100
premium_percentage = st.number_input("Premium Percentage (%)", value=20.0, format="%.2f") / 100
hei_multiplier = st.number_input("HEI Multiplier", value=2.0, format="%.2f")
investor_cap = st.number_input("Investor Cap (%)", value=20.0, format="%.2f") / 100

premium_amount = homeValue * premium_percentage
investor_percentage = hei_multiplier * premium_percentage

st.markdown(f"**Premium Amount:** ${premium_amount:,.0f}")
st.markdown(f"**Investor Percentage:** {investor_percentage*100:.0f}%")

# Calculation logic
hei_cap = premium_amount
years = list(range(11))
data = []
current_home_value = home_value

for year in years:
    hei_intrinsic_value = investor_percentage * current_home_value
    settlement_value = min(hei_cap, hei_intrinsic_value)

    data.append({
        "Year": year,
        "Home Value": current_home_value,
        "HEI Cap": hei_cap,
        "HEI Intrinsic Value": hei_intrinsic_value := investor_percentage * current_home_value,
        "Settlement Value": min(hei_cap, hei_intrinsic_value)
    })

    # Update values for next year
    hei_cap *= (1 + investor_cap)
    current_home_value *= (1 + home_appreciation := home_appreciation)

# Create dataframe
df = pd.DataFrame(data)

# Display table with highlighting
def highlight_lesser(row):
    highlight = ["" for _ in row]
    if row["HEI Cap"] < row["HEI Intrinsic Value"]:
        highlight_col = "HEI Cap"
    else:
        highlight_col = "HEI Intrinsic Value"

    highlight = ["background-color: lightgreen" if col == highlight_col else "" for col in row.index]
    return highlight

st.dataframe(pd.DataFrame(data).style.apply(highlight, axis=1))

# Chart visualization
chart_data = {
    'Home Value': [row["Home Value"] for row in data],
    'HEI Cap': [row["HEI Cap"] for row in data],
    'HEI Intrinsic Value': [row["HEI Intrinsic Value"] for row in data],
    'Settlement Value': [row["Settlement Value"] for row in data],
}

st.line_chart(chart_data := pd.DataFrame(chart, index=years))
