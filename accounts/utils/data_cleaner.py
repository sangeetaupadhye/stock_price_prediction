import pandas as pd


class StockDataCleaner:

    def __init__(self, file_path, save_path):
        self.file_path = file_path
        self.save_path = save_path
        self.df = None

    # Load dataset
    def load_data(self):
        try:
            self.df = pd.read_csv(self.file_path)
            print("Dataset loaded successfully")
        except Exception as e:
            print("Error loading file:", e)
            self.df = pd.DataFrame()
        return self.df

    # Standardize column names
    def standardize_columns(self):
        if self.df is not None:
            self.df.columns = [
                col.strip().lower().replace(" ", "_")
                for col in self.df.columns
            ]
        return self.df

    # Convert date column
    def convert_date(self):
        possible_date_cols = ['date', 'timestamp', 'time']

        for col in possible_date_cols:
            if col in self.df.columns:
                try:
                    # self.df[col] = pd.to_datetime(self.df[col])
                    self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
                    self.df = self.df.sort_values(by=col)
                    print(f"Date column converted: {col}")
                except Exception as e:
                    print(f"Date conversion failed for {col}: {e}")
                break

        return self.df

    # Remove duplicates
    def remove_duplicates(self):
        before = len(self.df)
        self.df = self.df.drop_duplicates()
        after = len(self.df)

        print(f"Removed {before - after} duplicate rows")
        return self.df, (before - after)

    # Handle missing values
    def handle_missing_values(self):
        before = len(self.df)
        self.df = self.df.dropna()
        after = len(self.df)

        print(f"Removed {before - after} rows with missing values")
        return self.df, (before - after)

    # Filter important columns
    def filter_columns(self):
        required_columns = [
            'date',
            'open_price',
            'high_price',
            'low_price',
            'close_price',
            'total_traded_quantity'
        ]

        available_columns = [col for col in required_columns if col in self.df.columns]

        if available_columns:
            self.df = self.df[available_columns]

        return self.df

    # Save cleaned dataset
    def save_cleaned_data(self):
        try:
            self.df.to_csv(self.save_path, index=False)
            print(f"Cleaned dataset saved at: {self.save_path}")
        except Exception as e:
            print("Error saving file:", e)

    # Main pipeline
    def clean_data(self):

        # Step 1: Load
        self.load_data()

        if self.df.empty:
            return self.df, {
                "original_rows": 0,
                "final_rows": 0,
                "duplicates_removed": 0,
                "missing_removed": 0,
                "columns": []
            }

        original_rows = len(self.df)

        # Step 2: Standardize
        self.standardize_columns()

        # Step 3: Date handling
        self.convert_date()

        # Step 4: Remove duplicates
        self.df, duplicates_removed = self.remove_duplicates()

        # Step 5: Handle missing values
        self.df, missing_removed = self.handle_missing_values()

        # Step 6: Filter columns
        self.filter_columns()

        final_rows = len(self.df)

        # Step 7: Save cleaned file
        self.save_cleaned_data()

        # Stats for UI
        stats = {
            "original_rows": original_rows,
            "final_rows": final_rows,
            "duplicates_removed": duplicates_removed,
            "missing_removed": missing_removed,
            "columns": list(self.df.columns)
        }

        print("Data cleaning completed")

        return self.df, stats


# Trigger function for Django
def auto_clean_uploaded_file(file_path, save_path):
    cleaner = StockDataCleaner(file_path, save_path)
    cleaned_df, stats = cleaner.clean_data()
    return cleaned_df, stats


# Standalone testing (optional)
# if __name__ == "__main__":

#     file = "sample.csv"
#     save_file = "cleaned_sample.csv"

#     cleaned_df, stats = auto_clean_uploaded_file(file, save_file)

#     print(cleaned_df.head())
#     print(stats)