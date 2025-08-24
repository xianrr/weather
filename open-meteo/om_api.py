import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry
def request_openmeteo_api(latitude:list[str],
                          longitude:list[str],
                          start_date:str,
                          end_date:str,
                          daily_indicators:list[str]) -> pd.DataFrame:
    '''
    The len(latitude) and len(longitude) entered must be equal.
    Latitude would be positive (negative) when a location is in the north (south) of the equator.
    Longitude would be positive (negative) when a location is in the east (west) of the prime meridian.
    The available parameters of daily_indicators please refer: https://open-meteo.com/en/docs/historical-weather-api

    :param latitude:         [float, ...]
    :param longitude:        [float, ...]
    :param start_date:       "YYYY-MM-DD"
    :param end_date:         "YYYY-MM-DD"
    :param daily_indicators: [String, ...]
    :return:pd.DataFrame:    [[ "date", "latitude", "longitude", daily_indicators[0], ...]]
    '''
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "daily": daily_indicators
    }
    responses = openmeteo.weather_api(url, params=params)

    request_pd = pd.DataFrame()

    for response in responses:
        # 日度指标数据
        daily_datas = response.Daily()
        # 日期列
        daily_dic = {"date": pd.date_range(
            start = pd.to_datetime(daily_datas.Time(), unit = "s", utc = True),
            end = pd.to_datetime(daily_datas.TimeEnd(), unit = "s", utc = True),
            freq = pd.Timedelta(seconds = daily_datas.Interval()),
            inclusive = "left"
        )}
        # 维度列、经度列
        daily_dic["LocationID"] = response.LocationId()
        daily_dic["latitude"] = response.Latitude()
        daily_dic["longitude"] = response.Longitude()

        # 指标列
        i = 0
        for daily_indicator in daily_indicators:
            daily_dic[daily_indicator] = daily_datas.Variables(i).ValuesAsNumpy()
            i = i + 1

        daily_pd = pd.DataFrame(data = daily_dic)
        request_pd = pd.concat([request_pd, daily_pd])

    return request_pd

def om_request_api(expire_after:int,
                   url:str,
                   latitude:list[str],
                   longitude:list[str],
                   start_date:str,
                   end_date:str,
                   daily_indicators:list[str])-> pd.DataFrame:
    cache_session = requests_cache.CachedSession('.cache', expire_after = expire_after)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "daily": daily_indicators
    }
    responses = openmeteo.weather_api(url, params=params)

    request_df = pd.DataFrame()

    for response in responses:
        # 日度指标数据
        daily_datas = response.Daily()
        # 日期列
        daily_dic = {"date": pd.date_range(
            start = pd.to_datetime(daily_datas.Time(), unit = "s", utc = True),
            end = pd.to_datetime(daily_datas.TimeEnd(), unit = "s", utc = True),
            freq = pd.Timedelta(seconds = daily_datas.Interval()),
            inclusive = "left"
        )}
        # 维度列、经度列
        daily_dic["LocationID"] = response.LocationId()
        daily_dic["latitude"] = response.Latitude()
        daily_dic["longitude"] = response.Longitude()

        # 指标列
        i = 0
        for daily_indicator in daily_indicators:
            daily_dic[daily_indicator] = daily_datas.Variables(i).ValuesAsNumpy()
            i = i + 1

        daily_df = pd.DataFrame(data = daily_dic)
        request_df = pd.concat([request_df, daily_df])

    return request_df

def om_daily_history(latitude:list[str],
                     longitude:list[str],
                     start_date:str,
                     end_date:str,
                     daily_indicators:list[str]):
    expire_after = -1
    url = "https://archive-api.open-meteo.com/v1/archive"
    history_df = om_request_api(expire_after, url,
                                latitude, longitude,
                                start_date, end_date,
                                daily_indicators)
    return history_df

def om_daily_forecast(latitude:list[str],
                      longitude:list[str],
                      start_date:str,
                      end_date:str,
                      daily_indicators:list[str]):
    expire_after = 3600
    url = "https://api.open-meteo.com/v1/forecast"
    forecast_df = om_request_api(expire_after, url,
                                 latitude, longitude,
                                 start_date, end_date,
                                 daily_indicators)
    return forecast_df