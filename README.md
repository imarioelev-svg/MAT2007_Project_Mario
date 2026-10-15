# MAT2007_Project_Mario
Intro to programing project assignment.
# Sleep Impact Over Blood Pressure: An Analysis of the NHANES Dataset

## Description
This project explores the scientific question of whether a measurable correlation exists between self-reported sleep duration and average clinical blood pressure. The repository contains a Python script that analyzes clinical and demographic data to generate visual and statistical insights, specifically testing for correlations across different age groups and sleep duration brackets.

## Dataset
**Source:** [2021-2023 National Health and Nutrition Examination Survey (NHANES)](https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/default.aspx?Cycle=2021-2023)

To reproduce this analysis, you need to download the following three SAS Transport files (.XPT) from the NHANES website:
* `DEMO_L.XPT` (Demographics)
* `SLQ_L.XPT` (Sleep Disorders)
* `BPXO_L.XPT` (Oscillometric Blood Pressure)

**Data Cleaning:**
The script automatically handles the necessary data cleaning. It merges the three datasets using the unique respondent sequence number (`SEQN`), drops incomplete records, handles refused/missing sleep values (coded as `77` and `99`), and calculates a single mean systolic blood pressure from the three individual readings.

## Dependencies
This project is built with Python 3. To run the script, you must install the following packages:
* `pandas`
* `numpy`
* `seaborn`
* `matplotlib`

You can install these via pip:
```bash
pip install pandas numpy seaborn matplotlib
