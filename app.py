# Wind Turbine Power Estimator - Streamlit App

import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import streamlit as st

# --- Regional Wind Data ---
REGION_WIND_DATA = {
    "northwest":    {"avg_wind_speed": 6.5, "air_density": 1.20, "states": "WA, OR, ID, MT"},
    "southwest":    {"avg_wind_speed": 6.0, "air_density": 1.18, "states": "CA, NV, AZ, NM"},
    "great plains": {"avg_wind_speed": 9.0, "air_density": 1.22, "states": "ND, SD, NE, KS, OK, TX"},
    "midwest":      {"avg_wind_speed": 7.5, "air_density": 1.22, "states": "MN, IA, MO, WI, IL, MI"},
    "northeast":    {"avg_wind_speed": 5.5, "air_density": 1.23, "states": "NY, PA, VT, ME, MA, CT"},
    "southeast":    {"avg_wind_speed": 4.5, "air_density": 1.22, "states": "FL, GA, SC, NC, VA, AL"},
    "mountain":     {"avg_wind_speed": 7.0, "air_density": 1.10, "states": "CO, UT, WY"},
    "offshore":     {"avg_wind_speed": 10.5, "air_density": 1.23, "states": "Atlantic & Gulf Coast"},
}

TURBINE_IMAGE_URL = "Wind_Turbine_Estimator/turbine.jpeg"

def calculate_power(wind_speed, rotor_radius, air_density):
    A = math.pi * rotor_radius ** 2
    Cp = 0.4
    theoretical = 0.5 * air_density * A * wind_speed ** 3
    actual = theoretical * Cp
    return theoretical / 1000, actual / 1000


def plot_power_curve(wind_speed, rotor_radius, air_density, region):
    speeds = [x * 0.5 for x in range(2, 41)]  # 1 to 20 m/s
    theoretical_powers = []
    actual_powers = []

    for v in speeds:
        t, a = calculate_power(v, rotor_radius, air_density)
        theoretical_powers.append(t)
        actual_powers.append(a)

    reg_data = REGION_WIND_DATA[region]
    reg_speed = reg_data["avg_wind_speed"]

    fig, ax = plt.subplots(figsize=(12, 5))
    fig.patch.set_facecolor("#0e1117")
    ax.set_facecolor("#1a1d23")

    ax.plot(speeds, theoretical_powers, label="Theoretical Power", color="#4fc3f7", linewidth=2)
    ax.plot(speeds, actual_powers, label="Actual Estimated Power (Cp=0.4)", color="#81c784", linewidth=2)
    ax.axvline(x=wind_speed, color="#ef5350", linestyle="--", label=f"Your Wind Speed: {wind_speed} m/s")
    ax.axvline(x=reg_speed, color="#ffa726", linestyle="--", label=f"{region.title()} Avg: {reg_speed} m/s")

    ax.set_title("Power Curve", color="white", fontsize=14)
    ax.set_xlabel("Wind Speed (m/s)", color="white", fontsize=12)
    ax.set_ylabel("Power Output (kW)", color="white", fontsize=12)
    ax.tick_params(colors="white")
    ax.legend(facecolor="#1a1d23", labelcolor="white", fontsize=10)
    ax.grid(True, color="#333842")
    for spine in ax.spines.values():
        spine.set_edgecolor("#333842")

    plt.tight_layout()
    return fig


# --- Page Config ---
st.set_page_config(page_title="Wind Turbine Estimator", layout="wide", page_icon="⚡")

# --- Header ---
col_title, col_img = st.columns([3, 1])
with col_title:
    st.title("🌬️ Wind Turbine Power Estimator")
    st.markdown("Estimate wind turbine power output using the formula **P = ½ρAv³** and compare against real U.S. regional wind data.")
with col_img:
    st.image(TURBINE_IMAGE_URL, caption="Wind Turbines in a Field", use_container_width=True)

st.divider()

# --- Sidebar ---
st.sidebar.header("⚙️ Turbine Parameters")
st.sidebar.markdown("Adjust the sliders to match your turbine and location.")

