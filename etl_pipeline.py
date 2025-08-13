import pandas as pd
import numpy as np
import os
from sql_manager import SQLManager

class GDPDataProcessor:
    def __init__(self, data_dir="raw data"):
        self.data_dir = data_dir
        self.file_mappings = {
            'gdp.csv': 'GDP',
            'gdp_per_capita.csv': 'GDP_per_capita',
            'population.csv': 'Population',
            'sector_agriculture.csv': 'Agri_%',
            'sector_industry.csv': 'Indus_%',
            'sector_service.csv': 'Serv_%',
            'inflation.csv': 'Inflation_%',
            'unemployment.csv': 'Unemployment_%'
        }
        
        # Comprehensive region mapping
        self.region_mapping = {
            # East Asia & Pacific
            'Australia': 'East Asia & Pacific', 'Brunei': 'East Asia & Pacific', 'Cambodia': 'East Asia & Pacific',
            'China': 'East Asia & Pacific', 'Fiji': 'East Asia & Pacific', 'Indonesia': 'East Asia & Pacific',
            'Japan': 'East Asia & Pacific', 'Kiribati': 'East Asia & Pacific', 'Korea, Rep.': 'East Asia & Pacific',
            'Lao PDR': 'East Asia & Pacific', 'Malaysia': 'East Asia & Pacific', 'Marshall Islands': 'East Asia & Pacific',
            'Micronesia, Fed. Sts.': 'East Asia & Pacific', 'Mongolia': 'East Asia & Pacific', 'Myanmar': 'East Asia & Pacific',
            'New Zealand': 'East Asia & Pacific', 'Palau': 'East Asia & Pacific', 'Papua New Guinea': 'East Asia & Pacific',
            'Philippines': 'East Asia & Pacific', 'Samoa': 'East Asia & Pacific', 'Singapore': 'East Asia & Pacific',
            'Solomon Islands': 'East Asia & Pacific', 'Thailand': 'East Asia & Pacific', 'Timor-Leste': 'East Asia & Pacific',
            'Tonga': 'East Asia & Pacific', 'Tuvalu': 'East Asia & Pacific', 'Vanuatu': 'East Asia & Pacific',
            'Vietnam': 'East Asia & Pacific',
            
            # Europe & Central Asia
            'Albania': 'Europe & Central Asia', 'Armenia': 'Europe & Central Asia', 'Austria': 'Europe & Central Asia',
            'Azerbaijan': 'Europe & Central Asia', 'Belarus': 'Europe & Central Asia', 'Belgium': 'Europe & Central Asia',
            'Bosnia and Herzegovina': 'Europe & Central Asia', 'Bulgaria': 'Europe & Central Asia', 'Croatia': 'Europe & Central Asia',
            'Cyprus': 'Europe & Central Asia', 'Czech Republic': 'Europe & Central Asia', 'Denmark': 'Europe & Central Asia',
            'Estonia': 'Europe & Central Asia', 'Finland': 'Europe & Central Asia', 'France': 'Europe & Central Asia',
            'Georgia': 'Europe & Central Asia', 'Germany': 'Europe & Central Asia', 'Greece': 'Europe & Central Asia',
            'Hungary': 'Europe & Central Asia', 'Iceland': 'Europe & Central Asia', 'Ireland': 'Europe & Central Asia',
            'Italy': 'Europe & Central Asia', 'Kazakhstan': 'Europe & Central Asia', 'Kosovo': 'Europe & Central Asia',
            'Kyrgyz Republic': 'Europe & Central Asia', 'Latvia': 'Europe & Central Asia', 'Lithuania': 'Europe & Central Asia',
            'Luxembourg': 'Europe & Central Asia', 'Moldova': 'Europe & Central Asia', 'Montenegro': 'Europe & Central Asia',
            'Netherlands': 'Europe & Central Asia', 'North Macedonia': 'Europe & Central Asia', 'Norway': 'Europe & Central Asia',
            'Poland': 'Europe & Central Asia', 'Portugal': 'Europe & Central Asia', 'Romania': 'Europe & Central Asia',
            'Russian Federation': 'Europe & Central Asia', 'Serbia': 'Europe & Central Asia', 'Slovak Republic': 'Europe & Central Asia',
            'Slovenia': 'Europe & Central Asia', 'Spain': 'Europe & Central Asia', 'Sweden': 'Europe & Central Asia',
            'Switzerland': 'Europe & Central Asia', 'Tajikistan': 'Europe & Central Asia', 'Turkey': 'Europe & Central Asia',
            'Turkmenistan': 'Europe & Central Asia', 'Ukraine': 'Europe & Central Asia', 'United Kingdom': 'Europe & Central Asia',
            'Uzbekistan': 'Europe & Central Asia',
            
            # Latin America & Caribbean
            'Antigua and Barbuda': 'Latin America & Caribbean', 'Argentina': 'Latin America & Caribbean',
            'Bahamas, The': 'Latin America & Caribbean', 'Barbados': 'Latin America & Caribbean', 'Belize': 'Latin America & Caribbean',
            'Bolivia': 'Latin America & Caribbean', 'Brazil': 'Latin America & Caribbean', 'Chile': 'Latin America & Caribbean',
            'Colombia': 'Latin America & Caribbean', 'Costa Rica': 'Latin America & Caribbean', 'Cuba': 'Latin America & Caribbean',
            'Dominica': 'Latin America & Caribbean', 'Dominican Republic': 'Latin America & Caribbean', 'Ecuador': 'Latin America & Caribbean',
            'El Salvador': 'Latin America & Caribbean', 'Grenada': 'Latin America & Caribbean', 'Guatemala': 'Latin America & Caribbean',
            'Guyana': 'Latin America & Caribbean', 'Haiti': 'Latin America & Caribbean', 'Honduras': 'Latin America & Caribbean',
            'Jamaica': 'Latin America & Caribbean', 'Mexico': 'Latin America & Caribbean', 'Nicaragua': 'Latin America & Caribbean',
            'Panama': 'Latin America & Caribbean', 'Paraguay': 'Latin America & Caribbean', 'Peru': 'Latin America & Caribbean',
            'St. Kitts and Nevis': 'Latin America & Caribbean', 'St. Lucia': 'Latin America & Caribbean',
            'St. Vincent and the Grenadines': 'Latin America & Caribbean', 'Suriname': 'Latin America & Caribbean',
            'Trinidad and Tobago': 'Latin America & Caribbean', 'Uruguay': 'Latin America & Caribbean', 'Venezuela, RB': 'Latin America & Caribbean',
            
            # Middle East & North Africa
            'Algeria': 'Middle East & North Africa', 'Bahrain': 'Middle East & North Africa', 'Egypt, Arab Rep.': 'Middle East & North Africa',
            'Iran, Islamic Rep.': 'Middle East & North Africa', 'Iraq': 'Middle East & North Africa', 'Israel': 'Middle East & North Africa',
            'Jordan': 'Middle East & North Africa', 'Kuwait': 'Middle East & North Africa', 'Lebanon': 'Middle East & North Africa',
            'Libya': 'Middle East & North Africa', 'Morocco': 'Middle East & North Africa', 'Oman': 'Middle East & North Africa',
            'Qatar': 'Middle East & North Africa', 'Saudi Arabia': 'Middle East & North Africa', 'Syrian Arab Republic': 'Middle East & North Africa',
            'Tunisia': 'Middle East & North Africa', 'United Arab Emirates': 'Middle East & North Africa', 'Yemen, Rep.': 'Middle East & North Africa',
            
            # North America
            'Canada': 'North America', 'United States': 'North America',
            
            # South Asia
            'Afghanistan': 'South Asia', 'Bangladesh': 'South Asia', 'Bhutan': 'South Asia', 'India': 'South Asia',
            'Maldives': 'South Asia', 'Nepal': 'South Asia', 'Pakistan': 'South Asia', 'Sri Lanka': 'South Asia',
            
            # Sub-Saharan Africa
            'Angola': 'Sub-Saharan Africa', 'Benin': 'Sub-Saharan Africa', 'Botswana': 'Sub-Saharan Africa',
            'Burkina Faso': 'Sub-Saharan Africa', 'Burundi': 'Sub-Saharan Africa', 'Cameroon': 'Sub-Saharan Africa',
            'Cape Verde': 'Sub-Saharan Africa', 'Central African Republic': 'Sub-Saharan Africa', 'Chad': 'Sub-Saharan Africa',
            'Comoros': 'Sub-Saharan Africa', 'Congo, Dem. Rep.': 'Sub-Saharan Africa', 'Congo, Rep.': 'Sub-Saharan Africa',
            'Cote d\'Ivoire': 'Sub-Saharan Africa', 'Equatorial Guinea': 'Sub-Saharan Africa', 'Eritrea': 'Sub-Saharan Africa',
            'Eswatini': 'Sub-Saharan Africa', 'Ethiopia': 'Sub-Saharan Africa', 'Gabon': 'Sub-Saharan Africa',
            'Gambia, The': 'Sub-Saharan Africa', 'Ghana': 'Sub-Saharan Africa', 'Guinea': 'Sub-Saharan Africa',
            'Guinea-Bissau': 'Sub-Saharan Africa', 'Kenya': 'Sub-Saharan Africa', 'Lesotho': 'Sub-Saharan Africa',
            'Liberia': 'Sub-Saharan Africa', 'Madagascar': 'Sub-Saharan Africa', 'Malawi': 'Sub-Saharan Africa',
            'Mali': 'Sub-Saharan Africa', 'Mauritania': 'Sub-Saharan Africa', 'Mauritius': 'Sub-Saharan Africa',
            'Mozambique': 'Sub-Saharan Africa', 'Namibia': 'Sub-Saharan Africa', 'Niger': 'Sub-Saharan Africa',
            'Nigeria': 'Sub-Saharan Africa', 'Rwanda': 'Sub-Saharan Africa', 'Sao Tome and Principe': 'Sub-Saharan Africa',
            'Senegal': 'Sub-Saharan Africa', 'Seychelles': 'Sub-Saharan Africa', 'Sierra Leone': 'Sub-Saharan Africa',
            'Somalia': 'Sub-Saharan Africa', 'South Africa': 'Sub-Saharan Africa', 'South Sudan': 'Sub-Saharan Africa',
            'Sudan': 'Sub-Saharan Africa', 'Tanzania': 'Sub-Saharan Africa', 'Togo': 'Sub-Saharan Africa',
            'Uganda': 'Sub-Saharan Africa', 'Zambia': 'Sub-Saharan Africa', 'Zimbabwe': 'Sub-Saharan Africa'
        }
        
        # Regional aggregates to filter out
        self.regional_aggregates = [
            'World', 'High income', 'Low income', 'Lower middle income', 'Upper middle income',
            'East Asia & Pacific', 'Europe & Central Asia', 'Latin America & Caribbean', 'Middle East & North Africa',
            'North America', 'South Asia', 'Sub-Saharan Africa', 'Euro area', 'European Union',
            'Arab World', 'Caribbean small states', 'Central Europe and the Baltics', 'Early-demographic dividend',
            'East Asia & Pacific (excluding high income)', 'Europe & Central Asia (excluding high income)',
            'Fragile and conflict affected situations', 'Heavily indebted poor countries (HIPC)',
            'IBRD only', 'IDA & IBRD total', 'IDA blend', 'IDA only', 'IDA total',
            'Late-demographic dividend', 'Latin America & Caribbean (excluding high income)',
            'Least developed countries: UN classification', 'Low & middle income', 'Middle East & North Africa (excluding high income)',
            'Middle income', 'OECD members', 'Other small states', 'Pacific island small states',
            'Post-demographic dividend', 'Pre-demographic dividend', 'Small states', 'South Asia (IDA & IBRD)',
            'Sub-Saharan Africa (excluding high income)', 'Sub-Saharan Africa (IDA & IBRD countries)',
            'East Asia & Pacific (IDA & IBRD countries)', 'Latin America & the Caribbean (IDA & IBRD countries)',
            'Europe & Central Asia (IDA & IBRD countries)', 'Middle East, North Africa, Afghanistan & Pakistan',
            'Middle East, North Africa, Afghanistan & Pakistan (excluding high income)',
            'Middle East, North Africa, Afghanistan & Pakistan (IDA & IBRD)',
            'Africa Eastern and Southern', 'Africa Western and Central', 'American Samoa',
            'Andorra', 'Aruba', 'Bermuda', 'British Virgin Islands', 'Cayman Islands', 'Curacao',
            'Faroe Islands', 'French Polynesia', 'Gibraltar', 'Greenland', 'Guam', 'Hong Kong SAR, China',
            'Isle of Man', 'Kosovo', 'Macao SAR, China', 'Marshall Islands', 'Micronesia, Fed. Sts.',
            'Monaco', 'New Caledonia', 'Northern Mariana Islands', 'Palau', 'Puerto Rico',
            'San Marino', 'Sint Maarten (Dutch part)', 'Turks and Caicos Islands', 'U.S. Virgin Islands'
        ]

    def read_and_preprocess_file(self, filename):
        print(f"Processing {filename}...")
        filepath = f"{self.data_dir}/{filename}"
        
        # Try different encodings
        for encoding in ['utf-8', 'latin-1', 'cp1252']:
            try:
                df = pd.read_csv(filepath, encoding=encoding)
                break
            except UnicodeDecodeError:
                continue
        else:
            raise Exception(f"Could not read {filename} with any encoding")
        
        id_vars = ["Country Name"]
        year_columns = []
        for col in df.columns:
            col_str = str(col)
            if col_str.isdigit():
                year_columns.append(col)
            elif "[YR" in col_str:
                year_columns.append(col)
        
        df_melted = pd.melt(
            df,
            id_vars=id_vars,
            value_vars=year_columns,
            var_name="Year",
            value_name=self.file_mappings[filename]
        )
        
        def extract_year(year_str):
            year_str = str(year_str)
            if year_str.isdigit():
                return int(year_str)
            elif "[YR" in year_str:
                return int(year_str.split()[0])
            return None
        
        df_melted['Year'] = df_melted['Year'].apply(extract_year)
        df_melted['Year'] = pd.to_numeric(df_melted['Year'], errors='coerce')
        df_melted[self.file_mappings[filename]] = pd.to_numeric(
            df_melted[self.file_mappings[filename]], 
            errors='coerce'
        )
        df_melted = df_melted[df_melted['Year'] >= 1975]
        return df_melted

    def detect_gdp_anomalies(self, df):
        """Detect GDP anomalies using 3-sigma rule"""
        print("Detecting GDP anomalies...")
        
        # Calculate rolling statistics for each country
        df_anomalies = df.copy()
        df_anomalies['GDP_Anomaly_Flag'] = 0
        
        for country in df_anomalies['Country'].unique():
            country_data = df_anomalies[df_anomalies['Country'] == country]
            gdp_values = country_data['GDP'].dropna()
            
            if len(gdp_values) > 10:  # Need sufficient data for anomaly detection
                mean_gdp = gdp_values.mean()
                std_gdp = gdp_values.std()
                
                if std_gdp > 0:  # Avoid division by zero
                    # Find anomalies (values beyond 3 standard deviations)
                    anomalies = country_data[
                        (country_data['GDP'] > mean_gdp + 3 * std_gdp) |
                        (country_data['GDP'] < mean_gdp - 3 * std_gdp)
                    ]
                    
                    if len(anomalies) > 0:
                        df_anomalies.loc[anomalies.index, 'GDP_Anomaly_Flag'] = 1
        
        anomaly_count = df_anomalies['GDP_Anomaly_Flag'].sum()
        print(f"✓ Detected {anomaly_count} GDP anomalies")
        return df_anomalies

    def assign_regions(self, df):
        """Assign regions to countries using comprehensive mapping"""
        print("Assigning regions to countries...")
        
        df['Region'] = df['Country'].map(self.region_mapping)
        
        # Count assigned vs unassigned
        assigned = df['Region'].notna().sum()
        unassigned = df['Region'].isna().sum()
        print(f"✓ Assigned regions to {assigned:,} records, {unassigned:,} remain unassigned")
        
        return df

    def filter_countries_only(self, df):
        """Filter out regional aggregates, keep only actual countries"""
        print("Filtering out regional aggregates...")
        
        initial_count = len(df)
        df_filtered = df[~df['Country'].isin(self.regional_aggregates)]
        final_count = len(df_filtered)
        
        removed_count = initial_count - final_count
        print(f"✓ Removed {removed_count:,} regional aggregate records")
        print(f"✓ Kept {final_count:,} country records")
        
        return df_filtered

    def process_all_files(self):
        print("Starting ETL pipeline...")
        dataframes = {}
        
        for filename, column_name in self.file_mappings.items():
            try:
                df = self.read_and_preprocess_file(filename)
                dataframes[column_name] = df
                print(f"✓ {filename} processed successfully")
            except Exception as e:
                print(f"✗ Error processing {filename}: {e}")
                return None
        
        print("Merging datasets...")
        merged_df = dataframes['GDP'].copy()
        
        for column_name, df in dataframes.items():
            if column_name != 'GDP':
                merged_df = merged_df.merge(
                    df[['Country Name', 'Year', column_name]],
                    on=['Country Name', 'Year'],
                    how='outer'
                )
        
        # Clean and prepare data
        merged_df = merged_df.rename(columns={'Country Name': 'Country'})
        merged_df = merged_df.replace('..', np.nan)
        
        # Remove placeholder columns (Export, Import, Debt_%)
        value_columns = [col for col in merged_df.columns if col not in ['Country', 'Year']]
        merged_df = merged_df.dropna(subset=value_columns, how='all')
        
        # Add Country Code
        merged_df['Country Code'] = merged_df['Country'].str[:3].str.upper()
        
        # Filter out regional aggregates
        merged_df = self.filter_countries_only(merged_df)
        
        # Assign regions
        merged_df = self.assign_regions(merged_df)
        
        # Detect GDP anomalies
        merged_df = self.detect_gdp_anomalies(merged_df)
        
        print(f"✓ Final dataset created with {len(merged_df)} rows")
        return merged_df

    def save_to_database(self, df):
        """Save processed data to database using SQL manager"""
        sql_manager = SQLManager()
        sql_manager.save_dataframe_to_db(df)
        sql_manager.create_analytical_views()
        sql_manager.test_views()

    def run_pipeline(self):
        """Run the complete ETL pipeline"""
        # Process data
        merged_df = self.process_all_files()
        if merged_df is None:
            print("❌ Pipeline failed")
            return
        
        # Save to CSV
        print("Saving to CSV...")
        merged_df.to_csv('master_data.csv', index=False)
        print("✓ master_data.csv saved")
        
        # Save to database using SQL manager
        self.save_to_database(merged_df)
        
        # Print summary statistics
        print("\n📊 FINAL DATASET SUMMARY:")
        print(f"  Total records: {len(merged_df):,}")
        print(f"  Countries: {merged_df['Country'].nunique()}")
        print(f"  Years: {merged_df['Year'].min()} - {merged_df['Year'].max()}")
        print(f"  GDP coverage: {(merged_df['GDP'].notna().sum() / len(merged_df) * 100):.1f}%")
        print(f"  Anomalies detected: {merged_df['GDP_Anomaly_Flag'].sum()}")
        print(f"  Regions assigned: {(merged_df['Region'].notna().sum() / len(merged_df) * 100):.1f}%")

if __name__ == "__main__":
    processor = GDPDataProcessor()
    processor.run_pipeline() 