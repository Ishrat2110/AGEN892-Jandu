import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from folium.features import GeoJsonTooltip
from streamlit_folium import st_folium
import requests

# === Header and Greeting ===
st.set_page_config(page_title="State Income Explorer", layout="wide")
st.title("🗺️ U.S. Income Heatmap")
st.markdown(
    '<h3 style="margin-top:0;">'
    '<a href="https://www.linkedin.com/in/ishrat-jandu-b3b478255/" target="_blank">Ishrat Jandu</a>'
    ' — Assignment 3, AGEN 892</h3><hr>',
    unsafe_allow_html=True
)

# === Load data ===
@st.cache_data
def load_data():
    income = pd.read_csv("https://raw.githubusercontent.com/pri-data/50-states/master/data/income-counties-states-national.csv", dtype={"fips": str})
    income["income-2015"] = pd.to_numeric(income["income-2015"], errors="coerce")
    if "income-1989a" in income.columns:
        income["income-1989a"] = pd.to_numeric(income["income-1989a"], errors="coerce")
    return income
income = load_data()

# === Explain Columns ===
st.markdown("### 🧾 Column Descriptions")
st.markdown("""
- **fips**: Unique code for each county (used for geographic referencing).
- **county**: Name of the county.
- **state**: Two-letter state abbreviation.
- **income-2015**: Median household income in 2015 (in actual 2015 dollars).
- **income-1989a**: Median income in 1989 **adjusted to 2015 dollars** (real income, inflation-adjusted).
- **income-1989b**: Median income in 1989 in **actual 1989 dollars** (not adjusted).
- **change**: Percent change in income between 1989 and 2015 (adjusted).
""")

# === Income sources and vibes ===
common_income_sources = {
    'AL': 'Automotive', 'AK': 'Oil & Gas', 'AZ': 'Aerospace', 'AR': 'Agriculture', 'CA': 'Technology',
    'CO': 'Tourism', 'CT': 'Insurance', 'DE': 'Chemicals', 'FL': 'Tourism', 'GA': 'Logistics',
    'HI': 'Hospitality', 'ID': 'Agriculture', 'IL': 'Manufacturing', 'IN': 'Automotive', 'IA': 'Agriculture',
    'KS': 'Aviation', 'KY': 'Bourbon & Manufacturing', 'LA': 'Petrochemicals', 'ME': 'Paper & Forestry',
    'MD': 'Defense', 'MA': 'Biotech', 'MI': 'Automotive', 'MN': 'Healthcare', 'MS': 'Agriculture',
    'MO': 'Aerospace', 'MT': 'Mining', 'NE': 'Agriculture', 'NV': 'Gaming & Tourism',
    'NH': 'Manufacturing', 'NJ': 'Pharmaceuticals', 'NM': 'Energy', 'NY': 'Finance', 'NC': 'Banking',
    'ND': 'Energy', 'OH': 'Automotive', 'OK': 'Oil & Gas', 'OR': 'Technology', 'PA': 'Healthcare',
    'RI': 'Jewelry & Design', 'SC': 'Automotive', 'SD': 'Agriculture', 'TN': 'Music & Manufacturing',
    'TX': 'Oil & Gas', 'UT': 'Tech Startups', 'VT': 'Dairy', 'VA': 'Defense', 'WA': 'Software',
    'WV': 'Coal Mining', 'WI': 'Dairy', 'WY': 'Mining'
}

vibe_quotes = {
    'Agriculture': "Grounded, steady, and feeding the nation 🌾",
    'Automotive': "Fast lanes and high torque dreams 🚗",
    'Oil & Gas': "Fueled by fire, driving the economy 🔥",
    'Technology': "Innovating the future with every click 💻",
    'Tourism': "Always open, always welcoming 🏝️",
    'Finance': "Money never sleeps 💰",
    'Aerospace': "Soaring above the rest 🚀",
    'Biotech': "Science with a heartbeat 🧬",
    'Healthcare': "Healing hands and healthy hearts ❤️",
    'Defense': "Strength in service and security 🛡️",
    'Music & Manufacturing': "Beats, bolts, and brilliance 🎶🔧",
    'Gaming & Tourism': "Play hard, relax harder 🎰",
    'Energy': "Powering everything 🌞⚡",
    'Dairy': "Cream of the crop 🐄",
    'Mining': "Digging deep for growth ⛏️",
    'Software': "Coding the new world 🌐",
    'Jewelry & Design': "Shining bright with elegance 💎",
    'Pharmaceuticals': "Health in every capsule 💊",
    'Paper & Forestry': "Rooted in nature 🌲",
    'Banking': "Where money meets trust 🏦",
    'Aviation': "Wings of opportunity ✈️",
    'Insurance': "Peace of mind, policy by policy 📄"
}

