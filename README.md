# 🌍 UN Data Analytics Dashboard

A comprehensive, interactive data analytics platform for exploring United Nations data across six major domains: Sustainable Development Goals, Population Demographics, Climate & Environment, Human Development Index, Peacekeeping Operations, and Global Health Statistics.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Dashboard Sections](#dashboard-sections)
- [Project Structure](#project-structure)
- [Data](#data)
- [Screenshots](#screenshots)
- [Contributing](#contributing)

## ✨ Features

### 🎯 SDG Progress Tracking
- Track progress across all 17 Sustainable Development Goals
- Interactive filters by year, region, and specific SDG goals
- Radar charts, heatmaps, and trend analysis
- Country rankings and regional comparisons
- Progress tracking from 2015-2025

### 👥 Population & Demographics
- Global population trends from 1960-2025
- Population distribution by continent and region
- Urban vs rural population analysis
- Population age pyramids
- Growth rate comparisons
- Interactive visualizations with pie charts, line graphs, and bar charts

### 🌡️ Climate & Environment Metrics
- CO2 emissions tracking by country and region
- Global temperature anomaly trends
- Renewable energy adoption rates
- Deforestation monitoring
- Interactive world maps (choropleth)
- Country-by-country climate comparisons

### 📊 Human Development Index (HDI)
- HDI rankings with search and filter capabilities
- HDI trends over time (1990-2025)
- Component breakdown (life expectancy, education, GNI)
- Country comparison tool
- Interactive choropleth world maps
- Regional analysis

### 🕊️ UN Peacekeeping Operations
- Overview of active peacekeeping missions
- Interactive mission location maps
- Personnel deployment statistics (troops, police, civilians)
- Budget allocation analysis
- Mission timeline and duration tracking
- Regional breakdowns

### 🏥 Global Health Statistics
- Life expectancy trends by country and region
- Disease prevalence tracking (HIV, etc.)
- Healthcare infrastructure metrics (physicians, hospital beds)
- Vaccination coverage rates
- Maternal and infant mortality statistics
- Comprehensive health indicator correlations

## 🛠️ Tech Stack

- **Python 3.9+** - Core programming language
- **Streamlit 1.31.0** - Web application framework
- **Pandas 2.1.4** - Data manipulation and analysis
- **Plotly 5.18.0** - Interactive visualizations and charts
- **NumPy 1.26.3** - Numerical computing

## 📦 Installation

### Prerequisites

- Python 3.9 or higher
- pip package manager

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/rithvikpathi/model-united-nations-dashboard.git
   cd model-united-nations-dashboard
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

1. **Run the dashboard**
   ```bash
   streamlit run app.py
   ```

2. **Access the dashboard**
   - Open your web browser
   - Navigate to `http://localhost:8501`

3. **Navigate through sections**
   - Use the sidebar to switch between different dashboard pages
   - Apply filters to customize data views
   - Interact with charts and visualizations
   - Explore detailed metrics and insights

## 📊 Dashboard Sections

### Main Landing Page
- Global overview with key metrics
- Summary visualizations from all domains
- Quick access to all dashboard sections
- High-level KPIs and trends

### Section Pages
Each section is accessible via the sidebar navigation:

1. **🎯 SDG Tracking** - `/pages/1_🎯_SDG_Tracking.py`
2. **👥 Population** - `/pages/2_👥_Population.py`
3. **🌡️ Climate** - `/pages/3_🌡️_Climate.py`
4. **📊 HDI** - `/pages/4_📊_HDI.py`
5. **🕊️ Peacekeeping** - `/pages/5_🕊️_Peacekeeping.py`
6. **🏥 Health** - `/pages/6_🏥_Health.py`

## 📁 Project Structure

```
model-united-nations-dashboard/
├── app.py                          # Main Streamlit entry point
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
│
├── pages/                          # Multi-page dashboard sections
│   ├── 1_🎯_SDG_Tracking.py       # SDG progress tracking
│   ├── 2_👥_Population.py         # Population & demographics
│   ├── 3_🌡️_Climate.py            # Climate & environment
│   ├── 4_📊_HDI.py                # Human Development Index
│   ├── 5_🕊️_Peacekeeping.py      # Peacekeeping operations
│   └── 6_🏥_Health.py             # Global health statistics
│
├── data/                           # Data generation module
│   └── generate_data.py            # Mock data generation functions
│
├── utils/                          # Utility modules
│   ├── charts.py                   # Reusable chart functions
│   └── helpers.py                  # Helper functions
│
└── .streamlit/                     # Streamlit configuration
    └── config.toml                 # Theme and settings
```

## 📊 Data

The dashboard uses **generated sample/mock data** for demonstration purposes. All data is created programmatically to represent realistic trends and values across:

- **30 countries** spanning all continents
- **Multiple time periods** (1960-2025 depending on domain)
- **Realistic data ranges** based on actual UN data patterns

### Data Generation

Data is generated using the `data/generate_data.py` module with functions for each domain:
- `generate_sdg_data()` - SDG scores from 2015-2025
- `generate_population_data()` - Population data from 1960-2025
- `generate_climate_data()` - Climate metrics from 1990-2025
- `generate_hdi_data()` - HDI values from 1990-2025
- `generate_peacekeeping_data()` - Active UN missions
- `generate_health_data()` - Health statistics from 2000-2025

Data is cached for performance using Streamlit's `@st.cache_data` decorator.

## 🎨 Design & Theme

The dashboard features a **UN-themed design** with:
- Primary color: UN Blue (#009EDB)
- Clean, professional layout
- Responsive design using Streamlit columns
- Interactive filters and controls
- Consistent color schemes across visualizations
- Professional metric cards and KPI displays

## 🖼️ Screenshots

The dashboard includes:
- Interactive world maps with choropleth visualizations
- Multi-metric comparison charts
- Time series trend analysis
- Regional and country-level breakdowns
- Population pyramids and demographic distributions
- Radar charts for SDG tracking
- Mission location maps for peacekeeping operations

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- United Nations for inspiration and data domains
- Streamlit for the amazing dashboard framework
- Plotly for interactive visualizations
- The open-source community

## 📧 Contact

Project Link: [https://github.com/rithvikpathi/model-united-nations-dashboard](https://github.com/rithvikpathi/model-united-nations-dashboard)

---

**Note:** All data in this dashboard is generated for demonstration purposes and does not represent actual UN data. For official UN statistics, please visit official UN data portals.
