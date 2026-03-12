CREATE TABLE IF NOT EXISTS cve (
    cve_id TEXT PRIMARY KEY,
    cve_description TEXT,
    published_date TEXT,
    cvss_score REAL,
    severity TEXT CHECK (severity IN ("LOW", "MEDIUM", "HIGH", "CRITICAL")),
    cve_status TEXT
);

CREATE TABLE IF NOT EXISTS cwe (
    cwe_id TEXT PRIMARY KEY,
    cwe_name TEXT
);

CREATE TABLE IF NOT EXISTS cve_cwe (
    cve_id TEXT,
    cwe_id TEXT,
    FOREIGN KEY (cve_id) REFERENCES cve(cve_id),
    FOREIGN KEY (cwe_id) REFERENCES cwe(cwe_id),
    PRIMARY KEY (cve_id, cwe_id)
);

-- CREATE TABLE IF NOT EXISTS vendor (
--     vendor_id INTEGER PRIMARY KEY AUTOINCREMENT,
--     vendor_name TEXT
-- );

-- CREATE TABLE IF NOT EXISTS cve_vendor (
--     cve_id TEXT,
--     vendor_id INT,
--     FOREIGN KEY (cve_id) REFERENCES cve(cve_id),
--     FOREIGN KEY (vendor_id) REFERENCES vendor(vendor_id),
--     PRIMARY KEY (cve_id, vendor_id)
-- );