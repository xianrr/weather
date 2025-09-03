import pandas as pd
from src import charts, om_api
import matplotlib.pyplot as plt
def with_forecast(countries, api_start_date, api_end_date, forecast_start_date, forecast_end_date, daily_indicators, config, **kwargs):

    for country in countries:

        # 读取 CSV 历史数据（全部）
        csv_df = pd.DataFrame()
        for path in country['csv_path']:
            df = pd.read_csv(path)
            csv_df = pd.concat([csv_df, df])
        csv_df['date'] = pd.to_datetime(csv_df['date'])
        if 'csv_start_date' in kwargs:
            csv_df = csv_df[csv_df['date'] >= kwargs['csv_start_date']]
        if 'csv_end_date' in kwargs:
            csv_df = csv_df[csv_df['date'] <= kwargs['csv_end_date']]

        for city in country['city_list']:
            # 读取 CSV 历史数据（特定城市）
            city_csv_df = csv_df[csv_df['name'] == city['name']]

            # 请求 API 历史数据
            api_history_df = om_api.daily_history(city['latitude'], city['longitude'],
                                                  api_start_date, api_end_date,
                                                  daily_indicators)
            # 请求 API 预测数据
            api_forecast_df = om_api.daily_forecast(city['latitude'], city['longitude'],
                                                    forecast_start_date, forecast_end_date,
                                                    daily_indicators)
            # 合并数据
            concat_df = pd.concat([city_csv_df, api_history_df, api_forecast_df])
            concat_df = concat_df.groupby('date', as_index=False)[daily_indicators].mean()
            concat_df['name'] = city['name']

            # 数据处理
            concat_df = config.data_prapare(concat_df)

            # 制图
            for style in config.styles:
                chart_params = {
                    'forecast_after' : forecast_start_date,
                    'ylabel': style['ylabel'],
                    'title' : style['title'] + city['name'] +', ' + country['name'],
                }
                if 'min_history_year' in style:
                    chart_params['min_history_year'] = style['min_history_year']
                if 'ylim' in style:
                    chart_params['ylim'] = style['ylim']
                if 'xlim' in style:
                    chart_params['xlim'] = style['xlim']


                chart = charts.day_annul_plot(concat_df, style['column'], **chart_params)
                path = f'./diagram/{country['code']}/{country['code']}{city['code']}_{style['path']}.jpg'
                chart.savefig(path, dpi=300)
                plt.close()

            print('.. Loading: ' + city['name'])
        print('Finished: ' + country['name'])