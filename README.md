
# 使用说明


## 文件目录结构

- `weather` 文件根目录
  - `dataset` 用于原始数据的存放
    - `AR_2015-2024.csv` 
    - `XX_YYYY_YYYY.csv` 其他数据文件
  - `diagram` 图表保存一级路径
    - `CN` 图表保存二级路径
      - `.jpg` 输出的图表
  - `src` 可以复用的资源包
    - `open_meteo_indicator.md` Open-Meteo 提供的天气指标及其含义
    - `charts.py` 通用的绘图方法
    - `om_api.py` 通用的 API 请求方法
    - `meteo_congfig_xx.py` 记录绘图所需的配置信息
    - `weather_history_saver.py` 历史数据存储
    - `weather_charts_builder.py` 批量图表绘制
  - `weather_xx.ipynb` 数据加工代码


## 文件依赖关系

```mermaid
flowchart LR
id1(config.py)
id2(om_api.py)
id3(history_saver.py)
id4(weather.ipynb)
id5(.csv)
id8(charts.py)
id6(chart_builder.py)
id7(.jpg)
id1 --> id4
id2 --> id4
id3 --> id4
id4 --> id5
id1 --> id6
id2 --> id6
id5 --> id6
id8 --> id6
id6 --> id7
```

## `config` 文件配置规范

- 属性
  - `countries`
  - `daily_indicators`
  - `styles`
- 方法
  - `data_prapare()`

### 属性 `countries`

```python
countries = [
  {
    'code': 'US',
    'name': 'United States',
    'city_list': city_list
  },{
     ...
  }
]

# 实际代码中 city_list 应当在 countries 上方，否则会报错：未定义变量 city_list
city_list = [
  {
    'code': '(1)IA',
    'name': 'Iowa',
    'latitude':  [ 43.37,  42.67,  43.29,  43.31],
    'longitude': [-96.30, -95.87, -92.14, -93.84]
  }
]
```

注意事项：

- `countries` 
  - 类型为 `list` 数组
  - 可以多个国家，也可以只有一个国家
  - 即便只有一个国家，也需要用方括号包围
- 假设 `country = countries[i]` 其中 `i` 为整数
  - `country` 的类型为 `dict` 字典
  - `country['code']` 
    - 代表国家的代码
    - 参考标准 ***ISO 3166-1, alpha-2***
    - 用于控制图表保存「二级路径」
    - 用于控制图表「文件名」
  - `country['name']`
    - 代表为国家的英文名称（简称即可）
    - 用于控制图表的「标题」
- `city_list`
  - 类型为 `list` 数组
  - 可以多个城市，也可以只有一个城市
  - 控制一个 `csv` 文件「包含的城市」
- 假设 `city = city_list[i]` 其中 `i` 为整数
  - `city['code']`
    - （序号）+代表城市的代码
    - 参考标准 ***ISO 3166-2*** （如该标准为数字则自编，如乌克兰、马来西亚）
    - 用于控制图表「文件名」
  - `city['name']`
    - 城市名称
    - 用于控制图表「标题」
  - `city['latitude']`
    - 类型为 `list` 数组
    - 包含一个或者多个 `float` 浮点数
    - 数据范围 `[-90, 90]` 负数为南纬、正数为北纬
    - 注意进制转换例如 23°30' 为 23.5 而非 23.3
    - 建议保留两位小数点即可（赤道上纬度相差 1° 大约为 111.14 公里）
  - `city['longitude']`
    - 同 `city['latitude']`
    - 数据范围 `[-180, 180]` 负数为西经、正数为东经
    - 数量需要与 `city['latitude']` 保持一致

### 属性 `daily_indicators`

见 [open_meteo_indicator](src/OPEN-METEO-INDICATOR.md) 或官方文档

### 属性 `styles`

```python
styles = [
  {
    'column': 'cum_precip',
    'min_history_year' : 2022,
    'ylabel' : 'Precipitation (mm)',
    'title' : 'Cumulative Annual Precipitation of ',
    'path' : 'a_cum_precip'
  }
]
```

注意事项：

- `styles` 类型为 `list` 数组
- 假设 `style = styles[i]` 其中 `i` 为整数
  - `style['column']` 控制制图的数据列（选取 `pandas.DataFrame` 的列明
  - `style['min_history_year']` 控制显示的最小历史年份
  - `style['ylabel']` 控制 y 轴标题
  - `style['title']` 控制图表的标题名称
  - `style['path']` 控制输出图表文件名称


### 方法 `data_prapare(df:pandas.DataFrame) -> pandas.DataFrame`

如果获取到的指标不能直接使用，使用该方法对指标进行加工。例如：

- 将「降水」加工为「年度累计降水」
- 将「气温」数据取前五日滚动平均值进行平滑
- 等等

注意事项：

- 确保数据有一列为 `date` 且保存着日期数据
- 加工后的列，如需绘制图表，列名需与 `style['column']` 保持一致


