# === Dropdown to select state ===
states = sorted(income["state"].unique())
selected_state = st.selectbox("Select a state:", states)

# === Filter county data ===
state_data = income[income["state"] == selected_state]

# === Display table ===
st.subheader(f"County Incomes in {selected_state}")
st.write("Includes 1989 and 2015 values, with state medians.")

if "income-1989a" in state_data.columns:
    st.dataframe(state_data[["county", "income-1989a", "income-2015"]].sort_values("income-2015", ascending=False))
    median_1989 = state_data["income-1989a"].median()
    st.markdown(f"**Median (1989 adjusted):** ${median_1989:,.0f}", unsafe_allow_html=True)
else:
    st.dataframe(state_data[["county", "income-2015"]].sort_values("income-2015", ascending=False))
    st.markdown("_Adjusted income-1989 data not available in this dataset._")

median_2015 = state_data["income-2015"].median()
st.markdown(f"**Median (2015):** ${median_2015:,.0f}", unsafe_allow_html=True)

# === Display Income Source and Vibe ===
source = common_income_sources.get(selected_state, "Unknown")
vibe = vibe_quotes.get(source, "Driven by ambition 🌟")
st.success(f"**{selected_state} Income Source:** {source}  \n *{vibe}*")

# === Load and prepare state geometry data ===
@st.cache_data
def load_states():
    geo = requests.get("https://raw.githubusercontent.com/python-visualization/folium-example-data/main/us_states.json").json()
    gdf = gpd.GeoDataFrame.from_features(geo, crs="EPSG:4326")
    abbr = requests.get("https://gist.githubusercontent.com/tvpmb/4734703/raw/b54d03154c339ed3047c66fefcece4727dfc931a/US%2520State%2520List").json()
    abbr_df = pd.DataFrame(abbr)
    merged = gdf.merge(abbr_df, how="inner", on="name")
    state_medians = income.groupby("state").agg(medianincome=("income-2015", "median")).reset_index()
    merged = merged.merge(state_medians, left_on="alpha-2", right_on="state", how="left")
    return merged

states_gdf = load_states()

import branca.colormap as cm

# === Create a custom vibrant colormap (red → tan → green) ===
min_income = states_gdf["medianincome"].min()
max_income = states_gdf["medianincome"].max()
colormap = cm.StepColormap(
    colors=["#ff0000", "#fc8d59", "#fefa8b", "#d9ef8b", "#31ee5d", "#02ff12"],
    vmin=min_income,
    vmax=max_income,
    index=None,
    caption="2015 Median Household Income (USD)"
)

# === Create the Folium map ===
m = folium.Map(location=[37.8, -96], zoom_start=4, tiles="cartodbpositron")

# === Add colored states with tooltip ===
folium.GeoJson(
    states_gdf,
    name="US Income",
    style_function=lambda feature: {
        "fillColor": colormap(feature["properties"]["medianincome"])
        if feature["properties"]["medianincome"] is not None else "lightgray",
        "color": "black",
        "weight": 3,
        "fillOpacity": 1,
    },
    tooltip=GeoJsonTooltip(
        fields=["name", "medianincome"],
        aliases=["State:", "2015 Median Income (USD):"],
        localize=True,
        sticky=True,
        labels=True,
        style="""
            background-color: white;
            border: 1px solid black;
            border-radius: 3px;
            padding: 5px;
        """
    )
).add_to(m)

colormap.add_to(m)
st_folium(m, width=900, height=550)

# Tooltip
folium.GeoJson(
    states_gdf,
    name="hover",
    tooltip=GeoJsonTooltip(
        fields=["name", "medianincome"],
        aliases=["State", "Median Income (2015)"],
        localize=True,
        labels=True,
        sticky=True,
        style="background-color: white; color: black; font-family: Arial; font-size: 12px;"
    )
).add_to(m)
