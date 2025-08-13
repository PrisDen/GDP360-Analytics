# GDP360 Analytics - Technical Documentation

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Data Pipeline](#data-pipeline)
4. [Database Schema](#database-schema)
5. [API Reference](#api-reference)
6. [Installation Guide](#installation-guide)
7. [Usage Examples](#usage-examples)
8. [Troubleshooting](#troubleshooting)
9. [Performance Optimization](#performance-optimization)
10. [Contributing Guidelines](#contributing-guidelines)

## 🎯 Project Overview

GDP360 Analytics is a comprehensive data analysis platform designed to process, analyze, and visualize global economic data. The system provides insights into GDP trends, regional economic patterns, sectoral analysis, and statistical anomaly detection across 196 countries from 1975 to 2024.

### Key Objectives
- **Data Integration**: Consolidate multiple economic datasets into a unified format
- **Quality Assurance**: Implement data validation and anomaly detection
- **Analytics Engine**: Provide comprehensive economic analysis capabilities
- **Visualization**: Create interactive dashboards and reports
- **Scalability**: Design for future data expansion and additional metrics

## 🏗️ Architecture

### System Components

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Raw Data      │    │   ETL Pipeline  │    │   Analytics     │
│   (CSV Files)   │───▶│   (Python)      │───▶│   Engine        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   SQLite DB     │    │   Visualizations│
                       │   (Processed)   │    │   (Tableau)     │
                       └─────────────────┘    └─────────────────┘
```

### Technology Stack
- **Backend**: Python 3.8+
- **Data Processing**: Pandas, NumPy
- **Database**: SQLite
- **Analytics**: Scikit-learn, SciPy
- **Visualization**: Tableau, Matplotlib, Seaborn
- **Development**: Jupyter Notebooks

## 🔄 Data Pipeline

### ETL Process Flow

1. **Extraction Phase**
   ```python
   # Load raw CSV files
   gdp_data = pd.read_csv('raw data/gdp.csv')
   population_data = pd.read_csv('raw data/population.csv')
   # ... additional data sources
   ```

2. **Transformation Phase**
   ```python
   # Data cleaning and standardization
   df = self.clean_data(df)
   df = self.add_regional_mapping(df)
   df = self.detect_anomalies(df)
   ```

3. **Loading Phase**
   ```python
   # Save to master dataset and database
   df.to_csv('master_data.csv', index=False)
   df.to_sql('gdp_data', conn, if_exists='replace', index=False)
   ```

### Data Quality Checks

- **Completeness**: Check for missing values
- **Consistency**: Validate data types and ranges
- **Accuracy**: Detect statistical anomalies
- **Timeliness**: Ensure data currency

## 🗄️ Database Schema

### Main Table: `gdp_data`

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| `Country` | TEXT | Country name | NOT NULL |
| `Year` | INTEGER | Year of data | NOT NULL, 1975-2024 |
| `GDP` | REAL | Gross Domestic Product (USD) | >= 0 |
| `GDP_per_capita` | REAL | GDP per capita (USD) | >= 0 |
| `Population` | INTEGER | Total population | >= 0 |
| `Agri_%` | REAL | Agricultural sector % | 0-100 |
| `Indus_%` | REAL | Industrial sector % | 0-100 |
| `Serv_%` | REAL | Service sector % | 0-100 |
| `Inflation_%` | REAL | Inflation rate % | Any value |
| `Unemployment_%` | REAL | Unemployment rate % | 0-100 |
| `Country_Code` | TEXT | ISO country code | 3 characters |
| `Region` | TEXT | Geographic region | 7 predefined regions |
| `GDP_Anomaly_Flag` | INTEGER | Anomaly flag | 0 or 1 |

### Database Views

1. **yoy_gdp_growth**: Year-over-year GDP growth calculations
2. **top20_economies_2024**: Latest economic rankings
3. **sectoral_split**: Economic sector breakdowns
4. **gdp_anomalies**: Flagged outlier data
5. **regional_gdp_summary**: Geographic economic patterns

## 🔌 API Reference

### SQLManager Class

#### Constructor
```python
SQLManager(db_path='master_gdp.db')
```

#### Methods

##### `get_top_economies(limit=20, year=2024)`
Returns top economies by GDP for a specific year.

**Parameters:**
- `limit` (int): Number of countries to return (default: 20)
- `year` (int): Year for analysis (default: 2024)

**Returns:** DataFrame with columns: Country, GDP, GDP_per_capita, Region

##### `get_regional_analysis(year=2024)`
Returns regional economic analysis.

**Parameters:**
- `year` (int): Year for analysis (default: 2024)

**Returns:** DataFrame with columns: Region, Countries, Total_GDP_Trillions, Avg_GDP_per_capita

##### `get_anomalies()`
Returns detected GDP anomalies.

**Returns:** DataFrame with all columns for anomalous records

##### `get_growth_analysis(min_years=20)`
Returns GDP growth analysis for countries with sufficient data.

**Parameters:**
- `min_years` (int): Minimum years of data required (default: 20)

**Returns:** DataFrame with growth metrics

### GDPDataProcessor Class

#### Constructor
```python
GDPDataProcessor(data_dir="raw data")
```

#### Methods

##### `process_all_data()`
Main method to process all raw data files.

**Returns:** Processed DataFrame

##### `detect_anomalies(df)`
Detects statistical anomalies in GDP data.

**Parameters:**
- `df` (DataFrame): Input data

**Returns:** DataFrame with anomaly flags

## 🚀 Installation Guide

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git

### Step-by-Step Installation

1. **Clone Repository**
   ```bash
   git clone https://github.com/PrisDen/GDP360-Analytics.git
   cd GDP360-Analytics
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv gdp_env
   source gdp_env/bin/activate  # On Windows: gdp_env\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify Installation**
   ```bash
   python -c "import pandas, numpy, sqlite3; print('Installation successful!')"
   ```

### Environment Setup

Create a `.env` file for configuration:
```env
DATA_DIR=raw data
DB_PATH=master_gdp.db
LOG_LEVEL=INFO
```

## 📊 Usage Examples

### Basic Data Analysis

```python
from etl_pipeline import GDPDataProcessor
from data_analysis import main

# Process raw data
processor = GDPDataProcessor()
master_data = processor.process_all_data()

# Run analysis
main()
```

### Custom SQL Queries

```python
import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect('master_gdp.db')

# Custom query example
query = """
SELECT Country, Year, GDP, GDP_per_capita
FROM gdp_data
WHERE Year = 2024 AND GDP IS NOT NULL
ORDER BY GDP DESC
LIMIT 10
"""

results = pd.read_sql_query(query, conn)
print(results)
```

### Anomaly Detection

```python
from etl_pipeline import GDPDataProcessor

processor = GDPDataProcessor()
df = processor.load_master_data()

# Get anomalies
anomalies = df[df['GDP_Anomaly_Flag'] == 1]
print(f"Found {len(anomalies)} anomalies:")
print(anomalies[['Country', 'Year', 'GDP']])
```

### Regional Analysis

```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('master_gdp.db')

# Regional GDP analysis
regional_query = """
SELECT 
    Region,
    COUNT(DISTINCT Country) as Countries,
    SUM(GDP) / 1e12 as Total_GDP_Trillions,
    AVG(GDP_per_capita) as Avg_GDP_per_capita
FROM gdp_data
WHERE Year = 2024 AND GDP IS NOT NULL
GROUP BY Region
ORDER BY Total_GDP_Trillions DESC
"""

regional_data = pd.read_sql_query(regional_query, conn)
print(regional_data)
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Import Errors
**Problem:** `ModuleNotFoundError: No module named 'pandas'`
**Solution:** Install dependencies: `pip install -r requirements.txt`

#### 2. Database Connection Issues
**Problem:** `sqlite3.OperationalError: no such table`
**Solution:** Run ETL pipeline first: `python etl_pipeline.py`

#### 3. Memory Issues
**Problem:** `MemoryError` when processing large datasets
**Solution:** Process data in chunks or increase system memory

#### 4. Data Quality Issues
**Problem:** Missing or inconsistent data
**Solution:** Check raw data files and run data validation

### Debug Mode

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Performance Monitoring

```python
import time
import psutil

def monitor_performance(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss
        
        result = func(*args, **kwargs)
        
        end_time = time.time()
        end_memory = psutil.Process().memory_info().rss
        
        print(f"Execution time: {end_time - start_time:.2f} seconds")
        print(f"Memory usage: {(end_memory - start_memory) / 1024 / 1024:.2f} MB")
        
        return result
    return wrapper
```

## ⚡ Performance Optimization

### Database Optimization

1. **Index Creation**
   ```sql
   CREATE INDEX idx_country_year ON gdp_data(Country, Year);
   CREATE INDEX idx_region_year ON gdp_data(Region, Year);
   CREATE INDEX idx_gdp_year ON gdp_data(GDP, Year);
   ```

2. **Query Optimization**
   ```sql
   -- Use EXPLAIN to analyze query performance
   EXPLAIN QUERY PLAN SELECT * FROM gdp_data WHERE Year = 2024;
   ```

### Memory Management

1. **Chunk Processing**
   ```python
   def process_in_chunks(df, chunk_size=1000):
       for i in range(0, len(df), chunk_size):
           chunk = df[i:i+chunk_size]
           # Process chunk
           yield chunk
   ```

2. **Data Type Optimization**
   ```python
   # Use appropriate data types to reduce memory usage
   df['Year'] = df['Year'].astype('int16')
   df['Country_Code'] = df['Country_Code'].astype('category')
   ```

## 🤝 Contributing Guidelines

### Development Setup

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/new-feature`
3. **Make changes and test**
4. **Commit changes**: `git commit -m 'Add new feature'`
5. **Push to branch**: `git push origin feature/new-feature`
6. **Create pull request**

### Code Standards

- Follow PEP 8 style guidelines
- Add docstrings to all functions
- Include type hints
- Write unit tests for new features
- Update documentation

### Testing

```bash
# Run tests
python -m pytest tests/

# Run with coverage
python -m pytest --cov=. tests/
```

### Documentation Updates

- Update README.md for user-facing changes
- Update DOCUMENTATION.md for technical changes
- Add inline comments for complex logic
- Create examples for new features

## 📈 Future Enhancements

### Planned Features

1. **Real-time Data Integration**
   - API connections to live economic data sources
   - Automated data updates

2. **Advanced Analytics**
   - Machine learning models for GDP prediction
   - Trend analysis and forecasting

3. **Enhanced Visualizations**
   - Interactive web dashboards
   - Real-time charts and graphs

4. **Data Export Options**
   - Multiple format support (JSON, XML, Excel)
   - API endpoints for data access

5. **User Management**
   - Multi-user support
   - Role-based access control

### Performance Improvements

1. **Database Migration**
   - Consider PostgreSQL for larger datasets
   - Implement connection pooling

2. **Caching Layer**
   - Redis for frequently accessed data
   - Query result caching

3. **Parallel Processing**
   - Multi-threading for data processing
   - Distributed computing for large-scale analysis

---

**Last Updated**: January 2024
**Version**: 1.0.0
**Maintainer**: Priyansh Nandwana
