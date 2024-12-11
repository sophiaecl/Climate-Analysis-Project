import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional, Tuple, Dict

class ClimatePredictor:
    """Class to handle predictions of climate variables"""
    
    def __init__(self):
        self.temp_model = None
        self.co2_model = None
        self.disaster_model = None
        self.predictions = {}
        
    def train_models(self, data: pd.DataFrame, forecast_years: int = 30) -> Dict:
        """
        Train prediction models for temperature, CO2, and disasters
        
        Parameters:
        data (pd.DataFrame): Historical data
        forecast_years (int): Number of years to forecast
        
        Returns:
        Dict: Dictionary containing predictions
        """
        last_year = data['Year'].max()
        future_years = np.arange(last_year + 1, last_year + forecast_years + 1)
        
        # Reshape data for scikit-learn
        X = data['Year'].values.reshape(-1, 1)
        
        # Train temperature model
        y_temp = data['Temperature_Anomaly'].values
        self.temp_model = LinearRegression()
        self.temp_model.fit(X, y_temp)
        temp_predictions = self.temp_model.predict(future_years.reshape(-1, 1))
        
        # Train CO2 model (exponential growth model)
        y_co2 = np.log(data['CO2_Level'].values)  # Log transform for exponential growth
        self.co2_model = LinearRegression()
        self.co2_model.fit(X, y_co2)
        co2_predictions = np.exp(self.co2_model.predict(future_years.reshape(-1, 1)))
        
        # Train disaster model
        y_disasters = data['Disasters'].values
        self.disaster_model = LinearRegression()
        self.disaster_model.fit(X, y_disasters)
        disaster_predictions = self.disaster_model.predict(future_years.reshape(-1, 1))
        disaster_predictions = np.maximum(disaster_predictions, 0)  # Ensure non-negative
        
        # Store predictions
        self.predictions = {
            'years': future_years,
            'temperature': temp_predictions,
            'co2': co2_predictions,
            'disasters': disaster_predictions
        }
        
        return self.predictions
    
    def plot_predictions(self, 
                        historical_data: pd.DataFrame, 
                        country: Optional[str] = None,
                        disaster_type: str = 'TOTAL',
                        output_dir: Optional[str] = None):
        """Plot historical data and predictions"""
        if not self.predictions:
            raise ValueError("Must train models before plotting predictions")
        
        region = country if country else 'Global'
        
        # Create figure with three subplots
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 15))
        
        # Temperature predictions
        ax1.scatter(historical_data['Year'], historical_data['Temperature_Anomaly'], alpha=0.5, label='Historical')
        ax1.plot(self.predictions['years'], self.predictions['temperature'], color='red', label='Predicted')
        ax1.set_title(f'Temperature Anomaly Projection - {region}')
        ax1.set_xlabel('Year')
        ax1.set_ylabel('Temperature Anomaly (°C)')
        ax1.legend()
        ax1.grid(True)
        
        # Add confidence intervals for temperature
        X_pred = self.predictions['years'].reshape(-1, 1)
        y_pred = self.predictions['temperature']
        mse = mean_squared_error(historical_data['Temperature_Anomaly'], self.temp_model.predict(historical_data['Year'].values.reshape(-1, 1)))
        std_dev = np.sqrt(mse)
        ax1.fill_between(self.predictions['years'],
                        y_pred - 2*std_dev,
                        y_pred + 2*std_dev,
                        color='red', alpha=0.1,
                        label='95% Confidence Interval')
        
        # CO2 predictions
        ax2.scatter(historical_data['Year'], historical_data['CO2_Level'], alpha=0.5, label='Historical')
        ax2.plot(self.predictions['years'], self.predictions['co2'], color='green', label='Predicted')
        ax2.set_title(f'CO2 Level Projection - {region}')
        ax2.set_xlabel('Year')
        ax2.set_ylabel('CO2 Level (ppm)')
        ax2.legend()
        ax2.grid(True)
        
        # Disaster predictions
        ax3.scatter(historical_data['Year'], historical_data['Disasters'], alpha=0.5, label='Historical')
        ax3.plot(self.predictions['years'], self.predictions['disasters'], color='purple', label='Predicted')
        ax3.set_title(f'{disaster_type} Disasters Projection - {region}')
        ax3.set_xlabel('Year')
        ax3.set_ylabel('Number of Disasters')
        ax3.legend()
        ax3.grid(True)
        
        plt.tight_layout()
        
        if output_dir:
            region_str = region.lower().replace(' ', '_')
            disaster_str = disaster_type.lower().replace(' ', '_')
            filename = f'predictions_{region_str}_{disaster_str}.png'
            plt.savefig(os.path.join(output_dir, filename))
            plt.close()
        else:
            plt.show()
    
    def get_prediction_summary(self, 
                             historical_data: pd.DataFrame, 
                             target_years: list = [2030, 2040, 2050]) -> Dict:
        """Generate summary of predictions for specific target years"""
        if not self.predictions:
            raise ValueError("Must train models before getting prediction summary")
        
        summary = {
            'model_metrics': {
                'temperature_r2': r2_score(
                    historical_data['Temperature_Anomaly'],
                    self.temp_model.predict(historical_data['Year'].values.reshape(-1, 1))
                ),
                'co2_r2': r2_score(
                    np.log(historical_data['CO2_Level']),
                    self.co2_model.predict(historical_data['Year'].values.reshape(-1, 1))
                ),
                'disasters_r2': r2_score(
                    historical_data['Disasters'],
                    self.disaster_model.predict(historical_data['Year'].values.reshape(-1, 1))
                )
            },
            'predictions_by_year': {}
        }
        
        # Get predictions for specified target years
        for year in target_years:
            if year in self.predictions['years']:
                idx = np.where(self.predictions['years'] == year)[0][0]
                summary['predictions_by_year'][year] = {
                    'temperature': self.predictions['temperature'][idx],
                    'co2': self.predictions['co2'][idx],
                    'disasters': self.predictions['disasters'][idx]
                }
        
        return summary