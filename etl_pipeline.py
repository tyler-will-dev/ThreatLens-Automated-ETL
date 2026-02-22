import os
import pandas as pd
import requests
import io
from urllib.parse import urlparse
from sqlalchemy import create_engine

# |--- Parameters & Configuration ---|
# Target endpoint for the live URLhaus CSV feed
url = "https://urlhaus.abuse.ch/downloads/csv_recent/"

# Securely load the database connection string from environment variables
# This prevents credential leakage in version control (e.g., GitHub)
# Locally, this relies on a .env file. In production, it relies on server secrets
db_url = os.getenv("DATABASE_CONNECTION_STRING")


# |--- Extract ---|
def extract_data(source_url):
    """Fetches live, unstructured threat data from the target API."""
    print("Fetching live threat data from URLhaus...")
    response = requests.get(source_url)
    
    if response.status_code == 200:
        print("Data downloaded successfully!")
        # Skip the first 8 rows of metadata headers to prevent dataframe corruption
        return pd.read_csv(io.StringIO(response.text), skiprows=8)
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None


# |--- Transform ---|
def transform_data(raw_df):
    """Cleans raw threat data and engineers new features for relational mapping."""
    print("\nStarting advanced data transformation...")
    
    # Create a copy to preserve the immutable raw data
    clean_df = raw_df.copy()
    
    # Standardize column nomenclature
    clean_df = clean_df.rename(columns={'# id': 'id'})
    
    # Handle missing values to prevent SQL insertion errors downstream
    clean_df['tags'] = clean_df['tags'].fillna('no_tags')
    
    # Cast temporal strings into strict Datetime objects for time-series analysis
    clean_df['dateadded'] = pd.to_datetime(clean_df['dateadded'], errors='coerce')
    clean_df['last_online'] = pd.to_datetime(clean_df['last_online'], errors='coerce')
    
    # Feature Engineering: Isolate the core IP/Domain from the messy URL string
    def extract_domain(url_string):
        try:
            return urlparse(url_string).netloc.split(':')[0]
        except:
            return "unknown"
            
    clean_df['domain_or_ip'] = clean_df['url'].apply(extract_domain)
    
    # Feature Engineering: Apply categorization logic to determine severity
    def assign_risk(threat_type):
        threat = str(threat_type).lower()
        if 'botnet' in threat or 'malware_download' in threat:
            return 'High'
        elif 'phishing' in threat:
            return 'Medium'
        else:
            return 'Low'
            
    clean_df['risk_level'] = clean_df['threat'].apply(assign_risk)
    
    print("Transformation complete!")
    return clean_df

def generate_internal_servers(threat_df):
    """Generates a mock inventory of internal corporate servers for relational joining."""
    print("\nGenerating mock internal server inventory...")
    
    # Extract a sample of actual malicious IPs to guarantee successful table joins
    compromised_ips = threat_df['domain_or_ip'].dropna().sample(5).tolist()

    # Create safe, localized internal IPs
    safe_ips = [f"192.168.1.{i}" for i in range(10, 20)]
    all_server_ips = compromised_ips + safe_ips
    
    # Map out the server infrastructure hierarchy
    server_data = {
        'server_id': [f"SRV-{i+100}" for i in range(len(all_server_ips))],
        'ip_address': all_server_ips,
        'department': ['Finance', 'HR', 'Engineering', 'Executive', 'Sales'] * 3,
        'os_version': ['Windows Server 2019', 'Ubuntu 20.04', 'Red Hat'] * 5
    }
    
    servers_df = pd.DataFrame(server_data)
    print("Internal server inventory generated!")
    return servers_df


# |--- Load ---|
def load_data_to_cloud(threats_df, servers_df, target_db_url):
    """Pushes the sanitized dataframes directly into a remote PostgreSQL data warehouse."""
    print("\nConnecting to Cloud PostgreSQL Database...")
    
    if not target_db_url:
        print("ERROR: No database connection string found. Check environment variables.")
        return

    # Create the SQLAlchemy engine to manage the cloud connection pool
    engine = create_engine(target_db_url)
    
    # Push the data utilizing a full-refresh strategy (dropping old data)
    print("Loading active threats table...")
    threats_df.to_sql("active_threats", engine, if_exists='replace', index=False)
    
    print("Loading internal servers table...")
    servers_df.to_sql("internal_servers", engine, if_exists='replace', index=False)
    
    print("Success! Both tables are now live in the cloud.")


# |--- Execution Block --- |
if __name__ == "__main__":
    
    raw_data = extract_data(url)
    
    if raw_data is not None:
        cleaned_threats = transform_data(raw_data)
        internal_servers = generate_internal_servers(cleaned_threats)
        
        # Pass the environment variable DATABASE_URL into our cloud loader
        load_data_to_cloud(cleaned_threats, internal_servers, db_url)
        print("\n--- Cloud ETL Pipeline Run Complete ---")