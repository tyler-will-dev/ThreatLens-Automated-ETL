<div align="center">
  <h1>🛡️ ThreatLens</h1>
  <p><b>Automated Threat Intelligence ETL & BI Pipeline</b></p>

  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black" alt="Power BI" />
</div>

<br>

> **Project Overview:** An end to end automated ETL (Extract, Transform, Load) pipeline and Business Intelligence architecture designed to ingest unstructured live threat feeds, engineer the data relationally, and visualize active risks to internal corporate assets.

***

## ⚙️ Pipeline Architecture

### 1. Extract (Automated Ingestion)
The pipeline programmatically connects to the **URLhaus API** (Abuse.ch) to ingest a continuously updating CSV feed of known malicious URLs. The extraction script bypasses raw metadata headers to cleanly capture the core payload, ensuring efficient downstream processing.

### 2. Transform (Data Cleansing & Feature Engineering)
To ensure data integrity before warehouse ingestion, heavy transformations are handled in-memory using `pandas`:
* **Data Cleansing:** Standardized schema nomenclature, sanitized null values (`NaN`), and cast strings to proper `datetime` objects for accurate time series analysis.
* **Feature Engineering:** Implemented custom parsing logic utilizing `urlparse` to strip ports and file paths from raw URLs. This isolates the core `domain_or_ip`, enabling seamless relational joins.
* **Risk Categorization:** Applied conditional logic to generate a custom `risk_level` metric (High/Medium/Low) based on the identified malware family (e.g., Botnet, Phishing).

### 3. Load (Cloud Relational Database)
The pipeline replicates an enterprise environment by pushing processed data directly to a cloud based **PostgreSQL** data warehouse. 
* Utilized `SQLAlchemy` to establish a secure, authenticated connection pool.
* Configured a full refresh load to automate daily batch updates for both the external threat feed and the internal corporate server inventory.

### 4. Upstream Data Modeling (SQL)
To optimize Business Intelligence compute performance, complex data relationships were pushed upstream to the database layer. 
* Implemented a `CREATE VIEW` utilizing an `INNER JOIN` to actively map compromised external IPs directly to internal server IPs. 
* This pre-filtered, virtual table surfaces active internal breaches, significantly reducing the rendering load on the Power BI frontend.

### 5. Business Intelligence (Power BI)
Power BI connects directly to the PostgreSQL warehouse via DirectQuery/Import to power an interactive SOC (Security Operations Center) dashboard.
* **DAX Formulas:** Authored custom DAX measures leveraging `CALCULATE` and dynamic filter contexts to track live security KPIs.
* **Interactive Visualizations:** Designed funnel analysis, malware distribution matrices, and time series charts to provide actionable intelligence for security analysts. 

***

## 🚀 Local Deployment

**1. Clone the repository:**
```bash
git clone [https://github.com/yourusername/ThreatLens.git](https://github.com/yourusername/ThreatLens.git)
cd ThreatLens
```

**2. Install dependencies:**
```bash
pip install pandas requests sqlalchemy psycopg2-binary
```

**3. Configure Environment:**
Create a `.env` file in the root directory and add your PostgreSQL connection string:
```env
DATABASE_CONNECTION_STRING=postgresql://user:password@server/db
```

**4. Execute the Pipeline:**
```bash
python etl_pipeline.py
```
