import os
import sqlite3
import pandas as pd

from src import om_api
from datetime import datetime, timedelta

# 数据库路径
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, 'om_palm.db')

# 获取的指标
variables = ['temperature_2m_mean', 'precipitation_sum', 'soil_moisture_7_to_28cm_mean']

def read_sqlite(sql:str):
    conn = sqlite3.connect(db_path)
    try:
       df = pd.read_sql_query(sql, conn)
    finally:
        conn.close()

    return df

def read_locations():
    return read_sqlite('SELECT * FROM locations')

def read_cities():
    return read_sqlite('SELECT * FROM cities')

def read_cities_locations():
    return read_sqlite('SELECT * FROM view_cities_locations')

def read_charts():
    return read_sqlite('SELECT * FROM charts')

def _save(start_date, end_date):

    # 读取「样本点」
    locations_df = read_locations()

    # 请求 open meteo api 的数据
    params = {
        'latitude' : locations_df['latitude'].tolist(),
        'longitude' : locations_df['longitude'].tolist(),
        'start_date' : start_date,
        'end_date' : end_date,
        'daily_indicators' : variables,
    }
    response_df = om_api.daily_archive(**params)

    # 数据加工
    locations_df['LocationID'] = locations_df.index
    merge_df = pd.merge(locations_df, response_df, on='LocationID')
    merge_df['date'] = pd.to_datetime(merge_df['date']).dt.strftime('%Y-%m-%d')
    merge_df = merge_df[['location_code', 'date', 'temperature_2m_mean', 'precipitation_sum', 'soil_moisture_7_to_28cm_mean']]
    merge_df.dropna(inplace=True)

    print(f'.. 实际写入区间：{merge_df['date'].min()}~{merge_df['date'].max()}; ')

    # 写入数据
    conn = sqlite3.connect(db_path)
    try:
        merge_df.to_sql(
            name = 'archive',
            con = conn,
            if_exists = 'append',  # 可选：'fail'（默认，存在则报错）、'replace'（覆盖）、'append'（追加）
            index = False  # 不写入索引列
        )
        print(f'.. 写入成功')
    finally:
        conn.close() # 关闭连接

def save_archive():
    df = read_archive()
    print(f'.. 库内最新日期：{df['date'].max()}; ')
    # 请求区间
    start_date = (datetime.strptime(df['date'].max(), '%Y-%m-%d') - timedelta(days=3)).strftime('%Y-%m-%d')
    end_date = datetime.today().strftime('%Y-%m-%d')
    print(f'.. 请求日期区间：{start_date}~{end_date}; ')

    # 请求数据
    _save(start_date, end_date)


def read_archive():
    archive_df = read_sqlite('SELECT * FROM archive')
    print(f'.. 历史数据量：{archive_df.shape[0]}; ')
    return archive_df

def get_forecast(start_date: str):

    # 确定预测时间范围
    start_date = datetime.strptime(start_date, '%Y-%m-%d')+ timedelta(days=1)
    end_date = start_date + timedelta(days=14)
    start_date = start_date.strftime('%Y-%m-%d')
    end_date = end_date.strftime('%Y-%m-%d')
    print(f'.. 请求日期区间：{start_date}~{end_date}; ')

    # 读取「样本点」
    locations_df = read_locations()

    # 请求 open meteo api 的数据
    params = {
        'latitude' : locations_df['latitude'].tolist(),
        'longitude' : locations_df['longitude'].tolist(),
        'start_date' : start_date,
        'end_date' : end_date,
        'daily_indicators' : variables,
    }
    response_df = om_api.daily_forecast(**params)

    # 数据加工
    locations_df['LocationID'] = locations_df.index
    merge_df = pd.merge(locations_df, response_df, on='LocationID')
    merge_df['date'] = pd.to_datetime(merge_df['date']).dt.strftime('%Y-%m-%d')
    forecast_df = merge_df[['location_code', 'date', 'temperature_2m_mean', 'precipitation_sum', 'soil_moisture_7_to_28cm_mean']]
    print(f'.. 预测数据量：{forecast_df.shape[0]}; ')

    return forecast_df

def data_process(archive_df, forecast_df=None):

    if forecast_df is not None:
        concat_pd = pd.concat([archive_df, forecast_df])
    else:
        concat_pd = archive_df
    concat_pd['city_code'] = concat_pd['location_code'].str[:5]
    groupby_df  = concat_pd.groupby(['city_code', 'date']).mean(variables).reset_index()
    # 梳理辅助列
    groupby_df['date'] = pd.to_datetime(groupby_df['date'])
    groupby_df['year'] = groupby_df['date'].dt.year
    groupby_df['day_of_year'] = groupby_df['date'].dt.dayofyear
    groupby_df = groupby_df[ groupby_df['day_of_year'] != 366 ]
    # 所需指标
    groupby_df['cum_precip'] = groupby_df.groupby(['year', 'city_code'])['precipitation_sum'].cumsum()
    groupby_df['precip_ma7'] = groupby_df['precipitation_sum'].rolling(window=7, min_periods=1).mean()
    groupby_df['precip_ma30'] = groupby_df['precipitation_sum'].rolling(window=30, min_periods=1).mean()
    groupby_df['temper_ma5'] = groupby_df['temperature_2m_mean'].rolling(window=5, min_periods=1).mean()

    groupby_df.rename(columns={'soil_moisture_7_to_28cm_mean': 'soil_moisture'}, inplace=True)
    print(f'.. 处理后数据量：{groupby_df.shape[0]}; ')

    return groupby_df


if __name__ == '__main__':
    # 保存历史数据
    # save_archive()
    pass