SET SEARCH_PATH = "core";

CREATE TABLE dim_city (
    city_id                 BIGINT,
    city_name               VARCHAR(100),
    city_lon                DOUBLE PRECISION,
    city_lat                DOUBLE PRECISION,
    city_country            VARCHAR(10),
    city_timezone           INTEGER
);

CREATE TABLE dim_weather (
    weather_id              INTEGER,
    weather_main            VARCHAR(50),
    weather_description     VARCHAR(100),
    weather_icon            VARCHAR(10)
);

CREATE TABLE fct_weather_data (
    dt                      TIMESTAMPTZ,
    weather_id              INTEGER,
    city_id                 BIGINT,
    main_temp               DOUBLE PRECISION,
    main_feels_like         DOUBLE PRECISION,
    main_temp_min           DOUBLE PRECISION,
    main_temp_max           DOUBLE PRECISION,
    main_pressure           DOUBLE PRECISION,
    main_humidity           INTEGER,
    visibility              INTEGER,
    wind_speed              DOUBLE PRECISION,
    wind_deg                DOUBLE PRECISION,
    clouds_all              INTEGER,
    sunrise                 TIMESTAMPTZ,
    sunset                  TIMESTAMPTZ
);