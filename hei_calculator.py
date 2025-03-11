import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Page setup
st.set_page_config(page_title="HEI Calculator", layout="wide")
st.title("🏡 Home Equity Investment (HEI) Calculator")

# Sanity check
st.success("✅ The latest version of the app has been loaded.")

# Parsing functions for formatted inputs
def parse_currency(x):
    return float(x.replace('$', '').replace(',', '').strip())

def parse_percent(x):
    return float(x.replace('%', '').strip()) / 100

def parse_multiplier(x):
    return float(x.lower().replace('x', '').strip())

# Sidebar Inputs
with st.sidebar:
    st.header("📌 Input Parameters (Formatted)")

    home_value_str = st.text_input("Home Value", "$1,000,000")
    appreciation_rate_str = st.text_input("Annual Appreciation", "2.00%")
    premium_pct_str = st.text_input("Premium Percentage", "20.00%")
    hei_multiplier_str = st.text_input("HEI Multiplier", "2.0x")
    investor_cap_str = st.text_input("Investor Cap", "20.00%")

# Convert formatted inputs to numeric values
try:
    home_value = parse_currency(home_value_str)
    appreciation_rate = parse_percent(appreciation_rate_str)
    premium_percentage = parse_percent(premium_pct_str)
    hei_multiplier = parse_multiplier(hei_multiplier_str)
    investor_cap_rate = parse_percent(investor_cap_str)
except ValueError:
    st.error("⚠️ Please verify input formats.")
    st.stop()

# Calculations
premium_amount = home_value * premium_percentage
investor_percentage = premium_percentage * hei_multiplier

years = list(range(11))
home_values, hei_caps, hei_intrinsic_values, settlement_values = [], [], [], []

current_home_value = home_value
current_hei_cap = premium_amount

for year in years:
    if year > 0:
        current_home_value *= (1 + appreciation_rate)
        current_hei_cap *= (1 + investor_cap_rate)

    intrinsic_value = current_home_value * investor_percentage
    settlement_value = min(current_hei_cap, intrinsic_value)

    home_values.append(current_home_value)
    hei_caps.append(current_hei_cap)
    hei_intrinsic_values.append(intrinsic_value)
    settlement_values.append(settlement_value)

# Create DataFrame
df_results = pd.DataFrame({
    "Year": years,
    "Home Value": home_values,
    "HEI Cap": hei_caps,
    "HEI Intrinsic Value": hei_intrinsic_values,
    "Settlement Value": settlement_values
})

# Currency formatting function
def currency_fmt(x):
    return "${:,.0f}".format(x)

# Function to highlight cells
def highlight_cells(row):
    cap = row["HEI Cap"]
    intrinsic = row["HEI Intrinsic Value"]
    settlement = min(cap, intrinsic)
    return [
        '',  # Year
        '',  # Home Value
        'background-color: #90ee90' if cap == settlement else '',
        'background-color: #90ee90' if intrinsic == settlement else '',
        'background-color: #90ee90'  # Settlement always matches min(cap, intrinsic)
    ]

# Apply formatting and highlighting
styled_df = df_results.style.format({
    "Home Value": currency_fmt,
    "HEI Cap": currency_fmt,
    "HEI Intrinsic Value": currency_fmt,
    "Settlement Value": currency_fmt
}).apply(highlight_cells, axis=1)

# Display Metrics
col1, col2 = st.columns(2)
col1.metric("🏷️ Premium Amount", currency_fmt(premium_amount))
col2.metric("📈 Investor Percentage", f"{investor_percentage:.0%}")

# Plotly interactive chart
fig = go.Figure()
fig.add_trace(go.Scatter(x=years, y=home_values, name="Home Value"))
fig.add_trace(go.Scatter(x=years, y=hei_caps, name="HEI Cap"))
fig.add_trace(go.Scatter(x=years, y=hei_intrinsic_values, name="HEI Intrinsic Value"))
fig.add_trace(go.Scatter(x=years, y=settlement_values, name="Settlement Value", fill='tozeroy'))

fig.update_layout(
    title="HEI Investment Values Over 10 Years",
    xaxis_title="Year",
    yaxis_title="Value ($)",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

# Display results table with conditional highlighting
st.subheader("📊 Annual HEI Breakdown (Highlighted)")
st.dataframe(styled_df, use_container_width=True)
