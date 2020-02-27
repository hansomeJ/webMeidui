from django.shortcuts import render

# Create your views here.

from pyecharts.commons.utils import JsCode
from pyecharts.charts import Line
from deviceManage.models import equipment, data, equipmentAttr, warning
from pyecharts import options as opts
import re


def line_color_with_js_func(time, temperature, voltage, name) -> Line:
    background_color_js = (
        "new echarts.graphic.LinearGradient(0, 0, 0, 1, "
        "[{offset: 0, color: '#c86589'}, {offset: 1, color: '#06a7ff'}], false)"
    )
    area_color_js = (
        "new echarts.graphic.LinearGradient(0, 0, 0, 1, "
        "[{offset: 0, color: '#eb64fb'}, {offset: 1, color: '#3fbbff0d'}], false)"
    )

    c = (
        Line(init_opts=opts.InitOpts(bg_color=JsCode(background_color_js)))
            .add_xaxis(xaxis_data=time)
            .add_yaxis(
            markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")]),
            series_name="温度",
            y_axis=temperature,
            is_smooth=True,
            is_symbol_show=True,
            symbol="circle",
            symbol_size=6,
            linestyle_opts=opts.LineStyleOpts(color="#fff"),
            label_opts=opts.LabelOpts(is_show=True, position="top", color="white"),
            itemstyle_opts=opts.ItemStyleOpts(
                color="red", border_color="#fff", border_width=3
            ),
            tooltip_opts=opts.TooltipOpts(is_show=False),
            areastyle_opts=opts.AreaStyleOpts(color=JsCode(area_color_js), opacity=1),
        )
            .add_yaxis(
            markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")]),
            series_name="电压",
            y_axis=voltage,
            is_smooth=True,
            is_symbol_show=True,
            symbol="circle",
            symbol_size=6,
            linestyle_opts=opts.LineStyleOpts(color="#fff"),
            label_opts=opts.LabelOpts(is_show=True, position="top", color="white"),
            itemstyle_opts=opts.ItemStyleOpts(
                color="red", border_color="#fff", border_width=3
            ),
            tooltip_opts=opts.TooltipOpts(is_show=False),
            areastyle_opts=opts.AreaStyleOpts(color=JsCode(area_color_js), opacity=1),
        )
            .extend_axis(
            yaxis=opts.AxisOpts(
                type_="value",
                position="right",
                axislabel_opts=opts.LabelOpts(margin=20, color="#ffffff63"),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(width=2, color="#fff")
                ),
                axistick_opts=opts.AxisTickOpts(
                    is_show=True,
                    length=15,
                    linestyle_opts=opts.LineStyleOpts(color="#ffffff1f"),
                ),
                splitline_opts=opts.SplitLineOpts(
                    is_show=True, linestyle_opts=opts.LineStyleOpts(color="#ffffff1f")
                ),
            ),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(
                title=name + "-温度变化（单位：摄氏度）电压变化（单位：伏特）",
                pos_bottom="5%",
                pos_left="center",
                title_textstyle_opts=opts.TextStyleOpts(color="#fff", font_size=16),
            ),
            xaxis_opts=opts.AxisOpts(
                type_="category",
                boundary_gap=False,
                axislabel_opts=opts.LabelOpts(margin=30, color="#ffffff63"),
                axisline_opts=opts.AxisLineOpts(is_show=False),
                axistick_opts=opts.AxisTickOpts(
                    is_show=True,
                    length=25,
                    linestyle_opts=opts.LineStyleOpts(color="#ffffff1f"),
                ),
                splitline_opts=opts.SplitLineOpts(
                    is_show=True, linestyle_opts=opts.LineStyleOpts(color="#ffffff1f")
                ),
            ),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                # position="right",
                axislabel_opts=opts.LabelOpts(margin=20, color="#ffffff63"),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(width=2, color="#fff")
                ),
                axistick_opts=opts.AxisTickOpts(
                    is_show=True,
                    length=15,
                    linestyle_opts=opts.LineStyleOpts(color="#ffffff1f"),
                ),
                splitline_opts=opts.SplitLineOpts(
                    is_show=True, linestyle_opts=opts.LineStyleOpts(color="#ffffff1f")
                ),
            ),
            legend_opts=opts.LegendOpts(is_show=False),
        )
    )
    return c


def index(request, id):
    # time = ['2020-02-03 09:50:36','2020-02-03 09:50:46','2020-02-03 09:50:56','2020-02-03 09:51:06','2020-02-03 09:51:16']
    # temperature = ['27.17','95.17','65.17','25.17','45.17']
    device = equipment.objects.get(pk=id)
    datas = data.objects.filter(equipment_id=device)
    name = device.name
    time = []
    temperature = []
    voltage = []
    for i in datas:
        t = i.time.strftime("%Y-%m-%d %H:%M:%S")
        temp = float(re.findall('[0-9.]+', i.temperature)[0])
        volt = float(re.findall('[0-9.]+', i.voltage)[0])
        time.insert(0, t)
        temperature.insert(0, temp)
        voltage.insert(0, volt)
    print(time, temperature)
    path: str = "./templates/viewData/render.html"
    line_color_with_js_func(time, temperature, voltage, name).render(path)
    return render(request, 'viewData/render.html')
