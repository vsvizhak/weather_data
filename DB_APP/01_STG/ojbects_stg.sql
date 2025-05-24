CREATE TABLE stg.weather_data (
    weather_id              INTEGER,
    weather_main            VARCHAR(50),
    weather_description     VARCHAR(100),
    weather_icon            VARCHAR(10),
    visibility              INTEGER,
    dt                      TIMESTAMPTZ,
    city_id                 BIGINT,
    city_name               VARCHAR(100),
    city_lon                DOUBLE PRECISION,
    city_lat                DOUBLE PRECISION,
    city_country            VARCHAR(10),
    city_timezone           INTEGER,
    sunrise                 TIMESTAMPTZ,
    sunset                  TIMESTAMPTZ,
    main_temp               DOUBLE PRECISION,
    main_feels_like         DOUBLE PRECISION,
    main_temp_min           DOUBLE PRECISION,
    main_temp_max           DOUBLE PRECISION,
    main_pressure           DOUBLE PRECISION,
    main_grnd_level         DOUBLE PRECISION,
    main_humidity           INTEGER,
    main_sea_level          DOUBLE PRECISION,
    wind_speed              DOUBLE PRECISION,
    wind_deg                INTEGER,
    clouds_all              INTEGER,
    load_id                 INTEGER,
    load_date               TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE stg.weather_data_loads (
    load_id SERIAL PRIMARY KEY,
    load_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

create table stg.stg_geonames
(
    geonameid         bigint,
    name              varchar(255),
    asciiname         varchar(255),
    alternatenames    varchar(10000),
    latitude          double precision,
    longitude         double precision,
    feature_class     varchar(255),
    feature_code      varchar(255),
    country_code      varchar(255),
    cc2               varchar(255),
    admin1_code       varchar(255),
    admin2_code       varchar(255),
    admin3_code       varchar(255),
    admin4_code       varchar(255),
    population        bigint,
    elevation         double precision,
    dem               bigint,
    timezone          text,
    modification_date text,
    load_date         TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

create table stg_owm_city
(
    id          double precision,
    name        varchar(255),
    state       varchar(255),
    country     varchar(255),
    coord_lon   double precision,
    coord_lat   double precision,
    load_date   timestamp
);



