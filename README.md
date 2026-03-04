

# Contract Data Pipeline -- Python / SQL / Selenium → Analytics-Ready Dataset

## What this is

A production-style data pipeline that extracts, normalizes, and prepares
contract opportunity data from a third-party system for downstream analytics
and reporting.

**Why it matters:**  
The third-party platform functioned as the system of record for opportunity and
capture data, but its isolation from internal analytics environments created
significant operational friction. Teams relied on manual exports and re-entry,
introducing latency, data quality risk, and limited visibility into the true
state of the sales pipeline.

This pipeline establishes a reliable analytical foundation by programmatically
extracting and standardizing pipeline data into an analytics-ready dataset.
Because key fields in this dataset are reused throughout the business
lifecycle—from proposal and award through contract execution and future
business development—the workflow improves cross-functional alignment and
enables more consistent, data-driven pipeline and revenue decisions.

---

## ⚠️ Public version note (important)

This repository is a **sanitized reference implementation** of an internal
pipeline I built in a production environment.

To protect proprietary systems and data:

- Live endpoints are redacted  
- Credentials and MFA flow are removed  
- Sample outputs are illustrative only  
- The script is intentionally non-runnable  

**Purpose:** demonstrate pipeline architecture, data-wrangling patterns, and
analytics engineering approach.

---

## Decision context (business framing)

**Primary question supported:**  
> What does our true pipeline look like once custom capture fields and nested
> metadata are normalized into an analytics-ready dataset?

**Stakeholders**

- Business Development / Capture  
- Sales Operations  
- Finance & FP&A  
- Executive leadership  
- Analytics teams  

**Decisions enabled**

- Pipeline health and coverage analysis  
- Opportunity segmentation and prioritization  
- Capture performance tracking  
- Downstream forecasting inputs  

---

## What the pipeline does (end-to-end)

### 1. Authenticated session handling
- Uses Selenium to establish an authenticated session  
- Extracts session cookies for API reuse  
- Demonstrates hybrid browser/API pattern common in enterprise systems  

### 2. Metadata discovery
- Dynamically retrieves custom field definitions  
- Maps field IDs → human-readable names  
- Builds reusable filter structures  

### 3. Paginated data extraction
- Pulls large opportunity datasets via API  
- Handles multi-page retrieval  
- Applies structured request filters  

### 4. Data transformation & normalization
- Expands nested custom capture fields  
- Aligns schema across records  
- Standardizes date formats  
- Handles null and missing values  

### 5. Analytics-ready output
- Produces flattened dataset suitable for:
  - BI dashboards  
  - pipeline analytics  
  - forecasting models  
  - ad hoc analysis  

---

## Repository structure
```text
contract-data-pipeline/
├── src/
│   └── c2p_functions.py        # core pipeline utilities
├── internal_example/
│   └── run_pipeline_REDACTED.py # sanitized runner
├── dashboards/
│   └── screenshots/             # sample outputs
├── docs/
│   └── architecture.md          # (in process)
├── requirements.txt
└── README.md
```


---

## Tech stack

**Languages & libraries**

- Python (pandas, numpy, requests)  
- Selenium (session bootstrap pattern)  

**Data engineering patterns**

- Cookie-based API authentication  
- Paginated extraction  
- JSON normalization  
- Custom field mapping  
- Schema standardization  

**Downstream compatibility**

- Tableau / Power BI  
- SQL warehouses  
- forecasting workflows  
- GTM analytics  

---

## Example output (illustrative)

<!-- *(Insert your screenshots here)*

- Pipeline dataset preview  
- Custom field expansion example  
- Cleaned analytics table  
-->

---

## What this code demonstrates

This project is intended to showcase **production-relevant analytics engineering
capabilities**, including:

- Designing resilient data extraction workflows  
- Handling authenticated enterprise systems  
- Normalizing highly nested JSON structures  
- Building reusable data preparation utilities  
- Preparing messy operational data for executive analytics  

---

## Limitations of the public version

Because this is a sanitized reference:

- Not intended to be executed as-is  
- External system access removed  
- Some values replaced with placeholders  
- Debug exports disabled  

---

## Future enhancements (roadmap)

- Revenue and pipeline forecasting layer  
- dbt-style transformation model  
- orchestration (Airflow/Prefect)  
- automated data quality checks  
- semantic metrics layer  

---

## About me

I’m a Business Intelligence & Analytics professional with a background in
Operations Research, focused on building data products that support strategic
decision-making.

**Target roles**

- Strategic Analytics  
- Decision Intelligence  
- GTM Analytics  
- Analytics Engineering  
- Data Science (business-facing)

---

