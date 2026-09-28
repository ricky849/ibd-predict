# Engineering and Research Logbook

**Project Title:** Wearable-Based Flare-Up Prediction for Inflammatory Bowel Disease    
**Principal Investigator:** Rikhav Patil  
**Target Institutions:** Johns Hopkins University (BME) / Stanford University (Bio-X / CS / EE)  
**Repository:** `github.com/ricky849/ibd-predict`

* **Primary Hypothesis ($H_1$):** When an IBD flare-up is starting, the body's immune response stresses the nervous system. This should show up on an Apple Watch as a sustained spike in Resting Heart Rate and a drop in HRV. More importantly, this can be proven as an actual illness, not just a hard workout, by checking if her daily step count is low during that same time.
* **Null Hypothesis ($H_0$):** Spikes in heart rate are frequently caused by exercise, caffeine, or psychological stress, meaning normal daily noise cannot be easily separated from an autoimmune flare-up.

---

## Entry: Day 1
**Date:** 9/20/2026
**Work Time:** 15 minutes

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
**Work Time:** 33 minutes  

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
**Work Time:** 1 hour 14 minutes

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



---


### Entry: Day 4
**Date:** [9/27/26]
**Work Time:** 2 hours 53 minutes

### 1. Objective:
Combine daily heart rate, HRV, and step count data into one dataset (daily_features.csv) that tracks trends over time.

### 2. What I Built & Learned:
* Read two review papers on ulcerative colitis and how limitations in the field are being solved with our project. Also researched this project idea and what other apps/commercial tools are trying this.
  * Learned that clinical guidelines classify severe Ulcerative Colitis by tachycardia (resting heart rate >90 BPM) alongside fever and frequent bloody stools. This confirms elevated heart rate is an established medical indicator of gut inflammation.
  * Advanced IBD medications only work for 30%–60% of patients, leading to high rates of unpredictable breakthrough flares and a 20% 5-year hospitalization rate.
  * Current tests (colonoscopies, fecal calprotectin) are invasive and only happen every few months or years. Wearable tracking fills this daily blind spot.
  * Researched current commercial tools (like Flarity) and identified why flare prediction is hard: acute daily noise (exercise, caffeine, general stress) causes false alarms.
  * Confirmed our engineering strategy: we must combine HRV with **Step count (to control for physical exertion)** and **7-day rolling averages (to filter out 1-day acute spikes)**.
* Created Github `README.md`, containing research findings, project background, dataset stats, and roadmaps.
* Created a visual diagram in Canva (`assets/biomarker_diagram.png`) showing the chain reaction:
  * Gut Inflammation (Cytokines) → Vagus Nerve Suppression → Apple Watch Signals (HRV drops, Resting HR rises, Steps filter).
* Saved the diagram in an `assets/` folder and linked it directly in the README.
* Built `build_daily_features.py`:
  * Extracted and aggregated Resting HR (mean), HRV (mean), and Step counts (sum) by calendar date.
  * Performed an outer merge across all 3 metrics and filtered out pre-Apple Watch phone-only data (before July 2020).
  * Calculated 7-day rolling averages for both RHR (`rhr_7day_avg`) and HRV (`hrv_7day_avg`) to filter out single-day data fluctuation and noise.
* Created and ran `experiment_rhr_steps.py` to compare step counts on extreme Resting HR days against the 4-year baseline average (**7,177 steps/day**).
  * **Highest RHR Day (Sept 3, 2021 - 98.0 BPM):** Step count was **5,609 steps** (below average) and HRV dropped to **19.5 ms** (drop in vagal tone). This proves the 98 BPM spike was *not* caused by physical exercise, but indicates systemic illness/inflammatory stress (matching the Mayo Clinic paper's definition of tachycardia).
  * **Lowest RHR Day (Oct 26, 2022 - 44.0 BPM):** Step count was **22,292 steps** (3x average). This proves high physical activity does not falsely inflate resting HR when the body is healthy.
* Created `plot_features.py` using pandas and matplotlib:
  * Generated a 3-panel stacked plot (`assets/multi_year_trends.png`)
  * Found patterns in the years 2021-2023. 
    * Late 2021 seemed like her inflammatory event window: The resting HR (red) had a bold peak above **85 BPM**. The HRV (blue) dropped extremely low at the same time, dropping below **20 ms**. The steps (green) stayed around the average (dotted line) or below. This is a huge sign of systemic autonomic stress, illness, and IBD flare due to a high heart rate, low HRV, and low physical activity.
    * Late 2022 was her physical fitness window. She had huge green spikes, reaching up to **20k-30k** steps per day. Around this time her HR drops to her lowest baseline (44 BPM). This shows that physical activity improved her baseline cardiovascular health without causing artificial "resting" heart rate spikes   
    * In 2023-2024, the data starts to get sparser as watch usage decreased, showing why filtering for data was the right call.


### 3. Quantitative Results:
* **Processed Output:** Generated `data/daily_features.csv`.
* **Dataset Scale:** **1,340+ continuous days** of multi-modal watch telemetry (July 19, 2020 – March 22, 2024).
* **Baselines:** 7-day RHR baseline ~74 BPM; 7-day HRV baseline ~30–35 ms; average daily activity **7,177 steps/day**.
* **Validated Extremes:** 
  * Max RHR: **98.0 BPM** (Sept 3, 2021) paired with **5,609 steps** (below average) and **19.5 ms HRV** (low vagal tone).
  * Min RHR: **44.0 BPM** (Oct 26, 2022) paired with **22,292 steps** (3x average) and **28.9 ms HRV**.
  * These findings from `experiment_rhr_steps.py` further prove our primary hypothesis, which states that it's possible to seperate inflammation from workout noise. This was done by using the step count as a filter. On Sept 3, 2021, the patient's resting HR hit 98 BPM while her steps were below average (5,609 steps) and HRV dropped to 19.5 ms. This proves her highest heart rate day wasn't caused by working out, but by internal stress/illness. However, since this experiment was only based on one day, there's still a chance (even if it's low) this could've been caused by excessive caffeine, heavy-lifting workouts, or just non-IBD related stress. This is why `plot_features.py` will gonna use the 7 day rolling average we've constantly been using to see if there was any build-up to this huge spike.
* With `plot_features.py`, we were able to create a 3-panel stacked plot and furthermore prove our hypothesis with a visual representation displaying periods of inflammatory events, increased physical activity, and sparse data. We found that late 2021 was when her inflammatory window was the strongest. This is proved because late 2021 showed a sustained multi-week RHR mountain (>85 BPM) paired with a deep HRV valley (<20 ms) while step counts remained average/low. Late 2022 was when she had high-fitness. 2023-2024 is when the data starts to cut off after she starts wearing her watch less.

  ### 4. Next Steps
* Turn raw RHR and HRV numbers into Z-scores (standard deviations from normal) to mathematically define what counts as a "spike" or "drop".
* Write a script (`detect_anomalies.py`) that automatically scans the 1,340 days and flags potential flare-up windows instead of just relying on human eye inspection of the graph.
* Cross-reference the top flagged anomaly dates (like Sept 3, 2021) with my sister to see if she remembers those exact periods as bad sickness/flare windows.

