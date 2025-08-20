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

def dig(df_l2, style, city_name, file_city_name, year_of_today):
    # 样式
    column = style["column"]       # 列名（指标）
    min_history_year = style["min_history_year"] # 显示最小的年份
    ylabel = style["ylabel"]       # y轴名称
    title = style["title"]         # 标题
    pathname = style["pathname"]   # 文件名


    # 历史数据-分析
    df_l2_history = df_l2[df_l2['year'] != year_of_today]
    ## 历史数据平均
    average_accumulated = df_l2_history.groupby('day_of_year')[column].mean().reset_index()
    ## 历史数据区间 5%-95%
    quantiles = df_l2_history.groupby('day_of_year')[column].quantile([0.05, 0.95]).unstack().reset_index()

    # 可视化
    fig = plt.figure(figsize=(10.5, 6))
    fig.text(0.5, 0.5, '© Xiamen Xiangyu', fontsize=30, color='gray',
             alpha=0.2, ha='center', va='center', rotation=30)
    ## (1)历史数据区间
    plt.fill_between(quantiles['day_of_year'],
                     quantiles[0.05],
                     quantiles[0.95],
                     color='skyblue',
                     alpha= 0.4,
                     label='5%-95%')
    ## (2)历史数据平均
    plt.plot(average_accumulated['day_of_year'],
             average_accumulated[column],
             "k--",
             linewidth=1.2,
             label='10yr_average')
    ## (3)历史历年数据
    years = df_l2['year'].unique()
    for year in years:
        if year != year_of_today and year >= min_history_year:
            year_data = df_l2[df_l2['year'] == year]
            plt.plot(year_data['day_of_year'],
                     year_data[column],
                     alpha=0.6,
                     linewidth=1.2,
                     label=year)
    ## (4)今年数据
    year_data = df_l2[df_l2['year'] == year_of_today]
    plt.plot(year_data['day_of_year'],
             year_data[column],
             alpha=1.0,
             linewidth=1.5,
             color='red',
             label=year)
    ##
    month_ticks = [1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]
    month_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    plt.xticks(month_ticks, month_labels)
    plt.xlabel('Months')
    plt.ylabel(ylabel)
    plt.title(f'{title}{city_name}')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    # plt.show()
    if pathname == "e_Degree_Day":
        plt.xlim(105, 260)
    fig.savefig(f'./diagram/US/{file_city_name}_{pathname}.jpg', dpi=300)
    plt.close(fig)

def dig_merge(city_list, col_num, output_path, styles):
    image_paths = []
    for city in city_list:
        #image_paths.append(f'./floder/{city['file']}_Weekly_Precip.jpg')
        for style in styles:
            image_paths.append(f'./diagram/US/{city['file']}_{style['pathname']}.jpg')

    images = [Image.open(path) for path in image_paths]

    img_width, img_height = images[0].size

    grid_img = Image.new('RGB', (img_width * col_num, img_height * int(len(images)//col_num)))

    for idx, img in enumerate(images):
        row = idx // col_num
        col = idx % col_num
        grid_img.paste(img, (col * img_width, row * img_height))
    #
    grid_img.save(output_path)