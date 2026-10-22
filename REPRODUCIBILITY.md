
# Reproducibility Guide — SpaceX Falcon 9 Analytics

This guide explains how to set up, inspect and rerun the SpaceX Falcon 9 analytics project.

The repository includes archived input data, processed datasets, generated visualisations, model outputs and a Power BI dashboard.

**Reproducibility status:** The analyses were executed successfully during project development. However, a clean installation and complete execution on a separate computer have not yet been independently verified.

## 1. System Requirements

Recommended environment:

- Windows 10 or Windows 11
- Python 3.11 or newer
- Git
- Visual Studio Code or JupyterLab
- Power BI Desktop for the `.pbix` dashboard
- Internet access for workflows that retrieve external resources

The project was developed using Python 3.13 on Windows. Compatibility with other Python versions has not been comprehensively tested.

## 2. Clone the Repository

Open PowerShell and run:

```powershell
git clone https://github.com/Kan-21/IBM-Applied-Data-Science-Capstone.git
cd IBM-Applied-Data-Science-Capstone
```

## 3. Create a Virtual Environment

From the repository root:

```powershell
python -m venv .venv
```

Activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

This execution-policy change applies only to the current PowerShell process.

Check Python:

```powershell
python --version
```

## 4. Install Dependencies

Upgrade pip:

```powershell
python -m pip install --upgrade pip
```

Install the project's dependencies:

```powershell
python -m pip install -r requirements.txt
```

Register the environment as a Jupyter kernel:

```powershell
python -m ipykernel install --user --name spacex-falcon9 --display-name "Python (SpaceX Falcon 9)"
```

In VS Code or Jupyter, select the **Python (SpaceX Falcon 9)** kernel.

### Dependency Notes

The requirements file contains the expected primary libraries used by the project.

Exact package versions have not yet been pinned against a verified clean-room installation. For stronger reproducibility, record and test compatible versions after completing an environment validation.

## 5. Repository Layout

```text
IBM-Applied-Data-Science-Capstone/
├── dashboards/
│   ├── docs/
│   ├── power-bi/
│   └── screenshots/
├── notebooks/
│   ├── data/
│   │   ├── raw/
│   │   └── processed/
│   ├── images/
│   ├── models/
│   ├── reports/
│   ├── 01_spacex_historical_data_collection.ipynb
│   ├── 02_spacex_data_wrangling.ipynb
│   ├── 03_spacex_web_scraping.ipynb
│   ├── 04_spacex_sql_analysis.ipynb
│   ├── 05_spacex_exploratory_visualisation.ipynb
│   ├── 06_spacex_geospatial_folium.ipynb
│   ├── 07_spacex_dash_dashboard.py
│   └── 08_spacex_predictive_modelling.ipynb
├── .gitignore
├── README.md
├── REPRODUCIBILITY.md
└── requirements.txt
```

## 6. Working Directory

The notebooks and scripts may use relative file paths.

For the initial reproduction attempt, open the repository in VS Code, then use the `notebooks/` directory as the working directory when executing notebook code that references paths such as:

```text
data/raw/
data/processed/
images/
models/
reports/
```

For example, the expected path from within `notebooks/` is:

```text
data/processed/falcon9_launches_historical.csv
```

The equivalent path from the repository root is:

```text
notebooks/data/processed/falcon9_launches_historical.csv
```

If a `FileNotFoundError` occurs, inspect the notebook's path definitions and verify the current working directory:

```python
from pathlib import Path
print(Path.cwd())
```

Do not assume that every notebook automatically changes its working directory.

## 7. Data Sources

The project uses several historical data sources.

### Historical Falcon 9 Recovery Dataset

Primary historical source:

```text
https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_1.csv
```

Cached raw file:

```text
notebooks/data/raw/ibm_spacex_dataset_part_1.csv
```

Processed files include:

```text
notebooks/data/processed/falcon9_launches_historical.csv
notebooks/data/processed/falcon9_labeled_historical.csv
notebooks/data/processed/falcon9_site_summary.csv
notebooks/data/processed/falcon9_data_quality.json
```

The primary historical recovery dataset contains 90 launch records.

### SQL Mission Dataset

Cached raw data:

```text
notebooks/data/raw/ibm_spacex_sql_missions.csv
```

Processed data:

```text
notebooks/data/processed/spacex_sql_mission_dataset.csv
```

This is a separate mission-level dataset and should not be assumed to contain exactly the same records as the historical recovery dataset.

### Wikipedia Historical Snapshot

Archived source:

```text
notebooks/data/raw/wikipedia_falcon_launches_oldid_1027686922.html
```

Processed output:

```text
notebooks/data/processed/wikipedia_falcon_launches_archived.csv
```

Using the archived snapshot is preferable when reproducing historical results because the current Wikipedia page may have changed.

## 8. Notebook Execution Order

The numbered analyses provide the recommended workflow.

