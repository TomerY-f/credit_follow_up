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

### Method 1: Direct Execution

Run the application by providing the path to your Excel file:

```bash
python main.py bills/October_2025.xlsx
```

*   Replace `bills/October_2025.xlsx` with your actual file path.
*   The application will automatically open in your default web browser at `http://127.0.0.1:8050/`.

### Method 2: Using the `credit_review` Alias (Recommended)

You can set up a quick command to run the dashboard from anywhere and automatically import your bill files.

1.  Copy the contents of `credit_review_alias.zsh` to your `~/.zshrc` file:
    ```bash
    cat credit_review_alias.zsh >> ~/.zshrc
    source ~/.zshrc
    ```

2.  Use the command with any bill file:
    ```bash
    credit_review ~/Downloads/November_2025.xlsx
    ```

This will:
*   Copy the file to the repository's `bills/` folder (enabling historical comparison).
*   Launch the dashboard with the new file.

## Data Format

The Excel file should contain at least the following columns (Hebrew):
*   **ענף** (Category)
*   **שם בית העסק** (Business Name)
*   **סכום חיוב** (Transaction Amount)

The tool attempts to handle variations in column names automatically.
