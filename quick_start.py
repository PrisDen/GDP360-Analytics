#!/usr/bin/env python3
"""
GDP360 Analytics - Quick Start Script
This script helps users get started with the GDP360 Analytics project quickly.
"""

import os
import sys
import subprocess
import sqlite3
import pandas as pd

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required.")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_dependencies():
    """Check if required packages are installed."""
    required_packages = ['pandas', 'numpy', 'sqlite3']
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'sqlite3':
                import sqlite3
            else:
                __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} is missing")
    
    if missing_packages:
        print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
            print("✅ All packages installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install packages. Please run: pip install -r requirements.txt")
            return False
    
    return True

def check_data_files():
    """Check if raw data files exist."""
    raw_data_dir = "raw data"
    required_files = [
        "gdp.csv",
        "gdp_per_capita.csv", 
        "population.csv",
        "sector_agriculture.csv",
        "sector_industry.csv",
        "sector_service.csv",
        "inflation.csv",
        "unemployment.csv"
    ]
    
    if not os.path.exists(raw_data_dir):
        print(f"❌ Raw data directory '{raw_data_dir}' not found")
        return False
    
    missing_files = []
    for file in required_files:
        file_path = os.path.join(raw_data_dir, file)
        if os.path.exists(file_path):
            print(f"✅ {file}")
        else:
            missing_files.append(file)
            print(f"❌ {file} - missing")
    
    if missing_files:
        print(f"\n⚠️  Warning: {len(missing_files)} data files are missing:")
        for file in missing_files:
            print(f"   - {file}")
        print("Please ensure all raw data files are present in the 'raw data' directory.")
        return False
    
    return True

def run_etl_pipeline():
    """Run the ETL pipeline to process data."""
    print("\n🔄 Running ETL Pipeline...")
    try:
        from etl_pipeline import GDPDataProcessor
        
        processor = GDPDataProcessor()
        master_data = processor.process_all_data()
        
        print(f"✅ ETL Pipeline completed successfully!")
        print(f"📊 Processed {len(master_data):,} records")
        print(f"🌍 Data covers {master_data['Country'].nunique()} countries")
        print(f"📅 Time span: {master_data['Year'].min()} - {master_data['Year'].max()}")
        
        return True
    except Exception as e:
        print(f"❌ ETL Pipeline failed: {str(e)}")
        return False

def run_data_analysis():
    """Run the data analysis script."""
    print("\n📈 Running Data Analysis...")
    try:
        from data_analysis import main
        main()
        print("✅ Data analysis completed successfully!")
        return True
    except Exception as e:
        print(f"❌ Data analysis failed: {str(e)}")
        return False

def check_database():
    """Check if the database was created successfully."""
    db_path = "master_gdp.db"
    if not os.path.exists(db_path):
        print(f"❌ Database file '{db_path}' not found")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='gdp_data'")
        if not cursor.fetchone():
            print("❌ 'gdp_data' table not found in database")
            return False
        
        # Get record count
        cursor.execute("SELECT COUNT(*) FROM gdp_data")
        count = cursor.fetchone()[0]
        
        # Get year range
        cursor.execute("SELECT MIN(Year), MAX(Year) FROM gdp_data")
        min_year, max_year = cursor.fetchone()
        
        # Get country count
        cursor.execute("SELECT COUNT(DISTINCT Country) FROM gdp_data")
        country_count = cursor.fetchone()[0]
        
        conn.close()
        
        print(f"✅ Database created successfully!")
        print(f"📊 Records: {count:,}")
        print(f"🌍 Countries: {country_count}")
        print(f"📅 Years: {min_year} - {max_year}")
        
        return True
    except Exception as e:
        print(f"❌ Database check failed: {str(e)}")
        return False

def show_next_steps():
    """Show next steps for users."""
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next Steps:")
    print("1. 📊 Explore the data:")
    print("   python data_analysis.py")
    print("\n2. 🔍 Run custom queries:")
    print("   sqlite3 master_gdp.db")
    print("\n3. 📈 View visualizations:")
    print("   Open tableau/Book1.twb in Tableau")
    print("\n4. 📖 Read documentation:")
    print("   Open README.md and DOCUMENTATION.md")
    print("\n5. 🛠️  Customize analysis:")
    print("   Modify etl_pipeline.py or data_analysis.py")
    
    print("\n🔗 Useful Resources:")
    print("- GitHub Repository: https://github.com/PrisDen/GDP360-Analytics")
    print("- Documentation: DOCUMENTATION.md")
    print("- Issues: https://github.com/PrisDen/GDP360-Analytics/issues")

def main():
    """Main function to run the quick start process."""
    print("🚀 GDP360 Analytics - Quick Start")
    print("=" * 50)
    
    # Step 1: Check Python version
    print("\n1️⃣ Checking Python version...")
    if not check_python_version():
        return False
    
    # Step 2: Check dependencies
    print("\n2️⃣ Checking dependencies...")
    if not check_dependencies():
        return False
    
    # Step 3: Check data files
    print("\n3️⃣ Checking data files...")
    if not check_data_files():
        print("\n⚠️  Please ensure all raw data files are present before continuing.")
        response = input("Continue anyway? (y/N): ").lower().strip()
        if response != 'y':
            return False
    
    # Step 4: Run ETL pipeline
    print("\n4️⃣ Processing data...")
    if not run_etl_pipeline():
        return False
    
    # Step 5: Check database
    print("\n5️⃣ Verifying database...")
    if not check_database():
        return False
    
    # Step 6: Run analysis
    print("\n6️⃣ Running analysis...")
    run_data_analysis()
    
    # Step 7: Show next steps
    show_next_steps()
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n✅ Quick start completed successfully!")
        else:
            print("\n❌ Quick start failed. Please check the errors above.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)
