import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Streamlit app setup
st.set_page_config(page_title="HEI Calculator", layout="wide")
st.title("🏠 Home Equity Investment (HEI) Calculator")

# Sanity Check
st.success("✅ The latest version of the app has been loaded.")

# User Inputs
st.sidebar.header("📌 Input Parameters")

home_value = st.sidebar.number_input("Home Value ($)", value=1_000_000, step=10_000)
appreciation_rate = st.sidebar.number_input("Appreciation Rate (%)", value=2.0, step=0.1) / 100
premium_percentage = st.sidebar.number_input("Premium Percentage (%)", value=20.0, step=0.1) / 100
hei_multiplier = st.sidebar.number_input("HEI Multiplier", value=2.0, step=0.1)
investor_cap_rate = st.sidebar.number_input("Investor Cap (%)", value=20.0, step=0.1) / 100

# Initial Calculations
premium_amount = home_value * premium_percentage
investor_percentage = premium_percentage * hei_multiplier

# Data Preparation
years = list(range(11))
home_values = []
hei_caps = []
hei_intrinsic_values = []
settlement_values = []

current_home_value = home_value
current_hei_cap = premium_amount = home_value * premium_percentage
investor_percentage = premium_percentage * hei_multiplier

for year in years:
    if year > 0:
        current_home_value *= (1 + appreciation_rate)
        current_hei_cap *= (1 + investor_cap_rate)

    hei_intrinsic_value = current_home_value * investor_percentage
    settlement_value = min(current_hei_cap, hei_intrinsic_value)

    home_values.append(current_home_value)
    hei_caps.append(current_hei_cap)
    hei_intrinsic_values.append(hei_intrinsic_value)
    settlement_values.append(settlement_value)

# Create DataFrame
df_results = pd.DataFrame({
    "Year": years,
    "Home Value": home_values,
    "HEI Cap": hei_caps,
    "HEI Intrinsic Value": hei_intrinsic_values,
    "Settlement Value": settlement_values,
})

# Formatting for Display
formatted_df = df_results.copy()
currency_format = lambda x: "${:,.0f}".format(x)
formatted_df["Home Value"] = formatted_df["Home Value"].map(currency_format)
formatted_df["HEI Cap"] = formatted_df["HEI Cap"].map(currency_format)
formatted_df["HEI Intrinsic Value"] = formatted_df["HEI Intrinsic Value"].map(currency_format)
formatted_df["Settlement Value"] = formatted_df["Settlement Value"].map(currency_format)

# Display calculated Premium Amount and Investor Percentage
col1, col2 = st.columns(2)
with col1:
    st.metric("🏷️ Premium Amount", currency_format(premium_amount))
with col2:
    st.metric("📈 Investor Percentage", f"{investor_percentage:.0%}")

# Interactive Plotly Chart
fig = go.Figure()
fig.add_trace(go.Scatter(x=years, y=home_values, name="Home Value"))
fig.add_trace(go.Scatter(x=years, y=hei_caps, name="HEI Cap"))
fig.add_trace(go.Scatter(x=years, y=hei_intrinsic_values, name="HEI Intrinsic Value"))
fig.add_trace(go.Scatter(x=years, y=settlement_values, name="Settlement Value", fill='tozeroy'))

fig.update_layout(
    title="HEI Values Over 10 Years",
    xaxis_title="Year",
    yaxis_title="Value ($)",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

# Display Results Table
st.subheader("📊 Annual HEI Breakdown")
st.dataframe(formatted_df.set_index("Year"), use_container_width=True)
