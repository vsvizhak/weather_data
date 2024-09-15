/*
 Load weather data to fact table CORE.FCT_WEATHER_DATA
 set search_path = "core";
*/
CREATE OR REPLACE PROCEDURE SP_LOAD_FCT_WEATHER_DATA ()
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO core.fct_weather_data
    SELECT
        dt,
        weather_id,
        city_id,
        main_temp,
        main_feels_like,
        main_temp_min,
        main_temp_max,
        main_pressure,
        main_humidity,
        visibility,
        wind_speed,
        wind_deg,
        clouds_all,
        sunrise,
        sunset
    FROM stg.weather_data;
END;
$$