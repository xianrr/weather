cn_cities = [
    {
        'code' : '(1)HL',
        'name' : 'Heilongjiang',
        'latitude' : [ 45.71,  47.25,  50.20,  46.70,  46.80,  46.66],
        'longitude': [126.91, 124.12, 127.49, 131.19, 130.15, 127.07]
    },{
        'code' : '(2)JL',
        'name' : 'Jilin',
        'latitude' : [ 45.16,  45.60,  43.92,  43.70,  43.34],
        'longitude': [124.93, 122.72, 125.12, 126.42, 128.34]
    },{
        'code' : '(3)NM',
        'name' : 'Nei Mongolia',
        'latitude' : [ 43.57,  42.22,  46.08,  49.18],
        'longitude': [122.32, 118.96, 122.19, 119.82]
    },{
        'code' : '(4)LN',
        'name' : 'Liaoning',
        'latitude' : [ 42.26,  42.12,  41.88],
        'longitude': [123.80, 121.73, 123.29]
    },{
        'code' : '(5)SD',
        'name' : 'Shandong',
        'latitude' : [ 35.37,  35.17,  37.41,  37.49],
        'longitude': [116.71, 115.43, 118.12, 116.43]
    },{
        'code' : '(6)HE',
        'name' : 'Hebei',
        'latitude' : [ 37.94,  36.59,  36.98,  37.78],
        'longitude': [114.80, 114.63, 114.63, 115.56]
    },{
        'code' : '(7)HA',
        'name' : 'Henan',
        'latitude' : [ 32.98,  33.01,  33.63,  34.43],
        'longitude': [112.64, 114.10, 114.59, 115.75]
    },{
        'code' : '(8)AH',
        'name' : 'Anhui',
        'latitude' : [ 33.86,  32.93],
        'longitude': [115.82, 117.52]
    }
]

# 1 国家 8 城市 32 样本点
countries = [
    {
        'code' : 'CN',
        'name' : 'China',
        'city_list' : cn_cities
    }
]


daily_indicators = ["temperature_2m_mean",
                    "precipitation_sum",
                    "soil_moisture_7_to_28cm_mean"]

styles = [
    { # 累计降水
        'column' : 'cum_precip',
        'min_history_year' : 2022,
        'ylabel' : 'Precipitation (mm)',
        'title' : 'Cumulative Annual Precipitation of ',
        'path' : 'a_cum_precip'
    },{ # 7日累计降水
        'column' : 'precip_sum7',
        'min_history_year' : 2022,
        'ylabel' : 'Precipitation (mm)',
        'title' : 'Last 7 days Sum Precipitation of ',
        'path' : 'b_precip_sum7'
    },{ # 土壤墒情
        'column' : 'soil_moisture_7_to_28cm_mean',
        'min_history_year' : 2022,
        'ylabel' : 'Soil Moisture (m³/m³)',
        'title' : 'Mean Soil Moisture (7-28cm) of ',
        'path' : 'c_soil_moisture'
    },{ # 平均气温
        'column' : 'temperature_2m_mean',
        'min_history_year' : 2024,
        'ylabel' : 'Temperature (°C)',
        'title' : 'Mean Temperature of ',
        'path' : 'd_mean_temper'
    },{ # 积温
        'column' : 'degree_day',
        'min_history_year' : 2024,
        'ylabel' : 'Degree Day (°C)',
        'xlim' : (105, 260),
        'title' : 'Degree Day after 15th Apr. of ',
        'path' : 'e_degree_day'
    }
]


import pandas as pd
def data_prapare(df):
    # 统一处理
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['year'] = df['date'].dt.year
    df['day_of_year'] = df['date'].dt.dayofyear
    df = df[df['day_of_year'] <= 365]

    # 个性化处理
    df['cum_precip'] = df.groupby('year')['precipitation_sum'].cumsum()
    df['precip_sum7'] = df['precipitation_sum'].rolling(window=7, min_periods=1).sum()
    # 积温
    df = df.assign(t=0.0)
    mask = (df['day_of_year'] > 105) & (df['temperature_2m_mean'] >= 10)
    df.loc[mask, 't'] = df.loc[mask, 'temperature_2m_mean']
    df.loc[:, 'degree_day'] = df.groupby('year')['t'].cumsum()
    df.drop(columns = ['t'], inplace = True)

    return df