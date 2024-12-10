# climate_analysis/data_processor.py

import pandas as pd
import numpy as np

class ClimateDataProcessor:
    """Class to handle loading and processing of climate data"""
    
    def __init__(self):
        self.temp_data = None
        self.co2_data = None
        self.merged_data = None
    
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
            
            # Create clean dataset
            temp_data = df[['Year', 'Mean']].copy()
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
            
            # Extract year by truncating the decimal date
            df['Year'] = df['Date'].astype(float).astype(int)
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
        """Merge temperature and CO2 data on year"""
        if self.temp_data is None or self.co2_data is None:
            raise ValueError("Must load both temperature and CO2 data before merging")
        
        try:
            print("\nPre-merge data ranges:")
            print(f"Temperature years: {self.temp_data['Year'].min()} to {self.temp_data['Year'].max()}")
            print(f"CO2 years: {self.co2_data['Year'].min()} to {self.co2_data['Year'].max()}")
            
            # Merge datasets
            merged = pd.merge(
                self.temp_data, 
                self.co2_data,
                on='Year',
                how='inner'
            )
            
            # Sort by year
            merged = merged.sort_values('Year')
            
            if merged.empty:
                raise ValueError("No overlapping years found between temperature and CO2 data")
            
            print(f"\nMerged dataset:")
            print(f"Number of records: {len(merged)}")
            print(f"Year range: {merged['Year'].min()} to {merged['Year'].max()}")
            print("\nFirst few records:")
            print(merged.head())
            
            self.merged_data = merged
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
    
    def get_summary_stats(self):
        """Generate summary statistics for the data"""
        if self.merged_data is None or self.merged_data.empty:
            raise ValueError("Must have valid merged data before calculating summary statistics")
        
        stats = {
            'temp_correlation': np.corrcoef(
                self.merged_data['Temperature_Anomaly'],
                self.merged_data['CO2_Level']
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
            ])
        }
        
        return stats
