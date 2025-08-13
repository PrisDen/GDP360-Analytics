-- View 1: Year-over-Year GDP Growth per Country
CREATE VIEW IF NOT EXISTS yoy_gdp_growth AS
SELECT 
    Country,
    Year,
    GDP,
    LAG(GDP) OVER (PARTITION BY Country ORDER BY Year) AS Prev_Year_GDP,
    ROUND(
        (GDP - LAG(GDP) OVER (PARTITION BY Country ORDER BY Year)) * 100.0 / 
        NULLIF(LAG(GDP) OVER (PARTITION BY Country ORDER BY Year), 0), 2
    ) AS YoY_Growth_%
FROM gdp_data
WHERE GDP IS NOT NULL;

-- View 2: Top 20 Economies in Latest Year (2024)
CREATE VIEW IF NOT EXISTS top20_economies_2024 AS
SELECT 
    Country,
    Region,
    GDP,
    GDP_per_capita,
    Population
FROM gdp_data
WHERE Year = 2024 AND GDP IS NOT NULL
ORDER BY GDP DESC
LIMIT 20;

-- View 3: Sectoral Split per Country-Year
CREATE VIEW IF NOT EXISTS sectoral_split AS
SELECT
    Country,
    Year,
    Agri_%,
    Indus_%,
    Serv_%,
    GDP
FROM gdp_data
WHERE Agri_% IS NOT NULL OR Indus_% IS NOT NULL OR Serv_% IS NOT NULL;

-- View 4: GDP Anomalies (Only rows flagged)
CREATE VIEW IF NOT EXISTS gdp_anomalies AS
SELECT *
FROM gdp_data
WHERE GDP_Anomaly_Flag = 1;

-- View 5: Regional GDP Summary (Total GDP by Region & Year)
CREATE VIEW IF NOT EXISTS regional_gdp_summary AS
SELECT
    Region,
    Year,
    SUM(GDP) AS Total_Regional_GDP,
    ROUND(AVG(GDP_per_capita), 2) AS Avg_GDP_per_Capita
FROM gdp_data
WHERE GDP IS NOT NULL
GROUP BY Region, Year
ORDER BY Year;