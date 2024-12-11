# main.py

import argparse
import os
from climate_analysis.data_processor import ClimateDataProcessor
from climate_analysis.visualizer import ClimateVisualizer

def get_default_paths():
    """Get default paths for data files and output directory"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    return {
        'temp_file': os.path.join(base_dir, 'data', 'raw', 'annual.csv'),
        'co2_file': os.path.join(base_dir, 'data', 'raw', 'co2-mm-gl.csv'),
        'output_dir': os.path.join(base_dir, 'output')
    }

def main():
    # Get default paths
    default_paths = get_default_paths()
    
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Climate Change Data Analysis')
    parser.add_argument(
        '--temp-file',
        default=default_paths['temp_file'],
        help='Path to temperature data CSV (default: data/raw/annual.csv)'
    )
    parser.add_argument(
        '--co2-file',
        default=default_paths['co2_file'],
        help='Path to CO2 data CSV (default: data/raw/co2-mm-gl.csv)'
    )
    parser.add_argument(
        '--output-dir',
        default=default_paths['output_dir'],
        help='Directory for output files (default: output/)'
    )
    
    args = parser.parse_args()
    
    # Verify input files exist
    if not os.path.exists(args.temp_file):
        raise FileNotFoundError(f"Temperature data file not found: {args.temp_file}")
    if not os.path.exists(args.co2_file):
        raise FileNotFoundError(f"CO2 data file not found: {args.co2_file}")
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Initialize processors
    data_processor = ClimateDataProcessor()
    visualizer = ClimateVisualizer()
    
    # Load and process data
    print(f"Loading temperature data from {args.temp_file}...")
    data_processor.load_temperature_data(args.temp_file)
    
    # Add validation print for temperature data
    print("\nTemperature data preview:")
    print(data_processor.temp_data.head())
    print("\nTemperature data shape:", data_processor.temp_data.shape)
    
    print(f"\nLoading CO2 data from {args.co2_file}...")
    data_processor.load_co2_data(args.co2_file)
    
    # Add validation print for CO2 data
    print("\nCO2 data preview:")
    print(data_processor.co2_data.head())
    print("\nCO2 data shape:", data_processor.co2_data.shape)
    
    print("\nMerging datasets...")
    merged_data = data_processor.merge_datasets()
    
    # Add validation print for merged data
    print("\nMerged data preview:")
    print(merged_data.head())
    print("\nMerged data shape:", merged_data.shape)
    
    print("\nCalculating trends and statistics...")
    trend_data = data_processor.calculate_trends()
    decade_averages = data_processor.calculate_decade_averages()
    summary_stats = data_processor.get_summary_stats()
    
    # Generate visualizations
    print(f"\nGenerating visualizations in {args.output_dir}...")
    
    visualizer.plot_temperature_trend(
        merged_data,
        os.path.join(args.output_dir, 'temperature_trend.png')
    )
    
    visualizer.plot_co2_trend(
        merged_data,
        os.path.join(args.output_dir, 'co2_trend.png')
    )
    
    visualizer.plot_correlation(
        merged_data,
        os.path.join(args.output_dir, 'correlation.png')
    )
    
    visualizer.plot_decade_comparison(
        decade_averages,
        os.path.join(args.output_dir, 'decade_comparison.png')
    )
    
    # Print summary statistics
    print("\nSummary Statistics:")
    print(f"Temperature-CO2 Correlation: {summary_stats['temp_correlation']:.3f}")
    print(f"Warmest Year: {summary_stats['temp_max_year']}")
    print(f"Coolest Year: {summary_stats['temp_min_year']}")
    print(f"Highest CO2 Year: {summary_stats['co2_max_year']}")
    print(f"Lowest CO2 Year: {summary_stats['co2_min_year']}")

if __name__ == "__main__":
    main()
