# Wind Turbine Power Estimator
# Formula: P = 0.5 * rho * A * v^3

import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# --- US Regional Wind Data (avg wind speed in m/s) ---
REGION_WIND_DATA = {
    "northwest":     {"avg_wind_speed": 6.5, "air_density": 1.20, "states": "WA, OR, ID, MT"},
    "southwest":     {"avg_wind_speed": 6.0, "air_density": 1.18, "states": "CA, NV, AZ, NM"},
    "great plains":  {"avg_wind_speed": 9.0, "air_density": 1.22, "states": "ND, SD, NE, KS, OK, TX"},
    "midwest":       {"avg_wind_speed": 7.5, "air_density": 1.22, "states": "MN, IA, MO, WI, IL, MI"},
    "northeast":     {"avg_wind_speed": 5.5, "air_density": 1.23, "states": "NY, PA, VT, ME, MA, CT"},
    "southeast":     {"avg_wind_speed": 4.5, "air_density": 1.22, "states": "FL, GA, SC, NC, VA, AL"},
    "mountain":      {"avg_wind_speed": 7.0, "air_density": 1.10, "states": "CO, UT, WY"},
    "offshore":      {"avg_wind_speed": 10.5, "air_density": 1.23, "states": "Atlantic & Gulf Coast"},
}


def show_reference_table():
    """Displays average wind turbine specs for reference."""
    print("=" * 50)
    print("       WIND TURBINE REFERENCE SPECS")
    print("=" * 50)
    print(f"{'Turbine Type':<20} {'Rotor Radius (m)':<18} {'Typical Wind Speed (m/s)'}")
    print("-" * 50)
    print(f"{'Small (Residential)':<20} {'5 - 15':<18} {'4 - 7'}")
    print(f"{'Medium (Commercial)':<20} {'15 - 40':<18} {'6 - 9'}")
    print(f"{'Large (Utility)':<20} {'40 - 80':<18} {'8 - 12'}")
    print(f"{'Offshore':<20} {'80 - 120':<18} {'10 - 15'}")
    print("=" * 50)
    print("Default air density: 1.225 kg/m³ (sea level)")
    print("=" * 50)
    print()


def show_region_table():
    """Displays US regional wind data."""
    print("=" * 65)
    print("            US REGIONAL WIND DATA")
    print("=" * 65)
    print(f"{'Region':<15} {'Avg Wind (m/s)':<18} {'Air Density (kg/m³)':<22} {'States'}")
    print("-" * 65)
    for region, data in REGION_WIND_DATA.items():
        print(f"{region.title():<15} {data['avg_wind_speed']:<18} {data['air_density']:<22} {data['states']}")
    print("=" * 65)
    print()


def get_user_inputs():
    """Prompts user for turbine parameters."""
    print("Enter your turbine parameters (or press Enter to use defaults):\n")

    wind_speed = input("Wind speed (m/s) [default: 10]: ")
    wind_speed = float(wind_speed) if wind_speed else 10.0

    rotor_radius = input("Rotor radius (m) [default: 40]: ")
    rotor_radius = float(rotor_radius) if rotor_radius else 40.0

    air_density = input("Air density (kg/m³) [default: 1.225]: ")
    air_density = float(air_density) if air_density else 1.225

    return wind_speed, rotor_radius, air_density


def get_region_input():
    """Prompts user to select a US region."""
    print("Enter your US region to compare with regional wind data.")
    print("Options:", ", ".join([r.title() for r in REGION_WIND_DATA.keys()]))
    region = input("\nYour region [default: great plains]: ").strip().lower()
    return region if region in REGION_WIND_DATA else "great plains"


