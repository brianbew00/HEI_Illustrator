import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Page configuration
st.set_page_config(page_title="HEI Calculator", layout="wide")
st.title("🏡 Home Equity Investment (HEI) Calculator")

# Sanity Check
st.success("✅ The latest version of the app has been loaded.")

# Parsing helper functions
def parse_currency(x):
    return float(x.replace('$', '').replace(',', '').strip())

def parse_percent(x):
    return float(x.replace('%', '').strip()) / 100

def parse_multiplier(x):
    return float(x.lower().replace('x', '').strip())

# Sidebar Inputs
with st.sidebar:
    st.header("📌 Input Parameters")
    home_value_str = st.text_input("Home Value", "$1,000,000")
    appreciation_rate_str = st.text_input("Annual Appreciation", "2.00%")
    premium_pct_str = st.text_input("Premium Percentage", "20.00%")
    hei_multiplier_str = st.text_input("HEI Multiplier", "2.0x")
    investor_cap_str = st.text_input("Investor Cap", "20.00%")

# Parse inputs
try:
    home_value = parse_currency(home_value_str)
    appreciation_rate = parse_percent(appreciation_rate_str)
    premium_percentage = parse_percent(premium_pct_str)
    hei_multiplier = parse_multiplier(hei_multiplier_str)
    investor_cap_rate = parse_percent(investor_cap_str)
except ValueError:
    st.error("⚠️ Check your input formats.")
    st.stop()

# Calculations
premium_amount = home_value * premium_percentage
investor_percentage = premium_percentage * hei_multiplier

years = list(range(11))
home_values, hei_caps, contract_values, settlement_values = [], [], [], []

current_home_value = home_value
current_hei_cap = premium_amount

for year in years:
    if year != 0:
        current_home_value *= (1 + appreciation_rate)
        current_hei_cap *= (1 + investor_cap_rate)

    contract_value = current_home_value * investor_percentage
    settlement_value = min(current_hei_cap, contract_value)

    home_values.append(current_home_value)
    hei_caps.append(current_hei_cap)
    contract_values.append(contract_value)
    settlement_values.append(settlement_value)

# DataFrame creation
df_results = pd.DataFrame({
    "Year": years,
    "Home Value": home_values,
    "HEI Cap": hei_caps,
    "Contract Value": contract_values,
    "Settlement Value": settlement_values
}).set_index("Year")

# Conditional highlighting logic
def highlight_min(row):
    cap = row["HEI Cap"]
    contract = row["Contract Value"]
    if cap < contract:
        return ["background-color: #90ee90", "", ""]
    elif contract < cap:
        return ["", "background-color: #90ee90", ""]
    return [""] * 3

# Format DataFrame for neatness, apply minimal padding and clear width settings
formatted_df = df_results.style.format("${:,.0f}")\
    .apply(highlight_min, axis=1, subset=["HEI Cap", "Contract Value", "Settlement Value"])\
    .set_table_styles([
        {'selector': 'th, td', 'props': [('padding', '4px 8px'), ('text-align', 'center')]},
        {'selector': 'th.col_heading', 'props': [('width', '25%')]},
        {'selector': 'th.row_heading', 'props': [('width', '10%')]}
    ])

# Display metrics
col1, col2 = st.columns(2)
col1.metric("🏷️ Premium Amount", f"${premium_amount:,.0f}")
col2.metric("📈 Investor Percentage", f"{investor_percentage:.0%}")

# Plotly chart
fig = go.Figure()
fig.add_trace(go.Scatter(x=years, y=home_values, name="Home Value"))
fig.add_trace(go.Scatter(x=years, y=hei_caps, name="HEI Cap"))
fig.add_trace(go.Scatter(x=years, y=contract_values, name="Contract Value"))
fig.add_trace(go.Scatter(x=years, y=settlement_values, name="Settlement Value", fill='tozeroy'))

fig.update_layout(
    title='HEI Values Over 10 Years',
    xaxis_title='Year',
    yaxis_title='Value ($)',
    hovermode='x unified'
)

st.plotly_chart(fig, use_container_width=True)

# Display formatted DataFrame (proper width, no extra rows)
st.subheader("📊 Annual HEI Breakdown")
st.dataframe(
    formatted_df,
    use_container_width=True,
    height=(len(df_results) + 1) * 30  # Adjusted exact height for no scrolling
)
