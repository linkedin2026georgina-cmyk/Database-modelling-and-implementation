import pandas as pd
from datetime import datetime
import zipfile

def crop_and_cleanse():
    # Load the measurement data with error handling
    try:
        df = pd.read_csv('/Users/djihene/Downloads/Air_Quality_Continuous.csv')
    except FileNotFoundError:
        print("Error: Input file not found at specified path")
        return
    
    # Converting datetime column to pandas format (with UTC timezone)
    df['Date_Time'] = pd.to_datetime(
        df['Date_Time'],
        errors='coerce',
        format='mixed',
        utc=True  # Ensure all dates have UTC timezone
    )
    
    # Removed rows with invalid dates
    df = df.dropna(subset=['Date_Time'])
    print(f"Found {len(df)} valid records after initial date cleaning")

    # Creating timezone-aware comparison dates
    start_date = pd.to_datetime('2015-01-01', utc=True)  
    end_date = pd.to_datetime('2023-10-22', utc=True)   

    # Filtering to date range (now all timezone-aware)
    filtered = df[
        (df['Date_Time'] >= start_date) & 
        (df['Date_Time'] <= end_date)
    ].copy()
    
    # Save cleaned data to CSV
    filtered.to_csv('cleaned_measurements.csv', index=False)
    print(f"Successfully saved {len(filtered)} records between {filtered['Date_Time'].min()} and {filtered['Date_Time'].max()}")

    # Create a ZIP file for submission
    with zipfile.ZipFile('cropped.zip', 'w') as zipf:
        zipf.write('cleaned_measurements.csv')
        print("ZIP archive created: cropped.zip")

    # Final verification
    print("\n=== Summary ===")
    print(f"Original records: {len(df)}")
    print(f"Records after cropping: {len(filtered)}")
    print(f"Date range in final data: {filtered['Date_Time'].min()} to {filtered['Date_Time'].max()}")

if __name__ == "__main__":
    crop_and_cleanse()
