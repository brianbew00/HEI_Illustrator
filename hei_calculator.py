import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Page setup
st.set_page_config(page_title="HEI Calculator", layout="wide")
st.title("🏡 Home Equity Investment (HEI) Calculator")

# Sanity Check
st.write("✅ The latest version of the app has been loaded.")

# Sidebar Inputs
with st.sidebar:
    st.header("📌 Input Parameters")

    home_value = st.number_input("Home Value ($)", value=1_000_000, step=10_000, format="%d")
    appreciation_rate = st.number_input("Annual Appreciation Rate (%)", value=2.0, step=0.1, format="%.2f") / 100
    premium_percentage = st.number_input("Premium Percentage (%)", value=20.0, step=0.1, format="%.2f") / 100
    hei_multiplier = st.number_input("HEI Multiplier", value=2.0, step=0.1, format="%.2f")
    investor_cap_rate = st.number_input("Investor Cap (%)", value=20.0, step=0.1, format="%.2f") / 100

# Perform calculations clearly (without walrus operator)
premium_amount = home_value * premium_percentage
investor_percentage = premium_percentage * hei_multiplier

years = list(range(11))
home_values = []
hei_caps = []
hei_intrinsic_values = []
settlement_values = []

current_home_value = home_value
current_hei_cap = premium_amount

for year in years:
    if year != 0:
        current_home_value *= (1 + appreciation_rate)
        current_hei_cap *= (1 + investor_cap_rate)
    else:
        current_home_value = home_value
        current_hei_cap = premium_amount

    hei_intrinsic_value = current_home_value * investor_percentage
    settlement_value = min(current_hei_cap, hei_intrinsic_value)

    home_values.append(current_home_value)
    hei_caps.append(current_hei_cap)
    hei_intrinsic_values.append(hei_intrinsic_value)
    settlement_values.append(settlement_value)

# Build DataFrame
df_results = pd.DataFrame({
    "Year": years,
    "Home Value": home_values,
    "HEI Cap": hei_caps,
    "HEI Intrinsic Value": hei_intrinsic_values,
    "Settlement Value": settlement_values
})

# Formatting dataframe for display
def currency_format(x):
    return "${:,.0f}".format(x)

formatted_df = df_results.copy()
formatted_df["Home Value"] = formatted_df["Home Value"].apply(currency_format)
formatted_df["HEI Cap"] = formatted_df["HEI Cap"].apply(currency_format)
formatted_df["HEI Intrinsic Value"] = formatted_df["HEI Intrinsic Value"].apply(currency_format)
formatted_df["Settlement Value"] = formatted_df["Settlement Value"].apply(currency_format)

# Display Metrics
col1, col2 = st.columns(2)
with col1:
    st.metric("🏷️ Premium Amount", currency_format(premium_amount))
with col2:
    st.metric("📈 Investor Percentage", f"{investor_percentage:.0%}")

# Plotly Chart
fig = go.Figure()
fig.add_trace(go.Scatter(x=years, y=home_values, name="Home Value", line=dict(width=3)))
fig.add_trace(go.Scatter(x=years, y=hei_caps, name="HEI Cap", line=dict(width=3, dash='dash')))
fig.add_trace(go.Scatter(x=years, y=hei_intrinsic_values, name="HEI Intrinsic Value", line=dict(width=3)))
fig.add_trace(go.Scatter(x=years, y=settlement_values, name="Settlement Value", fill='tozeroy', line=dict(width=3)))

fig.update_layout(
    title='HEI Values Over Time',
    xaxis_title='Year',
    yaxis_title='Value ($)',
    hovermode='x unified'
)

st.plotly_chart(fig, use_container_width=True)

# Display formatted table
st.subheader("📊 Annual HEI Breakdown")
st.dataframe(formatted_df.set_index("Year"), use_container_width=True)
