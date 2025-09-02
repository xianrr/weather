# 澳大利亚 5 城市 21 样本点
au_cities = [
    {
        'code' : '(1)QLD',
        'name' : 'Queensland',
        'latitude' : [-22.38, -27.01, -28.14, -26.71, -23.78],
        'longitude': [146.71, 150.43, 149.53, 151.80, 149.05]
    },{
        'code' : '(2)NSW',
        'name' : 'New South Wales',
        'latitude' : [-29.39, -29.48, -32.17, -35.14],
        'longitude': [149.97, 147.82, 146.55, 146.18]
    },{
        'code' : '(3)VIC',
        'name' : 'Victoria',
        'latitude' : [-35.32, -34.71, -35.80, -36.25],
        'longitude': [144.31, 141.95, 142.20, 143.69]
    },{
        'code' : '(4)SA',
        'name' : 'South Australia',
        'latitude' : [-33.55, -34.66, -32.77, -33.55],
        'longitude': [135.24, 137.69, 138.16, 139.06]
    },{
        'code' : '(5)WA',
        'name' : 'Western Australia',
        'latitude' : [-33.36, -33.30, -33.76, -32.09],
        'longitude': [123.34, 121.71, 118.78, 117.60]
    },
]

# 欧盟 5 城市 28 样本点
eu_cities = [
    {
        'code': '(1)ES',
        'name' : 'Spain',
        'latitude' : [42.07, 40.92, 38.92, 41.83],
        'longitude': [-5.56, -3.61, -2.94, -1.53]
    },{
        'code': '(2)FR',
        'name' : 'France',
        'latitude' : [46.09, 47.76, 47.34, 47.99, 49.49, 50.05],
        'longitude': [-0.54, -1.20,  2.03,  4.07,  4.61,  2.74]
    },{
        'code': '(3)DE',
        'name' : 'Germany',
        'latitude' : [50.58, 51.83, 53.12, 53.27, 49.73, 48.35],
        'longitude': [ 6.97,  7.72,  9.67, 12.74, 10.62, 10.74]
    },{
        'code': '(4)PL',
        'name' : 'Poland',
        'latitude' : [51.24, 51.19, 52.94, 53.32, 51.47],
        'longitude': [15.56, 17.59, 17.42, 19.91, 22.90]
    },{
        'code': '(5)RO',
        'name' : 'Romania',
        'latitude' : [46.05, 45.53, 47.68, 46.32, 45.19, 45.16],
        'longitude': [21.11, 22.23, 26.09, 26.62, 25.26, 27.80]
    }
]

# 俄罗斯 5 城市 23 样本点
ru_cities = [
    {
        'code': '(1)ROS',
        'name' : 'Rostov',
        'latitude' : [47.64, 48.79, 47.86, 46.75, 46.26],
        'longitude': [39.37, 40.80, 42.07, 43.35, 41.33]
    },{
        'code': '(2)BEL',
        'name' : 'Belgorod',
        'latitude' : [50.78, 50.58, 50.18, 51.23],
        'longitude': [35.71, 37.29, 38.86, 37.72]
    },{
        'code': '(3)SAR',
        'name' : 'Saratov',
        'latitude' : [51.92, 52.12, 52.33, 50.95, 51.59],
        'longitude': [43.02, 45.43, 47.73, 46.52, 49.60]
    },{
        'code': '(4)ALT',
        'name' : 'Altai',
        'latitude' : [53.23, 53.75, 52.04, 51.48, 52.09],
        'longitude': [78.72, 83.08, 81.35, 82.83, 85.20]
    },{
        'code': '(5)STA',
        'name' : 'Stavropol',
        'latitude' : [45.89, 45.04, 44.60, 44.54],
        'longitude': [43.06, 45.14, 43.33, 41.98]
    },
]

# 乌克兰 6 城市 25 样本点
ua_cities = [
    {
        'code' : '(1)CHE',
        'name' : 'Chernihiv',
        'latitude' : [51.61, 51.56, 50.89, 51.35],
        'longitude': [30.91, 32.55, 31.28, 31.88]
    },{
        'code' : '(2)PLT',
        'name' : 'Poltava',
        'latitude' : [50.36, 49.63, 49.97, 50.47, 50.78],
        'longitude': [32.81, 32.95, 34.37, 35.14, 34.08]
    },{
        'code' : '(3)VIN',
        'name' : 'Vinnytsia',
        'latitude' : [48.86, 48.35, 48.30, 49.16],
        'longitude': [27.97, 28.39, 29.02, 29.38]
    },{
        'code' : '(4)DNP',
        'name' : 'Dnipropetrovsk',
        'latitude' : [48.19, 47.96, 49.00, 48.36],
        'longitude': [35.03, 33.73, 35.00, 36.57]
    },{
        'code' : '(5)KHA',
        'name' : 'Kharkiv',
        'latitude' : [49.74, 49.52, 49.90, 50.21],
        'longitude': [35.71, 36.54, 37.48, 36.44]
    },{
        'code' : '(6)ODE',
        'name' : 'Odesa',
        'latitude' : [45.89, 46.24, 47.05, 47.37],
        'longitude': [29.07, 29.73, 30.95, 29.90]
    }
]

# 4 国家 21 城市 97 样本点
countries = [
    {
        'code' : 'AU',
        'name' : 'Australia',
        'city_list' : au_cities
    },{
        'code' : 'EU',
        'name' : 'Europe Union',
        'city_list' : eu_cities
    },{
        'code' : 'RU',
        'name' : 'Russia',
        'city_list' : ru_cities
    },{
        'code' : 'UA',
        'name' : 'Ukraine',
        'city_list' : ua_cities
    }
]


# 获取的天气指标
aure_daily_indicators = ["temperature_2m_mean",
                         "precipitation_sum",
                         "soil_moisture_7_to_28cm_mean"]


aure_styles = [
    {   # 累计降水
        'column' : 'cum_precip',
        'min_history_year' : 2022,
        'ylabel' : 'Precipitation (mm)',
        'title' : 'Cumulative Annual Precipitation of ',
        'path' : 'a_cum_precip'
    },{ # 7日累计降水
        'column' : 'precip_sum7',
        'min_history_year' : 2024,
        'ylabel' : 'Precipitation (mm)',
        'title' : 'Last 7 days Sum Precipitation of ',
        'path' : 'b_precip_ma7'
    },{ # 土壤墒情
        'column' : 'soil_moisture_7_to_28cm_mean',
        'min_history_year' : 2022,
        'ylabel' : 'Soil Moisture (m³/m³)',
        'title' : 'Soil Moisture (7-28cm) of ',
        'path' : 'c_soil_moisture'
    },{ # 平均气温
        'column' : 'temperature_2m_mean',
        'min_history_year' : 2024,
        'ylabel' : 'Temperature (°C)',
        'title' : 'Mean Temperature of ',
        'path' : 'd_temper_ma5'
    }
]

import pandas as pd
def data_prapare(df):
    # 数据准备
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['year'] = df['date'].dt.year
    df['day_of_year'] = df['date'].dt.dayofyear
    df = df[df['day_of_year'] <= 365]
    # 累计降水
    df['cum_precip']= df.groupby('year')['precipitation_sum'].cumsum()
    # 7日累计降水
    df['precip_sum7'] = df['precipitation_sum'].rolling(window=7, min_periods=1).sum()
    return df
