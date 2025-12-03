# Credit Research Dashboard

An interactive tool to analyze and visualize credit card transaction data.

## Features

*   **Pie Chart Visualization**: View expenses broken down by category ("ענף").
*   **Interactive Drill-Down**: Click on any pie slice to see detailed transactions for that category.
*   **Summary Table**: View business names and transaction amounts with a total sum for each category.

## Requirements

*   Python 3.x
*   Packages listed in `requirements.txt`:
    *   `pandas`
    *   `openpyxl`
    *   `dash`
    *   `plotly`

## Installation

1.  Clone or download this repository.
2.  Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the application by providing the path to your Excel file:

```bash
python main.py October_2025.xlsx
```

*   Replace `October_2025.xlsx` with your actual file name.
*   The application will automatically open in your default web browser at `http://127.0.0.1:8050/`.

## Data Format

The Excel file should contain at least the following columns (Hebrew):
*   **ענף** (Category)
*   **שם בית העסק** (Business Name)
*   **סכום עסקה** (Transaction Amount)

The tool attempts to handle variations in column names automatically.

