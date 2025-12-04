import pandas as pd
import os

class DataHandler:
    def __init__(self, file_path, verbose=True):
        """
        Initialize with the path to the Excel file.
        """
        self.file_path = file_path
        self.filename = os.path.basename(file_path)
        self.df = self._load_data()
        self.business_col = self._find_business_column()
        self.amount_col = self._find_amount_column()
        
        if verbose:
            # Print columns for debugging
            print(f"Loaded columns: {self.df.columns.tolist()}")
            print(f"Identified Business Column: {self.business_col}")
            print(f"Identified Amount Column: {self.amount_col}")

    def _load_data(self):
        """
        Load data and normalize column names.
        """
        try:
            df = pd.read_excel(self.file_path)
            
            # Normalize column names: remove newlines and strip whitespace
            df.columns = [str(col).replace('\n', ' ').strip() for col in df.columns]
            
            return df
        except Exception as e:
            print(f"Error loading file: {e}")
            return pd.DataFrame()

    def _find_business_column(self):
        """
        Finds the column name corresponding to the business/merchant name.
        """
        return self._find_column_by_candidates(['שם בית עסק'])

    def _find_amount_column(self):
        """
        Finds the column name corresponding to the transaction amount.
        """
        col = self._find_column_by_candidates(['סכום חיוב'])
        if col:
             # Ensure it's numeric
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce').fillna(0)
        return col

    def _find_column_by_candidates(self, candidates):
        if self.df.empty:
            return None
        for col in self.df.columns:
            for candidate in candidates:
                if candidate in col:
                    return col
        return None

    def get_category_summary(self):
        """
        Returns the sum of transactions grouped by 'ענף'.
        """
        if self.df.empty or not self.amount_col:
            return pd.Series()
            
        return self.df.groupby('ענף')[self.amount_col].sum().sort_values(ascending=False)

    def get_details_by_category(self, category_name):
        """
        Returns the details for a specific category.
        """
        if self.df.empty:
            return pd.DataFrame()
            
        # Filter by category
        filtered_df = self.df[self.df['ענף'] == category_name].copy()
        
        cols_to_show = []
        if self.business_col and self.business_col in filtered_df.columns:
            cols_to_show.append(self.business_col)
            
        if self.amount_col and self.amount_col in filtered_df.columns:
            cols_to_show.append(self.amount_col)
            
        return filtered_df[cols_to_show].sort_values(self.amount_col, ascending=False)

    def get_comparison_stats(self):
        """
        Calculates average statistics from other files in the same directory.
        Returns:
            tuple: (avg_category_series, avg_total_amount)
        """
        bills_dir = os.path.dirname(self.file_path)
        all_files = [f for f in os.listdir(bills_dir) if f.endswith('.xlsx') and f != self.filename]
        
        if not all_files:
            return pd.Series(), 0

        category_sums = []
        total_amounts = []

        for file in all_files:
            file_path = os.path.join(bills_dir, file)
            try:
                # Use a temporary handler to reuse loading logic, suppress output
                handler = DataHandler(file_path, verbose=False)
                if not handler.df.empty and handler.amount_col:
                    # Get category summary for this file
                    summary = handler.get_category_summary()
                    category_sums.append(summary)
                    
                    # Get total for this file
                    total = handler.df[handler.amount_col].sum()
                    total_amounts.append(total)
            except Exception as e:
                print(f"Skipping file {file} due to error: {e}")

        if not category_sums:
            return pd.Series(), 0

        # Calculate averages
        # Sum all category series (aligning keys) and divide by number of files
        combined_categories = pd.concat(category_sums, axis=1).fillna(0)
        avg_category_series = combined_categories.mean(axis=1).sort_values(ascending=False)
        
        avg_total_amount = sum(total_amounts) / len(total_amounts) if total_amounts else 0
        
        return avg_category_series, avg_total_amount
