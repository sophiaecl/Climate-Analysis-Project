# Climate Change Analysis: Temperature, CO2, and Natural Disasters

## Overview
This Python data analysis project examines the relationships between global temperature anomalies, atmospheric CO2 concentrations, and climate-related natural disasters from 1980 to 2024. Through processing and visualization of climate data, the project demonstrates long-term trends and correlations between temperature changes, CO2 levels, and the frequency of various types of natural disasters.

## Features
- Processing and analysis of temperature, CO2, and natural disaster data
- Global and country-specific analysis options
- Multiple disaster type analysis (floods, droughts, storms, etc.)
- Time series analysis of climate trends
- Visualization of:
  - Temperature anomalies and CO2 concentration changes
  - Natural disaster frequency trends
  - Stacked bar charts of disaster type distribution
  - Correlation analysis between variables
- Statistical analysis and predictions
- Calculation of decadal averages and year-over-year changes

## Data Sources
The project utilizes three primary data sources:
- Global temperature anomalies (1850-2024)
  [Global Temperature Time Series](https://github.com/datasets/global-temp)
- Atmospheric CO2 concentrations from Mauna Loa Observatory (1958-2024)
  [CO2 PPM - Trends in Atmospheric Carbon Dioxide](https://github.com/datasets/co2-ppm)
- Climate-related natural disasters (1980-2024)
  [Natural Disasters Dataset](https://climatedata.imf.org/datasets/b13b69ee0dde43a99c811f592af4e821/explore)

## Technologies Used
- Python 3.x
- Pandas for data processing
- Matplotlib and Seaborn for visualization
- NumPy for numerical analysis
- Scikit-learn for predictive modeling

## Project Structure
```
climate_analysis/
├── data/
│   ├── raw/                    # Original data files
│   │   ├── annual.csv          # Temperature data
│   │   ├── co2-mm-gl.csv       # CO2 measurements
│   │   └── climate-related-disasters.csv  # Disaster data
│   └── processed/             # Processed data outputs
├── climate_analysis/          # Source code
│   ├── __init__.py
│   ├── data_processor.py     # Data processing module
│   ├── visualizer.py         # Visualization module
│   └── predictor.py          # Prediction modeling module
├── output/                   # Visualization outputs
├── main.py                   # Main execution script
├── requirements.txt          # Project dependencies
└── README.md                # Project documentation
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/sophiaecl/Climate-Analysis-Project.git
cd Climate-Analysis-Project
```

2. Create and activate a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Analysis
Run the main analysis script for global data:
```bash
python main.py
```

### Country-Specific Analysis
Analyze data for a specific country:
```bash
python main.py --country "Spain"
```

### Specific Disaster Type Analysis
Analyze a specific type of natural disaster:
```bash
python main.py --disaster-type "Flood"
```

### Specific Country and Disaster Type Analysis
Analyze a specific type of natural disaster:
```bash
python main.py --country "Spain" --disaster-type "Flood"
```

### List Available Options
View available countries:
```bash
python main.py --list-countries
```

View available disaster types:
```bash
python main.py --list-disasters
```

### Output
- Processed data files will be saved in the `data/processed/` directory
- Visualizations will be saved in the `output/` directory, including:
  - Temperature trends
  - CO2 concentration trends
  - Disaster frequency trends
  - Correlation analyses
  - Disaster type breakdown charts
  - Prediction visualizations

## Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/awesome-feature`)
3. Commit your changes (`git commit -am 'Add awesome feature'`)
4. Push to the branch (`git push origin feature/awesome-feature`)
5. Create a Pull Request

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements
- This project was developed to demonstrate comprehensive climate data analysis using Python
- Special thanks to the maintainers of the global temperature, CO2, and natural disaster datasets
- Developed as part of the Programming with Python course to showcase data analysis, visualization, and predictive modeling skills

## Contact
For questions and feedback, please open an issue in the GitHub repository.
