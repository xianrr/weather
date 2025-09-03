"""
面向对象改写：将各区域的气象配置与数据加工逻辑抽象为类。
用法示例：
from meteo_config_oo import get_config
cfg = get_config("CN")  # 传入区域代号：CN/US/AU-RE/CBA/IM
df_prepared = cfg.prepare(raw_df)
print(cfg.daily_indicators)
for st in cfg.styles:
    print(st.path, st.column)

说明：
- 所有区域共享的“通用预处理（日期解析、年/年内日等）”在基类中实现。
- 各区域特有的派生指标（例如累计降水、7日/30日滚动、积温等）在子类中实现。
- 城市/国家/图表样式使用数据类（dataclass）来表达，更清晰更易维护。
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Tuple
import pandas as pd

# =========================
# 基础数据结构（数据类）
# =========================

@dataclass
class City:
    """ 城市（或州、省）下的经纬度样本集合
    - code: 城市/州代码
    - name: 名称
    - latitude/longitude: 该城市内一个或多个样本点的纬度、经度组成的
    - title_tag: （可选）标题附加标签，部分区域需要
    """
    code: str
    name: str
    latitude: List[float]
    longitude: List[float]
    title_tag: Optional[str] = None


@dataclass
class Country:
    """国家配置，包含若干城市样本。"""
    code: str
    name: str
    city_list: List[City]


@dataclass
class StyleConfig:
    """图表样式配置。
    - column: 需要绘制的数据列名（来自 prepare 之后的列）
    - min_history_year: 最小历史年份（用于过滤历史曲线）
    - ylabel: y 轴标题
    - title: 图表主标题前缀（通常后接城市/国家名）
    - path: 输出文件夹或文件名前缀
    - xlim: （可选）x 轴范围，例如积温图需要限制年内日
    """
    column: str
    min_history_year: int
    ylabel: str
    title: str
    path: str
    xlim: Optional[Tuple[int, int]] = None


# =========================
# 抽象基类：定义通用行为
# =========================

class MeteoConfigBase:
    """气象配置抽象基类。

    子类必须提供：
    - countries: List[Country]
    - daily_indicators: List[str]
    - styles: List[StyleConfig]

    并覆盖：
    - _customize(df): 根据区域规则生成派生指标列
    """

    countries: List[Country] = []
    daily_indicators: List[str] = []
    styles: List[StyleConfig] = []

    # -------- 通用预处理逻辑 --------
    def prepare(self, df: pd.DataFrame) -> pd.DataFrame:
        """统一的数据预处理入口。
        步骤：
        1) 日期解析，生成 year/day_of_year；
        2) 过滤闰日（仅保留 day_of_year <= 365）；
        3) 调用区域自定义处理，生成特定派生列（例如累计降水、滚动均值/和、积温等）。
        """
        d = df.copy()
        d['date'] = pd.to_datetime(d['date'], errors='coerce')
        d['year'] = d['date'].dt.year
        d['day_of_year'] = d['date'].dt.dayofyear
        d = d[d['day_of_year'] <= 365]
        d = self._customize(d)
        return d

    # -------- 区域个性化逻辑（由子类实现） --------
    def _customize(self, df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError

    # -------- 一些便捷属性/方法 --------
    @property
    def country_codes(self) -> List[str]:
        return [c.code for c in self.countries]

    @property
    def city_count(self) -> int:
        return sum(len(c.city_list) for c in self.countries)


# =========================
# AUS/EU/RU/UA（合并自 meteo_config_aure.py）
# =========================

class AureConfig(MeteoConfigBase):
    """澳洲/欧盟/俄罗斯/乌克兰组合配置。
    指标：temperature_2m_mean, precipitation_sum, soil_moisture_7_to_28cm_mean
    派生：cum_precip（年累计降水）, precip_sum7（7日累计降水）
    """

    # ---------- 数据（从原脚本迁移） ----------
    countries: List[Country] = [
        Country(
            code='AU', name='Australia', city_list=[
                City('(1)QLD','Queensland',[-22.38,-27.01,-28.14,-26.71,-23.78],[146.71,150.43,149.53,151.80,149.05]),
                City('(2)NSW','New South Wales',[-29.39,-29.48,-32.17,-35.14],[149.97,147.82,146.55,146.18]),
                City('(3)VIC','Victoria',[-35.32,-34.71,-35.80,-36.25],[144.31,141.95,142.20,143.69]),
                City('(4)SA','South Australia',[-33.55,-34.66,-32.77,-33.55],[135.24,137.69,138.16,139.06]),
                City('(5)WA','Western Australia',[-33.36,-33.30,-33.76,-32.09],[123.34,121.71,118.78,117.60]),
            ]
        ),
        Country(
            code='EU', name='Europe Union', city_list=[
                City('(1)ES','Spain',[42.07,40.92,38.92,41.83],[-5.56,-3.61,-2.94,-1.53]),
                City('(2)FR','France',[46.09,47.76,47.34,47.99,49.49,50.05],[-0.54,-1.20,2.03,4.07,4.61,2.74]),
                City('(3)DE','Germany',[50.58,51.83,53.12,53.27,49.73,48.35],[6.97,7.72,9.67,12.74,10.62,10.74]),
                City('(4)PL','Poland',[51.24,51.19,52.94,53.32,51.47],[15.56,17.59,17.42,19.91,22.90]),
                City('(5)RO','Romania',[46.05,45.53,47.68,46.32,45.19,45.16],[21.11,22.23,26.09,26.62,25.26,27.80]),
            ]
        ),
        Country(
            code='RU', name='Russia', city_list=[
                City('(1)ROS','Rostov',[47.64,48.79,47.86,46.75,46.26],[39.37,40.80,42.07,43.35,41.33]),
                City('(2)BEL','Belgorod',[50.78,50.58,50.18,51.23],[35.71,37.29,38.86,37.72]),
                City('(3)SAR','Saratov',[51.92,52.12,52.33,50.95,51.59],[43.02,45.43,47.73,46.52,49.60]),
                City('(4)ALT','Altai',[53.23,53.75,52.04,51.48,52.09],[78.72,83.08,81.35,82.83,85.20]),
                City('(5)STA','Stavropol',[45.89,45.04,44.60,44.54],[43.06,45.14,43.33,41.98]),
            ]
        ),
        Country(
            code='UA', name='Ukraine', city_list=[
                City('(1)CHE','Chernihiv',[51.61,51.56,50.89,51.35],[30.91,32.55,31.28,31.88]),
                City('(2)PLT','Poltava',[50.36,49.63,49.97,50.47,50.78],[32.81,32.95,34.37,35.14,34.08]),
                City('(3)VIN','Vinnytsia',[48.86,48.35,48.30,49.16],[27.97,28.39,29.02,29.38]),
                City('(4)DNP','Dnipropetrovsk',[48.19,47.96,49.00,48.36],[35.03,33.73,35.00,36.57]),
                City('(5)KHA','Kharkiv',[49.74,49.52,49.90,50.21],[35.71,36.54,37.48,36.44]),
                City('(6)ODE','Odesa',[45.89,46.24,47.05,47.37],[29.07,29.73,30.95,29.90]),
            ]
        ),
    ]

    daily_indicators: List[str] = [
        "temperature_2m_mean",
        "precipitation_sum",
        "soil_moisture_7_to_28cm_mean",
    ]

    styles: List[StyleConfig] = [
        StyleConfig('cum_precip', 2022, 'Precipitation (mm)', 'Cumulative Annual Precipitation of ', 'a_cum_precip'),
        StyleConfig('precip_sum7', 2024, 'Precipitation (mm)', 'Last 7 days Sum Precipitation of ', 'b_precip_sum7'),
        StyleConfig('soil_moisture_7_to_28cm_mean', 2022, 'Soil Moisture (m³/m³)', 'Soil Moisture (7-28cm) of ', 'c_soil_moisture'),
        StyleConfig('temperature_2m_mean', 2024, 'Temperature (°C)', 'Mean Temperature of ', 'd_temper'),
    ]

    def _customize(self, df: pd.DataFrame) -> pd.DataFrame:
        # 年累计降水：按年分组累加
        df['cum_precip'] = df.groupby('year')['precipitation_sum'].cumsum()
        # 7 日累计降水（滚动求和）
        df['precip_sum7'] = df['precipitation_sum'].rolling(window=7, min_periods=1).sum()
        return df


# =========================
# CBA（CA/BR/AR，来自 meteo_config_cba.py）
# =========================

class CbaConfig(MeteoConfigBase):
    """加拿大/巴西/阿根廷组合配置。
    指标：temperature_2m_mean, precipitation_sum, soil_moisture_7_to_28cm_mean
    派生：cum_precip（年累计降水）, precip_sum7（7日累计）, precip_sum30（30日累计）
    """

    countries: List[Country] = [
        Country('CA','Canada',[
            City('(01)SK','Saskatchewan',[49.48,50.42,52.26,50.75,50.87,50.15,51.70],[-102.53,-104.07,-104.35,-102.58,-105.68,-109.73,-109.77]),
            City('(02)AB','Alberta',[49.79,51.74,53.76,53.17,55.59],[-113.49,-114.27,-113.79,-111.36,-117.50]),
            City('(03)MB','Manitoba',[49.69,49.29,50.42],[-99.00,-101.19,-101.26]),
        ]),
        Country('BR','Brazil',[
            City('(01)MT','Mato Grosso',[-9.58,-11.42,-13.12,-13.47,-15.30],[-56.69,-51.25,-55.25,-58.88,-54.90]),
            City('(02)PR','Paraná',[-25.52,-26.49,-24.80,-23.31],[-54.22,-51.91,-50.53,-51.26]),
            City('(03)RS','Rio Grande do Sul',[-28.49,-29.02,-28.28,-30.83],[-55.71,-54.05,-50.89,-55.73]),
            City('(04)GO','Goiás',[-14.53,-16.33,-17.95],[-49.28,-47.50,-51.98]),
            City('(05)MS','Mato Grosso do Sul',[-19.58,-20.58,-22.81],[-53.16,-54.33,-55.56]),
            City('(06)MG','Minas Gerais',[-18.33,-20.04],[-47.46,-48.33]),
            City('(07)BA','Bahia',[-11.66,-13.44],[-45.00,-44.56]),
        ]),
        Country('AR','Argentina',[
            City('(01)B','Buenos Aires',[-38.16,-38.46,-36.59,-35.53,-34.65,-33.48],[-58.06,-60.34,-61.96,-60.26,-62.90,-60.33]),
            City('(02)X','Córdoba',[-33.57,-33.41,-33.16,-31.28,-30.74],[-64.69,-63.63,-62.23,-62.57,-63.84]),
            City('(03)S','Santa Fe',[-34.06,-33.05,-32.14,-32.00,-30.34],[-61.86,-60.96,-61.20,-61.74,-61.51]),
            City('(04)G','Santiago d Estero',[-28.55,-27.40,-26.52],[-62.30,-62.17,-63.00]),
        ]),
    ]

    daily_indicators: List[str] = [
        "temperature_2m_mean",
        "precipitation_sum",
        "soil_moisture_7_to_28cm_mean",
    ]

    styles: List[StyleConfig] = [
        StyleConfig('cum_precip', 2022, 'Precipitation (mm)', 'Cumulative Annual Precipitation of ', 'a_cum_precip'),
        StyleConfig('precip_sum7', 2024, 'Precipitation (mm)', 'Last 7 days Precipitation Summary of ', 'b_precip_sum7'),
        StyleConfig('precip_sum30', 2022, 'Precipitation (mm)', 'Last 30 days Precipitation Summary of ', 'c_precip_sum30'),
        StyleConfig('soil_moisture_7_to_28cm_mean', 2022, 'Soil Moisture (m³/m³)', 'Mean Soil Moisture (7-28cm) of ', 'd_soil_moisture'),
        StyleConfig('temperature_2m_mean', 2024, 'Temperature (°C)', 'Mean Temperature of ', 'e_mean_temper'),
    ]

    def _customize(self, df: pd.DataFrame) -> pd.DataFrame:
        df['cum_precip']   = df.groupby('year')['precipitation_sum'].cumsum()
        df['precip_sum7']  = df['precipitation_sum'].rolling(window=7,  min_periods=1).sum()
        df['precip_sum30'] = df['precipitation_sum'].rolling(window=30, min_periods=1).sum()
        return df


# =========================
# CN（来自 meteo_config_cn.py）
# =========================

class CnConfig(MeteoConfigBase):
    """中国配置。
    指标：temperature_2m_mean, precipitation_sum, soil_moisture_7_to_28cm_mean
    派生：cum_precip, precip_sum7, degree_day（4月15日后且 T>=10 的积温）
    """

    countries: List[Country] = [
        Country('CN','China',[
            City('(1)HL','Heilongjiang',[45.71,47.25,50.20,46.70,46.80,46.66],[126.91,124.12,127.49,131.19,130.15,127.07]),
            City('(2)JL','Jilin',[45.16,45.60,43.92,43.70,43.34],[124.93,122.72,125.12,126.42,128.34]),
            City('(3)NM','Nei Mongolia',[43.57,42.22,46.08,49.18],[122.32,118.96,122.19,119.82]),
            City('(4)LN','Liaoning',[42.26,42.12,41.88],[123.80,121.73,123.29]),
            City('(5)SD','Shandong',[35.37,35.17,37.41,37.49],[116.71,115.43,118.12,116.43]),
            City('(6)HE','Hebei',[37.94,36.59,36.98,37.78],[114.80,114.63,114.63,115.56]),
            City('(7)HA','Henan',[32.98,33.01,33.63,34.43],[112.64,114.10,114.59,115.75]),
            City('(8)AH','Anhui',[33.86,32.93],[115.82,117.52]),
        ])
    ]

    daily_indicators: List[str] = [
        "temperature_2m_mean",
        "precipitation_sum",
        "soil_moisture_7_to_28cm_mean",
    ]

    styles: List[StyleConfig] = [
        StyleConfig('cum_precip', 2022, 'Precipitation (mm)', 'Cumulative Annual Precipitation of ', 'a_cum_precip'),
        StyleConfig('precip_sum7', 2022, 'Precipitation (mm)', 'Last 7 days Sum Precipitation of ', 'b_precip_sum7'),
        StyleConfig('soil_moisture_7_to_28cm_mean', 2022, 'Soil Moisture (m³/m³)', 'Mean Soil Moisture (7-28cm) of ', 'c_soil_moisture'),
        StyleConfig('temperature_2m_mean', 2024, 'Temperature (°C)', 'Mean Temperature of ', 'd_mean_temper'),
        StyleConfig('degree_day', 2024, 'Degree Day (°C)', 'Degree Day after 15th Apr. of ', 'e_degree_day', xlim=(105,260)),
    ]

    def _customize(self, df: pd.DataFrame) -> pd.DataFrame:
        df['cum_precip']  = df.groupby('year')['precipitation_sum'].cumsum()
        df['precip_sum7'] = df['precipitation_sum'].rolling(window=7, min_periods=1).sum()
        # 积温：从年内第 105 天（约 4/15）开始，且日均温 >= 10℃ 时累加
        t = pd.Series(0.0, index=df.index)
        mask = (df['day_of_year'] > 105) & (df['temperature_2m_mean'] >= 10)
        t.loc[mask] = df.loc[mask, 'temperature_2m_mean']
        df['degree_day'] = t.groupby(df['year']).cumsum()
        return df


# =========================
# IM（ID/MY，来自 meteo_config_im.py）
# =========================

class ImConfig(MeteoConfigBase):
    """印尼/马来配置。
    指标：temperature_2m_mean, precipitation_sum, soil_moisture_28_to_100cm_mean
    派生：cum_precip, precip_ma7（7日均值）, precip_ma30（30日均值）, temper_ma5（5日均温）
    """

    countries: List[Country] = [
        Country('ID','Indonesia',[
            City('(1)RI','Riau',[1.55,-0.28,0.59],[100.73,102.05,100.98], title_tag='(#1 20%)'),
            City('(2)SU','North Sumatra',[3.92,2.92,1.48],[98.18,99.54,99.94], title_tag='(#2 12%)'),
            City('(3)KT','Central Kalimantan',[-2.37,-2.38,-3.36],[111.79,112.74,113.77], title_tag='(#2 12%)'),
            City('(4)KI','East Kalimantan',[-1.63,0.19,1.22],[116.18,116.90,117.83], title_tag='(#4 10%)'),
            City('(5)KB','West Kalimantan',[1.48,0.14,0.26,-1.66],[109.68,110.44,111.39,110.46], title_tag='(#5 9%)'),
            City('(6)JA','Jambi',[-0.94,-2.11,-1.83],[103.20,102.68,103.44], title_tag='(#6)'),
            City('(7)SS','South Sumatra',[-3.56,-2.89,-2.53],[103.84,105.02,104.25], title_tag='(#7)'),
        ]),
        Country('MY','Malaysia',[
            City('(1)S','Sabah',[5.80,5.57,5.28,4.58],[117.54,118.27,119.11,117.75], title_tag='(#1 24%)'),
            City('(2)Q','Sarawak',[4.23,3.21,2.73,2.45],[114.09,113.27,112.42,111.76], title_tag='(#2 21%)'),
            City('(3)J','Johor',[1.78,1.99,2.32],[104.04,103.35,102.52], title_tag='(#3 16%)'),
            City('(4)C','Pahang',[2.89,3.61,3.98],[102.80,103.06,102.38], title_tag='(#4 16%)'),
            City('(5)A','Parak',[4.16,4.91],[100.93,100.70], title_tag='(#5 10%)'),
        ]),
    ]

    daily_indicators: List[str] = [
        "temperature_2m_mean",
        "precipitation_sum",
        "soil_moisture_28_to_100cm_mean",
    ]

    styles: List[StyleConfig] = [
        StyleConfig('cum_precip', 2022, 'Precipitation (mm)', 'Cumulative Annual Precipitation of ', 'a_cum_precip'),
        StyleConfig('precip_ma7', 2024, 'Precipitation (mm)', 'Last 7 days Mean Precipitation of ', 'b_precip_ma7'),
        StyleConfig('precip_ma30', 2024, 'Precipitation (mm)', 'Last 30 days Mean Precipitation of ', 'c_precip_ma30'),
        StyleConfig('soil_moisture_28_to_100cm_mean', 2022, 'Soil Moisture (m³/m³)', 'Soil Moisture (28-100cm) of ', 'd_soil_moisture'),
        StyleConfig('temper_ma5', 2024, 'Temperature (°C)', 'Last 5 days Mean Temperature of ', 'e_temper_ma5'),
    ]

    def _customize(self, df: pd.DataFrame) -> pd.DataFrame:
        df['cum_precip'] = df.groupby('year')['precipitation_sum'].cumsum()
        # 降水：7/30 日滚动“均值”
        df['precip_ma7']  = df['precipitation_sum'].rolling(window=7,  min_periods=1).mean()
        df['precip_ma30'] = df['precipitation_sum'].rolling(window=30, min_periods=1).mean()
        # 气温：5 日滚动均温
        df['temper_ma5']  = df['temperature_2m_mean'].rolling(window=5,  min_periods=1).mean()
        return df


# =========================
# US（来自 meteo_config_us.py）
# =========================

class UsConfig(MeteoConfigBase):
    """美国配置。
    指标：temperature_2m_mean, precipitation_sum, soil_moisture_7_to_28cm_mean
    派生：cum_precip, precip_sum7, degree_day（4/15 后且 T>=10 的积温）
    """

    countries: List[Country] = [
        Country('US','United States',[
            City('(1)IA','Iowa',[43.37,42.67,43.29,43.31,42.95,42.04],[-96.30,-95.87,-92.14,-93.84,-94.04,-94.12]),
            City('(2)IL','Illinois',[40.05,40.91,41.89,41.08,39.99],[-91.27,-90.34,-89.93,-87.81,-89.17]),
            City('(3)NE','Nebraska',[42.36,42.68,40.12,40.20,41.23,40.76],[-99.16,-97.27,-96.93,-95.75,-96.39,-99.70]),
            City('(4)MN','Minnesota',[43.74,44.15,43.64,45.77,46.27,43.62],[-96.28,-95.23,-94.08,-96.38,-95.85,-92.53]),
            City('(5)KS','Kansas',[39.91,37.15,37.14,38.11],[-95.61,-100.78,-94.80,-94.83]),
            City('(6)ND','North Dakota',[47.20,46.95,48.15,46.17,46.59],[-97.40,-99.62,-97.45,-100.11,-97.80]),
        ])
    ]

    daily_indicators: List[str] = [
        "temperature_2m_mean",
        "precipitation_sum",
        "soil_moisture_7_to_28cm_mean",
    ]

    styles: List[StyleConfig] = [
        StyleConfig('cum_precip', 2022, 'Precipitation (mm)', 'Cumulative Annual Precipitation of ', 'a_cum_precip'),
        StyleConfig('precip_sum7', 2022, 'Precipitation (mm)', 'Last 7 days Sum Precipitation of ', 'b_precip_sum7'),
        StyleConfig('soil_moisture_7_to_28cm_mean', 2022, 'Soil Moisture (m³/m³)', 'Mean Soil Moisture (7-28cm) of ', 'c_soil_moisture'),
        StyleConfig('temperature_2m_mean', 2024, 'Temperature (°C)', 'Mean Temperature of ', 'd_mean_temper'),
        StyleConfig('degree_day', 2024, 'Degree Day (°C)', 'Degree Day after 15th Apr. of ', 'e_degree_day', xlim=(105,260)),
    ]

    def _customize(self, df: pd.DataFrame) -> pd.DataFrame:
        df['cum_precip']  = df.groupby('year')['precipitation_sum'].cumsum()
        df['precip_sum7'] = df['precipitation_sum'].rolling(window=7, min_periods=1).sum()
        # 积温规则同中国：从年内第 105 天起，且 T>=10℃ 时累加
        t = pd.Series(0.0, index=df.index)
        mask = (df['day_of_year'] > 105) & (df['temperature_2m_mean'] >= 10)
        t.loc[mask] = df.loc[mask, 'temperature_2m_mean']
        df['degree_day'] = t.groupby(df['year']).cumsum()
        return df


# =========================
# 简单工厂：按区域代号获取配置实例
# =========================

def get_config(region: str) -> MeteoConfigBase:
    """根据区域代号返回对应配置：
    - "AU-RE": 澳洲/欧盟/俄罗斯/乌克兰（AureConfig）
    - "CBA"  : 加拿大/巴西/阿根廷（CbaConfig）
    - "CN"   : 中国（CnConfig）
    - "IM"   : 印尼/马来（ImConfig）
    - "US"   : 美国（UsConfig）
    """
    key = region.strip().upper()
    if key in {"AU", "EU", "RU", "UA", "AU-RE", "AURE"}:
        return AureConfig()
    if key == "CBA":
        return CbaConfig()
    if key == "CN":
        return CnConfig()
    if key in {"IM", "ID", "MY"}:
        return ImConfig()
    if key == "US":
        return UsConfig()
    raise ValueError(f"未知区域代号：{region}")

