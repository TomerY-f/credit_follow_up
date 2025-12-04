import pandas as pd
import os

class DataHandler:
    def __init__(self, file_path):
        """
        Initialize with the path to the Excel file.
        """
        self.file_path = file_path
        self.filename = os.path.basename(file_path)
        self.df = self._load_data()
        self.business_col = self._find_business_column()
        self.amount_col = self._find_amount_column()
        
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
        if self.df.empty:
            return None
            
        candidates = ['שם בית העסק', 'שם בית', 'שם עסק', 'תיאור עסקה', 'שם']
        for col in self.df.columns:
            for candidate in candidates:
                if candidate in col:
                    return col
        return None

    def _find_amount_column(self):
        """
        Finds the column name corresponding to the transaction amount.
        """
        if self.df.empty:
            return None
            
        candidates = ['סכום חיוב']
        
        # First try exact matches from candidates
        for col in self.df.columns:
            if col in candidates:
                # Ensure it's numeric
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce').fillna(0)
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
