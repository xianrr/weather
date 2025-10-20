import pandas as pd
from src import om_api

def save(countries, start_date, end_date, daily_indicators, tail_of_file):
    for country in countries:
        all_df = pd.DataFrame()
        for city  in country['city_list']:
            params = {
                'latitude'  : city['latitude'],
                'longitude' : city['longitude'],
                'start_date': start_date,
                'end_date'  : end_date,
                'daily_indicators': daily_indicators
            }
            api_df = om_api.daily_history(**params)
            groupby_df = api_df.groupby('date', as_index=False)[daily_indicators].mean()
            groupby_df['name'] = city['name']
            print('.. Loading: ' + city['name'])
            all_df = pd.concat([all_df, groupby_df])
        all_df.to_csv(f'dataset/{country['code']}_{tail_of_file}.csv', index=False)
        print('Finished: ' + country['name'])