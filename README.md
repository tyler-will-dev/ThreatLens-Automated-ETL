ThreatLens: Automated Threat Intelligence ETL & BI Pipeline
📊 Project Overview
ThreatLens is an end-to-end automated ETL (Extract, Transform, Load) pipeline and Business Intelligence dashboard designed to monitor and analyze active malware threats. This project ingests live, unstructured threat data, engineers it into a relational data model, and visualizes the risk landscape to internal corporate assets using Power BI.

This project demonstrates full-stack data architecture, bridging the gap between backend data engineering (Python/SQL) and frontend business intelligence.

🛠️ Technology Stack
Extraction & Transformation: Python, pandas, requests, urllib

Database / Data Warehouse: PostgreSQL (Cloud-Hosted via Neon.tech), SQLAlchemy

Data Modeling & SQL: Standard SQL (DDL & DML), CREATE VIEW, INNER JOIN

Business Intelligence: Power BI, DAX (Data Analysis Expressions)

⚙️ The Data Architecture
1. Extract (Automated Ingestion)
The pipeline begins by programmatically connecting to the URLhaus API (Abuse.ch) to ingest a live, constantly updating CSV feed of known malicious URLs. The script uses the requests library to handle HTTP connections and bypasses raw metadata headers to capture the core payload.

2. Transform (Data Cleansing & Feature Engineering)
Raw threat feeds are notoriously messy. The pipeline utilizes pandas to perform heavy lifting before the data ever reaches the database:

Data Cleansing: Standardized column nomenclature, handled null values (NaN), and casted string objects to proper datetime formats for accurate time-series analysis.

Feature Engineering: Built custom string-parsing functions using urlparse to strip ports and file paths from raw URLs, isolating the core domain_or_ip to allow for relational joining.

Conditional Logic: Applied tiered categorization logic to create a new risk_level metric (High/Medium/Low) based on the specific malware family (e.g., Botnet, Phishing).

3. Load (Cloud Relational Database)
To mimic an enterprise environment, local flat files were discarded in favor of a cloud-based PostgreSQL database.

Utilized SQLAlchemy to establish a secure connection to the remote server.

Executed a full-refresh load (if_exists='replace') to automate daily batch updates for both the external threat feed and a mock inventory of internal corporate servers.

4. Upstream Data Modeling (SQL)
To optimize Business Intelligence performance, heavy data transformations were pushed "upstream" to the database layer.

Authored a standard SQL CREATE VIEW utilizing an INNER JOIN to actively map compromised external IPs directly to internal server IPs. This creates a pre-filtered, virtual table of active internal breaches, significantly reducing the compute load on the Power BI frontend.

5. Business Intelligence & Analytics (Power BI)
Connected Power BI directly to the cloud PostgreSQL database to build an interactive, cross-filtered SOC (Security Operations Center) dashboard.

DAX Formulas: Authored custom DAX measures (leveraging CALCULATE and dynamic filter context) to track live KPIs, such as total compromised servers.

Interactive Visualizations: Designed intuitive dashboards featuring funnel analysis, malware distribution categorizations, and time-series line charts to track threat spikes over time. Cross-filtering allows stakeholders to drill down into specific cohorts without writing custom SQL.

🚀 How to Run Locally
Clone this repository to your local machine.

Install the required Python dependencies:

Bash
pip install pandas requests sqlalchemy psycopg2-binary
Insert your PostgreSQL connection string into the DATABASE_URL variable inside etl_pipeline.py.

Run the ETL script: python etl_pipeline.py

Connect your BI tool of choice to your database to visualize the newly generated tables and views.
