# Engineering and Research Logbook

**Project Title:** Wearable-Based Flare-Up Prediction for Inflammatory Bowel Disease    
**Principal Investigator:** Rikhav Patil  
**Target Institutions:** Johns Hopkins University (BME) / Stanford University (Bio-X / CS / EE)  
**Repository:** `github.com/ricky849/ibd-predict`  

---

## Entry: Day 1
**Date:** 9/20/2026

### 1. Objective
Set up the Python environment, connect GitHub version control, and lock down privacy rules for handling health data.

### 2. What I Built And Learned
* **Project Definition:** Predict IBD (Crohn's / Colitis) flare-ups using historical Apple Watch physiological data (Resting HR and HRV).
* Set up Python 3.12, VS Code, and initialized the Git repository.
* **Privacy & Security Architecture:**
  * Created `.gitignore` rules to prevent raw patient data from being pushed to public github:
    ```text
    data/export.xml
    data/health_data_clean.csv
    data/*.zip
    __pycache__/
    .env
    ```
* Practiced basic Pandas dataframe operations (indexing, filtering, file loading) on Kaggle.
* **Biomarker Decision**: Selectd the Apple Watch because it continuously and automatically tracks resting heart rate, HRV, and sleep stages using built-in sensors.


### 3. Next Steps
* Secure Apple Health raw archive from patient (sister).



---



## Entry: Day 2
**Date:** [9/22/26]  

### 1. Objective
Extract heart rate, HRV, and step data from my sister's raw Apple Health XML export.

### 2. What I Built And Learned
*Received raw `export.xml` archive (~644,881 KB).
* **Main Problem:** Standard XML parsers (`ET.parse`) load the entire 645 MB file into RAM simultaneously, which freezes/crashes the system.
* **The Solution:** `ET.iterparse()` in `parse_health_data.py` to stream through the XML tag-by-tag, grabbing relevant records and immediately clearing them from memory (`elem.clear()`).
* Extracted targeted metrics: Resting Heart Rate, Active Heart Rate, HRV (SDNN), and Steps.
* Saved the cleaned output into `data/health_data_clean.csv`.
* Created `inspect_data.py` to find the total records in the dataset (`row_count`) and find the minimum (`minimum_resting_heartbeat`) and maximum (`minimum_resting_heartbeat`) resting heart rates.

### 3. Quantitative Results & Metrics
* Processed 645 MB XML file.
* Extracted 271,148 rows.
* The resting HR range was 44.0 BPM (min) to 98.0 BPM (max). This is a 54 BPM range, which indicates distinct physiological states (remission vs. stress/inflammation). 


### 4. Next Steps
* Write a script to group individual sensor readings into clean daily averages.
* Apply a rolling average filter to smooth out day-to-day noise from the resting heart rate signal.



---



## Entry: Day 3
**Date:** [9/26/26]

### 1. Objective
Transform high-frequency Apple Watch biometric records into a clean daily time-series and apply a 7-day moving average filter to reduce acute noise.

### 2. What I Built & Learned
* Created `daily_analysis.py` to process resting heart rate.
* Converted timestamps to datetime objects, grouped by calendar date, and calculated the daily mean resting heart rate.
* Implemented a 7-day rolling average (`.rolling(window=7).mean()`). A single bad night or cup of coffee spikes heart rate for 1 day (noise), but a gut flare-up elevates baseline heart rate for a week or more (signal).
* Investigated why data started in March 2016 for steps but July 2020 for heart rate. Realized the 2016–2020 data was recorded by an iPhone in a pocket (accelerometer steps only), while July 19, 2020 was the exact day she started wearing an Apple Watch (PPG optical heart rate sensors).
* Saved processed data to `data/daily_summary.csv`.

### 3. Quantitative Results
* Continuous optical watch data from **July 19, 2020 to March 22, 2024 (~1,340 days)**.
* Filtered out single-day drops (e.g., 62 BPM on 2020-07-21) while capturing the true baseline (~74 BPM).

### 4. Next Steps
* Add HRV (SDNN) and daily Step counts into the daily summary table.
* Research papers on Heart Rate Variability and 
* Build a script to plot these trends over the full 4-year timeline.