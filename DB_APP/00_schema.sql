create user app_admin with password 'app_admin';
CREATE USER etl WITH PASSWORD 'etl';

CREATE SCHEMA STG;
CREATE SCHEMA CORE;

GRANT USAGE ON SCHEMA stg TO etl;
GRANT ALL PRIVILEGES ON ALL TABLES IN schema stg TO app_admin;
GRANT ALL PRIVILEGES ON ALL TABLES IN schema stg TO etl;




SELECT * FROM pg_user;

revoke all privileges on database postgres from etl;
drop user etl;

grant insert on stg.weather_data to etl;