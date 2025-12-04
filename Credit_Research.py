import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def analyze_credit_data(file_path):
    """
    Read Excel file, analyze transaction amounts by category, and create a pie chart.
    
    Args:
        file_path: Path to the Excel file
    """
    # 1. Open the Excel file and convert to dataframe
    df = pd.read_excel(file_path)
    
    # Display basic info about the dataframe
    print("DataFrame loaded successfully!")
    print(f"Shape: {df.shape}")
    print(f"\nColumn names: {df.columns.tolist()}")
    print(f"\nFirst few rows:")
    print(df.head())
    
    # 3. Sum "סכום חיוב" values according to "ענף" key names
    summary = df.groupby('ענף')['סכום\nחיוב'].sum().sort_values(ascending=False)
    
    print(f"\n\nSummary by ענף:")
    print(summary)
    
    # 4. Plot the summary on a pie chart
    plt.figure(figsize=(10, 8))
    # To display Hebrew labels right-to-left (correctly), reverse the label string using slicing:
    hebrew_labels = [str(label)[::-1] for label in summary.index]
    plt.pie(summary.values, labels=hebrew_labels, autopct=lambda p: f'{p * summary.values.sum() / 100:,.0f}', startangle=90)
    plt.title('סכום עסקאות לפי ענף', fontsize=16, pad=20)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    
    # Save the plot
    output_path = Path(file_path).parent / f'credit_analysis_pie_chart_{file_path}.png'
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    print(f"\n\nPie chart saved to: {output_path}")
    
    # Display the plot
    plt.show()
    
    return df, summary


if __name__ == "__main__":
    # Path to the Excel file
    excel_path = "October_2025.xlsx"
    
    # Run the analysis
    df, summary = analyze_credit_data(excel_path)

