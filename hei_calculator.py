import streamlit as st
import pandas as pd

st.title("Home Equity Investment (HEI) Calculator")

# Input Fields
home_value = st.number_input("Home Value ($)", value=1000000, step=5000)
home_price_appreciation = st.number_input("Home Price Appreciation (%)", value=2.0, step=0.1) / 100
premium_percentage = st.number_input("Premium Percentage (%)", value=20.0, step=0.1) / 100
hei_multiplier = st.number_input("HEI Multiplier", value=2.0, step=0.1)
investor_cap = st.number_input("Investor Cap (%)", value=20.0, step=0.1) / 100

# Calculations
premium_amount = home_value * premium_percentage
investor_percentage = premium_percentage * hei_multiplier

hei_cap = premium_amount
years = list(range(11))
data = []
current_home_value = home_value

for year in years:
    hei_intrinsic_value = investor_percentage * current_home_value
    settlement_value = min(hei_cap, hei_intrinsic_value)

    data.append({
        'Year': year,
        'Home Value': round(current_home_value, 2),
        'HEI Cap': round(hei_cap, 2),
        'HEI Intrinsic Value': round(hei_intrinsic_value, 2),
        'Settlement Value': round(settlement_value, 2)
    })

    hei_cap *= (1 + investor_cap)
    current_home_value *= (1 + home_price_appreciation)

# Create dataframe
df = pd.DataFrame(data)

st.subheader("Calculated Values by Year")
st.dataframe(df.style.highlight_min(axis=1, subset=['HEI Cap', 'HEI Intrinsic Value'], color='lightgreen'))

# Chart Visualization
st.subheader("Investment Growth Over Time")
chart_data = pd.DataFrame({
    'Home Value': [row['Home Value'] for row in data],
    'HEI Cap': [row['HEI Cap'] for row in data],
    'HEI Intrinsic Value': [row['HEI Intrinsic Value'] for row in data],
    'Settlement Value': [row['Settlement Value'] for row in data]
}, index=years)

st.line_chart(chart_data)
