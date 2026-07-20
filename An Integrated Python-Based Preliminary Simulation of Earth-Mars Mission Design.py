import math
import numpy as np
import matplotlib.pyplot as plt

# DATA & VARIABLES

# Variable
G0 = 9.81

# String
mission_name = "Preliminary Earth-Mars Exploration Mission"

# List
mission_phases = [
    "Low Earth Orbit Assembly",
    "Trans-Mars Injection",
    "Mars Arrival",
    "Deep Space Cruise",
    "Mars Orbit Insertion",
    "Surface Operations"
]

# Tuple
mars_transfer_dv_budget = (
    3200,   # Earth departure
    2100,   # Cruise correction
    900     # Mars Arrival
)

# Array
dv_test_values = np.array([
    4000,
    8000,
    12000,
    16000,
    24000
])

# Dictionary
engines = {
    "Methane LOX Chemical": 380,
    "Hydrogen LOX Chemical": 450,
    "Ion Thruster": 3000,
    "Nuclear Thermal Rocket": 900,
    "Hall Effect Thruster": 2000,
    "Solar Sail": 10000
}

# Planet database
planets = {

    "Earth": {
        "orbit_radius": 149.6e9,
        "gravity": 9.81
    },

    "Mars": {
        "orbit_radius": 227.9e9,
        "gravity": 3.71
    }
}

# FUNCTIONS
# Rocket Equation
def rocket_equation(dv, isp, dry_mass):
    mass_ratio = math.exp(
        dv / (isp * G0)
    )

    initial_mass = dry_mass * mass_ratio
    fuel_mass = initial_mass - dry_mass
    return initial_mass, fuel_mass

# Hohmann Transfer
def hohmann_transfer(r1, r2):
    mu_sun = 1.32712440018e20

    a_transfer = (r1 + r2) / 2

    v_initial = math.sqrt(
        mu_sun / r1
    )

    v_transfer = math.sqrt(
        mu_sun *
        ((2 / r1) - (1 / a_transfer))
    )

    delta_v = abs(
        v_transfer - v_initial
    )

    transfer_time = math.pi * math.sqrt(
        a_transfer ** 3 / mu_sun
    )

    return delta_v, transfer_time

# Simplified Lambert Transfer
def lambert_transfer(r1, r2, tof):
    mu_sun = 1.32712440018e20

    # Transfer angle
    theta = math.pi

    # Semi-major axis approximation
    a = (r1 + r2) / 2

    # Departure velocity
    v_departure = math.sqrt(
        mu_sun *
        ((2 / r1) - (1 / a))
    )

    # Arrival velocity
    v_arrival = math.sqrt(
        mu_sun *
        ((2 / r2) - (1 / a))
    )

    return (
        v_departure,
        v_arrival
    )

# OPERATORS
# MISSION RISK MODEL

def mission_risk_score(
        dv,
        fuel,
        travel_days,
        engine_type):
    risk_score = 0

    # Delta-V risk
    if dv > 10000:
        risk_score += 30

    elif dv > 6000:
        risk_score += 20

    else:
        risk_score += 10

    # Fuel risk
    if fuel > 20000:
        risk_score += 30

    elif fuel > 10000:
        risk_score += 20

    else:
        risk_score += 10

    # Mission duration risk

    if travel_days > 500:
        risk_score += 25

    elif travel_days > 250:
        risk_score += 15

    else:
        risk_score += 5

    # Technology risk

    if engine_type == "Ion Thruster":
        risk_score += 10

    elif engine_type == "Solar Sail":
        risk_score += 15

    else:
        risk_score += 5

    return risk_score

# MISSION RISK MODEL

def mission_risk_score(
        dv,
        fuel,
        travel_days,
        engine_type):
    risk_score = 0

    # Delta-v risk

    if dv > 10000:
        risk_score += 30

    elif dv > 6000:
        risk_score += 20

    else:
        risk_score += 10

    # Fuel mass risk

    if fuel > 20000:
        risk_score += 30

    elif fuel > 10000:
        risk_score += 20

    else:
        risk_score += 10

    # Mission duration risk

    if travel_days > 500:
        risk_score += 25

    elif travel_days > 250:
        risk_score += 15

    else:
        risk_score += 5

    # Technology risk

    if engine_type == "Ion Thruster":
        risk_score += 10

    elif engine_type == "Solar Sail":
        risk_score += 15

    else:
        risk_score += 5

    return risk_score

# OPERATORS

total_dv = sum(
    mars_transfer_dv_budget
)

earth_orbit = planets["Earth"]["orbit_radius"]

mars_orbit = planets["Mars"]["orbit_radius"]

# CONDITIONALS

print("\n============================")
print("MISSION ANALYSIS")
print("============================")

print(
    "Mission:",
    mission_name
)

