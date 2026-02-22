CREATE OR REPLACE VIEW vw_compromised_servers AS
SELECT 
    s.department,
    s.server_id,
    s.ip_address,
    s.os_version,
    t.threat,
    t.risk_level,
    t.dateadded AS date_compromised
FROM internal_servers s
INNER JOIN active_threats t 
    ON s.ip_address = t.domain_or_ip;