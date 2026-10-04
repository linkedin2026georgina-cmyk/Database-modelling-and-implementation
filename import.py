import mysql.connector
import pandas as pd
import numpy as np
from zipfile import ZipFile
import os
import time

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'pollution',
    'autocommit': False
}

# File paths
zip_path = '/Users/djihene/Desktop/dmf-assign/cropped.zip'
extract_path = '/Users/djihene/Desktop/dmf-assign/temp_extract'
csv_filename = 'cleaned_measurements.csv'

# Column mapping
column_mapping = {
    'Date_Time': 'datetime',
    'Site_ID': 'station_id',
    'NOx': 'nitrogen_oxides',
    'NO2': 'nitrogen_dioxide',
    'NO': 'nitric_oxide',
    'PM10': 'pm_10',
    'O3': 'ozone_concentration',
    'Temperature': 'temperature',
    'ObjectId': 'object_1',
    'ObjectId2': 'object_2',
    'NVPM10': 'non_vol_pm_10',
    'VPM10': 'vol_pm_10',
    'NVPM2_5': 'non_vol_pm_2_5',
    'PM2_5': 'pm_2_5',
    'VPM2_5': 'vol_pm_2_5',
    'CO': 'carbon_monoxide',
    'RH': 'relative_humidity',
    'Pressure': 'air_pressure',
    'SO2': 'sulphur_dioxide'
}

# data for Constituency table
constituency_data = [
    ('Bristol East', 'Kerry', 'McCarthy'),
    ('Bristol Northwest', 'Darren', 'Jones'),
    ('Bristol South', 'Karin', 'Smyth'),
    ('Bristol West', 'Thangam', 'Debbonaire')
]

# Data for Station table
station_data = [
    (188, 'AURN Bristol Centre', 51.4572041156, -2.58564914143, 'Bristol East'),
    (203, 'Brislington Depot', 51.4417471802, -2.55995583224, 'Bristol Northwest'),
    (206, 'Rupert Street', 51.4554331987, -2.59626237324, 'Bristol West'),
    (209, 'IKEA M32', 51.4752847609, -2.56207998299, 'Bristol Northwest'),
    (213, 'Old Market', 51.4560189999, -2.58348949026, 'Bristol South'),
    (215, 'Parson Street School', 51.432675707, -2.60495665673, 'Bristol Northwest'),
    (228, 'Temple Meads Station', 51.4488837041, -2.58447776241, 'Bristol West'),
    (270, 'Wells Road', 51.4278638883, -2.56374153315, 'Bristol Northwest'),
    (271, 'Trailer Portway P&R', 51.4899934596, -2.68877856929, 'Bristol South'),
    (375, 'Newfoundland Road Police Station', 51.4606738207, -2.58225341824, 'Bristol West'),
    (395, "Shiner's Garage", 51.4577930324, -2.56271419977, 'Bristol West'),
    (452, 'AURN St Pauls', 51.4628294172, -2.58454081635, 'Bristol East'),
    (447, 'Bath Road', 51.4425372726, -2.57137536073, 'Bristol East'),
    (459, 'Cheltenham Road \\ Station Road', 51.4689385901, -2.5927241667, 'Bristol East'),
    (463, 'Fishponds Road', 51.4780449714, -2.53523027459, 'Bristol East'),
    (481, 'CREATE Centre Roof', 51.447213417, -2.62247405516, 'Bristol South'),
    (500, 'Temple Way', 51.4579497132, -2.5839890903, 'Bristol West'),
    (501, 'Colston Avenue', 51.4552693827, -2.59664882855, 'Bristol West'),
    (672, 'Marlborough Street', 51.4591419717, -2.59543271836, 'Bristol West')
]

# the code below attempts to repopulate Constituency and Station. this is because I imported them wrong the first time.

