import openmeteo_requests
import requests_cache
from retry_requests import retry
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

# def 获取 CSV 数据
def read_csv(dataset_path, city_name, start_date, end_date):
    history_pd = pd.read_csv(dataset_path)  #'./dataset/MY.csv'
    city_history_pd = history_pd[
        (history_pd['date'] >= start_date) &
        (history_pd['date'] <= end_date) &
        (history_pd['city'] == city_name)]  #'Sabah, Malaysia(#1 24%)'
    return city_history_pd


# def 获取 OM 数据
def request_openmeteo_data(start_date, end_date, latitude, longitude, daily):
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)
    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "start_date": start_date,
        "end_date": end_date,
        "latitude": latitude,
        "longitude": longitude,
        "daily": daily
    }
    responses = openmeteo.weather_api(url, params=params)
    return responses


# def API 样本➜省份
def process_sample_data(responses):
    df_all_sample = pd.DataFrame()
    for response in responses:
        daily = response.Daily()
        daily_temperature_2m_mean = daily.Variables(0).ValuesAsNumpy()
        daily_precipitation_sum = daily.Variables(1).ValuesAsNumpy()
        daily_soil_moisture_7_to_28cm_mean = daily.Variables(2).ValuesAsNumpy()
        # 日期
        daily_data = {"date": pd.date_range(
            start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
            end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
            freq = pd.Timedelta(seconds = daily.Interval()),
            inclusive = "left"
        )}
        # 指标
        daily_data["temperature_2m_mean"] = daily_temperature_2m_mean
        daily_data["precipitation_sum"] = daily_precipitation_sum
        daily_data["soil_moisture_7_to_28cm_mean"] = daily_soil_moisture_7_to_28cm_mean
        #整合
        daily_dataframe = pd.DataFrame(data = daily_data)
        df_all_sample = pd.concat([df_all_sample, daily_dataframe], ignore_index=True)
    # 样本合并
    df_l2 = df_all_sample.groupby('date', as_index=False)[['temperature_2m_mean', 'precipitation_sum', 'soil_moisture_7_to_28cm_mean']].mean()

    return df_l2


# def 数据处理
def polt_data_prepare(merge_pd):
    # 转换：date 列为 datetime 类型
    merge_pd['date'] = pd.to_datetime(merge_pd['date'], errors='coerce')
    # 添加：年份列
    merge_pd['year'] = merge_pd['date'].dt.year
    # 添加：日序列
    merge_pd['day_of_year'] = merge_pd['date'].dt.dayofyear
    # 添加：累计降水列
    merge_pd['cum_sum_precipitation_sum'] = merge_pd.groupby('year')['precipitation_sum'].cumsum()
    # 添加：7日降水和
    merge_pd['precip_sum7'] = merge_pd['precipitation_sum'].rolling(window=7, min_periods=1).sum()
    # # 添加：30日降水和
    # merge_pd['precip_sum30'] = merge_pd['precipitation_sum'].rolling(window=30, min_periods=1).sum()
    # # 添加：5日气温平均
    # merge_pd['temper_ma5'] = merge_pd['temperature_2m_mean'].rolling(window=5, min_periods=1).mean()
    # 处理闰年
    merge_pd = merge_pd[merge_pd['day_of_year'] <= 365]
    # 积温
    merge_pd = merge_pd.assign(t=0.0)
    mask = (merge_pd['day_of_year'] > 105) & (merge_pd['temperature_2m_mean'] >= 10)
    merge_pd.loc[mask, 't'] = merge_pd.loc[mask, 'temperature_2m_mean']
    merge_pd.loc[:, 'degree_day'] = merge_pd.groupby('year')['t'].cumsum()
    merge_pd.drop(columns = ['t'], inplace = True)

    return merge_pd