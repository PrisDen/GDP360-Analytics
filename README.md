# GDP360 Analytics - Global Economic Data Analysis Platform

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Complete-brightgreen.svg)]()

## 📊 Project Overview

GDP360 Analytics is a comprehensive data analysis platform that processes and analyzes global economic data from 1975 to 2024. The project provides insights into GDP trends, regional economic patterns, sectoral analysis, and anomaly detection across 196 countries.

### 🌟 Key Features

- **Comprehensive Data Coverage**: 50 years of economic data (1975-2024)
- **Global Scope**: 196 countries across 7 regions
- **Multi-dimensional Analysis**: GDP, population, sectoral data, inflation, unemployment
- **Anomaly Detection**: Statistical outlier identification
- **Interactive Visualizations**: Tableau dashboards and Python-based analytics
- **ETL Pipeline**: Automated data processing and cleaning
- **SQL Analytics**: Advanced database queries and views

## 📈 Dataset Statistics

- **Total Records**: 9,632 rows × 13 columns
- **Countries**: 196 countries with economic data
- **Time Span**: 1975-2024 (50 years)
- **GDP Coverage**: 91.1% of records
- **Regional Coverage**: 92.2% with region assignments
- **Anomalies Detected**: 8 statistical outliers

### Regional Distribution
- **Sub-Saharan Africa**: 24.4% (2,350 records)
- **Europe & Central Asia**: 24.1% (2,323 records)
- **Latin America & Caribbean**: 17.1% (1,650 records)
- **East Asia & Pacific**: 12.1% (1,162 records)
- **Middle East & North Africa**: 9.3% (900 records)
- **South Asia**: 4.2% (400 records)
- **North America**: 1.0% (100 records)

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/PrisDen/GDP360-Analytics.git
   cd GDP360-Analytics
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the ETL pipeline**
   ```bash
   python etl_pipeline.py
   ```

4. **Execute data analysis**
   ```bash
   python data_analysis.py
   ```

## 📁 Project Structure

```
GDP360-Analytics/
├── 📊 raw data/                    # Source CSV files
│   ├── gdp.csv                     # GDP data
│   ├── gdp_per_capita.csv          # GDP per capita data
│   ├── population.csv              # Population data
│   ├── sector_agriculture.csv      # Agricultural sector data
│   ├── sector_industry.csv         # Industrial sector data
│   ├── sector_service.csv          # Service sector data
│   ├── inflation.csv               # Inflation data
│   └── unemployment.csv            # Unemployment data
├── 🐍 Python Scripts/
│   ├── etl_pipeline.py             # Main ETL processing pipeline
│   ├── data_analysis.py            # Data analysis and insights
│   └── csv_2_sql.py                # CSV to SQLite conversion
├── 🗄️ Database/
│   ├── master_gdp.db               # SQLite database
│   └── sql_analytics.sql           # SQL views and queries
├── 📊 Visualizations/
│   ├── tableau/                    # Tableau dashboards
│   ├── anomalies.png               # Anomaly detection visualization
│   └── db.png                      # Database schema visualization
├── 📄 Documentation/
│   ├── master_data.csv             # Processed master dataset
│   └── country_region_mapping.csv  # Country-region mappings
└── 📋 Analysis Results/
    └── try                         # Comprehensive data analysis output
```

## 🔧 Core Components

### 1. ETL Pipeline (`etl_pipeline.py`)
- **Data Extraction**: Loads raw CSV files from multiple sources
- **Data Transformation**: Cleans, standardizes, and enriches data
- **Data Loading**: Creates master dataset and SQLite database
- **Anomaly Detection**: Identifies statistical outliers in GDP data
- **Regional Mapping**: Assigns countries to 7 global regions

### 2. Data Analysis (`data_analysis.py`)
- **Top Economies Analysis**: Ranks countries by GDP
- **Regional Analysis**: Economic patterns by geographic regions
- **Growth Analysis**: Year-over-year GDP growth trends
- **Anomaly Reporting**: Statistical outlier identification
- **Summary Statistics**: Comprehensive dataset overview

