
## Open Meteo 基本信息

- **链接**：[Open-Meteo](https://open-meteo.com/)

## API 提供的历史日频指标

### 基础信息

| 序号  | 气象指标         | 中文含义 |
| --- | ------------ | ---- |
| 1   | weather_code | 天气代码 |

### 温度

| 序号  | 气象指标                                | 中文含义      |
| --- | ----------------------------------- | --------- |
| 1   | temperature_2m_mean                 | 平均气温¹     |
| 2   | temperature_2m_max                  | 最高气温¹     |
| 3   | temperature_2m_min                  | 最低气温¹     |
| 4   | apparent_temperature_mean           | 平均体感温度    |
| 5   | apparent_temperature_max            | 最高体感温度    |
| 6   | apparent_temperature_min            | 最低体感温度    |
| 7   | wet_bulb_temperature_2m_mean        | 平均湿球温度¹ ² |
| 8   | wet_bulb_temperature_2m_max         | 最高湿球温度¹ ² |
| 9   | wet_bulb_temperature_2m_min         | 最低湿球温度¹ ² |
| 10  | growing_degree_days_base_0_limit_50 | 生长度日³     |

备注：
1. 测量高度距离地面 2 米；
2. 「湿球温度」是空气通过蒸发水汽冷却所能达到的温度，反映“蒸发冷却”的极限；
3. 基于0°C下限和50°C上限的积温，用于农业生长计算；

### 降水相关

| 序号  | 气象指标                           | 中文含义     |
| --- | ------------------------------ | -------- |
| 1   | precipitation_hours            | 降水小时数    |
| 2   | precipitation_probability_mean | 平均降水概率   |
| 3   | precipitation_probability_min  | 最小降水概率   |
| 4   | precipitation_sum              | 总降水量     |
| 5   | rain_sum                       | 总降雨量     |
| 6   | snowfall_sum                   | 总降雪量     |
| 7   | snowfall_water_equivalent_sum  | 降雪水当量总和¹ |

备注：
1. 将雪量转换为等效降雨量；

### 湿度与蒸散



| 序号  | 气象指标                           | 中文含义       |
| --- | ------------------------------ | ---------- |
| 1   | relative_humidity_2m_mean      | 平均相对湿度¹    |
| 2   | relative_humidity_2m_max       | 最大相对湿度¹    |
| 3   | relative_humidity_2m_min       | 最小相对湿度¹    |
| 4   | dew_point_2m_mean              | 平均露点温度¹ ²  |
| 5   | dew_point_2m_max               | 最高露点温度¹ ²  |
| 6   | dew_point_2m_min               | 最低露点温度¹ ²  |
| 7   | vapour_pressure_deficit_max    | 最大水汽压差³    |
| 1   | et0_fao_evapotranspiration     | 参考作物蒸散发速度⁴ |
| 2   | et0_fao_evapotranspiration_sum | 参考作物蒸散发量⁴  |
| 3   | leaf_wetness_probability_mean  | 平均叶片湿润概率⁵  |

备注：
1. 测量高度距离地面 2 米；
2. 「露点」指空气冷却至饱和（相对湿度100%）时的温度，衡量空气中的水汽含量；
3. 「水汽压差」指「实际水汽压」与 「饱和水汽压」之间的差值，其中「实际水汽压」表示空气中实际存在的水汽量（与露点正相关）、「饱和水汽压」表示当前气温下空气所能容纳的最大水汽量（与温度正相关）；
4. 「参考作物蒸散」是联合国粮农组织（FAO）定义的参考作物蒸散量，表示理想化短草植被在充分供水条件下的水分蒸散量；
5. 「湿润」指植物叶片表面存在液态水，如露水、雨水、灌溉水等；

### 土壤

| 序号  | 气象指标                              | 中文含义           |
| --- | --------------------------------- | -------------- |
| 1   | soil_moisture_0_to_100cm_mean     | 0-100cm土壤平均湿度  |
| 2   | soil_moisture_0_to_10cm_mean      | 0-10cm土壤平均湿度   |
| 3   | soil_moisture_0_to_7cm_mean       | 0-7cm土壤平均湿度    |
| 4   | soil_moisture_7_to_28cm_mean      | 7-28cm土壤平均湿度   |
| 5   | soil_moisture_28_to_100cm_mean    | 28-100cm土壤平均湿度 |
| 6   | soil_temperature_0_to_100cm_mean  | 0-100cm土壤平均温度  |
| 7   | soil_temperature_0_to_7cm_mean    | 0-7cm土壤平均温度    |
| 8   | soil_temperature_7_to_28cm_mean   | 7-28cm土壤平均温度   |
| 9   | soil_temperature_28_to_100cm_mean | 28-100cm土壤平均温度 |


### 光照条件

| 序号  | 气象指标                    | 中文含义    |
| --- | ----------------------- | ------- |
| 1   | sunrise                 | 日出时间    |
| 2   | sunset                  | 日落时间    |
| 3   | daylight_duration       | 日照时长¹   |
| 4   | sunshine_duration       | 阳关直射时长² |
| 5   | shortwave_radiation_sum | 短波辐射总量³ |
| 6   | cloud_cover_mean        | 平均云量    |
| 7   | cloud_cover_max         | 最大云量    |
| 8   | cloud_cover_min         | 最小云量    |
| 9   | visibility_mean         | 平均能见度   |
| 10  | visibility_max          | 最大能见度   |
| 11  | visibility_min          | 最小能见度   |

备注：
1. 「日照时长」指从日出到日落的总时间；
2. 「阳关直射时长」指一天中实际被阳光直射的时间，剔除天气（云量、能见度）和地形（山脉、建筑物遮挡）影响的日照时长；
3. 「短波辐射总量」指单位面积地表在特定时间段接收的太阳短波辐射（含紫外、可见光、近红外波段）累计值；

### 大气

| 序号  | 气象指标                        | 中文含义      |
| --- | --------------------------- | --------- |
| 1   | wind_speed_10m_mean         | 平均风速¹     |
| 2   | wind_speed_10m_max          | 最大风速¹     |
| 3   | wind_speed_10m_min          | 最小风速¹     |
| 4   | wind_gusts_10m_mean         | 平均阵风¹     |
| 5   | wind_gusts_10m_max          | 最大阵风¹     |
| 6   | wind_gusts_10m_min          | 最小阵风¹     |
| 7   | wind_direction_10m_dominant | 主导风向¹     |
| 8   | updraft_max                 | 最大上升气流    |
| 9   | pressure_msl_mean           | 平均海平面气压   |
| 10  | pressure_msl_max            | 最大海平面气压   |
| 11  | pressure_msl_min            | 最小海平面气压   |
| 12  | surface_pressure_mean       | 平均地面气压    |
| 13  | surface_pressure_max        | 最大地面气压    |
| 14  | surface_pressure_min        | 最小地面气压    |
| 15  | cape_mean                   | 平均对流有效位能² |
| 16  | cape_max                    | 最大对流有效位能² |
| 17  | cape_min                    | 最小对流有效位能² |

备注：
1. 测量高度 10 米；
2. 衡量大气不稳定性和潜在对流强度的重要指标，常用于预测雷暴、强降水、冰雹甚至龙卷风等强对流天气，均值常用于评估区域性强对流天气的总体强弱、最大值用于定位对流最猛烈的区域、最小值用于排除非对流区域（或分析稳定天气的边界）；