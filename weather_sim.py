"""
Cairo Temperature Statistical Simulation
=========================================
A Monte Carlo simulation that uses 30 years of historical Cairo 
temperature data to model the probability distribution of future 
temperature scenarios using a calibrated random walk.

Data Source  : Open-Meteo Archive, ERA5 Model
Time Period  : 1 Jan 1994 - 31 Dec 2024 (30 years)
Method       : Random walk calibrated on historical daily temperature patterns
Output       : Probability distribution of simulated temperature scenarios

Author       : Mariam Abd El-Aziz

"""
# --- Imports ----------------------------

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- Constants ----------------------------

DATA_SOURCE = 'Open-Meteo'
MODEL = 'ERA5'
TIMEZONE = 'GMT+3'
LATITUDE = 30.0527
LONGITUDE = 31.1902
START_DATE = '1994-01-01'
END_DATE = '2024-12-31'
SEASONS = {'Winter':[12,1,2],
           'Spring':[3, 4, 5],
           'Summer':[6, 7, 8],
           'Autumn':[9, 10, 11]}
N_SIMULATIONS = 1000
N_DAYS = 365
PERSISTENCE = 0.7

# --- Load Data ----------------------------

# Load data into pandas dataframe
data_df = pd.read_csv('raw_data_open-meteo-30.05N31.19E19m.csv', skiprows=3)

# --- Clean Data ----------------------------

# Dropping NaN columns
data_df = data_df.dropna(axis=1, how='all')

# Dropping the time from the date
data_df ['time'] = pd.to_datetime(data_df['time'])

# Renaming the temperature colum
data_df = data_df.rename(columns={'temperature_2m_mean (°C)':'temp_c'})

# --- Explore Data ----------------------------

# Adding a month column
data_df['month'] = data_df['time'].dt.month

# Statistics by season

# Dictionary for statistics for each season
season_stats = {}

# Looping of the SEASONS dictionary, categorizing data by season
# Calculating Mean and Standard Deviation for each season

season_temps = [] # for visualization

for season, months in SEASONS.items():

    season_data = data_df[data_df['month'].isin(months)]
    mean = season_data['temp_c'].mean()
    std = season_data['temp_c'].std()
    season_stats[season] = {'mean': round(float(mean), 2), 'std': round(float(std), 2)}
    season_temps.append(season_data['temp_c'].values) # for visualization

# Printing the statistics dictionary
for season, stats in season_stats.items():
    print("Seasonal Statistics in Cairo: ")
    print (season, stats)

# --- Climatological daily mean ----------------------------

# Adding a day column
data_df['day'] = data_df['time'].dt.dayofyear

# Calculating the Mean and Std for the same day across 30 years
daily_mean = data_df.groupby('day')['temp_c'].mean()
daily_std = data_df.groupby('day')['temp_c'].std()

# Removing leap years from the dataframes and converting to numpy arrays

daily_mean = daily_mean.drop(366, errors='ignore').values
daily_std = daily_std.drop(366, errors='ignore').values

print("Daily mean temperature by day: ", daily_mean)
print("Daily temperature standard deviation by day: ", daily_std)

# --- The Simulation ----------------------------

# Monte Carlo simulation of Cairo's climate real 30-year historical data

""" 
For each of the 1000 simulations, 
walk through all 365 days and calculate each day's temperature based on:

- The historical mean for that day
- A persistence effect from yesterday
- A random step
- We conduct impact analysis based on different climate scenarios

"""
# Simulation logic - by Scenario

def run_simulations(warming = 0):
    
    adjusted_mean = daily_mean + warming
    adjusted_std = daily_std * (1 + 0.10 * warming)

    sim = np.zeros((N_SIMULATIONS, N_DAYS))
    
    for i in range(N_SIMULATIONS):

        for day in range(N_DAYS):
            
            random_s = np.random.normal (0, adjusted_std[day])
            
            if day == 0:
                sim[i, day] = adjusted_mean[day] + random_s
            
            else: 
                sim[i, day] = adjusted_mean[day] + PERSISTENCE * (sim[i, day-1] - adjusted_mean[day-1]) + random_s
    
    return sim


sim_baseline = run_simulations(0)
print("Baseline simulation complete, shape:", sim_baseline.shape)

# Paris Agreement target, what world leaders are trying to limit warming to
sim_1_5 = run_simulations(1.5)
print("1.5°C warming simulation complete, shape:", sim_1_5.shape)

# The upper Paris Agreement limit
sim_2_0 = run_simulations(2.0)
print("2°C upper limit simulation complete, shape:", sim_2_0.shape)

# The current trajectory if no action is taken
sim_3_0 = run_simulations(3.0)
print("3°C current trajectory simulation complete, shape:", sim_3_0.shape)


# --- Impact Analysis  ----------------------------

# 1. How many additional days above 40°C does Cairo experience under each scenario?

# sim is the warming scenario
# sim reference is the baseline

def days_above_40 (sim, sim_ref):
    
    ref_days = (sim_ref > 40).sum(axis=1).mean()
    scenario_days = (sim > 40).sum(axis=1).mean()
    additional = scenario_days - ref_days

    return round(additional, 1)

print("+1.5°C additional days above 40°C:", days_above_40(sim_1_5, sim_baseline))
print("+2.0°C additional days above 40°C:", days_above_40(sim_2_0, sim_baseline))
print("+3.0°C additional days above 40°C:", days_above_40(sim_3_0, sim_baseline))

# 2. Does winter disappear? How many days in January stay above 20°C under each scenario?

def jan_above_20 (sim):

    jan_days = sim[:, 0:31]

    above_20 = (jan_days > 20).sum(axis=1).mean()

    return round(above_20, 1)

