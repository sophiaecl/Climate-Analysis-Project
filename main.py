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
        'output_dir': os.path.join(base_dir, 'output'),
        'data_dir': os.path.join(base_dir, 'data')
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
        '--data-dir',
        default=default_paths['data_dir'],
        help='Directory for data files'
    )
    parser.add_argument(
        '--country',
        default=None,
        help='Country to analyze (default: global data)'
    )
    parser.add_argument(
        '--disaster-type',
        default='TOTAL',
        help='Type of disaster to analyze (default: TOTAL)'
    )
    parser.add_argument(
        '--list-countries',
        action='store_true',
        help='List available countries and exit'
    )
    parser.add_argument(
        '--list-disasters',
        action='store_true',
        help='List available disaster types and exit'
    )
    
    args = parser.parse_args()
    
    # Initialize processor
    data_processor = ClimateDataProcessor()
    
    # If --list-countries flag is used, print countries and exit
    if args.list_countries:
        # Need to load disaster data first to get country list
        data_processor.load_disaster_data(args.disaster_file)
        print("\nAvailable countries for analysis:")
        for country in data_processor.get_available_countries():
            print(f"  - {country}")
        return
    
    # If --list-disasters flag is used, print disaster types and exit
    if args.list_disasters:
        print("\nAvailable disaster types for analysis:")
        for disaster_type in data_processor.get_disaster_types():
            print(f"  - {disaster_type}")
        return
    
    os.makedirs(args.output_dir, exist_ok=True)

    # Load and process data
    print(f"Loading temperature data from {args.temp_file}...")
    data_processor.load_temperature_data(args.temp_file)
    
    print(f"\nLoading CO2 data from {args.co2_file}...")
    data_processor.load_co2_data(args.co2_file)
    
    print(f"\nLoading disaster data from {args.disaster_file}...")
    data_processor.load_disaster_data(
        args.disaster_file, 
        country=args.country,
        disaster_type=args.disaster_type
    )
    
    print("\nMerging datasets...")
    merged_data = data_processor.merge_datasets()

    print("\nSaving processed datasets...")
    data_processor.save_processed_data(
        args.data_dir,
        country=args.country,
        disaster_type=args.disaster_type
    )
    
    print("\nCalculating trends and statistics...")
    summary_stats = data_processor.get_summary_stats(
        country=args.country,
        disaster_type=args.disaster_type
    )
    
    # Generate visualizations
    region = args.country if args.country else 'global'
    disaster = args.disaster_type.lower().replace(' ', '_')
    viz_prefix = f"{region}_{disaster}"
    
    print(f"\nGenerating visualizations for {region} {args.disaster_type} disasters in {args.output_dir}...")
    
    visualizer = ClimateVisualizer()
    
    visualizer.plot_temperature_trend(
        merged_data,
        os.path.join(args.output_dir, f'temperature_trend_{viz_prefix}.png')
    )
    
    visualizer.plot_co2_trend(
        merged_data,
        os.path.join(args.output_dir, f'co2_trend_{viz_prefix}.png')
    )
    
    visualizer.plot_disasters_trend(
        merged_data,
        country=args.country,
        disaster_type=args.disaster_type,
        output_path=os.path.join(args.output_dir, f'disasters_trend_{viz_prefix}.png')
    )
    
    visualizer.plot_triple_correlation(
        merged_data,
        country=args.country,
        disaster_type=args.disaster_type,
        output_path=os.path.join(args.output_dir, f'correlations_{viz_prefix}.png')
    )

    # Add prediction analysis
    print("\nTraining prediction models...")
    predictor = ClimatePredictor()
    predictions = predictor.train_models(merged_data, forecast_years=30)
    
    print("\nGenerating prediction visualizations...")
    predictor.plot_predictions(
        historical_data=merged_data,
        country=args.country,
        disaster_type=args.disaster_type,
        output_dir=args.output_dir
    )
    
    # Get prediction summary
    summary = predictor.get_prediction_summary(merged_data)
    
    print("\nPrediction Model Performance:")
    print(f"Temperature Model R² Score: {summary['model_metrics']['temperature_r2']:.3f}")
    print(f"CO2 Model R² Score: {summary['model_metrics']['co2_r2']:.3f}")
    print(f"Disaster Model R² Score: {summary['model_metrics']['disasters_r2']:.3f}")
    
    print("\nPredictions for Key Years:")
    for year, values in summary['predictions_by_year'].items():
        print(f"\nYear {year}:")
        print(f"  Predicted Temperature Anomaly: {values['temperature']:.2f}°C")
        print(f"  Predicted CO2 Level: {values['co2']:.1f} ppm")
        print(f"  Predicted Number of Disasters: {values['disasters']:.0f}")
    
    # Print summary statistics
    print(f"\nSummary Statistics:")
    print(f"Region: {summary_stats['country']}")
    print(f"Disaster Type: {summary_stats['disaster_type']}")
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
    print(f"Years with Disasters: {summary_stats['years_with_disasters']}")

if __name__ == "__main__":
    main()