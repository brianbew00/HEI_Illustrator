import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Page Setup
st.set_page_config(page_title="HEI Calculator", layout="wide")
st.title("🏡 Home Equity Investment (HEI) Calculator")

# Sanity Check
st.success("✅ The latest version of the app has been loaded.")

# --- Input Parsing Functions ---
def parse_currency(x):
    return float(x.replace('$', '').replace(',', '').strip())

def parse_percent(x):
    return float(x.replace('%', '').strip()) / 100

def parse_multiplier(x):
    return float(x.lower().replace('x', '').strip())

# Sidebar Inputs (Clearly formatted)
with st.sidebar:
    st.header("📌 Input Parameters")

    home_value_str = st.text_input("Home Value", "$1,000,000")
    appreciation_rate_str = st.text_input("Annual Appreciation", "2.00%")
    premium_pct_str = st.text_input("Premium Percentage", "20.00%")
    hei_multiplier_str = st.text_input("HEI Multiplier", "2.0x")
    investor_cap_str = st.text_input("Investor Cap", "20.00%")

# Parsing inputs (corrected variables)
try:
    home_value = parse_currency(home_value_str)
    appreciation_rate = parse_percent(appreciation_rate_str)
    premium_percentage = parse_percent(premium_pct_str)
    hei_multiplier = parse_multiplier(hei_multiplier_str)
    investor_cap_rate = parse_percent(investor_cap_str)
except ValueError:
    st.error("⚠️ Please verify your input formats.")
    st.stop()

# Calculations (clearly structured, error-free)
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

    intrinsic_value = current_home_value * investor_percentage
    settlement_value = min(current_hei_cap, intrinsic_value)

    home_values.append(current_home_value)
    hei_caps.append(current_hei_cap)
    hei_intrinsic_values.append(intrinsic_value)
    settlement_values.append(settlement_value)

# DataFrame creation
df_results = pd.DataFrame({
    "Year": years,
    "Home Value": home_values,
    "HEI Cap": hei_caps,
    "HEI Intrinsic Value": hei_intrinsic_values,
    "Settlement Value": settlement_values,
})

# Conditional highlighting function (Corrected clearly)
def highlight_min(row):
    cap = row["HEI Cap"]
    intrinsic = row["HEI Intrinsic Value"]
    if cap < intrinsic:
        return ['', '', 'background-color: #90ee90', '', '']
    elif intrinsic < cap:
        return ['', '', '', 'background-color: #90ee90', '']
    else:
        return ['', '', '', '', '']

# Apply formatting to DataFrame
formatted_df = df_results.style.format({
    "Home Value": "${:,.0f}",
    "HEI Cap": "${:,.0f}",
    "HEI Intrinsic Value": "${:,.0f}",
    "Settlement Value": "${:,.0f}"
}).apply(highlight_min, axis=1)

# Display Metrics clearly
col1, col2 = st.columns(2)
with col1:
    st.metric("🏷️ Premium Amount", f"${premium_amount:,.0f}")
with col2:
    st.metric("📈 Investor Percentage", f"{investor_percentage:.0%}")

# Plotly Interactive Chart
fig = go.Figure()
fig.add_trace(go.Scatter(x=years, y=home_values, name="Home Value"))
fig.add_trace(go.Scatter(x=years, y=hei_caps, name="HEI Cap"))
fig.add_trace(go.Scatter(x=years, y=hei_intrinsic_values, name="HEI Intrinsic Value"))
fig.add_trace(go.Scatter(x=years, y=settlement_values, name="Settlement Value", fill='tozeroy'))

fig.update_layout(
    title='HEI Investment Values Over 10 Years',
    xaxis_title='Year',
    yaxis_title='Value ($)',
    hovermode='x unified'
)

st.plotly_chart(fig, use_container_width=True)

# Display formatted table
st.subheader("📊 Annual HEI Breakdown")
st.dataframe(formatted_df.set_index("Year"), use_container_width=True)
