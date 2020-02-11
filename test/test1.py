#!/usr/bin/env python3
# -*-coding:utf-8-*-
# __author__: hunter

import requests
import json
from pyecharts import options as opts
from pyecharts.charts import Geo
from pyecharts.globals import GeoType, RenderType

# 腾讯数据源
url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"
res = json.loads(requests.get(url).json()["data"])
datas = res["areaTree"][0]["children"]
# 全国数据做副标题
china_total = "确诊:{} 疑似:{} 治愈:{} 死亡:{} 更新日期:{}".format(res["chinaTotal"]["confirm"],
                                                       res["chinaTotal"]["suspect"], res["chinaTotal"]["heal"],
                                                       res["chinaTotal"]["dead"], res["lastUpdateTime"])
provinces = []
confirm_value = []

# 遍历获取各省份数据
for data in datas:
    provinces.append(data["name"])
    confirm_value.append(data["total"]["confirm"])

# 链式调用

geo = (
    Geo(init_opts = opts.InitOpts(width="1200px",height="600px",
                                  bg_color="#404a59",page_title="全国疫情实时报告",
                                  renderer=RenderType.SVG,theme="white"))#设置绘图尺寸，背景色，页面标题，绘制类型
    .add_schema(maptype="china",itemstyle_opts=opts.ItemStyleOpts(color="rgb(49,60,72)",border_color="rgb(0,0,0)"))#中国地图，地图区域颜色，区域边界颜色
    # .add(series_name="geo",data_pair=data,type_=GeoType.EFFECT_SCATTER)#设置地图数据，动画方式为涟漪特效effect scatter
    .set_series_opts(#设置系列配置
        label_opts=opts.LabelOpts(is_show=False),#不显示Label
        effect_opts = opts.EffectOpts(scale = 6))#设置涟漪特效缩放比例
    .set_global_opts(#设置全局系列配置
        visualmap_opts=opts.VisualMapOpts(is_piecewise=True, pieces=[
            {"min": 1000, "color": "#70161d"},
            {"min": 500, "max": 1000, "color": "#cb2a2f"},
            {"min": 100, "max": 500, "color": "#e55a4e"},
            {"min": 10, "max": 100, "color": "#f59e83"},
            {"min": 1, "max": 10, "color": "#fdebcf"}
        ]),#设置视觉映像配置，最大值为平均值
        title_opts=opts.TitleOpts(title="全国疫情地图", subtitle=china_total,pos_left="center",pos_top="10px",title_textstyle_opts=opts.TextStyleOpts(color="#fff")),#设置标题，副标题，标题位置，文字颜色
        legend_opts = opts.LegendOpts(is_show=False),#不显示图例
    )
)

geo.render()