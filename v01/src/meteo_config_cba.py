# 加拿大 城市3 样本点 15
ca_cities = [
    {
        'code' : '(01)SK',
        'name' : 'Saskatchewan',
        'latitude':  [  49.48,   50.42,   52.26,   50.75,   50.87,   50.15,   51.70],
        'longitude': [-102.53, -104.07, -104.35, -102.58, -105.68, -109.73, -109.77]
    },{
        'code' : '(02)AB',
        'name' : 'Alberta',
        'latitude':  [  49.79,   51.74,   53.76,   53.17,   55.59],
        'longitude': [-113.49, -114.27, -113.79, -111.36, -117.50]
    },{
        'code' : '(03)MB',
        'name' : 'Manitoba',
        'latitude':  [ 49.69,   49.29,   50.42],
        'longitude': [-99.00, -101.19, -101.26]
    }
]

# 巴西 城市 7 样本点 23
br_cities = [
    {
        'code' : '(01)MT',
        'name' : 'Mato Grosso',
        'latitude':  [ -9.58, -11.42, -13.12, -13.47, -15.30],
        'longitude': [-56.69, -51.25, -55.25, -58.88, -54.90]
    },{
        'code' : '(02)PR',
        'name' : 'Paraná',
        'latitude':  [-25.52, -26.49, -24.80, -23.31],
        'longitude': [-54.22, -51.91, -50.53, -51.26]
    },{
        'code' : '(03)RS',
        'name' : 'Rio Grande do Sul',
        'latitude':  [-28.49, -29.02, -28.28, -30.83],
        'longitude': [-55.71, -54.05, -50.89, -55.73]
    },{
        'code' : '(04)GO',
        'name' : 'Goiás',
        'latitude':  [-14.53, -16.33, -17.95],
        'longitude': [-49.28, -47.50, -51.98]
    },{
        'code' : '(05)MS',
        'name' : 'Mato Grosso do Sul',
        'latitude':  [-19.58, -20.58, -22.81],
        'longitude': [-53.16, -54.33, -55.56]
    },{
        'code' : '(06)MG',
        'name' : 'Minas Gerais',
        'latitude':  [-18.33, -20.04],
        'longitude': [-47.46, -48.33]
    },{
        'code' : '(07)BA',
        'name' : 'Bahia',
        'latitude':  [-11.66, -13.44],
        'longitude': [-45.00, -44.56]
    }
]

# 阿根廷 城市 4 样本点 19
ar_cities = [
    {
        'code' : '(01)B',
        'name' : 'Buenos Aires',
        'latitude':  [-38.16, -38.46, -36.59, -35.53, -34.65, -33.48],
        'longitude': [-58.06, -60.34, -61.96, -60.26, -62.90, -60.33]
    },{
        'code' : '(02)X',
        'name' : 'Córdoba',
        'latitude':  [-33.57, -33.41, -33.16, -31.28, -30.74],
        'longitude': [-64.69, -63.63, -62.23, -62.57, -63.84]
    },{
        'code' : '(03)S',
        'name' : 'Santa Fe',
        'latitude':  [-34.06, -33.05, -32.14, -32.00, -30.34],
        'longitude': [-61.86, -60.96, -61.20, -61.74, -61.51]
    },{
        'code' : '(04)G',
        'name' : 'Santiago d Estero',
        'latitude':  [-28.55, -27.40, -26.52],
        'longitude': [-62.30, -62.17, -63.00]
    }
]

# 3 国家 14 城市 57 样本点
countries = [
    {
        'code' : 'CA',
        'name' : 'Canada',
        'city_list' : ca_cities
    },{
        'code' : 'BR',
        'name' : 'Brazil',
        'city_list' : br_cities
    },{
        'code' : 'AR',
        'name' : 'Argentina',
        'city_list' : ar_cities
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
    },{ # 降水7日滚动
        'column' : 'precip_sum7',
        'min_history_year' : 2024,
        'ylabel' : 'Precipitation (mm)',
        'title' : 'Last 7 days Precipitation Summary of ',
        'path' : 'b_precip_sum7'
    },{ # 降水30日滚动
        'column' : 'precip_sum30',
        'min_history_year' : 2022,
        'ylabel' : 'Precipitation (mm)',
        'title' : 'Last 30 days Precipitation Summary of ',
        'path' : 'c_precip_sum30'
    },{ # 土壤墒情
        'column' : 'soil_moisture_7_to_28cm_mean',
        'min_history_year' : 2022,
        'ylabel' : 'Soil Moisture (m³/m³)',
        'title' : 'Mean Soil Moisture (7-28cm) of ',
        'path' : 'd_soil_moisture'
    },{  # 气温
        'column' : 'temperature_2m_mean',
        'min_history_year' : 2024,
        'ylabel' : 'Temperature (°C)',
        'title'  : 'Mean Temperature of ',
        'path' : 'e_mean_temper'
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
    df['precip_sum30'] = df['precipitation_sum'].rolling(window=30, min_periods=1).sum()


    return df
