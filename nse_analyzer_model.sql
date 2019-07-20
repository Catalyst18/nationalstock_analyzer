/*
Created: 19/07/2019
Modified: 20/07/2019
Project: postgres_nse_analyzer
Model: RE PostgreSQL 10
Database: PostgreSQL 10
*/


-- Create schemas section -------------------------------------------------

CREATE SCHEMA "nse_analyzer" AUTHORIZATION "postgres"
;

CREATE SCHEMA "public" AUTHORIZATION "postgres"
;

COMMENT ON SCHEMA "public" IS 'standard public schema'
;

-- Create tables section -------------------------------------------------

-- Table nse_analyzer.D_NSE_COMPANIES

CREATE TABLE "nse_analyzer"."D_NSE_COMPANIES"(
 "company_id" Integer DEFAULT nextval('nse_analyzer."D_NSE_COMPANIES_company_id_seq"'::regclass) NOT NULL,
 "ISIN_ID" Character varying NOT NULL,
 "COMPANY_NAME" Character varying NOT NULL,
 "COMPANY_SYMBOL" Character varying NOT NULL
)
WITH (
 autovacuum_enabled=true)
;

-- Add keys for table nse_analyzer.D_NSE_COMPANIES

ALTER TABLE "nse_analyzer"."D_NSE_COMPANIES" ADD CONSTRAINT "PK_D_NSE_COMPANIES" PRIMARY KEY ("company_id","ISIN_ID")
;

ALTER TABLE "nse_analyzer"."D_NSE_COMPANIES" ADD CONSTRAINT "company_id" UNIQUE ("company_id")
;

-- Table nse_analyzer.F_MWPL

CREATE TABLE "nse_analyzer"."F_MWPL"(
 "F_MWPL_ID" Integer DEFAULT nextval('nse_analyzer."F_MWPL_F_MWPL_ID_seq"'::regclass) NOT NULL,
 "MWPL_AMOUNT" Integer NOT NULL,
 "REPORTED_DATE" Date NOT NULL,
 "company_id" Integer DEFAULT nextval('nse_analyzer."D_NSE_COMPANIES_company_id_seq"'::regclass) NOT NULL,
 "ISIN_ID" Character varying NOT NULL
)
WITH (
 autovacuum_enabled=true)
;

-- Add keys for table nse_analyzer.F_MWPL

ALTER TABLE "nse_analyzer"."F_MWPL" ADD CONSTRAINT "PK_F_MWPL" PRIMARY KEY ("F_MWPL_ID","company_id","ISIN_ID")
;

ALTER TABLE "nse_analyzer"."F_MWPL" ADD CONSTRAINT "F_MWPL_ID" UNIQUE ("F_MWPL_ID")
;

-- Table nse_analyzer.F_OPEN_INTEREST_LIMIT

CREATE TABLE "nse_analyzer"."F_OPEN_INTEREST_LIMIT"(
 "AMOUNT_ID" Integer DEFAULT nextval('nse_analyzer."F_OPEN_INTEREST_LIMIT_AMOUNT_ID_seq"'::regclass) NOT NULL,
 "OPEN_INTEREST" Integer NOT NULL,
 "LIMIT_AMOUNT" Integer,
 "REPORT_DATE" Date,
 "company_id" Integer DEFAULT nextval('nse_analyzer."D_NSE_COMPANIES_company_id_seq"'::regclass) NOT NULL,
 "ISIN_ID" Character varying NOT NULL
)
WITH (
 autovacuum_enabled=true)
;

-- Add keys for table nse_analyzer.F_OPEN_INTEREST_LIMIT

ALTER TABLE "nse_analyzer"."F_OPEN_INTEREST_LIMIT" ADD CONSTRAINT "PK_F_OPEN_INTEREST_LIMIT" PRIMARY KEY ("AMOUNT_ID","company_id","ISIN_ID")
;

ALTER TABLE "nse_analyzer"."F_OPEN_INTEREST_LIMIT" ADD CONSTRAINT "AMOUNT_ID" UNIQUE ("AMOUNT_ID")
;

-- Table nse_analyzer.stage_raw_nse_data

CREATE TABLE "nse_analyzer"."stage_raw_nse_data"(
 "report_date" Character varying NOT NULL,
 "isin_id" Character varying NOT NULL,
 "company_name" Character varying,
 "company_symbol" Character varying,
 "mwpl_amount" Bigint DEFAULT 0,
 "open_interest" Bigint DEFAULT 0,
 "limit_amount" Bigint DEFAULT 0,
 "insert_time" Timestamp
)
WITH (
 autovacuum_enabled=true)
;
-- Create foreign keys (relationships) section ------------------------------------------------- 

ALTER TABLE "nse_analyzer"."F_MWPL" ADD CONSTRAINT "D_NSE_COMPANIES__F_MWPL" FOREIGN KEY ("company_id", "ISIN_ID") REFERENCES "nse_analyzer"."D_NSE_COMPANIES" ("company_id", "ISIN_ID") ON DELETE NO ACTION ON UPDATE NO ACTION
;

ALTER TABLE "nse_analyzer"."F_OPEN_INTEREST_LIMIT" ADD CONSTRAINT "D_NSE_COMPANIES__F_OPEN_INTEREST_LIMIT" FOREIGN KEY ("company_id", "ISIN_ID") REFERENCES "nse_analyzer"."D_NSE_COMPANIES" ("company_id", "ISIN_ID") ON DELETE NO ACTION ON UPDATE NO ACTION
;


-- Grant permissions section -------------------------------------------------

GRANT "pg_read_all_settings" TO "pg_monitor"
;
GRANT "pg_read_all_stats" TO "pg_monitor"
;
GRANT "pg_stat_scan_tables" TO "pg_monitor"
;

