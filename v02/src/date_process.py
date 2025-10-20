import pandas as pd
import uuid
from datetime import timedelta


def dayofyear_offset_label(offset: int = 181):
    df = pd.DataFrame({'month_ticks': [1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335],
                       'month_labels': ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                                        "Jul", "Aug","Sep", "Oct", "Nov", "Dec"]})
    df['month_ticks'] = (df['month_ticks'] + 365 - offset) % 365
    df.sort_values('month_ticks', inplace=True)

    month_ticks = df['month_ticks'].tolist()
    month_ticks.append(365)
    month_labels = df['month_labels'].tolist()
    month_labels.append('')

    return month_ticks, month_labels

def dayofyear_offset(input_df: pd.DataFrame,
                     *,
                     date_column: str = 'date',
                     leap_year: int = 0,
                     offset: int = 181,
                     year_format: int = 8,
                     connect: str = '~') -> pd.DataFrame:
    """
    - 通过给定的日期偏移天数，计算出偏移后的 year 与 day_of_year
    - 注意事项：
        - 所有闰年的 12月31日 将被丢弃
        - 要确保日期列的格式能被 pandas.to_datetime 处理
        - 将会创建 year 和 day_of_year 两列，若已存在将被覆盖

    :param input_df: 待计算的 pandas.to_datetime
    :param date_column: str 计算的日期列「名称」默认为 date
    :param leap_year: int 闰年的处理方式 0不处理 1剔除12月31日 2剔除2月29日
    :param offset: int 偏移的天数，默认为 181 即平年的 7月1日 为偏移后的第一天，允许值范围为 [1,365]
    :param year_format: int 输出的 year 样式类型，默认为 8，允许值及示例 4:21~22, 6:2021~22, 8:2021~2022
    :param connect: str 输出的 year 中间的连接符，默认为 '~'

    :return: pd.DataFrame
    """

    # 规范传入参数的范围
    if not (1 <= offset <= 365):
        raise ValueError("offset must be between 1 and 365")
    if year_format not in [4, 6, 8]:
        raise ValueError("type must be 4, 6, or 8")

    # 创建临时列
    temp_columns = {
        'date': uuid.uuid4().hex,
        'year': uuid.uuid4().hex,
        'day_of_year': uuid.uuid4().hex,
        'year_offset_start': uuid.uuid4().hex,
        'year_offset_end': uuid.uuid4().hex,
        'year_offset': uuid.uuid4().hex,
        'day_of_year_offset': uuid.uuid4().hex
    }

    # 创建工作副本
    output_df = input_df.copy()

    # 转换为日期类型
    output_df[temp_columns['date']] = pd.to_datetime(output_df[date_column])
    output_df[temp_columns['year']] = output_df[temp_columns['date']].dt.year
    output_df[temp_columns['day_of_year']] = output_df[temp_columns['date']].dt.dayofyear

    # 闰年处理方式
    if leap_year == 0:
        pass
    elif leap_year == 1:
        output_df = output_df[ output_df[temp_columns['day_of_year']] != 366 ]
    elif leap_year == 2:
        output_df = output_df.loc[
            ~((output_df[temp_columns['date']].dt.is_leap_year) & (output_df[temp_columns['day_of_year']] == 60))
        ]

        leap_year_mask = (output_df[temp_columns['date']].dt.is_leap_year) & (output_df[temp_columns['day_of_year']] > 60)

        output_df.loc[leap_year_mask,temp_columns['day_of_year']] = output_df.loc[leap_year_mask,temp_columns['day_of_year']] -1


    # 计算偏移后的 day_of_year
    if leap_year == 0:
        if offset <= 58:
            output_df[temp_columns['day_of_year_offset']] = (
                        output_df[temp_columns['date']] - timedelta(days=offset)).dt.dayofyear
        else:
            output_df[temp_columns['day_of_year_offset']] = (
                        output_df[temp_columns['date']] - timedelta(days=offset - 365)).dt.dayofyear
    else:
        output_df[temp_columns['day_of_year_offset']] = (
                (output_df[temp_columns['day_of_year']] + 364 - offset) % 365 + 1
        )


    # 计算偏移后的年份边界
    if leap_year == 0:
        output_df[temp_columns['year_offset_start']] = output_df[temp_columns['year']]
        output_df.loc[
            output_df[temp_columns['day_of_year']] < output_df[temp_columns['day_of_year_offset']],
            temp_columns['year_offset_start']
        ] = output_df[temp_columns['year']] - 1

        output_df[temp_columns['year_offset_end']] = output_df[temp_columns['year']]
        output_df.loc[
            output_df[temp_columns['day_of_year']] > output_df[temp_columns['day_of_year_offset']],
            temp_columns['year_offset_end']
        ] = output_df[temp_columns['year']] +1
    else:
        output_df[temp_columns['year_offset_start']] = (
            output_df[temp_columns['year']] +
            (output_df[temp_columns['day_of_year']] + 364 - offset) // 365 - 1
        )
        output_df[temp_columns['year_offset_end']] = (
            output_df[temp_columns['year']] +
            (output_df[temp_columns['day_of_year']] + 364 - offset) // 365
        )

    # 格式化 year 列的展示格式
    output_df[temp_columns['year_offset_start']] = output_df[temp_columns['year_offset_start']].astype(str)
    if year_format == 4:
        output_df[temp_columns['year_offset_start']] = output_df[temp_columns['year_offset_start']].str[-2:]

    output_df[temp_columns['year_offset_end']] = output_df[temp_columns['year_offset_end']].astype(str)
    if year_format != 8:
        output_df[temp_columns['year_offset_end']] = output_df[temp_columns['year_offset_end']].str[-2:]

    # 连接计算后的年份边界
    output_df[temp_columns['year_offset']] = (
            output_df[temp_columns['year_offset_start']] +
            connect +
            output_df[temp_columns['year_offset_end']]
    )


    # 创建要输出的列
    output_df['year'] = output_df[temp_columns['year_offset']]
    output_df['day_of_year'] = output_df[temp_columns['day_of_year_offset']]

    # 清理临时列
    temp_cols_to_drop = list(temp_columns.values())
    output_df.drop(columns=temp_cols_to_drop, inplace=True, axis=1)


    return output_df
