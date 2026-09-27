import xml.etree.ElementTree as ET
import pandas as pd
import time
import os

def parse_apple_health_fast(xml_file_path):
    if not os.path.exists(xml_file_path):
        print(f" Error: Could not find '{xml_file_path}'. Make sure it's in the data/ folder!")
        return None

    print(f"Processing {xml_file_path} (~645 MB)...")
    start_time = time.time()
    
    # Biomarkers linked to inflammation and physical stress
    target_types = {
        'HKQuantityTypeIdentifierHeartRate': 'HeartRate',
        'HKQuantityTypeIdentifierRestingHeartRate': 'RestingHeartRate',
        'HKQuantityTypeIdentifierHeartRateVariabilitySDNN': 'HRV',
        'HKQuantityTypeIdentifierStepCount': 'Steps',
        'HKQuantityTypeIdentifierAppleSleepingWristTemperature': 'WristTemperature',
        'HKQuantityTypeIdentifierBodyTemperature': 'BodyTemperature',
        'HKQuantityTypeIdentifierOxygenSaturation': 'SpO2'
    }

    records = []
    total_tags = 0

    # iterparse processes tag by tag without overloading your RAM
    for event, elem in ET.iterparse(xml_file_path, events=('end',)):
        if elem.tag == 'Record':
            rec_type = elem.get('type')
            
            if rec_type in target_types:
                val = elem.get('value')
                if val is not None:
                    try:
                        records.append({
                            'metric': target_types[rec_type],
                            'value': float(val),
                            'unit': elem.get('unit'),
                            'startDate': elem.get('startDate'),
                            'endDate': elem.get('endDate')
                        })
                    except ValueError:
                        pass
            
            total_tags += 1
            if total_tags % 200000 == 0:
                print(f"Processed {total_tags:,} records...")

            # Free memory immediately
            elem.clear()

    elapsed = round(time.time() - start_time, 2)
    print(f"\n Finished in {elapsed} seconds!")
    print(f"Scanned {total_tags:,} total XML elements.")
    
    df = pd.DataFrame(records)
    print(f"Extracted {len(df):,} relevant biometric rows.\n")
    return df

if __name__ == "__main__":
    # Adjust path if your export.xml is inside data/
    xml_path = "data/export.xml" if os.path.exists("data/export.xml") else "export.xml"
    
    df = parse_apple_health_fast(xml_path)
    
    if df is not None and not df.empty:
        # Convert date column to proper datetime format
        df['startDate'] = pd.to_datetime(df['startDate'])
        
        # Sort by date
        df = df.sort_values(by='startDate')
        
        # Save to CSV
        output_path = "data/health_data_clean.csv" if os.path.exists("data") else "health_data_clean.csv"
        df.to_csv(output_path, index=False)
        print(f"Clean dataset saved to: {output_path}")
        
        # Show dataset summary
        print("\n--- DATASET SUMMARY ---")
        print(f"Start Date: {df['startDate'].min()}")
        print(f"End Date:   {df['startDate'].max()}")
        print("\nBreakdown by Metric:")
        print(df['metric'].value_counts())
        print("\nFirst 5 Rows:")
        print(df.head())