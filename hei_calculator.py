import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Page setup
st.set_page_config(page_title="HEI Calculator", layout="wide")
st.title("🏡 Home Equity Investment (HEI) Calculator")

# Sanity Check
st.write("✅ The latest version of the app has been loaded.")

# Formatting helper functions
def currency_fmt(x):
    return "${:,.0f}".format(x)

def percent_fmt(x):
    return f"{x:.2%}"

# Sidebar input (with formatting)
with st.sidebar:
    st.header("📌 Input Parameters")

    home_value = st.number_input("Home Value", value=1_000_000, step=10_000, format="%d")
    appreciation_rate = st.number_input("Appreciation Rate (%)", value=2.0, step=0.1, format="%.2f") / 100
    premium_percentage = st.number_input("Premium Percentage (%)", value=20.0, step=0.1, format="%.2f") / 100
    hei_multiplier = st.number_input("HEI Multiplier", value=2.0, step=0.1, format="%.2f")
    investor_cap_rate = st.number_input("Investor Cap (%)", value=20.0, step=0.1, format="%.2f") / 100

# Initial Calculations
premium_amount = home_value * premium_percentage
investor_percentage = premium_percentage * hei_multiplier

# Data Preparation
years = list(range(11))
home_values, hei_caps, hei_intrinsic_values, settlement_values = [], [], [], []

current_home_value = home_value
current_hei_cap = premium_amount

for year in years:
    if year > 0:
        current_home_value *= (1 + appreciation_rate)
        current_hei_cap *= (1 + investor_cap_rate)
    else:
        current_home_value = home_value
        current_hei_cap = premium_amount

    intrinsic_value = current_home_value * investor_percentage
    settlement_value = min(current_hei_cap, intrinsic_value)

    home_values.append(current_home_value)
    hei_caps.append(current_hei_cap)
    hei_intrinsic_values.append(intrinsic_value)
    settlement_values.append(settlement_value)

# Results DataFrame
df_results = pd.DataFrame({
    "Year": range(11),
    "Home Value": home_values,
    "HEI Cap": hei_caps,
    "HEI Intrinsic Value": hei_intrinsic_values,
    "Settlement Value": settlement_values
})

# Conditional highlighting function (only HEI Cap and Intrinsic Value)
def highlight_min(row):
    cap = row["HEI Cap"]
    intrinsic = row["HEI Intrinsic Value"]
    styles = [''] * len(row)
    if cap <= intrinsic:
        styles = ['', '', 'background-color: #90EE90', '', '']
    else:
        styles = ['', '', '', 'background-color: #90EE90', '']
    return styles

# Apply currency formatting
formatted_df = df_results.style.format({
    "Home Value": "${:,.0f}",
    "HEI Cap": "${:,.0f}",
    "HEI Intrinsic Value": "${:,.0f}",
    "Settlement Value": "${:,.0f}"
}).apply(highlight_min, axis=1, subset=["HEI Cap", "HEI Intrinsic Value"])

# Display Metrics
col1, col2 = st.columns(2)
with col1:
    st.metric("🏷️ Premium Amount", currency_format(premium_amount))
with col2:
    st.metric("📈 Investor Percentage", f"{investor_percentage:.0%}")

# Plotly Interactive Chart
fig = go.Figure()
fig.add_trace(go.Scatter(x=years, y=home_values, name="Home Value"))
fig.add_trace(go.Scatter(x=years, y=hei_caps, name="HEI Cap"))
fig.add_trace(go.Scatter(x=years, y=hei_intrinsic_values, name="HEI Intrinsic Value"))
fig.add_trace(go.Scatter(x=years, y=settlement_values, name="Settlement Value", fill='tozeroy'))

fig.update_layout(
    title='HEI Investment Values Over Time',
    xaxis_title='Year',
    yaxis_title='Value ($)',
    hovermode='x unified'
)

st.plotly_chart(fig, use_container_width=True)

# Display results with conditional highlighting clearly defined
st.subheader("📊 Annual HEI Breakdown")
st.dataframe(formatted_df.set_index("Year"), use_container_width=True)
