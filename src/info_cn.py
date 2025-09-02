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
        'name' : 'Heibei',
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


cn_daily_indicators = ["temperature_2m_mean",
                       "precipitation_sum",
                       "soil_moisture_7_to_28cm_mean"]

cn_styles = [
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
        'path' : 'd_Mean_Temper'
    },{ # 积温
        'column' : 'degree_day',
        'min_history_year' : 2024,
        'ylabel' : 'Degree Day (°C)',
        'title' : 'Degree Day after 15th Apr. of ',
        'path' : 'e_Degree_Day'
    }
]