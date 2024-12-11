# climate_analysis/visualizer.py

import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional

class ClimateVisualizer:
    """Class to handle all visualization tasks for climate data"""
    
    def __init__(self):
        # Configure styling
        sns.set_theme()  # This is more reliable than plt.style.use('seaborn')
        self.default_figsize = (12, 6)
        self.default_dpi = 100

    def plot_disasters_trend(self, data, country=None, output_path: Optional[str] = None):
        """
        Plot climate-related disasters trend over time
        
        Parameters:
        data (pandas.DataFrame): Data to plot
        country (str): Country name for the title, if applicable
        output_path (str): Path to save the plot
        """
        plt.figure(figsize=self.default_figsize, dpi=self.default_dpi)
        
        sns.regplot(
            data=data,
            x='Year',
            y='Disasters',
            scatter_kws={'alpha':0.5},
            line_kws={'color': 'purple'}
        )
        
        title = f"Climate-Related Disasters Trend - {country if country else 'Global'}"
        plt.title(title, pad=20)
        plt.xlabel('Year')
        plt.ylabel('Number of Disasters')
        
        if output_path:
            plt.savefig(output_path, bbox_inches='tight')
        plt.close()

    def plot_triple_correlation(self, data, country=None, output_path: Optional[str] = None):
        """
        Plot correlation between temperature, CO2, and disasters
        
        Parameters:
        data (pandas.DataFrame): Data to plot
        country (str): Country name for the title, if applicable
        output_path (str): Path to save the plot
        """
        fig, axes = plt.subplots(1, 3, figsize=(18, 6), dpi=self.default_dpi)
        region = country if country else 'Global'
        
        # Temperature vs CO2
        sns.scatterplot(
            data=data,
            x='CO2_Level',
            y='Temperature_Anomaly',
            ax=axes[0],
            alpha=0.6
        )
        sns.regplot(
            data=data,
            x='CO2_Level',
            y='Temperature_Anomaly',
            ax=axes[0],
            scatter=False,
            color='red'
        )
        axes[0].set_title(f'Temperature vs CO2 - {region}')
        axes[0].set_xlabel('CO2 Level (ppm)')
        axes[0].set_ylabel('Temperature Anomaly (°C)')
        
        # Temperature vs Disasters
        sns.scatterplot(
            data=data,
            x='Temperature_Anomaly',
            y='Disasters',
            ax=axes[1],
            alpha=0.6
        )
        sns.regplot(
            data=data,
            x='Temperature_Anomaly',
            y='Disasters',
            ax=axes[1],
            scatter=False,
            color='purple'
        )
        axes[1].set_title(f'Disasters vs Temperature - {region}')
        axes[1].set_xlabel('Temperature Anomaly (°C)')
        axes[1].set_ylabel('Number of Disasters')
        
        # CO2 vs Disasters
        sns.scatterplot(
            data=data,
            x='CO2_Level',
            y='Disasters',
            ax=axes[2],
            alpha=0.6
        )
        sns.regplot(
            data=data,
            x='CO2_Level',
            y='Disasters',
            ax=axes[2],
            scatter=False,
            color='green'
        )
        axes[2].set_title(f'Disasters vs CO2 - {region}')
        axes[2].set_xlabel('CO2 Level (ppm)')
        axes[2].set_ylabel('Number of Disasters')
        
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, bbox_inches='tight')
        plt.close()
        
    def plot_temperature_trend(self, data, output_path: Optional[str] = None):
        """Plot temperature anomaly trend over time"""
        plt.figure(figsize=self.default_figsize, dpi=self.default_dpi)
        
        sns.regplot(
            data=data,
            x='Year',
            y='Temperature_Anomaly',
            scatter_kws={'alpha':0.5},
            line_kws={'color': 'red'}
        )
        
        plt.title('Global Temperature Anomaly Trend', pad=20)
        plt.xlabel('Year')
        plt.ylabel('Temperature Anomaly (°C)')
        
        if output_path:
            plt.savefig(output_path, bbox_inches='tight')
        plt.close()
    
    def plot_co2_trend(self, data, output_path: Optional[str] = None):
        """Plot CO2 concentration trend over time"""
        plt.figure(figsize=self.default_figsize, dpi=self.default_dpi)
        
        sns.regplot(
            data=data,
            x='Year',
            y='CO2_Level',
            scatter_kws={'alpha':0.5},
            line_kws={'color': 'green'}
        )
        
        plt.title('Atmospheric CO2 Concentration Trend', pad=20)
        plt.xlabel('Year')
        plt.ylabel('CO2 Level (ppm)')
        
        if output_path:
            plt.savefig(output_path, bbox_inches='tight')
        plt.close()
    
    def plot_correlation(self, data, output_path: Optional[str] = None):
        """Plot correlation between temperature and CO2"""
        plt.figure(figsize=self.default_figsize, dpi=self.default_dpi)
        
        sns.scatterplot(
            data=data,
            x='CO2_Level',
            y='Temperature_Anomaly',
            alpha=0.6
        )
        
        sns.regplot(
            data=data,
            x='CO2_Level',
            y='Temperature_Anomaly',
            scatter=False,
            color='red'
        )
        
        plt.title('Temperature Anomaly vs CO2 Concentration', pad=20)
        plt.xlabel('CO2 Level (ppm)')
        plt.ylabel('Temperature Anomaly (°C)')
        
        if output_path:
            plt.savefig(output_path, bbox_inches='tight')
        plt.close()
    
    def plot_decade_comparison(self, decade_data, output_path: Optional[str] = None):
        """Plot decadal averages comparison"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Temperature subplot
        sns.barplot(
            data=decade_data,
            x='Decade',
            y='Temperature_Anomaly',
            ax=ax1,
            color='coral'
        )
        ax1.set_title('Decadal Average Temperature Anomalies')
        ax1.set_xlabel('Decade')
        ax1.set_ylabel('Temperature Anomaly (°C)')
        ax1.tick_params(axis='x', rotation=45)
        
        # CO2 subplot
        sns.barplot(
            data=decade_data,
            x='Decade',
            y='CO2_Level',
            ax=ax2,
            color='lightgreen'
        )
        ax2.set_title('Decadal Average CO2 Levels')
        ax2.set_xlabel('Decade')
        ax2.set_ylabel('CO2 Level (ppm)')
        ax2.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, bbox_inches='tight')
        plt.close()
