# 🌬️ Wind Turbine Power Estimator

A Python web application that estimates wind turbine power output using the physics formula **P = ½ρAv³**. Built with Streamlit and Matplotlib, the app provides an interactive interface for comparing theoretical vs. actual power output across U.S. regions using real wind resource data from NREL.

---

## 🔗 Links
- **Live Demo:** [https://wind-turbine-power-estimator-hbicd3lzy7vkazj3hnje62.streamlit.app/]
- **Walkthrough Video:** [https://youtu.be/My1pSkBgQLA?si=iftkSjnR11gIEusi]

---

## 📊 Features

- **Power Estimation** — Calculates theoretical and actual power output based on user-defined wind speed, rotor radius, and air density
- **Betz Efficiency** — Applies a realistic power coefficient (Cp = 0.4) to estimate real-world turbine output
- **Regional Comparison** — Compares your inputs against average wind speed and air density across 8 U.S. regions using NREL data
- **Interactive Power Curve** — Matplotlib chart displaying theoretical vs. actual output across wind speeds up to 20 m/s
- **NREL Wind Resource Map** — Visual reference of U.S. wind energy potential by region
- **Reference Tables** — Built-in turbine specs and regional wind data for users unfamiliar with typical values

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core logic and calculations |
| Streamlit | Web app interface |
| Matplotlib | Power curve chart |
| NREL Wind Data | U.S. regional wind resource reference |

---

## ⚙️ How to Run Locally

1. Clone the repository
```
git clone https://github.com/your-username/wind-turbine-power-estimator.git
```
2. Install dependencies
```
pip install streamlit matplotlib
```
3. Run the app
```
streamlit run app.py
```

---

## 📐 Formula

```
P = ½ × ρ × A × v³
```

| Variable | Description |
|---|---|
| P | Power output (Watts) |
| ρ | Air density (kg/m³) |
| A | Rotor swept area (m²) |
| v | Wind speed (m/s) |

---

## 📁 Project Structure

```
wind-turbine-power-estimator/
│
├── app.py               # Main Streamlit application
├── us_wind_map.png      # NREL U.S. Wind Resource Map
├── turbine.jpg          # Header image
└── README.md            # Project documentation
```

---

## 📜 Data Sources

- [NREL U.S. Wind Resource Map](https://windexchange.energy.gov/maps-data/321)
- U.S. regional air density values based on elevation and climate averages

---

*Developed by Hammad — Electrical Engineering Student | University of Houston*
