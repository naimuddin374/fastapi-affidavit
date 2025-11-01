-- DEVELOPMENT ENVIRONMENT INITIALIZATION SCRIPT
-- This script performs cleanup of old migration data and creates all tables.
-- Run this manually whenever you need a fresh database slate (e.g., after dropping the database).

---
-- 2. DROP EXISTING TABLES
-- Uncomment the DROP TABLE commands below if you want to completely reset
-- your data and schema to an empty state every time this script runs.
-- WARNING: This will DELETE ALL DATA from these tables.
---

-- DROP TABLE IF EXISTS transactions;
-- DROP TABLE IF EXISTS histories;
-- DROP TABLE IF EXISTS documents;


---
-- 3. CREATE INITIAL TABLES (Schema Definition based on current models)
-- Note: Replace INTEGER with SERIAL or BIGSERIAL if you need auto-incrementing IDs.
-- PostgreSQL typically uses SERIAL for auto-incrementing primary keys.
---

CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    -- Add table specific columns here
    account_id INTEGER,
    description VARCHAR(255) NOT NULL,
    amount NUMERIC(10, 2) NOT NULL, -- Using NUMERIC for precise currency representation
    created_at TIMESTAMP WITHOUT TIME ZONE
);

CREATE TABLE IF NOT EXISTS histories (
    id SERIAL PRIMARY KEY,
    -- Add table specific columns here
    account_id INTEGER,
    event_type VARCHAR(50) NOT NULL,
    user_id INTEGER,
    timestamp TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    -- Add table specific columns here
    account_id INTEGER,
    title VARCHAR(255) NOT NULL,
    file_path VARCHAR(255) NOT NULL,
    file_type VARCHAR(50), -- Added based on your autogenerate detection
    upload_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);


-- Optional: Add indexes for frequently searched columns
CREATE INDEX IF NOT EXISTS idx_transactions_description ON transactions (description);
CREATE INDEX IF NOT EXISTS idx_histories_event_type ON histories (event_type);
