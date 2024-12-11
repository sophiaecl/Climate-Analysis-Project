# climate_analysis/data_processor.py

import pandas as pd
import numpy as np

class ClimateDataProcessor:
    """Class to handle loading and processing of climate data"""
    
    def __init__(self):
        self.temp_data = None
        self.co2_data = None
        self.disaster_data = None
        self.merged_data = None
        self.available_countries = None

    def load_disaster_data(self, filepath, country=None):
        """
        Load and process climate disaster data for a specific country or global data
        
        Parameters:
        filepath (str): Path to the disaster data CSV
        country (str): Country name to filter for. If None, uses global data
        """
        try:
            # Read CSV
            df = pd.read_csv(filepath)
            
            # Store available countries for reference
            self.available_countries = sorted(df['Country'].unique().tolist())
            
            # Filter for selected country or global data
            if country is None or country.lower() == 'global':
                selected_data = df[df['Country'] == 'All Countries and International Organizations']
                print("\nUsing global disaster data")
            else:
                if country not in self.available_countries:
                    raise ValueError(f"Country '{country}' not found in dataset. Use get_available_countries() to see options.")
                selected_data = df[df['Country'] == country]
                print(f"\nUsing disaster data for {country}")
            
            # Melt the year columns into rows
            years = [str(year) for year in range(1980, 2024)]
            disaster_data = pd.melt(
                selected_data,
                id_vars=['Country', 'Indicator'],
                value_vars=years,
                var_name='Year',
                value_name='Disasters'
            )
            
            # Convert Year to integer and filter for total disasters
            disaster_data['Year'] = disaster_data['Year'].astype(int)
            disaster_data = disaster_data[
                disaster_data['Indicator'].str.contains('TOTAL')
            ]
            
            # Clean up the data
            disaster_data = disaster_data[['Year', 'Disasters']].copy()
            
            print(f"Processed {len(disaster_data)} disaster records")
            print(f"Year range: {disaster_data['Year'].min()} to {disaster_data['Year'].max()}")
            
            self.disaster_data = disaster_data
            return self.disaster_data
            
        except Exception as e:
            print(f"Error loading disaster data: {str(e)}")
            raise

    def get_available_countries(self):
        """
        Get list of available countries in the dataset
        
        Returns:
        list: Sorted list of country names
        """
        if self.available_countries is None:
            return []
        return self.available_countries
    
    def load_temperature_data(self, filepath):
        """
        Load and process temperature anomaly data
        Schema:
        - Source (string): Data source
        - Year (year): YYYY
        - Mean (number): Temperature anomaly in Celsius
        """
        try:
            # Read CSV with specific dtypes
            df = pd.read_csv(filepath, dtype={
                'Source': str,
                'Year': int,
                'Mean': float
            })
            
            print("\nTemperature data columns found:", df.columns.tolist())
            
            # Basic validation
            required_columns = {'Source', 'Year', 'Mean'}
            if not all(col in df.columns for col in required_columns):
                raise ValueError(f"Temperature data must contain columns: {required_columns}")
            
            # Filter for valid data
            df = df.dropna(subset=['Year', 'Mean'])
            
            # Create clean dataset with single entry per year (taking mean if multiple entries)
            temp_data = df.groupby('Year')['Mean'].mean().reset_index()
            temp_data.columns = ['Year', 'Temperature_Anomaly']
            
            print(f"\nProcessed {len(temp_data)} temperature records")
            print(f"Year range: {temp_data['Year'].min()} to {temp_data['Year'].max()}")
            
            self.temp_data = temp_data
            return self.temp_data
            
        except Exception as e:
            print(f"Error loading temperature data: {str(e)}")
            raise
    
    def load_co2_data(self, filepath):
        """
        Load and process CO2 concentration data
        Extracts:
        - Year from Decimal Date column
        - Average CO2 measurements
        """
        try:
            # Read CSV
            df = pd.read_csv(filepath)
            
            print("\nCO2 data columns found:", df.columns.tolist())
            print("\nData types of columns:")
            print(df.dtypes)
            print("\nFirst few rows of raw data:")
            print(df[['Date', 'Average']].head())
            
            # Parse Date as datetime and extract the year
            df['Year'] = pd.to_datetime(df['Date'], format='%Y-%m').dt.year
            df['CO2_Level'] = df['Average']
            
            # Remove invalid measurements (marked as -99.99)
            df = df[df['CO2_Level'] > 0]
            
            # Calculate annual averages
            yearly_co2 = df.groupby('Year')['CO2_Level'].mean().reset_index()
            
            print(f"\nProcessed {len(yearly_co2)} CO2 records")
            print(f"Year range: {yearly_co2['Year'].min()} to {yearly_co2['Year'].max()}")
            print("\nCO2 annual averages preview:")
            print(yearly_co2.head())
            
            self.co2_data = yearly_co2
            return self.co2_data
            
        except Exception as e:
            print(f"Error loading CO2 data: {str(e)}")
            raise

    
    def merge_datasets(self):
        """Merge temperature, CO2, and disaster data on year"""
        if any(x is None for x in [self.temp_data, self.co2_data, self.disaster_data]):
            raise ValueError("Must load temperature, CO2, and disaster data before merging")
        
        try:
            print("\nPre-merge data ranges:")
            print(f"Temperature years: {self.temp_data['Year'].min()} to {self.temp_data['Year'].max()}")
            print(f"CO2 years: {self.co2_data['Year'].min()} to {self.co2_data['Year'].max()}")
            print(f"Disaster years: {self.disaster_data['Year'].min()} to {self.disaster_data['Year'].max()}")
            
            # First merge temp and CO2 data
            merged = pd.merge(
                self.temp_data, 
                self.co2_data,
                on='Year',
                how='inner'
            )
            
            # Then merge with disaster data
            final_merged = pd.merge(
                merged,
                self.disaster_data,
                on='Year',
                how='inner'
            )
            
            # Sort by year
            final_merged = final_merged.sort_values('Year')
            
            if final_merged.empty:
                raise ValueError("No overlapping years found between datasets")
            
            print(f"\nMerged dataset:")
            print(f"Number of records: {len(final_merged)}")
            print(f"Year range: {final_merged['Year'].min()} to {final_merged['Year'].max()}")
            print("\nFirst few records:")
            print(final_merged.head())
            
            self.merged_data = final_merged
            return self.merged_data
            
        except Exception as e:
            print(f"Error merging datasets: {str(e)}")
            raise
    
    def calculate_decade_averages(self):
        """Calculate decadal averages for both temperature and CO2"""
        if self.merged_data is None or self.merged_data.empty:
            raise ValueError("Must have valid merged data before calculating decadal averages")
        
        self.merged_data['Decade'] = (self.merged_data['Year'] // 10) * 10
        
        decade_avgs = self.merged_data.groupby('Decade').agg({
            'Temperature_Anomaly': 'mean',
            'CO2_Level': 'mean'
        }).reset_index()
        
        return decade_avgs
    
    def calculate_trends(self):
        """Calculate year-over-year trends"""
        if self.merged_data is None or self.merged_data.empty:
            raise ValueError("Must have valid merged data before calculating trends")
        
        df = self.merged_data.copy()
        df['Temp_Change'] = df['Temperature_Anomaly'].diff()
        df['CO2_Change'] = df['CO2_Level'].diff()
        
        return df
    
    def get_summary_stats(self, country=None):
        """
        Generate summary statistics including disaster correlations
        
        Parameters:
        country (str): Country name for the report header, if applicable
        """
        if self.merged_data is None or self.merged_data.empty:
            raise ValueError("Must have valid merged data before calculating summary statistics")
        
        stats = {
            'country': country if country else 'Global',
            'temp_correlation': np.corrcoef(
                self.merged_data['Temperature_Anomaly'],
                self.merged_data['CO2_Level']
            )[0,1],
            'disaster_temp_correlation': np.corrcoef(
                self.merged_data['Temperature_Anomaly'],
                self.merged_data['Disasters']
            )[0,1],
            'disaster_co2_correlation': np.corrcoef(
                self.merged_data['CO2_Level'],
                self.merged_data['Disasters']
            )[0,1],
            'temp_min_year': int(self.merged_data.loc[
                self.merged_data['Temperature_Anomaly'].idxmin(),
                'Year'
            ]),
            'temp_max_year': int(self.merged_data.loc[
                self.merged_data['Temperature_Anomaly'].idxmax(),
                'Year'
            ]),
            'co2_min_year': int(self.merged_data.loc[
                self.merged_data['CO2_Level'].idxmin(),
                'Year'
            ]),
            'co2_max_year': int(self.merged_data.loc[
                self.merged_data['CO2_Level'].idxmax(),
                'Year'
            ]),
            'disasters_min_year': int(self.merged_data.loc[
                self.merged_data['Disasters'].idxmin(),
                'Year'
            ]),
            'disasters_max_year': int(self.merged_data.loc[
                self.merged_data['Disasters'].idxmax(),
                'Year'
            ]),
            'avg_disasters_per_year': self.merged_data['Disasters'].mean(),
            'total_disasters': self.merged_data['Disasters'].sum()
        }
        
        return stats