print("Baseline January days above 20°C:", jan_above_20(sim_baseline))
print("+1.5°C January days above 20°C:", jan_above_20(sim_1_5))
print("+2.0°C January days above 20°C:", jan_above_20(sim_2_0))
print("+3.0°C January days above 20°C:", jan_above_20(sim_3_0))

# 3.  Probability of an extreme heatwave above 45°C under +3°C warming

def heatwave_probability (sim):

    probability = (sim > 45).any(axis =1).mean()

    return round(probability * 100, 1)

print("Baseline 45°C+ probability:", heatwave_probability(sim_baseline), "%")
print("+1.5°C 45°C+ probability:", heatwave_probability(sim_1_5), "%")
print("+2.0°C 45°C+ probability:", heatwave_probability(sim_2_0), "%")
print("+3.0°C 45°C+ probability:", heatwave_probability(sim_3_0), "%")

# --- Visualizations  ----------------------------

# Figure (1) ------------

fig1, axes1 = plt.subplots(1, 2, figsize=(14, 5))
fig1.suptitle('Cairo Historical Temperature Analysis (1994-2024)')

# Chart 1: Daily average temperature curve across 30 years

axes1[0].plot(daily_mean)
axes1[0].set_title('Average Daily Temperature - 30 Year Climatology')
axes1[0].set_xlabel('Day of Year')
axes1[0].set_ylabel('Temperature (°C)')

# Chart 2: Seasonal box plots

axes1[1].boxplot(season_temps, labels=list(SEASONS.keys()))
axes1[1].set_title('Temperature Distribution by Season')
axes1[1].set_xlabel('Season')
axes1[1].set_ylabel('Temperature (°C)')

plt.tight_layout()
plt.show()

# Figure (2) ------------

fig2, axes2 = plt.subplots(1, 3, figsize=(18, 5))
fig2.suptitle('Cairo Temperature Simulation - Climate Change Scenarios')

# Chart 1: The random walk visualization

axes2[0].plot(sim_baseline[0], label='Baseline', alpha=0.8)
axes2[0].plot(sim_1_5[0], label='+1.5°C', alpha=0.8)
axes2[0].plot(sim_2_0[0], label='+2.0°C', alpha=0.8)
axes2[0].plot(sim_3_0[0], label='+3.0°C', alpha=0.8)
axes2[0].set_title('Simulated Year - All Scenarios')
axes2[0].set_xlabel('Day of Year')
axes2[0].set_ylabel('Temperature (°C)')
axes2[0].legend()

# Chart 2: Heatwaves - Days above 40°C

d40_baseline = (sim_baseline > 40).sum(axis=1).mean()
d40_1_5 = (sim_1_5 > 40).sum(axis=1).mean()
d40_2_0 = (sim_2_0 > 40).sum(axis=1).mean()
d40_3_0 = (sim_3_0 > 40).sum(axis=1).mean()

scenarios = ['Baseline', '+1.5°C', '+2.0°C', '+3.0°C']
days_40_values = [d40_baseline, d40_1_5, d40_2_0, d40_3_0]

axes2[1].bar(scenarios, days_40_values, color=['green', 'yellow', 'orange', 'red'])
axes2[1].set_title('Average Days Above 40°C Per Year')
axes2[1].set_xlabel('Scenario')
axes2[1].set_ylabel('Number of Days')

# Chart 3: Extreme heat probability (45°C+)

prob_values = [heatwave_probability(sim_baseline),heatwave_probability(sim_1_5),heatwave_probability(sim_2_0),heatwave_probability(sim_3_0)]

axes2[2].bar(scenarios, prob_values, color=['green', 'yellow', 'orange', 'red'])
axes2[2].set_title('Probability of 45°C+ Event')
axes2[2].set_xlabel('Scenario')
axes2[2].set_ylabel('Probability (%)')

plt.tight_layout()
plt.show()

# Figure (2) ------------

fig3, axes3 = plt.subplots(1, 2, figsize=(14, 5))
fig3.suptitle('Cairo Climate Change Impact Analysis')

# Chart 1: January temperature distribution across scenarios

jan_baseline = sim_baseline[:, 0:31].flatten()
jan_1_5 = sim_1_5[:, 0:31].flatten()
jan_2_0 = sim_2_0[:, 0:31].flatten()
jan_3_0 = sim_3_0[:, 0:31].flatten()

axes3[0].boxplot([jan_baseline, jan_1_5, jan_2_0, jan_3_0], 
                  labels=['Baseline', '+1.5°C', '+2.0°C', '+3.0°C'])
axes3[0].set_title('January Temperature Distribution by Scenario')
axes3[0].set_xlabel('Scenario')
axes3[0].set_ylabel('Temperature (°C)')
axes3[0].axhline(y=20, color='red', linestyle='--', label='20°C threshold')
axes3[0].legend()

# Chart 2: Full year temperature envelope

days = np.arange(1, 366)

for sim, label, color in zip(
    [sim_baseline, sim_1_5, sim_2_0, sim_3_0],
    ['Baseline', '+1.5°C', '+2.0°C', '+3.0°C'],
    ['blue', 'yellow', 'orange', 'red']
):
    lower = np.percentile(sim, 10, axis=0)
    upper = np.percentile(sim, 90, axis=0)
    median = np.percentile(sim, 50, axis=0)
    
    axes3[1].fill_between(days, lower, upper, alpha=0.3, color=color)
    axes3[1].plot(days, median, color=color, label=label, linewidth=1)

axes3[1].set_title('Full Year Temperature Envelope - All Scenarios')
axes3[1].set_xlabel('Day of Year')
axes3[1].set_ylabel('Temperature (°C)')
axes3[1].legend()

plt.tight_layout()
plt.show()

"""

End of file

"""
