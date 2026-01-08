import sys
import os

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

try:
    from hwplib.hwp5.chart.chart_constants import ChartType, AxisId
    from hwplib.hwp5.chart.chart_model import VtChart, Axis
    from hwplib.hwp5.chart.chart_parser import ChartParser
    
    print("Imports successful!")
    
    # Test instantiation
    chart = VtChart()
    print(f"Chart created: {chart}")
    
    print("Constants check:", ChartType.Bar, AxisId.AxisX)
    
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
