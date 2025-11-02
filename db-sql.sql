-- ----------------------------------------------------------------------
-- DANGER: This script will drop ALL data from the listed tables!
-- Use ONLY for development environment setup.
-- ----------------------------------------------------------------------

-- Drop all tables to ensure a clean slate
DROP TABLE IF EXISTS transactions CASCADE;
DROP TABLE IF EXISTS histories CASCADE;
DROP TABLE IF EXISTS documents CASCADE;


-- ----------------------------------------------------------------------
-- 1. Create the TransactionModel Table
-- ----------------------------------------------------------------------
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    description VARCHAR NOT NULL,
    account_id INTEGER NOT NULL,
    -- Amount: FLOAT(2) corresponds to double precision in PostgreSQL for SQLAlchemy
    amount DOUBLE PRECISION NOT NULL,
    -- created_at: Defaults to the time the row is inserted
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    -- updated_at: Note: We cannot set an automatic 'on update' trigger 
    -- directly with standard SQL in this way. SQLAlchemy handles the 'onupdate' logic.
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Add index for quick lookups
CREATE INDEX ix_transactions_id ON transactions (id);
CREATE INDEX ix_transactions_description ON transactions (description);


-- ----------------------------------------------------------------------
-- 2. Create the DocumentModel Table
-- ----------------------------------------------------------------------
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    account_id INTEGER NOT NULL,
    name VARCHAR NOT NULL,
    
    -- file_type: VARCHAR(50) NOT NULL, default 'statement'
    file_type VARCHAR(50) NOT NULL DEFAULT 'statement',
    
    -- status: VARCHAR(50) NOT NULL, default 'pending'
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    
    -- created_at: Defaults to the time the row is inserted
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    -- updated_at: Note: We cannot set an automatic 'on update' trigger 
    -- directly with standard SQL in this way. SQLAlchemy handles the 'onupdate' logic.
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Add index for quick lookups
CREATE INDEX ix_documents_id ON documents (id);
