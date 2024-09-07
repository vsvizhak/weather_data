CREATE TABLE stg_weather_data (
    id                      BIGINT,
    main                    VARCHAR(50),
    description             VARCHAR(100),
    icon                    VARCHAR(10),
    meta_visibility         INTEGER,
    meta_dt                 TIMESTAMPTZ,
    meta_id                 BIGINT,
    meta_name               VARCHAR(100),
    coord_lon               FLOAT8,
    coord_lat               FLOAT8,
    sys_country             VARCHAR(10),
    sys_timezone            INTEGER,
    sys_sunrise             TIMESTAMPTZ,
    sys_sunset              TIMESTAMPTZ,
    main_temp               FLOAT8,
    main_feels_like         FLOAT8,
    main_temp_min           FLOAT8,
    main_temp_max           FLOAT8,
    main_pressure           FLOAT8,
    main_grnd_level         FLOAT8,
    main_humidity           INTEGER,
    main_sea_level          FLOAT8,
    wind_speed              FLOAT8,
    wind_deg                INTEGER,
    clouds_all              INTEGER
);


