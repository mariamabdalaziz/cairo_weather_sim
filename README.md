# Cairo Temperature Climate Simulation

**A Monte Carlo simulation analyzing the impact of climate change on Cairo's temperature patterns using 30 years of historical data.**

## Motivation

Cairo, Egypt’s capital, is home to approximately 25 million people and is one of the world’s oldest continuously inhabited cities. As a center of history, culture, and urban growth, Cairo reflects both Egypt’s heritage and the pressures of rapid urbanization. Today, the city faces increasing risks from overpopulation, pollution, and climate change.

This project applies real data science concepts to a meaningful real-world problem: understanding how climate change may affect Cairo’s future temperature patterns. Using 30 years of historical climate data, the project simulates different climate change scenarios to explore how the city’s climate could evolve in the coming decades.

## Data Source

Historical daily temperature data was retrieved from [Open-Meteo](https://open-meteo.com), a free and open-source weather API providing access to historical climate records dating back to 1940. The ERA5 reanalysis model was selected as the data source, which is the meteorological standard for long-term climate analysis ensuring consistency across decades.

Data was collected for Cairo, Egypt (latitude: 30.0527, longitude: 31.1902) covering 30 years from 1 January 1994 to 31 December 2024. The variable extracted was the daily mean temperature measured at 2 meters above ground level, yielding 11,323 daily observations.

## Methodology

A random walk is a method of simulating values where each step depends on the previous one — making it ideal for modelling temperature, since today's weather is always influenced by yesterday's. Each simulated day's temperature is calculated from the historical daily mean, a persistence factor of 0.7(meaning 70% of the previous day's deviation carries forward),  and a random step drawn from a normal distribution calibrated on 30 years of real Cairo data.

Running this simulation 1,000 times implements the Monte Carlo method, producing a range of possible outcomes rather than a single predicted value. Leap year days were excluded to ensure equal historical representation across all 365 days.

Climate change scenarios were modelled by shifting the daily mean temperature up by +1.5°C, +2.0°C, and +3.0°C respectively while increasing daily variability by 10% per degree of warming to reflect greater climate instability.

## Key Findings

Days above 40°C: How many additional days above 40°C does Cairo experience under each scenario?

    Baseline → 0 extra days (reference point)
    +1.5°C → 0.3 extra days above 40°C per year
    +2.0°C → 0.6 extra days above 40°C per year
    +3.0°C → 2.0 extra days above 40°C per year

    We notice a non-linear increase from the +2.0°C and +3.0°C.
    Climate change adds up to 2.0 extra scorching days per year at +3°C

January days above 20°C: How many days in January stay above 20°C under each scenario?

    Baseline → 0 extra days (reference point): 0.3
    +1.5°C January days above 20°C: 1.7
    +2.0°C January days above 20°C: 2.5
    +3.0°C January days above 20°C: 4.7

    Cairo goes from virtually no warm January days to 5 days at +3°C.

Extreme heat probability (45°C+): Out of 1000 simulated years, in how many did the temperature hit 45°C at least once?

    Baseline → 0 extra days (reference point): 0.0%
    +1.5°C: 0.8% — rare but now possible
    +2.0°C: 1.5% — doubles again
    +3.0°C: 6.5% — now a real meaningful risk every year

    A city that never experiences 45°C today faces a 1 in 15 chance every single year under current trajectory warming.

## How to Run

Python version: (3.14.2)

Packages: 
    pip install numpy pandas matplotlib

Data file source: Download historical daily temperature data from open-meteo.com
    - Location: Cairo, Egypt (lat: 30.0527, lon: 31.1902)
    - Date range: 1994-01-01 to 2024-12-31
    - Variable: temperature_2m_mean
    - Model: ERA5
    - Save the CSV file in the same folder as weather_sim.py

    Note: Update the filename in the pd.read_csv() line to match your downloaded CSV filename.

How to run the file: 

```
python weather_sim.py
```

## Limitations

This project is based on a statistical simulation rather than a machine learning or physical climate forecasting model, so it does not learn or represent causal relationships between variables such as temperature, humidity, and atmospheric pressure. Instead, it uses a random walk mechanism with a persistence factor of 0.7 to generate temperature patterns. While this factor reflects general weather persistence, it was not specifically calibrated using Cairo’s historical climate data. As a result, the simulation can occasionally produce unrealistic outliers, such as near-zero temperatures in Cairo, which are highly unlikely in reality.

Climate change effects are represented through simplified linear adjustments over time, whereas real climate systems involve complex non-linear interactions, feedback loops, and regional variability that are not captured here.

Despite these limitations, the simulation has credibility because it is grounded in 30 years of real ERA5 climate data and uses climatological daily means rather than broad seasonal averages. It is suitable for exploring probability ranges and general temperature trends, but not for precise forecasting, climate prediction, or policy-making. The findings should therefore be considered experimental rather than operational or decision-grade.

## Author

Name: Mariam Abd El-Aziz

    Published author, Data Scientist and MSc of Sustainable Development with concentration in green technologies. 

GitHub Profile: TBC

