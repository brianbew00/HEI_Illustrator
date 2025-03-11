import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Page setup
st.set_page_config(page_title="HEI Calculator", layout="wide")
st.title("🏡 Home Equity Investment (HEI) Calculator")

# Sanity check (deployment verification)
st.write("✅ The latest version of the app has been loaded.")

# Sidebar Inputs
st.sidebar.header("📌 Input Parameters")

home_value = st.sidebar.number_input(
    "Home Value ($)", value=1_000_000, step=10_000, format="%d"
)

appreciation_rate = st.sidebar.number_input(
    "Annual Appreciation (%)", value=2.0, step=0.1, format="%.2f"
) / 100

premium_percentage = st.sidebar.number_input(
    "Premium Percentage (%)", value=20.0, step=0.1, format="%.2f"
) / 100

hei_multiplier = st.sidebar.number_input(
    "HEI Multiplier", value=2.0, step=0.1, format="%.2f"
)

investor_cap_rate = st.sidebar.number_input(
    "Investor Cap (%)", value=20.0, step=0.1, format="%.2f"
) / 100

# Initial Calculations
premium_amount = home_value * premium_percentage
investor_percentage = premium_percentage * hei_multiplier

# Prepare calculation data for 10 years
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

    intrinsic_value = current_home_value * investor_percentage
    settlement_value = min(current_hei_cap, intrinsic_value)

    home_values.append(current_home_value)
    hei_caps.append(current_hei_cap)
    hei_intrinsic_values.append(intrinsic_value)
    settlement_values.append(settlement_value)

# DataFrame creation (NO walrus operator!)
df_results = pd.DataFrame({
    "Year": range(11),
    "Home Value": home_values,
    "HEI Cap": hei_caps,
    "HEI Intrinsic Value": hei_intrinsic_values,
    "Settlement Value": settlement_values
})

# Display Metrics
col1, col2 = st.columns(2)

with col1:
    st.metric("🏷️ Premium Amount", f"${premium_amount:,.0f}")
with col2:
    st.metric("📈 Investor Percentage", f"{investor_percentage:.0%}")

# Interactive Plotly Chart
fig = go.Figure()
fig.add_trace(go.Scatter(x=df_results["Year"], y=df_results["Home Value"], name="Home Value"))
fig.add_trace(go.Scatter(x=df_results["Year"], y=df_results["HEI Cap"], name="HEI Cap"))
fig.add_trace(go.Scatter(x=df_results["Year"], y=df_results["HEI Intrinsic Value"], name="HEI Intrinsic Value"))
fig.add_trace(go.Scatter(x=df_results["Year"], y=df_results["Settlement Value"], name="Settlement Value", fill='tozeroy'))

fig.update_layout(
    title='HEI Investment Values Over 10 Years',
    xaxis_title='Year',
    yaxis_title='Value ($)',
    hovermode='x unified'
)

st.plotly_chart(fig, use_container_width=True)

# DataFrame Formatting (Conditional Highlighting)
def highlight_min(row):
    cap = row["HEI Cap"]
    intrinsic = row["HEI Intrinsic Value"]
    if cap < intrinsic:
        return ["", "", "background-color: #90ee90", "", ""]
    elif intrinsic < cap:
        return ["", "", "", "background-color: #90ee90", ""]
    else:
        return [""] * 5

formatted_df = df_results.style.format({
    "Home Value": "${:,.0f}",
    "HEI Cap": "${:,.0f}",
    "HEI Intrinsic Value": "${:,.0f}",
    "Settlement Value": "${:,.0f}"
}).apply(highlight_min, axis=1)

# Display formatted table
st.subheader("📊 Annual HEI Breakdown")
st.dataframe(formatted_df, use_container_width=True)
