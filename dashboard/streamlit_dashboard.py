import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh
import pydeck as pdk
from datetime import datetime

# ---------------------------------
# AUTO REFRESH EVERY 5 SECONDS
# ---------------------------------

st_autorefresh(interval=5000, key="refresh")

# ---------------------------------
# PAGE CONFIG
# ---------------------------------

st.set_page_config(
    page_title="Smart City Waste Command Center",
    page_icon="🗑️",
    layout="wide"
)

# ---------------------------------
# CUSTOM CSS
# ---------------------------------

st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

.metric-card{
    padding:15px;
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------
# LOAD DATA
# ---------------------------------

CSV_FILE = "data/bin_telemetry_log.csv"

try:
    df = pd.read_csv(CSV_FILE)
except:
    st.error("Telemetry file not found")
    st.stop()

if len(df) == 0:
    st.warning("No records available")
    st.stop()

latest = df.iloc[-1]

# ---------------------------------
# SIDEBAR
# ---------------------------------

st.sidebar.title("🏙 Smart Waste Command Center")

st.sidebar.success("System Online")

st.sidebar.metric(
    "Total Records",
    len(df)
)

st.sidebar.metric(
    "Current Fill %",
    latest["FillPercent"]
)

st.sidebar.metric(
    "Status",
    latest["Status"]
)

# ---------------------------------
# TITLE
# ---------------------------------

st.title("🏙 Smart City Waste Monitoring Dashboard")

st.caption(
    "IoT-Based Smart Waste Management Platform"
)

# ---------------------------------
# ALERT SYSTEM
# ---------------------------------

if latest["FillPercent"] >= 80:

    st.error(
        "🚨 BIN FULL - COLLECTION REQUIRED"
    )

elif latest["FillPercent"] >= 50:

    st.warning(
        "⚠ BIN REACHING CAPACITY"
    )

else:

    st.success(
        "✅ BIN OPERATING NORMALLY"
    )

# ---------------------------------
# KPI CARDS
# ---------------------------------

col1,col2,col3,col4 = st.columns(4)

with col1:
    st.metric(
        "📏 Distance",
        f"{latest['Distance']} cm"
    )

with col2:
    st.metric(
        "🗑 Fill %",
        f"{latest['FillPercent']} %"
    )

with col3:
    st.metric(
        "📢 Alert",
        latest["Alert"]
    )

with col4:
    st.metric(
        "📦 Status",
        latest["Status"]
    )

# ---------------------------------
# GAUGE CHART
# ---------------------------------

gauge = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=latest["FillPercent"],
        title={"text":"Bin Fill Level"},
        gauge={
            "axis":{"range":[0,100]},
            "steps":[
                {"range":[0,50],"color":"green"},
                {"range":[50,80],"color":"yellow"},
                {"range":[80,100],"color":"red"}
            ]
        }
    )
)

# ---------------------------------
# TREND CHART
# ---------------------------------

line_chart = px.line(
    df,
    y="FillPercent",
    title="Fill Percentage Trend"
)

left,right = st.columns(2)

with left:
    st.plotly_chart(
        gauge,
        use_container_width=True
    )

with right:
    st.plotly_chart(
        line_chart,
        use_container_width=True
    )

# ---------------------------------
# PIE CHART
# ---------------------------------

status_count = (
    df["Status"]
    .value_counts()
    .reset_index()
)

status_count.columns = [
    "Status",
    "Count"
]

pie_chart = px.pie(
    status_count,
    names="Status",
    values="Count",
    title="Waste Status Distribution"
)

# ---------------------------------
# BAR CHART
# ---------------------------------

alert_count = (
    df["Alert"]
    .value_counts()
    .reset_index()
)

alert_count.columns = [
    "Alert",
    "Count"
]

bar_chart = px.bar(
    alert_count,
    x="Alert",
    y="Count",
    title="Alert Frequency"
)

left,right = st.columns(2)

with left:
    st.plotly_chart(
        pie_chart,
        use_container_width=True
    )

with right:
    st.plotly_chart(
        bar_chart,
        use_container_width=True
    )

# ---------------------------------
# ANALYTICS
# ---------------------------------

st.markdown("## 📊 Smart Analytics")

a,b,c,d = st.columns(4)

a.metric(
    "Average Fill %",
    round(
        df["FillPercent"].mean(),
        2
    )
)

b.metric(
    "Maximum Fill %",
    round(
        df["FillPercent"].max(),
        2
    )
)

c.metric(
    "Full Bin Events",
    len(
        df[df["Status"]=="FULL"]
    )
)

d.metric(
    "Alerts Generated",
    len(
        df[df["Alert"]=="YES"]
    )
)

# ---------------------------------
# PREDICTION ENGINE
# ---------------------------------

avg_fill = df["FillPercent"].mean()

remaining = 100 - latest["FillPercent"]

forecast_hours = round(
    remaining / max(avg_fill,1),
    2
)

st.info(
    f"🤖 Prediction: Bin may reach full capacity in approximately {forecast_hours} hours."
)

# ---------------------------------
# SMART RECOMMENDATION
# ---------------------------------

st.markdown("## 🤖 AI Recommendation")

if latest["FillPercent"] >= 80:

    st.error(
        "Dispatch collection vehicle immediately."
    )

elif latest["FillPercent"] >= 50:

    st.warning(
        "Schedule collection in next cycle."
    )

else:

    st.success(
        "No collection required."
    )

# ---------------------------------
# MULTI BIN VIEW
# ---------------------------------

st.markdown("## 🗑 Smart City Bin Network")

multi_bin = pd.DataFrame({

    "Bin":[
        "Airport",
        "Mall",
        "University",
        "Railway",
        "Hospital"
    ],

    "Fill":[
        35,
        82,
        61,
        92,
        40
    ]
})

st.dataframe(
    multi_bin,
    use_container_width=True
)

# ---------------------------------
# SMART CITY MAP
# ---------------------------------

st.markdown("## 🗺 Smart City Bin Locations")

map_data = pd.DataFrame({

    "lat":[
        30.9010,
        30.9020,
        30.9030,
        30.9040,
        30.9050
    ],

    "lon":[
        75.8573,
        75.8580,
        75.8590,
        75.8600,
        75.8610
    ]
})

st.pydeck_chart(

    pdk.Deck(

        map_style="mapbox://styles/mapbox/dark-v10",

        initial_view_state=pdk.ViewState(

            latitude=30.9030,
            longitude=75.8590,
            zoom=13
        ),

        layers=[

            pdk.Layer(

                "ScatterplotLayer",

                data=map_data,

                get_position='[lon, lat]',

                get_radius=150,

                pickable=True
            )
        ]
    )
)

# ---------------------------------
# TELEMETRY TABLE
# ---------------------------------

st.markdown("## 📋 Telemetry Data")

st.dataframe(
    df.tail(50),
    use_container_width=True
)

# ---------------------------------
# DOWNLOAD BUTTON
# ---------------------------------

with open(CSV_FILE,"rb") as file:

    st.download_button(

        label="⬇ Download CSV",

        data=file,

        file_name="bin_telemetry_log.csv",

        mime="text/csv"
    )

# ---------------------------------
# FOOTER
# ---------------------------------

st.markdown("---")

st.caption(
    f"Last Updated : {datetime.now()}"
)