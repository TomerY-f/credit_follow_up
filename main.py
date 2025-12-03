import sys
import argparse
import webbrowser
from threading import Timer
from data_handler import DataHandler
from dashboard_app import create_app

def open_browser():
    """Helper to open the browser automatically"""
    webbrowser.open_new("http://127.0.0.1:8050/")

def main():
    # 1. Parse Arguments
    parser = argparse.ArgumentParser(description="Run Credit Research Dashboard")
    parser.add_argument("file_path", help="Path to the Excel file (e.g., October_2025.xlsx)")
    args = parser.parse_args()

    print(f"Loading data from: {args.file_path}...")

    # 2. Initialize Data Handler
    data_handler = DataHandler(args.file_path)
    
    if data_handler.df.empty:
        print("Failed to load data. Exiting.")
        sys.exit(1)

    # 3. Create App
    app = create_app(data_handler)

    # 4. Open Browser & Run Server
    print("Starting server on http://127.0.0.1:8050/")
    Timer(1, open_browser).start() # Wait 1 second for server to start then open browser
    
    # Turn off debug mode for cleaner production-like run
    app.run(debug=False, host='127.0.0.1', port=8050)

if __name__ == "__main__":
    main()

