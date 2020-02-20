from flask import Flask, render_template,request
from pyecharts import options as opts
from pyecharts.charts import Map,Line
from pyecharts.globals import ThemeType


from pyecharts.components import Table
from pyecharts.options import ComponentTitleOpts
import json
import pandas as pd
import datetime

app = Flask(__name__, static_folder="templates",)


# 第一部分：图表创建
def map_base()->Map:
    """实时疫情地图"""
    file = '中国疫情数据（省级）.csv'
    data = get_data(file)
    dict_province = data.set_index('地区')['累计确诊病例'].to_dict()

    province = list(dict_province.keys())
    values = list(dict_province.values())

    c = (
        Map()
        .add("确诊人数", [list(z) for z in zip(province,values)], "china")
        .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="全国实时疫情分布地图"),
            visualmap_opts=opts.VisualMapOpts(max_= 10000,
                                              pieces=[{'min': 10000, 'label': '>10000', "color": "Maroon"},
                                                  {'min': 1000, 'max': 9999, 'label': '1000-9999',"color": "Crimson"},
                                                  {'min': 500, 'max': 999, 'label': '500-999', "color": "LightCoral"},
                                                  {'min': 100, 'max': 499, 'label': '100-499', "color": "NavajoWhite"},
                                                  {'min': 10, 'max': 99, 'label': '10-99', "color": "PapayaWhip"},
                                                  {'min': 1, 'max': 9, 'label': '1-9', "color": "FloralWhite"}],
                                              is_piecewise=True
                                              )
        )
    )
    return c

# 02. 疫情新增趋势图
def conf_new_base() -> Line:
    """全国疫情累计/现有疑似"""
    # 静态数据

    dataY1 = [59, 77, 149, 131, 256, 444, 688, 769, 1771, 1459, 1737, 1982, 2102, 2590, 2829, 3235, 3887]
    dataY2 = [59, 27, 149, 131, 680,1118,1309, 3806, 2077, 3248, 4148, 4812, 5019, 4562, 5173, 5072, 3971]
    dataX = ['2020.01.18', '2020.01.19', '2020.01.20', '2020.01.21', '2020.01.22','2020.01.23','2020.01.24','2020.01.25',
             '2020.01.26', '2020.01.27', '2020.01.28', '2020.01.29', '2020.01.30','2020.01.31','2020.02.01','2020.02.02',
             '2020.02.03', '2020.02.04']
    file = '中国疫情历史数据.csv'
    data = get_data(file)
    dict_suspect = data.set_index('日期')['疑似病例'].to_dict()
    dict_comfirm = data.set_index('日期')['累计确诊病例'].to_dict()
    comfirm_list = list(dict_comfirm.values())
    suspect_list = list(dict_suspect.values())
    date_list = list(dict_comfirm.keys())

    date_list = [city.strip("'") for city in date_list]


    print(suspect_list)
    print(comfirm_list)
    print(date_list)


    c = (
        Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis(date_list)
        .add_yaxis("累计确诊", comfirm_list, is_smooth=True)
        .add_yaxis("现有疑似", suspect_list, is_smooth=True)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="全国疫情新增确诊/疑似趋势图"),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
        )
    )
    return c




# 05. 全国各省市数据明细
def table_province():
    """全国各省数据明细"""
    file = '中国疫情数据（省级）.csv'
    data = get_data(file)
    dict_province = data.T.to_dict('list')
    province_data = list(dict_province.values())
    return province_data

def table_city():
    """全国各市数据明细"""
    file = '中国疫情数据（市级）.csv'
    city_data = get_data(file)
    dict_city = city_data.T.to_dict('list')
    city_list = list(dict_city.values())
    return city_list



def get_data(path):
    """文件读取并格式化"""
    csv_path = 'F:/Python/疫情数据/' + datetime.datetime.now().strftime('%F') + '疫情数据/'
    dict_data = pd.read_csv(csv_path + path, encoding='GB2312')
    return dict_data



# 第二部分：路由配置
@app.route("/")
def index():
    province = table_province()
    city = table_city()
    return render_template("index.html", province=province,city = city)


@app.route("/mapChart")
def get_map_chart():
    c = map_base()
    return c.dump_options_with_quotes()

@app.route("/confChart")
def get_conf_chart():
    c = conf_new_base()
    return c.dump_options_with_quotes()


# 主函数
if __name__ == "__main__":
    app.run()