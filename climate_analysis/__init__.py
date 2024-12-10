# climate_analysis/__init__.py

from .data_processor import ClimateDataProcessor
from .visualizer import ClimateVisualizer

__version__ = '1.0.0'

__all__ = [
    'ClimateDataProcessor',
    'ClimateVisualizer'
]
