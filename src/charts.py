import matplotlib.pyplot as plt
import pandas as pd


def day_annul_plot(df:pd.DataFrame, column:str, **kwargs):
    '''
    该函数通过传入的 pandas.DataFrame 生成一个包含历史数据与当前数据的折线图。
    并可以自定义多个参数来调整图表样式、显示范围、以及标题等。

    参数:
    df : pandas.DataFrame
        包含时间序列数据的数据框，必须包含 'date' 和需要绘制的列 (column)。
        'date' 列应为日期类型数据。

    column : str
        需要在图表中展示的列名，必须存在于输入的 DataFrame 中。

    kwargs : 可选参数
        - 'min_history_year' : int, 可选。指定绘制的历史数据起始年份（默认显示所有年份的数据）。
        - 'forecast_after' : str, 可选。指定预测数据的起始日期（格式为 'YYYY-MM-DD'）。
        - 'xlim' : tuple, 可选。设置 x 轴显示的范围，格式为 (xmin, xmax)。
        - 'ylabel' : str, 可选。设置 y 轴的标签名称。
        - 'ylim' : tuple, 可选。设置 y 轴显示的范围，格式为 (ymin, ymax)。
        - 'title' : str, 可选。设置图表的标题。

    返回:
    fig : matplotlib.figure.Figure
        返回绘制好的图表对象，用户可进一步调整或保存。

    详细说明:
    - 本函数会绘制历史年份的日均值区间（5% - 95%），并标注出当前年份（如有预测数据则显示预测部分）。
    - x 轴代表的是日期的天序号，y 轴为传入的时间序列数据列（column）。
    - 图表包括年份数据的折线图、5%-95%分位区间和当前年份的数据（如有预测）。
    - 支持自定义图表样式，标题和轴标签等。
    '''
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['year'] = df['date'].dt.year
    df['day_of_year'] = df['date'].dt.dayofyear

    years = df['year'].unique()
    this_year = years.max()
    years = years[years < this_year]
    # this_year = 2025

    df_history = df[ df['year'] != this_year ]

    # 一、对历史数据展开分析
    # 1.1 均值
    average = df_history.groupby('day_of_year')[column].mean().reset_index()
    # 1.2 区间：分位数（上分位、下分位）
    quantiles = df_history.groupby('day_of_year')[column].quantile([0.05, 0.95])
    quantiles = quantiles.unstack().reset_index()
    # 1.3 区间：正态分布（概率区间）
    # 待完善

    # 二、可视化
    # 2.1 尺寸
    fig = plt.figure(figsize=(7.5, 4.5))

    # 2.2.1 绘图：区间
    plt.fill_between(quantiles['day_of_year'],
                     quantiles[0.05],
                     quantiles[0.95],
                     color='skyblue',
                     alpha= 0.4,
                     label='5%-95%')

    # 2.2.2 绘图：平均值
    plt.plot(average['day_of_year'],
             average[column],
             "k--",
             linewidth=1.2,
             label=f'{len(years)}yr_average')

    # 2.2.3 绘图：历史历年数据
    if 'min_history_year' in kwargs:
        years = years[ years >= kwargs['min_history_year'] ]
    for year in years:
            year_data = df_history[df_history['year'] == year]
            plt.plot(year_data['day_of_year'],
                     year_data[column],
                     alpha=0.6,
                     linewidth=1.2,
                     label=year)

    # 2.2.4 绘图：今年数据（含预测）
    this_year_data = df[ (df['year'] == this_year) ]
    if 'forecast_after' in kwargs:
        forecast_data = this_year_data[this_year_data['date'] >= kwargs['forecast_after']]
        this_year_data = this_year_data[this_year_data['date'] <= kwargs['forecast_after']]
        plt.plot(forecast_data['day_of_year'],
                 forecast_data[column],
                 alpha=1.0,
                 linewidth=1.5,
                 linestyle = '--',
                 color='red')
    plt.plot(this_year_data['day_of_year'],
             this_year_data[column],
             alpha=1.0,
             linewidth=1.5,
             color='red',
             label=this_year)

# 2.3 风格化
    fig.text(0.5, 0.5, '© Xiamen Xiangyu', fontsize=30, color='gray',
             alpha=0.2, ha='center', va='center', rotation=30)

    month_ticks = [1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335, 365]
    month_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", ""]
    plt.xticks(month_ticks, month_labels) # x轴
    plt.xlabel('Months')
    if 'xlim' in kwargs:
        plt.xlim(*kwargs['xlim'])
    if 'ylabel' in kwargs:  # y轴标题
        plt.ylabel(kwargs['ylabel'])
    if 'ylim' in kwargs:
        plt.ylim(*kwargs['ylim'])
    if 'title' in kwargs:  # 标题
        plt.title(kwargs['title'])

    plt.grid(True, alpha=0.3)
    plt.legend() #显示图例
    plt.tight_layout() # 自动调整

    return fig