| Order | File | Purpose |
|---|---|---|
| 01 | `01_spacex_historical_data_collection.ipynb` | Collect and inspect historical launch data |
| 02 | `02_spacex_data_wrangling.ipynb` | Clean, transform and validate data |
| 03 | `03_spacex_web_scraping.ipynb` | Extract archived Wikipedia launch information |
| 04 | `04_spacex_sql_analysis.ipynb` | Query and analyse mission-level records |
| 05 | `05_spacex_exploratory_visualisation.ipynb` | Produce exploratory charts |
| 06 | `06_spacex_geospatial_folium.ipynb` | Produce interactive geographic maps |
| 07 | `07_spacex_dash_dashboard.py` | Run the interactive Dash application |
| 08 | `08_spacex_predictive_modelling.ipynb` | Train and evaluate classification models |

### Running Jupyter

From the repository root:

```powershell
cd notebooks
jupyter lab
```

Open the notebooks in numerical order and select the project's Python kernel.

Use **Run All** within each notebook, inspecting any warnings, data-source failures or file-path errors before proceeding.

The SQL and web-scraping analyses may use separate inputs. Their execution does not necessarily depend on the outputs of every preceding notebook.

## 9. Running the Plotly Dash Application

From the repository root:

```powershell
cd notebooks
python 07_spacex_dash_dashboard.py
```

Open the local URL printed in the terminal.

Dash commonly runs on:

```text
http://127.0.0.1:8050/
```

Use the actual address reported by the application if it differs.

Stop the application using `Ctrl + C`.

## 10. Generated Outputs

### Processed Data

```text
notebooks/data/processed/
```

Contains cleaned datasets, labels, summaries and quality reports.

### Static Visualisations

```text
notebooks/images/
```

Includes:

- `spacex_flight_payload.png`
- `spacex_launch_sites.png`
- `spacex_orbit_recovery_rates.png`
- `spacex_recovery_by_year.png`
- `falcon9_model_confusion_matrix.png`

### Interactive Maps and Reports

```text
notebooks/reports/
```

Includes:

- `falcon9_launch_outcomes_map.html`
- `falcon9_launch_sites_map.html`
- `falcon9_model_comparison.csv`
- `falcon9_model_evaluation.json`

The HTML maps can be opened in a web browser.

### Saved Model

```text
notebooks/models/falcon9_recovery_classifier.joblib
```

The saved model is a Python serialization artifact. Only load it from a trusted source and preferably with compatible package versions.

Serialized scikit-learn models are not guaranteed to work across all library versions.

## 11. Power BI Dashboard

Report location:

```text
dashboards/power-bi/SpaceX_Falcon9_Analytics.pbix
```

Screenshot:

```text
dashboards/screenshots/Executive-Overview.png
```

Workflow documentation:

```text
dashboards/docs/Power_BI_Workflow_GitHub.md
```

Open the `.pbix` file using Microsoft Power BI Desktop.

### Refreshing Data

The Power BI file may contain a local file-source path from the development computer.

If refresh fails:

1. Open the report in Power BI Desktop.
2. Navigate to **Transform data → Data source settings**.
3. Identify the historical launch CSV source.
4. Update its path to the local copy:

```text
notebooks/data/processed/falcon9_launches_historical.csv
```

5. Apply changes and refresh the report.
6. Verify the dashboard measures and visuals.

The report's embedded data may remain viewable even if the original source path is unavailable.

### Dashboard Validation Reference

For the full historical recovery dataset:

| Measure | Expected value |
|---|---:|
| Total launches | 90 |
| Successful recorded landings | 60 |
| Other recorded outcomes | 30 |
| Recorded landing success rate | 66.7% |
| Average payload mass | Approximately 6.10K kg |

These values are useful for checking that the dashboard loads the expected dataset.

## 12. Validation Checks

After running the analysis, confirm:

- Input datasets load without unexpected errors.
- Historical recovery data contains the expected 90 records.
- Outcome classifications match the intended definitions.
- Generated CSV and JSON files are written to the expected directories.
- Visualisation files can be opened.
- Folium maps render in a browser.
- Model evaluation results are generated.
- The Dash application launches.
- Power BI displays the expected historical totals.

If results differ, investigate package versions, input data changes, missing values, random seeds, working-directory settings and transformations before assuming the new results are incorrect.

## 13. Known Limitations

### Historical Data

The project is based on historical data and does not represent current Falcon 9 launch performance.

### Multiple Dataset Populations

The recovery, SQL and Wikipedia datasets serve different analytical purposes and may contain different record counts.

### Outcome Definition

The binary target distinguishes recorded successful landings from other outcomes.

A classification of 0 does not necessarily identify a failed landing attempt.

### External Dependencies

Online resources may become unavailable or change format.

Cached and archived inputs help reduce this dependency.

### Environment Differences

Package releases and Python versions can affect execution, numerical results and saved-model compatibility.

### Reproducibility Verification

A complete clean-room run, including every notebook and the Power BI refresh, remains a recommended final validation step.

## 14. Future Improvements

- Pin and validate dependency versions.
- Add automated data-quality tests.
- Standardise file paths relative to the repository.
- Add automated notebook execution checks.
- Record model training configuration and random seeds.
- Document the exact development environment.
- Add a GitHub Actions validation workflow.

## Author

**Kanwar Kandolha**

GitHub: https://github.com/Kan-21

Project repository: https://github.com/Kan-21/IBM-Applied-Data-Science-Capstone

