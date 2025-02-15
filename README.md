# CSV Transformer Web App

## Description
The CSV Transformer Web App is a free, web-based tool that allows users to upload CSV files containing enrollment data, transform the data based on a user-defined year range, and download the transformed CSV file. The application processes CSV columns with a year identifier in the format `EF<year>`, and it intelligently ignores any additional suffixes (e.g., `_RV`) so that all matching columns for a given year are aggregated. The output is a transposed CSV where years (sorted in descending order) become the columns and the enrollment metrics become the rows.

## Features
- **File Upload:** Easily upload your CSV file containing enrollment data.
- **Customizable Year Range:** Specify a start year and an end year for the transformation.
- **Data Aggregation:** Automatically aggregates data for:
  - Undergrad Enrollment (Full Time & Part Time)
  - Graduate Enrollment
  - First-Time Freshman Enrollment
  - New Transfer Enrollment (Fall)
  - Total Enrollment (Undergrad + Graduate)
- **Flexible Column Matching:** Uses regular expressions to match columns with or without suffixes (e.g., `EF2019` or `EF2019_RV`).
- **Transposed Output:** The final CSV is transposed so that the metrics are rows and the years are columns (latest year first).
- **Free and Accessible:** Host it on a free platform like Render or Heroku to make it accessible anywhere.

## Requirements
- Python 3.x
- Flask
- Pandas

## Installation

1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   cd <repository-folder>
