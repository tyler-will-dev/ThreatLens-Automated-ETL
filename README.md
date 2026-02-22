<div align="center">
  <h1>🛡️ ThreatLens</h1>
  <p><b>Automated Threat Intelligence ETL & BI Pipeline</b></p>

  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black" alt="Power BI" />
</div>

<br>

> **Project Overview:** An end-to-end automated ETL (Extract, Transform, Load) pipeline and Business Intelligence dashboard designed to ingest unstructured live threat feeds, engineer the data relationally, and visualize the risk to internal corporate assets.

---

## ⚙️ The Data Architecture

### 1. Extract (Automated Ingestion)
The pipeline begins by programmatically connecting to the **URLhaus API** (Abuse.ch) to ingest a live, constantly updating CSV feed of known malicious URLs. The script bypasses raw metadata headers to cleanly capture the core payload.

### 2. Transform (Data Cleansing & Feature Engineering)
Raw threat feeds are notoriously messy. The pipeline utilizes `pandas` to perform heavy lifting before the data ever reaches the database:
* **Data Cleansing:** Standardized column nomenclature, handled null values (`NaN`), and casted strings to proper `datetime` objects for time-series analysis.
* **Feature Engineering:** Built custom string-parsing utilizing `urlparse` to strip ports and file paths from raw URLs, isolating the core `domain_or_ip` to allow for relational database joining.
* **Categorization Logic:** Applied logic to create a new `risk_level` metric (High/Medium/Low) based on the specific malware family (e.g., Botnet, Phishing).

### 3. Load (Cloud Relational Database)
To mimic a true enterprise environment, the pipeline pushes data directly to a cloud-based **PostgreSQL** data warehouse. 
* Utilized `SQLAlchemy` to establish a secure connection pool.
* Executed a full-refresh load to automate daily batch updates for both the external threat feed and a mock inventory of internal corporate servers.

### 4. Upstream Data Modeling (SQL)
To optimize Business Intelligence performance, heavy data transformations were pushed "upstream" to the database layer. 
* Authored a standard SQL `CREATE VIEW` utilizing an `INNER JOIN` to actively map compromised external IPs directly to internal server IPs. 
* This creates a pre-filtered, virtual table of active internal breaches, significantly reducing the compute load on the Power BI frontend.

### 5. Business Intelligence (Power BI)
Connected Power BI directly to the cloud PostgreSQL database to build an interactive, cross-filtered SOC (Security Operations Center) dashboard.
* **DAX Formulas:** Authored custom DAX measures leveraging `CALCULATE` and dynamic filter context to track live KPIs.
* **Interactive Visualizations:** Designed intuitive dashboards featuring funnel analysis, malware distribution categorizations, and time-series line charts. 

---

## 🚀 How to Run Locally
1. **Clone the repository:**
   git clone [https://github.com/yourusername/ThreatLens.git](https://github.com/yourusername/ThreatLens.git)
2. **Install dependencies:**
  pip install pandas requests sqlalchemy psycopg2-binary

3. **Configure Environment:**
  Create a .env file in the root directory and add your PostgreSQL connection string:
  Example --> DATABASE_CONNECTION_STRING=postgresql://user:password@server/db

4. **Execute the Pipeline:**
  python etl_pipeline.py