def reset_and_load_reference_data(conn):
    """Delete and reload Constituency and Station tables"""
    cursor = None
    try:
        cursor = conn.cursor()
        
        # disabling foreign key checks temporarily
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        # clear existing data (in correct order due to foreign keys)
        cursor.execute("DELETE FROM Measurement")
        cursor.execute("DELETE FROM Station")
        cursor.execute("DELETE FROM Constituency")
        
        # insert Constituency data
        constituency_sql = """
        INSERT INTO Constituency (c_name, mp_firstname, mp_surname)
        VALUES (%s, %s, %s)
        """
        cursor.executemany(constituency_sql, constituency_data)
        print(f"Inserted {len(constituency_data)} constituency records")
        
        # Insert Station data
        station_sql = """
        INSERT INTO Station (sid, s_name, latitude, longitude, constituency_name)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.executemany(station_sql, station_data)
        print(f"Inserted {len(station_data)} station records")
        
        # Re-enable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        conn.commit()
        print("Successfully reloaded reference data")
        
    except mysql.connector.Error as e:
        conn.rollback()
        print(f"Error reloading reference data: {e}")
        raise
    finally:
        if cursor:
            cursor.close()

def get_valid_station_ids(conn):
    """Get all valid station IDs from the Station table"""
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT sid FROM Station")
        return {int(row[0]) for row in cursor.fetchall()}
    finally:
        cursor.close()

def extract_zip(zip_path, extract_path):
    """Extract the zip file to a temporary directory"""
    if not os.path.exists(extract_path):
        os.makedirs(extract_path)
    with ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    return os.path.join(extract_path, csv_filename)

# sql connection

def create_connection():
    """Create a database connection with retry logic"""
    max_retries = 3
    retry_delay = 5
    
    for attempt in range(max_retries):
        try:
            conn = mysql.connector.connect(**db_config)
            return conn
        except mysql.connector.Error as e:
            print(f"Connection attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                raise

def clear_table(conn):
    """Efficiently clear the Measurement table"""
    cursor = conn.cursor()
    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        cursor.execute("TRUNCATE TABLE Measurement")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        conn.commit()
        print("Measurement table cleared successfully")
    except mysql.connector.Error as e:
        conn.rollback()
        print(f"Error clearing table: {e}")
        raise
    finally:
        cursor.close()

def clean_dataframe(df, valid_station_ids):
    """Clean the dataframe before import"""
    # Converting datetime
    if 'datetime' in df.columns:
        df['datetime'] = pd.to_datetime(df['datetime'])
    
    # Convert station_id to integer and filter invalid stations
    df['station_id'] = pd.to_numeric(df['station_id'], errors='coerce').astype('Int64')
    invalid_stations = df[~df['station_id'].isin(valid_station_ids)]
    
    if not invalid_stations.empty:
        print(f"Found {len(invalid_stations)} records with invalid station IDs:")
        print(invalid_stations['station_id'].unique())
        df = df[df['station_id'].isin(valid_station_ids)]
    
    # Replace NaN values with None (NULL in MySQL)
    df = df.replace({np.nan: None})
    
    # Ensure numeric columns are properly typed
    numeric_cols = [col for col in df.columns if col not in ['datetime', 'object_1', 'object_2', 'station_id']]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df

def import_measurements(csv_path, conn):
    """Import measurements data with robust error handling"""
    cursor = None
    try:
        # Getting valid station IDs first
        valid_station_ids = get_valid_station_ids(conn)
        print(f"Found {len(valid_station_ids)} valid station IDs in database")
        
        # Reading CSV file
        print("Reading CSV file...")
        df = pd.read_csv(csv_path)

        df.rename(columns=column_mapping, inplace=True)

        df = clean_dataframe(df, valid_station_ids)

        clear_table(conn)
        
        # Preparing INSERT statement
        db_columns = list(column_mapping.values())
        cols = ", ".join(db_columns)
        placeholders = ", ".join(["%s"] * len(db_columns))
        sql = f"INSERT INTO Measurement ({cols}) VALUES ({placeholders})"
        
        # Converting dataframe to list of tuples with proper NULL handling
        data = []
        for _, row in df.iterrows():
            row_data = []
            for col in db_columns:
                val = row[col]
                if pd.isna(val) or val == 'nan' or val == 'NaN':
                    row_data.append(None)
                else:
                    row_data.append(val)
            data.append(tuple(row_data))
        
        # Importing in chunks of data
        cursor = conn.cursor()
        chunk_size = 10000
        total_rows = len(data)
        
        print(f"Importing {total_rows} valid records in chunks of {chunk_size}...")
        
        for i in range(0, total_rows, chunk_size):
            chunk = data[i:i + chunk_size]
            try:
                cursor.executemany(sql, chunk)
                conn.commit()
                print(f"Inserted {len(chunk)} rows (total: {min(i + chunk_size, total_rows)}/{total_rows})")
            except mysql.connector.Error as e:
                conn.rollback()
                print(f"Error inserting chunk {i//chunk_size + 1}: {e}")
                if chunk:
                    print("First problematic row sample:")
                    for j, val in enumerate(chunk[0]):
                        print(f"{db_columns[j]}: {val} ({type(val)})")
                raise
        
        cursor.execute("SELECT COUNT(*) FROM Measurement")
        count = cursor.fetchone()[0]
        print(f"\nSuccessfully imported {count} records to Measurement table")
        
        cursor.execute("SELECT * FROM Measurement LIMIT 12")
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        
        print("\nFirst 12 records:")
        print("-" * 120)
        print("\t".join(columns))
        for row in results:
            print("\t".join(str(x) if x is not None else 'NULL' for x in row))
        print("-" * 120)
        print("\nPlease take a screenshot of these records as 'readings.png'")
        
    except Exception as e:
        print(f"Error during import: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if cursor:
            cursor.close()

def main():
    conn = None
    try:

        print("Connecting to database...")
        conn = create_connection()

        print("\nResetting and loading reference data...")
        reset_and_load_reference_data(conn)
 
        print("\nExtracting CSV file...")
        csv_path = extract_zip(zip_path, extract_path)
        
        print("\nImporting measurements data...")
        import_measurements(csv_path, conn)
        
        print("\nData import completed successfully!")
        
    except Exception as e:
        print(f"\nScript failed: {e}")
    finally:
        # Clean up
        if conn and conn.is_connected():
            conn.close()
        if os.path.exists(extract_path):
            for file in os.listdir(extract_path):
                os.remove(os.path.join(extract_path, file))
            os.rmdir(extract_path)
        print("Cleanup complete")

if __name__ == "__main__":
    main()