### 3. SQL Analytics (`sql_analytics.sql`)
- **YoY Growth Views**: Year-over-year GDP growth calculations
- **Top Economies Views**: Latest economic rankings
- **Sectoral Analysis**: Economic sector breakdowns
- **Anomaly Views**: Flagged outlier data
- **Regional Summaries**: Geographic economic patterns

## 📊 Key Insights

### Top 10 Economies (2024)
1. **United States**: $29.2T (North America)
2. **China**: $18.7T (East Asia & Pacific)
3. **Germany**: $4.7T (Europe & Central Asia)
4. **Japan**: $4.0T (East Asia & Pacific)
5. **India**: $3.9T (South Asia)
6. **United Kingdom**: $3.6T (Europe & Central Asia)
7. **France**: $3.2T (Europe & Central Asia)
8. **Italy**: $2.4T (Europe & Central Asia)
9. **Canada**: $2.2T (North America)
10. **Brazil**: $2.2T (Latin America & Caribbean)

### Detected Anomalies
- Ethiopia (2022): $126.8B
- Guinea (2024): $25.3B
- Guyana (2023): $16.9B
- Guyana (2024): $24.8B
- Kyrgyz Republic (2024): $17.5B
- Sao Tome and Principe (2024): $764M
- Syrian Arab Republic (2011): $67.5B
- Zimbabwe (2017): $51.1B

## 🛠️ Technical Details

### Data Quality Metrics
- ✅ **Complete Year Range**: 1975-2024 (50 years)
- ✅ **Clean Country Data**: 196 actual countries
- ✅ **High GDP Coverage**: 91.1%
- ✅ **Good Region Coverage**: 92.2%
- ✅ **Anomalies Detected**: 8 statistical outliers
- ✅ **No Negative GDP Values**: 0
- ✅ **No Extremely High Values**: 0

### Database Schema
The SQLite database contains a single table `gdp_data` with the following columns:
- `Country`: Country name
- `Year`: Year of data (1975-2024)
- `GDP`: Gross Domestic Product (USD)
- `GDP_per_capita`: GDP per capita (USD)
- `Population`: Total population
- `Agri_%`: Agricultural sector percentage
- `Indus_%`: Industrial sector percentage
- `Serv_%`: Service sector percentage
- `Inflation_%`: Inflation rate percentage
- `Unemployment_%`: Unemployment rate percentage
- `Country_Code`: ISO country code
- `Region`: Geographic region assignment
- `GDP_Anomaly_Flag`: Anomaly detection flag (0/1)

## 📈 Usage Examples

### Basic Data Analysis
```python
from sql_manager import SQLManager

# Initialize SQL manager
sql_manager = SQLManager()

# Get top economies
top_economies = sql_manager.get_top_economies(limit=10)

# Get regional analysis
regional_data = sql_manager.get_regional_analysis()

# Get anomalies
anomalies = sql_manager.get_anomalies()
```

### SQL Queries
```sql
-- Get GDP growth by country
SELECT * FROM yoy_gdp_growth WHERE Country = 'United States';

-- Get top economies in 2024
SELECT * FROM top20_economies_2024;

-- Get sectoral data
SELECT * FROM sectoral_split WHERE Country = 'China';
```

## 🎯 Use Cases

1. **Economic Research**: Academic and policy research on global economic trends
2. **Investment Analysis**: Country and regional economic performance evaluation
3. **Policy Making**: Government and international organization decision support
4. **Business Intelligence**: Market entry and expansion strategy development
5. **Educational Purposes**: Economics and data science learning resources

## 🤝 Contributing

We welcome contributions! Please feel free to submit issues, feature requests, or pull requests.

### Contribution Guidelines
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Priyansh Nandwana**
- GitHub: [@PrisDen](https://github.com/PrisDen)
- Project: GDP360 Hackathon Solution

## 🙏 Acknowledgments

- World Bank for providing the economic data
- Tableau for visualization capabilities
- Python community for excellent data science libraries
- GDP360 Hackathon organizers for the opportunity

## 📞 Contact

For questions, suggestions, or collaboration opportunities:
- Create an issue on GitHub
- Email: [Your Email]
- LinkedIn: [Your LinkedIn]

---

**Note**: This project was developed as part of the GDP360 Hackathon and represents a comprehensive solution for global economic data analysis.
