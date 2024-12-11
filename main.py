# main.py

import argparse
import os
from climate_analysis.data_processor import ClimateDataProcessor
from climate_analysis.visualizer import ClimateVisualizer
import pandas as pd

def get_default_paths():
    """Get default paths for data files and output directory"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    return {
        'temp_file': os.path.join(base_dir, 'data', 'raw', 'annual.csv'),
        'co2_file': os.path.join(base_dir, 'data', 'raw', 'co2-mm-gl.csv'),
        'disaster_file': os.path.join(base_dir, 'data', 'raw', 'climate-related-disasters.csv'),
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
        help='Path to temperature data CSV'
    )
    parser.add_argument(
        '--co2-file',
        default=default_paths['co2_file'],
        help='Path to CO2 data CSV'
    )
    parser.add_argument(
        '--disaster-file',
        default=default_paths['disaster_file'],
        help='Path to disaster data CSV'
    )
    parser.add_argument(
        '--output-dir',
        default=default_paths['output_dir'],
        help='Directory for output files'
    )
    parser.add_argument(
        '--country',
        default=None,
        help='Country to analyze (default: global data)'
    )
    parser.add_argument(
        '--list-countries',
        action='store_true',
        help='List available countries and exit'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Print debug information'
    )
    
    args = parser.parse_args()
    
    # Initialize processor and load disaster data to get country list
    data_processor = ClimateDataProcessor()
    print(f"Loading temperature data from {args.temp_file}...")
    temp_data = data_processor.load_temperature_data(args.temp_file)
    
    if args.debug:
        print("\nDEBUG: Temperature Data Sample:")
        print(temp_data.head())
        print("\nTemperature Data Shape:", temp_data.shape)
        print("\nTemperature Years:", sorted(temp_data['Year'].unique()))
    
    print(f"\nLoading CO2 data from {args.co2_file}...")
    co2_data = data_processor.load_co2_data(args.co2_file)
    
    if args.debug:
        print("\nDEBUG: CO2 Data Sample:")
        print(co2_data.head())
        print("\nCO2 Data Shape:", co2_data.shape)
        print("\nCO2 Years:", sorted(co2_data['Year'].unique()))
    
    print(f"\nLoading disaster data from {args.disaster_file}...")
    disaster_data = data_processor.load_disaster_data(args.disaster_file, country=args.country)
    
    if args.debug:
        print("\nDEBUG: Disaster Data Sample:")
        print(disaster_data.head())
        print("\nDisaster Data Shape:", disaster_data.shape)
        print("\nDisaster Years:", sorted(disaster_data['Year'].unique()))
        
    data_processor.load_disaster_data(args.disaster_file)
    
    # If --list-countries flag is used, print countries and exit
    if args.list_countries:
        print("\nAvailable countries for analysis:")
        for country in data_processor.get_available_countries():
            print(f"  - {country}")
        return
    
    # Verify input files exist
    for file_path in [args.temp_file, args.co2_file, args.disaster_file]:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Input file not found: {file_path}")
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Initialize visualizer
    visualizer = ClimateVisualizer()
    
    # Load and process data
    print(f"Loading temperature data from {args.temp_file}...")
    data_processor.load_temperature_data(args.temp_file)
    
    print(f"\nLoading CO2 data from {args.co2_file}...")
    data_processor.load_co2_data(args.co2_file)
    
    print(f"\nLoading disaster data from {args.disaster_file}...")
    data_processor.load_disaster_data(args.disaster_file, country=args.country)
    
    print("\nMerging datasets...")
    merged_data = data_processor.merge_datasets()
    
    print("\nCalculating trends and statistics...")
    summary_stats = data_processor.get_summary_stats(country=args.country)
    
    # Generate visualizations with country-specific names
    region = args.country if args.country else 'global'
    print(f"\nGenerating visualizations for {region} data in {args.output_dir}...")
    
    visualizer.plot_temperature_trend(
        merged_data,
        os.path.join(args.output_dir, f'temperature_trend_{region}.png')
    )
    
    visualizer.plot_co2_trend(
        merged_data,
        os.path.join(args.output_dir, f'co2_trend_{region}.png')
    )
    
    visualizer.plot_disasters_trend(
        merged_data,
        country=args.country,
        output_path=os.path.join(args.output_dir, f'disasters_trend_{region}.png')
    )
    
    visualizer.plot_triple_correlation(
        merged_data,
        country=args.country,
        output_path=os.path.join(args.output_dir, f'correlations_{region}.png')
    )
    
    # Print summary statistics
    print(f"\nSummary Statistics for {summary_stats['country']}:")
    print(f"Temperature-CO2 Correlation: {summary_stats['temp_correlation']:.3f}")
    print(f"Temperature-Disasters Correlation: {summary_stats['disaster_temp_correlation']:.3f}")
    print(f"CO2-Disasters Correlation: {summary_stats['disaster_co2_correlation']:.3f}")
    print(f"Warmest Year: {summary_stats['temp_max_year']}")
    print(f"Coolest Year: {summary_stats['temp_min_year']}")
    print(f"Highest CO2 Year: {summary_stats['co2_max_year']}")
    print(f"Lowest CO2 Year: {summary_stats['co2_min_year']}")
    print(f"Most Disasters Year: {summary_stats['disasters_max_year']}")
    print(f"Fewest Disasters Year: {summary_stats['disasters_min_year']}")
    print(f"Average Disasters per Year: {summary_stats['avg_disasters_per_year']:.1f}")
    print(f"Total Disasters: {summary_stats['total_disasters']:.0f}")

if __name__ == "__main__":
    main()