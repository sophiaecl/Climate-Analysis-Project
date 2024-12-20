import os
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
        self.disaster_types = [
            'Drought', 'Extreme temperature', 'Flood', 'Landslide', 'Storm',
            'Wildfire', 'TOTAL'
        ]

    def load_disaster_data(self, filepath, country=None, disaster_type='TOTAL'):
        """
        Load and process climate disaster data for a specific country or aggregate global data
        
        Parameters:
        filepath (str): Path to the disaster data CSV
        country (str): Country name to filter for. If None, aggregates global data
        """
        try:
            # Read CSV
            df = pd.read_csv(filepath)
            
            # Store available countries for reference
            self.available_countries = sorted(df['Country'].unique().tolist())

            # Validate disaster type
            if disaster_type not in self.disaster_types:
                raise ValueError(f"Invalid disaster type. Available types: {', '.join(self.disaster_types)}")
            
            # Filter for disaster type
            disaster_indicator = f"Climate related disasters frequency, Number of Disasters: {disaster_type}"
            selected_data = df[df['Indicator'] == disaster_indicator]

            if selected_data.empty:
                print(f"\nWarning: No disaster data found for {disaster_type}")
                years = list(range(1980, 2024))
                disaster_data = pd.DataFrame({
                    'Year': years,
                    'Disasters': [0] * len(years),
                    'Disaster_Type': [disaster_type] * len(years)
                })
            else:
                # Melt the data to create Year and Disasters columns
                years = [str(year) for year in range(1980, 2024)]
                melted_data = pd.melt(
                    selected_data,
                    id_vars=['Country', 'Indicator'],
                    value_vars=years,
                    var_name='Year',
                    value_name='Disasters'
                )
                melted_data['Year'] = melted_data['Year'].astype(int)
                melted_data['Disasters'] = melted_data['Disasters'].fillna(0)

                # Aggregate data globally if no specific country is provided
                if country is None or country.lower() == 'global':
                    print("\nAggregating global disaster data")
                    disaster_data = melted_data.groupby('Year', as_index=False).agg({'Disasters': 'sum'})
                    disaster_data['Disaster_Type'] = disaster_type
                else:
                    # Filter for the specified country
                    if country not in self.available_countries:
                        raise ValueError(f"Country '{country}' not found in dataset. Use get_available_countries() to see options.")
                    disaster_data = melted_data[melted_data['Country'] == country][['Year', 'Disasters']]
                    disaster_data['Disaster_Type'] = disaster_type

            print(f"Processed {len(disaster_data)} disaster records")
            print(f"Year range: {disaster_data['Year'].min()} to {disaster_data['Year'].max()}")
            print(f"Years with disasters: {len(disaster_data[disaster_data['Disasters'] > 0])}")
            print(f"Years with no disasters: {len(disaster_data[disaster_data['Disasters'] == 0])}")
            
            self.disaster_data = disaster_data
            return self.disaster_data

        except Exception as e:
            print(f"Error loading disaster data: {str(e)}")
            raise

    def get_disaster_types(self):
        """Get list of available disaster types"""
        return self.disaster_types

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
    
    def get_summary_stats(self, country=None, disaster_type='TOTAL'):
        """Generate summary statistics including disaster correlations"""
        if self.merged_data is None or self.merged_data.empty:
            raise ValueError("Must have valid merged data before calculating summary statistics")
        
        stats = {
            'country': country if country else 'Global',
            'disaster_type': disaster_type,
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
            'total_disasters': self.merged_data['Disasters'].sum(),
            'years_with_disasters': len(self.merged_data[self.merged_data['Disasters'] > 0])
        }
        
        return stats

    def save_processed_data(self, data_dir, country=None, disaster_type='TOTAL'):
        """
        Save processed datasets to CSV files
        
        Parameters:
        data_dir (str): Base directory for processed data
        country (str): Country name for filename
        disaster_type (str): Type of disaster for filename
        """
        try:
            # Create processed data directory if it doesn't exist
            processed_dir = os.path.join(data_dir, 'processed')
            os.makedirs(processed_dir, exist_ok=True)
            
            # Generate base filename
            region = country.lower().replace(' ', '_') if country else 'global'
            disaster = disaster_type.lower().replace(' ', '_')
            base_filename = f"{region}_{disaster}"
            
            # Save temperature data
            if self.temp_data is not None:
                temp_file = os.path.join(processed_dir, f'temperature_{base_filename}.csv')
                self.temp_data.to_csv(temp_file, index=False)
                print(f"Saved processed temperature data to: {temp_file}")
            
            # Save CO2 data
            if self.co2_data is not None:
                co2_file = os.path.join(processed_dir, f'co2_{base_filename}.csv')
                self.co2_data.to_csv(co2_file, index=False)
                print(f"Saved processed CO2 data to: {co2_file}")
            
            # Save disaster data
            if self.disaster_data is not None:
                disaster_file = os.path.join(processed_dir, f'disasters_{base_filename}.csv')
                self.disaster_data.to_csv(disaster_file, index=False)
                print(f"Saved processed disaster data to: {disaster_file}")
            
            # Save merged data
            if self.merged_data is not None:
                merged_file = os.path.join(processed_dir, f'merged_{base_filename}.csv')
                self.merged_data.to_csv(merged_file, index=False)
                print(f"Saved merged dataset to: {merged_file}")
                
        except Exception as e:
            print(f"Error saving processed data: {str(e)}")
            raise
