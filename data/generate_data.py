"""
Mock Data Generation Module for UN Data Analytics Dashboard
Generates realistic sample data for all dashboard sections
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

# Countries and regions data
COUNTRIES = [
    'United States', 'China', 'India', 'Brazil', 'Russia', 'Japan', 'Germany', 
    'United Kingdom', 'France', 'Italy', 'Canada', 'South Korea', 'Australia',
    'Spain', 'Mexico', 'Indonesia', 'Netherlands', 'Saudi Arabia', 'Turkey',
    'Switzerland', 'Poland', 'Belgium', 'Sweden', 'Nigeria', 'Argentina',
    'Austria', 'Norway', 'United Arab Emirates', 'Israel', 'Egypt'
]

REGIONS = {
    'United States': 'North America', 'Canada': 'North America', 'Mexico': 'North America',
    'Brazil': 'South America', 'Argentina': 'South America',
    'United Kingdom': 'Europe', 'Germany': 'Europe', 'France': 'Europe', 'Italy': 'Europe',
    'Spain': 'Europe', 'Netherlands': 'Europe', 'Switzerland': 'Europe', 'Poland': 'Europe',
    'Belgium': 'Europe', 'Sweden': 'Europe', 'Austria': 'Europe', 'Norway': 'Europe',
    'Russia': 'Europe', 'Turkey': 'Europe',
    'China': 'Asia', 'India': 'Asia', 'Japan': 'Asia', 'South Korea': 'Asia',
    'Indonesia': 'Asia', 'Saudi Arabia': 'Asia', 'United Arab Emirates': 'Asia', 'Israel': 'Asia',
    'Australia': 'Oceania',
    'Nigeria': 'Africa', 'Egypt': 'Africa'
}

CONTINENTS = {
    'North America': ['United States', 'Canada', 'Mexico'],
    'South America': ['Brazil', 'Argentina'],
    'Europe': ['United Kingdom', 'Germany', 'France', 'Italy', 'Spain', 'Netherlands', 
               'Switzerland', 'Poland', 'Belgium', 'Sweden', 'Austria', 'Norway', 'Russia', 'Turkey'],
    'Asia': ['China', 'India', 'Japan', 'South Korea', 'Indonesia', 'Saudi Arabia', 
             'United Arab Emirates', 'Israel'],
    'Oceania': ['Australia'],
    'Africa': ['Nigeria', 'Egypt']
}


def generate_sdg_data():
    """Generate SDG progress data for all 17 goals"""
    years = list(range(2015, 2026))
    data = []
    
    sdg_goals = [
        'No Poverty', 'Zero Hunger', 'Good Health and Well-being', 'Quality Education',
        'Gender Equality', 'Clean Water and Sanitation', 'Affordable and Clean Energy',
        'Decent Work and Economic Growth', 'Industry, Innovation and Infrastructure',
        'Reduced Inequalities', 'Sustainable Cities and Communities', 
        'Responsible Consumption and Production', 'Climate Action', 'Life Below Water',
        'Life on Land', 'Peace, Justice and Strong Institutions', 'Partnerships for the Goals'
    ]
    
    for country in COUNTRIES:
        region = REGIONS[country]
        base_score = np.random.uniform(45, 85)  # Base SDG score for country
        
        for i, goal in enumerate(sdg_goals, 1):
            goal_base = base_score + np.random.uniform(-15, 15)
            
            for year in years:
                # Progressive improvement over years
                year_improvement = (year - 2015) * np.random.uniform(0.5, 2)
                score = min(100, max(0, goal_base + year_improvement + np.random.uniform(-5, 5)))
                
                data.append({
                    'Country': country,
                    'Region': region,
                    'Year': year,
                    'SDG_Number': i,
                    'SDG_Goal': goal,
                    'Score': round(score, 2)
                })
    
    return pd.DataFrame(data)


def generate_population_data():
    """Generate population data from 1960 to 2025"""
    years = list(range(1960, 2026, 5))
    data = []
    
    population_bases = {
        'China': 667000000, 'India': 450000000, 'United States': 180000000,
        'Indonesia': 88000000, 'Brazil': 72000000, 'Russia': 120000000,
        'Japan': 93000000, 'Mexico': 38000000, 'Germany': 72000000,
        'United Kingdom': 52000000, 'France': 46000000, 'Italy': 50000000,
        'South Korea': 25000000, 'Spain': 30000000, 'Poland': 30000000,
        'Canada': 18000000, 'Australia': 10000000, 'Netherlands': 11000000,
        'Saudi Arabia': 4000000, 'Turkey': 28000000, 'Argentina': 20000000,
        'Sweden': 7500000, 'Switzerland': 5300000, 'Belgium': 9100000,
        'Austria': 7000000, 'Norway': 3600000, 'United Arab Emirates': 90000,
        'Israel': 2100000, 'Nigeria': 45000000, 'Egypt': 27000000
    }
    
    growth_rates = {
        'China': 1.5, 'India': 2.0, 'United States': 1.0, 'Indonesia': 1.8,
        'Brazil': 1.8, 'Russia': 0.3, 'Japan': 0.5, 'Mexico': 1.9,
        'Germany': 0.3, 'United Kingdom': 0.5, 'France': 0.6, 'Italy': 0.3,
        'South Korea': 1.0, 'Spain': 0.7, 'Poland': 0.2, 'Canada': 1.2,
        'Australia': 1.5, 'Netherlands': 0.7, 'Saudi Arabia': 2.8,
        'Turkey': 1.8, 'Argentina': 1.3, 'Sweden': 0.5, 'Switzerland': 0.8,
        'Belgium': 0.4, 'Austria': 0.4, 'Norway': 0.7, 
        'United Arab Emirates': 5.0, 'Israel': 2.2, 'Nigeria': 2.6, 'Egypt': 2.2
    }
    
    for country in COUNTRIES:
        base_pop = population_bases[country]
        growth = growth_rates[country]
        
        for i, year in enumerate(years):
            # Calculate population with growth
            population = base_pop * ((1 + growth/100) ** (i * 5))
            
            # Add some variation
            population = population * np.random.uniform(0.95, 1.05)
            
            # Urban/Rural split (urbanization increases over time)
            urban_pct = min(95, 30 + (year - 1960) * 0.5 + np.random.uniform(-5, 5))
            
            data.append({
                'Country': country,
                'Region': REGIONS[country],
                'Year': year,
                'Population': int(population),
                'Urban_Percentage': round(urban_pct, 1),
                'Rural_Percentage': round(100 - urban_pct, 1),
                'Growth_Rate': round(growth + np.random.uniform(-0.5, 0.5), 2)
            })
    
    return pd.DataFrame(data)


def generate_climate_data():
    """Generate climate and environmental data"""
    years = list(range(1990, 2026))
    data = []
    
    co2_bases = {
        'China': 2500, 'United States': 5000, 'India': 800, 'Russia': 1500,
        'Japan': 1200, 'Germany': 950, 'South Korea': 600, 'Canada': 550,
        'United Kingdom': 600, 'Brazil': 450, 'Indonesia': 500, 'France': 380,
        'Italy': 450, 'Mexico': 450, 'Australia': 400, 'Spain': 300,
        'Poland': 350, 'Netherlands': 180, 'Saudi Arabia': 400, 'Turkey': 250,
        'Argentina': 150, 'Sweden': 60, 'Switzerland': 45, 'Belgium': 120,
        'Austria': 70, 'Norway': 50, 'United Arab Emirates': 150,
        'Israel': 70, 'Nigeria': 100, 'Egypt': 200
    }
    
    for country in COUNTRIES:
        base_co2 = co2_bases[country]
        
        for year in years:
            # Different countries have different emission trends
            if country in ['China', 'India', 'Indonesia']:
                # Growing emissions
                multiplier = 1 + (year - 1990) * 0.04
            elif country in ['United States', 'Germany', 'United Kingdom', 'France']:
                # Declining emissions
                multiplier = 1 + (year - 1990) * -0.01
            else:
                # Stable or slight growth
                multiplier = 1 + (year - 1990) * 0.01
            
            co2 = base_co2 * multiplier * np.random.uniform(0.95, 1.05)
            
            # Renewable energy adoption (increasing over time)
            renewable_pct = min(90, 5 + (year - 1990) * np.random.uniform(0.8, 1.5))
            
            data.append({
                'Country': country,
                'Region': REGIONS[country],
                'Year': year,
                'CO2_Emissions_MT': round(co2, 2),
                'Renewable_Energy_Pct': round(renewable_pct, 1),
                'Deforestation_Rate': round(np.random.uniform(-2, 5), 2)
            })
    
    # Global temperature anomaly
    temp_data = []
    for year in years:
        anomaly = 0.4 + (year - 1990) * 0.02 + np.random.uniform(-0.1, 0.1)
        temp_data.append({
            'Year': year,
            'Temperature_Anomaly_C': round(anomaly, 3)
        })
    
    return pd.DataFrame(data), pd.DataFrame(temp_data)


def generate_hdi_data():
    """Generate Human Development Index data"""
    years = list(range(1990, 2026, 5))
    data = []
    
    hdi_bases = {
        'Norway': 0.920, 'Switzerland': 0.915, 'Australia': 0.910, 'Germany': 0.905,
        'Sweden': 0.905, 'Netherlands': 0.900, 'United States': 0.895,
        'United Kingdom': 0.895, 'Japan': 0.890, 'Canada': 0.890, 'France': 0.885,
        'Austria': 0.885, 'Belgium': 0.880, 'Israel': 0.875, 'Spain': 0.870,
        'Italy': 0.865, 'South Korea': 0.860, 'United Arab Emirates': 0.840,
        'Poland': 0.820, 'Russia': 0.780, 'Turkey': 0.760, 'Saudi Arabia': 0.825,
        'Argentina': 0.800, 'China': 0.680, 'Brazil': 0.720, 'Mexico': 0.730,
        'Indonesia': 0.650, 'Egypt': 0.630, 'India': 0.540, 'Nigeria': 0.470
    }
    
    for country in COUNTRIES:
        base_hdi = hdi_bases[country]
        
        for i, year in enumerate(years):
            # Progressive improvement
            hdi = min(0.99, base_hdi + i * 0.01 + np.random.uniform(-0.02, 0.02))
            
            # Components
            life_exp = 60 + hdi * 25 + np.random.uniform(-2, 2)
            edu_years = 8 + hdi * 8 + np.random.uniform(-1, 1)
            gni_per_capita = 5000 + (hdi * 60000) + np.random.uniform(-5000, 5000)
            
            data.append({
                'Country': country,
                'Region': REGIONS[country],
                'Year': year,
                'HDI': round(hdi, 3),
                'Life_Expectancy': round(life_exp, 1),
                'Expected_Education_Years': round(edu_years, 1),
                'GNI_Per_Capita': int(gni_per_capita)
            })
    
    return pd.DataFrame(data)


def generate_peacekeeping_data():
    """Generate UN peacekeeping operations data"""
    missions = [
        {'Name': 'MINUSMA', 'Location': 'Mali', 'Region': 'Africa', 'Start': '2013-04-25', 
         'Status': 'Active', 'Troops': 13000, 'Police': 1900, 'Civilians': 1200, 'Budget_M': 1200},
        {'Name': 'MONUSCO', 'Location': 'DR Congo', 'Region': 'Africa', 'Start': '2010-07-01',
         'Status': 'Active', 'Troops': 16000, 'Police': 1400, 'Civilians': 3600, 'Budget_M': 1100},
        {'Name': 'UNMISS', 'Location': 'South Sudan', 'Region': 'Africa', 'Start': '2011-07-09',
         'Status': 'Active', 'Troops': 15000, 'Police': 2100, 'Civilians': 2400, 'Budget_M': 1100},
        {'Name': 'UNIFIL', 'Location': 'Lebanon', 'Region': 'Middle East', 'Start': '1978-03-19',
         'Status': 'Active', 'Troops': 10500, 'Police': 0, 'Civilians': 800, 'Budget_M': 500},
        {'Name': 'UNFICYP', 'Location': 'Cyprus', 'Region': 'Europe', 'Start': '1964-03-27',
         'Status': 'Active', 'Troops': 900, 'Police': 70, 'Civilians': 150, 'Budget_M': 55},
        {'Name': 'UNDOF', 'Location': 'Golan Heights', 'Region': 'Middle East', 'Start': '1974-06-03',
         'Status': 'Active', 'Troops': 1100, 'Police': 0, 'Civilians': 150, 'Budget_M': 62},
        {'Name': 'MINURSO', 'Location': 'Western Sahara', 'Region': 'Africa', 'Start': '1991-04-29',
         'Status': 'Active', 'Troops': 230, 'Police': 0, 'Civilians': 240, 'Budget_M': 60},
        {'Name': 'UNMIK', 'Location': 'Kosovo', 'Region': 'Europe', 'Start': '1999-06-10',
         'Status': 'Active', 'Troops': 0, 'Police': 8, 'Civilians': 380, 'Budget_M': 41},
        {'Name': 'UNISFA', 'Location': 'Abyei', 'Region': 'Africa', 'Start': '2011-06-27',
         'Status': 'Active', 'Troops': 3800, 'Police': 50, 'Civilians': 300, 'Budget_M': 285},
        {'Name': 'MINUSCA', 'Location': 'Central African Republic', 'Region': 'Africa', 'Start': '2014-04-10',
         'Status': 'Active', 'Troops': 11500, 'Police': 2000, 'Civilians': 1500, 'Budget_M': 950}
    ]
    
    return pd.DataFrame(missions)


def generate_health_data():
    """Generate global health statistics"""
    years = list(range(2000, 2026, 5))
    data = []
    
    life_exp_bases = {
        'Japan': 82, 'Switzerland': 82, 'Australia': 81, 'Spain': 81, 'Italy': 81,
        'Sweden': 81, 'France': 80, 'Canada': 80, 'Norway': 80, 'Israel': 81,
        'South Korea': 80, 'Germany': 79, 'United Kingdom': 79, 'Austria': 79,
        'Netherlands': 80, 'Belgium': 79, 'United States': 77, 'Poland': 75,
        'United Arab Emirates': 76, 'Turkey': 73, 'Argentina': 75, 'Mexico': 74,
        'Brazil': 72, 'China': 74, 'Russia': 67, 'Saudi Arabia': 73,
        'Egypt': 70, 'Indonesia': 68, 'India': 67, 'Nigeria': 52
    }
    
    for country in COUNTRIES:
        base_life_exp = life_exp_bases[country]
        
        for i, year in enumerate(years):
            # Improving life expectancy
            life_exp = base_life_exp + i * 0.5 + np.random.uniform(-1, 1)
            
            # Health metrics
            physicians = np.random.uniform(1, 4.5) if country in ['Germany', 'Austria', 'Norway'] else np.random.uniform(0.5, 3)
            hospital_beds = np.random.uniform(3, 13) if country in ['Japan', 'South Korea', 'Germany'] else np.random.uniform(1, 5)
            
            # Disease rates (decreasing over time)
            hiv_rate = max(0.1, 2 - i * 0.2) * np.random.uniform(0.5, 1.5)
            
            # Maternal mortality (per 100,000 live births)
            if country in ['Norway', 'Sweden', 'Switzerland']:
                maternal_mort = np.random.uniform(3, 8)
            elif country in ['United States', 'United Kingdom']:
                maternal_mort = np.random.uniform(10, 20)
            elif country in ['China', 'Brazil']:
                maternal_mort = np.random.uniform(25, 60)
            else:
                maternal_mort = np.random.uniform(50, 300)
            
            data.append({
                'Country': country,
                'Region': REGIONS[country],
                'Year': year,
                'Life_Expectancy': round(life_exp, 1),
                'Physicians_Per_1000': round(physicians, 2),
                'Hospital_Beds_Per_1000': round(hospital_beds, 2),
                'HIV_Prevalence_Pct': round(hiv_rate, 2),
                'Maternal_Mortality_Rate': round(maternal_mort, 1),
                'Vaccination_Coverage_Pct': round(min(99, 70 + i * 3 + np.random.uniform(-5, 5)), 1)
            })
    
    return pd.DataFrame(data)


# Cache data generation
_cached_data = {}

def get_data(data_type):
    """Get cached or generate data"""
    if data_type not in _cached_data:
        if data_type == 'sdg':
            _cached_data[data_type] = generate_sdg_data()
        elif data_type == 'population':
            _cached_data[data_type] = generate_population_data()
        elif data_type == 'climate':
            climate_df, temp_df = generate_climate_data()
            _cached_data['climate'] = climate_df
            _cached_data['temperature'] = temp_df
        elif data_type == 'hdi':
            _cached_data[data_type] = generate_hdi_data()
        elif data_type == 'peacekeeping':
            _cached_data[data_type] = generate_peacekeeping_data()
        elif data_type == 'health':
            _cached_data[data_type] = generate_health_data()
    
    return _cached_data.get(data_type)
