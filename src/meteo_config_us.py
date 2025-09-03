# 美国 6 州 城市气象数据配置信息
us_cities = [
    {
        'code': '(1)IA',
        'name': 'Iowa',
        'latitude': [43.37, 42.67, 43.29, 43.31, 42.95, 42.04],
        'longitude': [-96.30, -95.87, -92.14, -93.84, -94.04, -94.12]
    }, {
        'code': '(2)IL',
        'name': 'Illinois',
        'latitude': [40.05, 40.91, 41.89, 41.08, 39.99],
        'longitude': [-91.27, -90.34, -89.93, -87.81, -89.17]
    }, {
        'code': '(3)NE',
        'name': 'Nebraska',
        'latitude': [42.36, 42.68, 40.12, 40.20, 41.23, 40.76],
        'longitude': [-99.16, -97.27, -96.93, -95.75, -96.39, -99.70]
    }, {
        'code': '(4)MN',
        'name': 'Minnesota',
        'latitude': [43.74, 44.15, 43.64, 45.77, 46.27, 43.62],
        'longitude': [-96.28, -95.23, -94.08, -96.38, -95.85, -92.53]
    }, {
        'code': '(5)KS',
        'name': 'Kansas',
        'latitude': [39.91, 37.15, 37.14, 38.11],
        'longitude': [-95.61, -100.78, -94.80, -94.83]
    }, {
        'code': '(6)ND',
        'name': 'North Dakota',
        'latitude': [47.20, 46.95, 48.15, 46.17, 46.59],
        'longitude': [-97.40, -99.62, -97.45, -100.11, -97.80]
    }
]

# 1 国家 8 城市 32 样本点
countries = [
    {
        'code' : 'US',
        'name' : 'United States',
        'city_list' : us_cities
    }
]


daily_indicators = ["temperature_2m_mean",
                    "precipitation_sum",
                    "soil_moisture_7_to_28cm_mean"]

# 图表样式配置
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