print("\nMission phases:")

for phase in mission_phases:
    print("-", phase)

if total_dv > 5000:

    print(
        "\nMission class: Deep Space Mission"
    )

else:

    print(
        "\nMission class: Low Energy Mission"
    )

# LOOPS

dry_mass = 12000

fuel_results = {}

print("\n============================")
print("PROPULSION ANALYSIS")
print("============================")

for engine, isp in engines.items():
    initial_mass, fuel = rocket_equation(
        total_dv,
        isp,
        dry_mass
    )

    fuel_results[engine] = fuel

    print("\nEngine:", engine)

    print(
        "Specific impulse:",
        isp,
        "seconds"
    )

    print(
        "Fuel required:",
        round(fuel, 2),
        "kg"
    )

# SIMPLIFIED ASTRODYNAMICS MODEL

print("\n============================")
print("HOHMANN TRANSFER")
print("============================")

hohmann_dv, travel_time = hohmann_transfer(
    earth_orbit,
    mars_orbit
)

print(
    "Transfer Delta-V:",
    round(hohmann_dv / 1000, 2),
    "km/s"
)

print(
    "Travel time:",
    round(
        travel_time / (86400),
        1
    ),
    "days"
)

print("\n============================")
print("LAMBERT TRANSFER")
print("============================")

flight_time = 180 * 86400

departure_velocity, arrival_velocity = lambert_transfer(
    earth_orbit,
    mars_orbit,
    flight_time
)

print(
    "Departure velocity:",
    round(
        departure_velocity / 1000,
        2
    ),
    "km/s"
)

print(
    "Arrival velocity:",
    round(
        arrival_velocity / 1000,
        2
    ),
    "km/s"
)

# PLOT 1
# PROPULSION COMPARISON

plt.figure(figsize=(8, 5))

plt.bar(
    fuel_results.keys(),
    fuel_results.values()
)

plt.ylabel(
    "Fuel Mass (kg)"
)

plt.title(
    "Propellant Comparison"
)

plt.xticks(
    rotation=30
)

plt.grid()

plt.show()

# PLOT 2
# ROCKET EQUATION

fuel_curve = []

for dv in dv_test_values:
    _, fuel = rocket_equation(
        dv,
        450,
        dry_mass
    )

    fuel_curve.append(
        fuel
    )

plt.figure(figsize=(8, 5))

plt.plot(
    dv_test_values,
    fuel_curve,
    marker="o"
)

plt.xlabel(
    "Delta-V (m/s)"
)

plt.ylabel(
    "Fuel Mass (kg)"
)

plt.title(
    "Rocket Equation: Fuel vs Delta-V"
)

plt.grid()

plt.show()

# PLOT 3
# EARTH-MARS TRANSFER

theta = np.linspace(
    0,
    np.pi,
    200
)

a = (
            earth_orbit +
            mars_orbit
    ) / 2

b = math.sqrt(
    earth_orbit *
    mars_orbit
)

x = a * np.cos(theta)

y = b * np.sin(theta)

plt.figure(figsize=(8, 8))

plt.plot(
    x / 1e9,
    y / 1e9,
    label="Transfer Orbit"
)

plt.scatter(
    [earth_orbit / 1e9],
    [0],
    label="Earth"
)

plt.scatter(
    [mars_orbit / 1e9],
    [0],
    label="Mars"
)

plt.xlabel(
    "Distance (billion km)"
)

plt.ylabel(
    "Distance (billion km)"
)

plt.title(
    "Earth-Mars Hohmann/Lambert Style Transfer"
)

plt.legend()

plt.axis(
    "equal"
)

plt.grid()

plt.show()

# PLOT 4
# MASS RATIO NON-LINEARITY

mass_ratio_curve = []

for dv in dv_test_values:
    MR = math.exp(
        dv / (450 * G0)
    )

    mass_ratio_curve.append(
        MR
    )

plt.figure(figsize=(8, 5))

plt.plot(
    dv_test_values,
    mass_ratio_curve,
    marker="o"
)

plt.xlabel(
    "Delta-V (m/s)"
)

plt.ylabel(
    "Mass Ratio (Initial Mass / Final Mass)"
)

plt.title(
    "Non-Linear Rocket Equation: Mass Ratio vs Delta-V"
)

plt.grid()

plt.show()

# PLOT 5
# MISSION RISK BREAKDOWN

risk_categories = [
    "Delta-V",
    "Fuel",
    "Duration",
    "Technology"
]

risk_values = [
    20,
    20,
    15,
    5
]

plt.figure(figsize=(8, 5))

plt.bar(
    risk_categories,
    risk_values
)

plt.ylabel(
    "Risk Contribution"
)

plt.title(
    "illustrative Mission Risk Assessment"
)

plt.grid()

plt.show()