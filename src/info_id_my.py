# 印尼  7 城市  22 样本点

id_cities = [
    {
        "l1_code"  : "(1)RI",
        "l1_name"  : "Riau",
        "title_tag": "(#1 20%)",
        "latitude" : [  1.55,  -0.28,   0.59],
        "longitude": [100.73, 102.05, 100.98]
    },{
        "l1_code"  : "(2)SU",
        "l1_name"  : "North Sumatra",
        "title_tag": "(#2 12%)",
        "latitude" : [ 3.92,  2.92,  1.48],
        "longitude": [98.18, 99.54, 99.94]
    },{
        "l1_code"  : "(3)KT",
        "l1_name"  : "Central Kalimantan",
        "title_tag": "(#3 12%)",
        "latitude" : [ -2.37,  -2.38,  -3.36],
        "longitude": [111.79, 112.74, 113.77]
    },{
        "l1_code"  : "(4)KI",
        "l1_name"  : "East Kalimantan",
        "title_tag": "(#4 10%)",
        "latitude" : [ -1.63,   0.19,   1.22],
        "longitude": [116.18, 116.90, 117.83]
    },{
        "l1_code"  : "(5)KB",
        "l1_name"  : "West Kalimantan",
        "title_tag": "(#5 9%)",
        "latitude" : [  1.48,   0.14,   0.26,  -1.66],
        "longitude": [109.68, 110.44, 111.39, 110.46]
    },{
        "l1_code"  : "(6)JA",
        "l1_name"  : "Jambi",
        "title_tag": "(#6)",
        "latitude" : [ -0.94,  -2.11,  -1.83],
        "longitude": [103.20, 102.68, 103.44]
    },{
        "l1_code"  : "(7)SS",
        "l1_name"  : "South Sumatra",
        "title_tag": "(#7)",
        "latitude" : [ -3.56,  -2.89,  -2.53],
        "longitude": [103.84, 105.02, 104.25]
    }
]

# 马来  5 城市  16 样本点
my_cities = [
    {
        "l1_code"  : "(1)S",
        "l1_name"  : "Sabah",
        "title_tag": "(#1 24%)",
        "latitude" : [  5.80,   5.57,   5.28,   4.58],
        "longitude": [117.54, 118.27, 119.11, 117.75]
    },{
        "l1_code"  : "(2)Q",
        "l1_name"  : "Sarawak",
        "title_tag": "(#2 21%)",
        "latitude" : [  4.23,   3.21,   2.73,   2.45],
        "longitude": [114.09, 113.27, 112.42, 111.76]
    },{
        "l1_code"  : "(3)J",
        "l1_name"  : "Johor",
        "title_tag": "(#3 16%)",
        "latitude" : [  1.78,   1.99,   2.32],
        "longitude": [104.04, 103.35, 102.52]
    },{
        "l1_code"  : "(4)C",
        "l1_name"  : "Pahang",
        "title_tag": "(#4 16%)",
        "latitude" : [  2.89,   3.61,   3.98],
        "longitude": [102.80, 103.06, 102.38]
    },{
        "l1_code"  : "(5)A",
        "l1_name"  : "Parak",
        "title_tag": "(#5 10%)",
        "latitude" : [  4.16,   4.91],
        "longitude": [100.93, 100.70]
    }
]

# 获取的天气指标
id_my_daily_indicators = ["temperature_2m_mean",
                          "precipitation_sum",
                          "soil_moisture_28_to_100cm_mean"]

id_my_styles = [
    { # 累计降水
        'column' : 'cum_precip',
        'min_history_year' : 2022,
        'ylabel' : 'Precipitation (mm)',
        'title' : 'Cumulative Annual Precipitation of ',
        'path' : 'a_cum_precip'
    },{ # 7日平均降水
        'column' : 'precip_ma7',
        'min_history_year' : 2024,
        'ylabel' : 'Precipitation (mm)',
        'ylim' : (0, 26),
        'title' : 'Last 7 days Mean Precipitation of ',
        'path' : 'b_precip_ma7'
    },{ # 30日平均降水
        'column' : 'precip_ma30',
        'min_history_year' : 2024,
        'ylabel' : 'Precipitation (mm)',
        'ylim' : (0, 26),
        'title' : 'Last 30 days Mean Precipitation of ',
        'path' : 'c_precip_ma30'
    },{ # 土壤墒情
        'column' : 'soil_moisture_28_to_100cm_mean',
        'min_history_year' : 2022,
        'ylabel' : 'Soil Moisture (m³/m³)',
        'title' : 'Soil Moisture (28-100cm) of ',
        'ylim' : (0.15, 0.55),
        'path' : 'd_soil_moisture'
    },{ # 5日平均气温
        'column' : 'temper_ma5',
        'min_history_year' : 2024,
        'ylabel' : 'Temperature (°C)',
        'ylim' : (23.5, 29.5),
        'title' : 'Last 5 days Mean Temperature of ',
        'path' : 'e_temper_ma5'
    }
]

# 印尼、马来基本信息
countries = [
    {
        'l0_code': 'ID',
        'l0_name':'Indonesia',
        'l1_list':id_cities
    },{
        'l0_code': 'MY',
        'l0_name':'Malaysia',
        'l1_list':my_cities
    }
]


import pandas as pd
def data_prapare(df):
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['year'] = df['date'].dt.year
    df['day_of_year'] = df['date'].dt.dayofyear
    df['cum_precip'] = df.groupby('year')['precipitation_sum'].cumsum()
    df['precip_ma7'] = df['precipitation_sum'].rolling(window=7, min_periods=1).mean()
    df['precip_ma30'] = df['precipitation_sum'].rolling(window=30, min_periods=1).mean()
    df['temper_ma5'] =  df['temperature_2m_mean'].rolling(window=5, min_periods=1).mean()
    df = df[df['day_of_year'] <= 365]
    return df