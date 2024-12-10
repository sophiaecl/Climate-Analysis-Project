# Climate Change Analysis: Temperature Anomalies and CO2 Levels

## Overview
This Python data analysis project examines the relationship between global temperature anomalies and atmospheric CO2 concentrations from 1850 to 2024. Through processing and visualization of climate data, the project demonstrates long-term trends and correlations between temperature changes and CO2 levels.

## Features
- Data processing of historical temperature and CO2 measurements
- Time series analysis of climate trends
- Visualization of temperature anomalies and CO2 concentration changes
- Calculation of decadal averages and year-over-year changes
- Statistical analysis of the relationship between temperature and CO2 levels

## Data Sources
The project utilizes two primary data sources:
- Global temperature anomalies (1850-2024)
- Atmospheric CO2 concentrations from Mauna Loa Observatory (1958-2024)

## Technologies Used
- Python 3.x
- Pandas for data processing
- Matplotlib and Seaborn for visualization
- NumPy for numerical analysis

## Project Structure
```
climate_analysis/
├── data/
│   ├── raw/                    # Original data files
│   │   ├── annual.csv         # Temperature data
│   │   └── co2-mm-mlo.csv    # CO2 measurements
│   └── processed/             # Processed data outputs
├── climate_analysis/          # Source code
│   ├── __init__.py
│   ├── data_processor.py     # Data processing module
│   └── visualizer.py         # Visualization module
├── main.py                   # Main execution script
├── requirements.txt          # Project dependencies
└── README.md                # Project documentation
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/sophiaecl/climate-analysis.git
cd climate-analysis
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

1. Place your raw data files in the `data/raw/` directory
2. Run the main analysis script:
```bash
python main.py
```

3. Find the processed results in the `data/processed/` directory

## Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/awesome-feature`)
3. Commit your changes (`git commit -am 'Add awesome feature'`)
4. Push to the branch (`git push origin feature/awesome-feature`)
5. Create a Pull Request

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements
This project was developed as part of the Programming with Python course to demonstrate proficiency in data analysis, object-oriented programming, and scientific computing with Python.

## Contact
For questions and feedback, please open an issue in the GitHub repository.
