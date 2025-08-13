#!/usr/bin/env python3

import pandas as pd
from sql_manager import SQLManager

def main():
    print("=" * 60)
    print("GDP DATA ANALYSIS")
    print("=" * 60)
    
    # Initialize SQL manager
    sql_manager = SQLManager()
    
    # 1. Top Economies Analysis
    print("\n🏆 TOP 20 ECONOMIES ANALYSIS")
    print("-" * 40)
    top_economies = sql_manager.get_top_economies(limit=20)
    
    for i, (_, row) in enumerate(top_economies.iterrows(), 1):
        gdp_trillions = row['GDP'] / 1e12
        gdp_per_capita = f"${row['GDP_per_capita']:,.0f}" if pd.notna(row['GDP_per_capita']) else "N/A"
        region = row['Region'] if pd.notna(row['Region']) else 'Unknown'
        print(f"{i:2d}. {row['Country']:<20}: ${gdp_trillions:>6.1f}T | {gdp_per_capita:>10} per capita | {region}")
    
    # 2. Regional Analysis
    print("\n🌍 REGIONAL GDP ANALYSIS (2024)")
    print("-" * 40)
    regional_data = sql_manager.get_regional_analysis()
    
    for _, row in regional_data.iterrows():
        avg_per_capita = f"${row['Avg_GDP_per_capita']:,.0f}" if pd.notna(row['Avg_GDP_per_capita']) else "N/A"
        print(f"{row['Region']:<30}: {row['Countries']:>2} countries | ${row['Total_GDP_Trillions']:>6.1f}T total | {avg_per_capita:>10} avg per capita")
    
    # 3. Anomaly Detection
    print("\n🚨 GDP ANOMALY ANALYSIS")
    print("-" * 40)
    anomalies = sql_manager.get_anomalies()
    
    if len(anomalies) > 0:
        print(f"Detected {len(anomalies)} GDP anomalies:")
        for _, row in anomalies.iterrows():
            gdp_formatted = f"${row['GDP']:,.0f}" if pd.notna(row['GDP']) else "N/A"
            region = row['Region'] if pd.notna(row['Region']) else 'Unknown'
            print(f"  {row['Country']} ({row['Year']}): {gdp_formatted} | {region}")
    else:
        print("No anomalies detected.")
    
    # 4. Growth Analysis
    print("\n📈 GDP GROWTH ANALYSIS")
    print("-" * 40)
    growth_data = sql_manager.get_growth_analysis(min_years=20)
    
    print("Countries with 20+ years of data, ranked by total growth:")
    for i, (_, row) in enumerate(growth_data.head(10).iterrows(), 1):
        total_growth = f"{row['Total_Growth_Pct']:.1f}%" if pd.notna(row['Total_Growth_Pct']) else "N/A"
        avg_gdp = f"${row['Avg_GDP']/1e9:.1f}B" if pd.notna(row['Avg_GDP']) else "N/A"
        print(f"{i:2d}. {row['Country']:<20}: {total_growth:>8} growth | {avg_gdp:>10} avg GDP | {row['Years_Data']:>2} years")
    
    # 5. Summary Statistics
    print("\n📊 DATASET SUMMARY")
    print("-" * 40)
    
    # Get basic stats from database
    conn = sql_manager.create_connection()
    
    # Total records
    total_records = pd.read_sql_query("SELECT COUNT(*) as count FROM gdp_data", conn)['count'].iloc[0]
    
    # Countries
    countries = pd.read_sql_query("SELECT COUNT(DISTINCT Country) as count FROM gdp_data", conn)['count'].iloc[0]
    
    # Years
    years = pd.read_sql_query("SELECT MIN(Year) as min_year, MAX(Year) as max_year FROM gdp_data", conn)
    year_range = f"{years['min_year'].iloc[0]} - {years['max_year'].iloc[0]}"
    
    # GDP coverage
    gdp_coverage = pd.read_sql_query("SELECT ROUND((COUNT(GDP) * 100.0 / COUNT(*)), 1) as coverage FROM gdp_data", conn)['coverage'].iloc[0]
    
    # Anomalies
    anomaly_count = pd.read_sql_query("SELECT COUNT(*) as count FROM gdp_data WHERE GDP_Anomaly_Flag = 1", conn)['count'].iloc[0]
    
    # Regions
    region_coverage = pd.read_sql_query("SELECT ROUND((COUNT(Region) * 100.0 / COUNT(*)), 1) as coverage FROM gdp_data", conn)['coverage'].iloc[0]
    
    conn.close()
    
    print(f"📈 Total Records: {total_records:,}")
    print(f"🌍 Countries: {countries}")
    print(f"📅 Year Range: {year_range}")
    print(f"💰 GDP Coverage: {gdp_coverage}%")
    print(f"🚨 Anomalies: {anomaly_count}")
    print(f"🗺️  Region Coverage: {region_coverage}%")
    
    
    print("=" * 60)

if __name__ == "__main__":
    main() 