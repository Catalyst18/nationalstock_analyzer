CREATE OR REPLACE VIEW nse_analyzer.v_nse_report_generator
AS WITH stageing_data AS (
         SELECT lead(stage_raw_nse_data.limit_amount) OVER (PARTITION BY stage_raw_nse_data.company_name ORDER BY stage_raw_nse_data.report_date) AS previous_limit,
            max(stage_raw_nse_data.report_date::text) OVER (PARTITION BY stage_raw_nse_data.company_name) AS mx_date,
            stage_raw_nse_data.mwpl_amount AS curr_limit,
            stage_raw_nse_data.report_date,
            stage_raw_nse_data.isin_id,
            stage_raw_nse_data.company_name,
            stage_raw_nse_data.company_symbol,
            stage_raw_nse_data.insert_time
           FROM nse_analyzer.stage_raw_nse_data
        )
 SELECT date_part('day'::text, to_date(stageing_data.report_date::text, 'DD-MON_YYYY'::text))::text AS days,
    stageing_data.isin_id,
    stageing_data.company_name,
    stageing_data.company_symbol,
    stageing_data.report_date,
    stageing_data.curr_limit,
    stageing_data.previous_limit,
    round(stageing_data.previous_limit::numeric / stageing_data.curr_limit::numeric * 100::numeric, 2)::bigint AS percentage
   FROM stageing_data
  WHERE to_date(stageing_data.report_date::text, 'DD-MON-YYYY'::text) >= date_trunc('month'::text, CURRENT_DATE::timestamp with time zone);

-- Permissions

ALTER TABLE nse_analyzer.v_nse_report_generator OWNER TO postgres;
GRANT ALL ON TABLE nse_analyzer.v_nse_report_generator TO postgres;