wind_speed_ms = st.sidebar.slider("Wind Speed (m/s)", 1.0, 20.0, st.session_state.get("wind_speed", 10.0), step=0.5)
wind_speed_mph = wind_speed_ms * 2.237
st.sidebar.caption(f"≈ {wind_speed_mph:.1f} mph")

rotor_radius = st.sidebar.slider("Rotor Radius (m)", 5.0, 120.0, st.session_state.get("rotor_radius", 40.0), step=1.0)
air_density = st.sidebar.slider("Air Density (kg/m³)", 1.05, 1.25, st.session_state.get("air_density", 1.225), step=0.005)

st.sidebar.divider()
st.sidebar.header("🗺️ US Region")
region = st.sidebar.selectbox("Select your region", list(REGION_WIND_DATA.keys()), format_func=lambda x: x.title())
reg_data = REGION_WIND_DATA[region]
st.sidebar.markdown(f"**States:** {reg_data['states']}")
st.sidebar.markdown(f"**Avg Wind Speed:** {reg_data['avg_wind_speed']} m/s")
st.sidebar.markdown(f"**Avg Air Density:** {reg_data['air_density']} kg/m³")

if st.sidebar.button("📍 Apply Regional Averages"):
    st.session_state["wind_speed"] = reg_data["avg_wind_speed"]
    st.session_state["air_density"] = reg_data["air_density"]
    st.rerun()

# --- Calculate ---
t_power, a_power = calculate_power(wind_speed_ms, rotor_radius, air_density)
reg_t, reg_a = calculate_power(reg_data["avg_wind_speed"], rotor_radius, reg_data["air_density"])

# --- Results ---
st.subheader("📊 Power Estimation Results")
col1, col2, col3, col4 = st.columns(4)
col1.metric("⚡ Your Theoretical Power", f"{t_power:.2f} kW", help="Maximum possible output based on your inputs (P = ½ρAv³)")
col2.metric("✅ Your Actual Est. Power", f"{a_power:.2f} kW", help="Realistic output applying Cp = 0.4 efficiency factor")
col3.metric(f"🌎 {region.title()} Theoretical", f"{reg_t:.2f} kW", f"{reg_t - t_power:+.2f} kW vs yours", help="What your turbine would theoretically produce using this region's avg wind speed and air density")
col4.metric(f"🌎 {region.title()} Actual Est.", f"{reg_a:.2f} kW", f"{reg_a - a_power:+.2f} kW vs yours", help="Realistic output for your turbine placed in this region")
st.divider()

# --- Reference Tables ---
col_a, col_b = st.columns(2)
with col_a:
    with st.expander("📋 Turbine Reference Specs"):
        st.markdown("""
| Turbine Type | Rotor Radius (m) | Typical Wind Speed (m/s) |
|---|---|---|
| Small (Residential) | 5 - 15 | 4 - 7 |
| Medium (Commercial) | 15 - 40 | 6 - 9 |
| Large (Utility) | 40 - 80 | 8 - 12 |
| Offshore | 80 - 120 | 10 - 15 |
""")
with col_b:
    with st.expander("🗺️ US Regional Wind Data"):
        for r, d in REGION_WIND_DATA.items():
            st.markdown(f"**{r.title()}** — {d['states']} | Avg Wind: {d['avg_wind_speed']} m/s | Air Density: {d['air_density']} kg/m³")

# --- Power Curve Chart ---
st.subheader("📈 Power Curve")
st.caption("Tip: Click the expand icon (⤢) in the top right of the chart to enlarge it.")
fig = plot_power_curve(wind_speed_ms, rotor_radius, air_density, region)
st.pyplot(fig, use_container_width=True)

# --- NREL Wind Map ---
st.subheader("🗺️ U.S. Wind Resource Map (NREL)")
st.caption("Color scale: darker blue = higher wind speeds. Best wind resources are in the Great Plains and offshore regions.")
try:
    st.image("Wind_Turbine_Estimator/us_wind_map.png", use_container_width=True)
except:
    st.error("Map image not found. Save us_wind_map.png in the project folder.")

# --- Footer ---
st.divider()
st.caption("Data sources: NREL Wind Resource Map | Air density values based on U.S. regional averages | Cp = 0.4 (typical utility-scale turbine)")