def calculate_power(wind_speed, rotor_radius, air_density=1.225):
    """
    Estimates wind turbine power output.

    Parameters:
        wind_speed (float): Wind speed in m/s
        rotor_radius (float): Rotor blade radius in meters
        air_density (float): Air density in kg/m^3 (default = 1.225 at sea level)

    Returns:
        tuple: (theoretical_power_kW, actual_power_kW)
    """
    A = math.pi * rotor_radius ** 2
    Cp = 0.4

    theoretical = 0.5 * air_density * A * wind_speed ** 3
    actual = theoretical * Cp

    return theoretical / 1000, actual / 1000


def display_results(wind_speed, rotor_radius, air_density, t_power, a_power, region):
    """Displays the power estimation results alongside regional comparison."""
    reg_data = REGION_WIND_DATA[region]
    reg_t, reg_a = calculate_power(reg_data["avg_wind_speed"], rotor_radius, reg_data["air_density"])

    print()
    print("=" * 55)
    print("               ESTIMATION RESULTS")
    print("=" * 55)
    print(f"  Wind Speed:          {wind_speed} m/s")
    print(f"  Rotor Radius:        {rotor_radius} m")
    print(f"  Air Density:         {air_density} kg/m³")
    print("-" * 55)
    print(f"  Theoretical Power:   {t_power:.2f} kW")
    print(f"  Actual Est. Power:   {a_power:.2f} kW")
    print(f"  Betz Efficiency:     40%")
    print("=" * 55)
    print(f"\n  REGIONAL COMPARISON  —  {region.title()}")
    print(f"  States:              {reg_data['states']}")
    print(f"  Avg Wind Speed:      {reg_data['avg_wind_speed']} m/s")
    print(f"  Avg Air Density:     {reg_data['air_density']} kg/m³")
    print("-" * 55)
    print(f"  Regional Theoretical:{reg_t:.2f} kW")
    print(f"  Regional Actual Est.:{reg_a:.2f} kW")
    print("=" * 55)


def plot_power_curve(wind_speed, rotor_radius, air_density, region):
    """Plots power curve + regional comparison + NREL wind map."""
    speeds = list(range(1, 26))
    theoretical_powers = []
    actual_powers = []

    for v in speeds:
        t, a = calculate_power(v, rotor_radius, air_density)
        theoretical_powers.append(t)
        actual_powers.append(a)

    reg_data = REGION_WIND_DATA[region]
    reg_speed = reg_data["avg_wind_speed"]

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle("Wind Turbine Power Estimator", fontsize=16, fontweight="bold")

    # --- Left: Power Curve ---
    axes[0].plot(speeds, theoretical_powers, label="Theoretical Power", color="blue", linewidth=2)
    axes[0].plot(speeds, actual_powers, label="Actual Estimated Power (Cp=0.4)", color="green", linewidth=2)
    axes[0].axvline(x=wind_speed, color="red", linestyle="--", label=f"Your Wind Speed: {wind_speed} m/s")
    axes[0].axvline(x=reg_speed, color="orange", linestyle="--", label=f"{region.title()} Avg: {reg_speed} m/s")
    axes[0].set_title("Power Curve")
    axes[0].set_xlabel("Wind Speed (m/s)")
    axes[0].set_ylabel("Power Output (kW)")
    axes[0].legend()
    axes[0].grid(True)

    # --- Right: NREL Wind Map ---
    try:
        img = mpimg.imread("nrel-wind-map.png")
        axes[1].imshow(img)
        axes[1].axis("off")
        axes[1].set_title("U.S. Wind Resource Map (NREL)")
    except FileNotFoundError:
        axes[1].text(0.5, 0.5, "Map image not found.\nSave nrel-wind-map.png\nin the project folder.",
                     ha="center", va="center", fontsize=12, color="red")
        axes[1].axis("off")

    plt.tight_layout()
    plt.show()


# --- Main Program ---
show_reference_table()
show_region_table()
wind_speed, rotor_radius, air_density = get_user_inputs()
region = get_region_input()
t_power, a_power = calculate_power(wind_speed, rotor_radius, air_density)
display_results(wind_speed, rotor_radius, air_density, t_power, a_power, region)
plot_power_curve(wind_speed, rotor_radius, air_density, region)