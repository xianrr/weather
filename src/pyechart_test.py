from pyecharts import options as opts
from pyecharts.charts import Line
from pyecharts.commons.utils import JsCode
import pandas as pd
import numpy as np

def day_annul_plot_pyecharts(df: pd.DataFrame, column: str, **kwargs):
    '''
    该函数通过传入的 pandas.DataFrame 生成一个包含历史数据与当前数据的折线图。
    使用 pyecharts 实现，支持交互式图表。

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
    line : pyecharts.charts.Line
        返回绘制好的图表对象，用户可进一步调整或保存。
    '''

    # 数据预处理
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['year'] = df['date'].dt.year
    df['day_of_year'] = df['date'].dt.dayofyear

    years = df['year'].unique()
    this_year = years.max()
    years = years[years < this_year]

    df_history = df[df['year'] != this_year]

    # 创建图表
    line = Line(init_opts=opts.InitOpts(width="800px", height="480px"))

    # 设置 x 轴
    month_ticks = [1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335, 365]

    # 配置项
    line.set_global_opts(
        xaxis_opts=opts.AxisOpts(
            type_="value",
            name="Months",
            min_=kwargs.get('xlim', (1, 365))[0] if 'xlim' in kwargs else 1,
            max_=kwargs.get('xlim', (1, 365))[1] if 'xlim' in kwargs else 365,
            axislabel_opts=opts.LabelOpts(formatter=JsCode(
                """
                function(value) {
                    var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', ''];
                    var ticks = [1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335, 365];
                    for (var i = 0; i < ticks.length; i++) {
                        if (Math.abs(value - ticks[i]) < 5) {
                            return months[i];
                        }
                    }
                    return '';
                }
                """
            ))
        ),

        legend_opts=opts.LegendOpts(is_show=True),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        toolbox_opts=opts.ToolboxOpts(is_show=True),
        # datazoom_opts=opts.DataZoomOpts(is_show=True),
    )

    # 添加历史数据区间（5%-95%分位数）
    if len(df_history) != 0:
        # 计算均值和极值（最小值和最大值）
        average = df_history.groupby('day_of_year')[column].mean().reset_index()

        extremes = df_history.groupby('day_of_year')[column].agg(['min', 'max']).reset_index()

        # 添加极值区间（使用两个面积图叠加）
        line.add_xaxis(xaxis_data=extremes['day_of_year'].tolist())

        line.add_yaxis(
            series_name="Min",
            y_axis=extremes['min'].tolist(),
            # is_smooth=True,
            is_symbol_show=False,
            linestyle_opts=opts.LineStyleOpts(width=1.2, type_="dashed", color="black"),
            # areastyle_opts=opts.AreaStyleOpts(opacity=0, color="rgba(0, 0, 0, 0)"),
            stack="all",
            # label_opts=opts.LabelOpts(is_show=False)
            label_opts=opts.LabelOpts(is_show=False)
        )

        line.add_yaxis(
            series_name="max-min",

            y_axis=(extremes['max']-extremes['min']).tolist(),
            # is_smooth=True,
            is_symbol_show=False,
            linestyle_opts=opts.LineStyleOpts(width=1.2, type_="dashed", color="red"),
            # areastyle_opts=opts.AreaStyleOpts(opacity=0.4, color="skyblue"),
            stack="all",
            # label_opts=opts.LabelOpts(is_show=False)
            label_opts=opts.LabelOpts(is_show=False)
        )

        line.add_yaxis(
            series_name="max-min-2",

            y_axis=(extremes['max']-extremes['min']).tolist(),
            # is_smooth=True,
            is_symbol_show=False,
            linestyle_opts=opts.LineStyleOpts(width=1.2, type_="dashed", color="red"),
            # areastyle_opts=opts.AreaStyleOpts(opacity=0.4, color="skyblue"),
            # stack="all",
            # label_opts=opts.LabelOpts(is_show=False)
            label_opts=opts.LabelOpts(is_show=False)
        )

        line.add_yaxis(
            series_name="Max",
            y_axis=extremes['max'].tolist(),
            # is_smooth=True,
            is_symbol_show=False,
            linestyle_opts=opts.LineStyleOpts(width=1.2, type_="dashed", color="black"),
            # areastyle_opts=opts.AreaStyleOpts(opacity=0.4, color="skyblue"),
            # stack="总量",
            # label_opts=opts.LabelOpts(is_show=False)
            label_opts=opts.LabelOpts(is_show=False)
        )




        # 添加平均值线
        # line.add_xaxis(xaxis_data=df['day_of_year'].tolist())
        line.add_yaxis(
            series_name=f'{len(years)}yr_average',
            y_axis=average[column].tolist(),
            is_smooth=True,
            linestyle_opts=opts.LineStyleOpts(width=1.2, type_="dashed", color="black"),
            symbol="none",
        )


        # for year in years:
        #     year_data = df_history[(df_history['year'] == year) & (df_history['year'] >= 2020)]
        #     if not year_data.empty:
        #         line.add_xaxis(xaxis_data=df['day_of_year'].tolist())
        #         line.add_yaxis(
        #             series_name=str(year),
        #             y_axis=year_data[column].tolist(),
        #             is_smooth=True,
        #             linestyle_opts=opts.LineStyleOpts(width=1.2),
        #             symbol="none",
        #             is_symbol_show=False,
        #         )

    # 添加今年数据
    this_year_data = df[df['year'] == this_year]

    # 添加实际部分
    if not this_year_data.empty:
        # line.add_xaxis(xaxis_data=this_year_data['day_of_year'].tolist())
        line.add_yaxis(
            series_name=str(this_year),
            y_axis=this_year_data[column].tolist(),
            is_smooth=True,
            linestyle_opts=opts.LineStyleOpts(width=1.5, color="red"),
            symbol="none",
        )

    return line

