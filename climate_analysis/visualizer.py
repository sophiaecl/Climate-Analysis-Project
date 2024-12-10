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
