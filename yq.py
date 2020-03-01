#!/usr/bin/env python
# -*- coding: utf-8 -*-

def get_ncp_raw_data():
    qq_url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'}
    qq_req = requests.get(qq_url, headers)
    qq_res = json.loads(qq_req.text)
    ncp_raw_data = json.loads(qq_res['data'])
    return ncp_raw_data

##2020/02/24 update for hubei/quanguo daylist
def get_day_raw_data():
    qq_url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_other"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'}
    qq_req = requests.get(qq_url, headers)
    qq_res = json.loads(qq_req.text)
    day_raw_data = json.loads(qq_res['data'])
    return day_raw_data

def get_total_ncp_data():
    input_data  = get_ncp_raw_data()
    total_ncp_data = input_data['chinaTotal']
    return total_ncp_data

def get_day_ncp_data():
    input_data  = get_day_raw_data()
    day_ncp_data = input_data['chinaDayList']
    return day_ncp_data

def get_day_newadd_ncp_data():
    input_data  = get_day_raw_data()
    day_newadd_ncp_data = input_data['dailyNewAddHistory']
    return day_newadd_ncp_data

def get_ncp_updatetime():
    input_data  = get_ncp_raw_data()
    ncp_updatetime = input_data['lastUpdateTime']
    return ncp_updatetime

def get_pc_ncp_data():
    input_data = get_ncp_raw_data()
    pc_ncp_data = input_data['areaTree'][0]['children']
    pc_ncp_list =[]
    for i in range(len(pc_ncp_data)):
        pc_ncp_list.append([pc_ncp_data[i]["name"],pc_ncp_data[i]["total"]['confirm']])
    return pc_ncp_list


if __name__  == '__main__':
    # import module
    from pyecharts import options as opts
    from pyecharts.charts import Bar, Grid, Line, Page, Pie
    import requests
    import json
    from pyecharts.charts import Map, Geo
    from pyecharts import options
    from pyecharts.globals import GeoType



    # get the hubei and country new add data
    dayadd_his = get_day_newadd_ncp_data()
    dayadd_date = []
    qg_dayadd = []
    hb_dayadd =[]
    nohb_dayadd = []
    for i in dayadd_his:
        dayadd_date.append(i['date'])
        qg_dayadd.append(i['country'])
        hb_dayadd.append(i['hubei'])
        nohb_dayadd.append(i['notHubei'])



    # change the key to chinese
    total = get_total_ncp_data()

    total["confirm"] = total["confirm"] - total['heal'] - total['dead'] - total['nowSevere']
    del total["nowConfirm"]

    total["确诊"] = total.pop("confirm")
    total["疑似"] = total.pop("suspect")
    total["死亡"] = total.pop("dead")
    total["治愈"] = total.pop("heal")
    total["重症"] = total.pop("nowSevere")

    print(total)


    #format the chinatotaldata for pie
    china_data_list = []
    temp_tupe = ()
    for k,v in total.items():
        temp_tupe = (k,v)
        china_data_list.append(temp_tupe)

    def pie_rosetype(data_list) -> Pie:
        c = (
            Pie()
                .add("", data_list)
                .set_global_opts(title_opts=opts.TitleOpts(title="全国肺炎数据汇总"))
                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        )
        return c


    ####day dead/heal data compare format for datazoom
    day_data = get_day_ncp_data()
    date_list = []
    total_day_confirm = []
    total_day_dead = []
    total_day_heal = []
    hb_day_confirm = []

    for i in day_data:
        date_list.append(i['date'])
        total_day_confirm.append(i['confirm'])
        total_day_dead.append(i['dead'])
        total_day_heal.append(i['heal'])

    print(total_day_dead)
    print(total_day_heal)

    def bar_datazoom_slider() -> Bar:
        c = (
            Bar()
                .add_xaxis(date_list)
                .add_yaxis("死亡人数", total_day_dead, color='green')
                .add_yaxis("治愈人数", total_day_heal, color='black')
                .set_global_opts(
                title_opts=opts.TitleOpts(title="全国肺炎康复/死亡人数对比"),
                datazoom_opts=[opts.DataZoomOpts()],
            )
        )
        return c



    #####日均增加全国对比湖北#####
    def line_base() -> Line:
        c = (
            Line()
                .add_xaxis(dayadd_date)
                .add_yaxis("全国", qg_dayadd)
                .add_yaxis("湖北", hb_dayadd)
                .add_yaxis("其他地区", nohb_dayadd)
                .set_global_opts(title_opts=opts.TitleOpts(title="每日新增确诊人数走势"))
        )
        return c

    #####全国数地图###
    update_time = get_ncp_updatetime()

    title_ncp_summary = "最近更新：" + str(update_time) + " 确诊: " + str(total['确诊']) + " 疑似: " + str(
        total['疑似']) + " 死亡：" + str(total['死亡']) + " 治愈：" + str(total['治愈'])

    pc_list = get_pc_ncp_data()
    # max_ncp_pc = (max(pc_list, key=lambda x:int(x[1])))
    max_ncp_pc_data = total['确诊'] / 34


    def geo_map() -> Geo:
        output = (
            Geo(init_opts=options.InitOpts(width="700px", height="500px", bg_color="#FFFFFF", page_title="全国疫情实时数据"))
                .add_schema(maptype="china", itemstyle_opts=options.ItemStyleOpts(color="RGB(204,204,204)", border_color="rgb(204,51,51)"),is_roam="false")
                .add("geo", data_pair=pc_list, type_=GeoType.EFFECT_SCATTER)
                .set_series_opts(
                label_opts=options.LabelOpts(is_show=False), effect_opts=options.EffectOpts(scale=6))
                .set_global_opts(
                visualmap_opts=options.VisualMapOpts(is_piecewise=True,pieces=[{"min":1, "max":9, "label": '1到9人'},{"min":10, "max":99,"label": '10到99人'},{"min":100,"max":499,"label": '100到499人'},{"min":500,"max":999,"label": '500到999人'},{"min":1000,"max":9999,"label": '1000到9999人'},{"min":10000,"label": '10000人以上'}]),
                title_opts=options.TitleOpts(title="全国疫情热点地图", subtitle=title_ncp_summary, pos_left="center",
                                             pos_top="10px", title_textstyle_opts=options.TextStyleOpts(color="#080808"),subtitle_textstyle_opts=options.TextStyleOpts(color="#080808")),
                legend_opts=options.LegendOpts(is_show=False))  # 不显示图例
        )
        return output

    page = Page(layout=Page.SimplePageLayout,page_title="疫情数据")
    # 需要自行调整每个 chart 的 height/width，显示效果在不同的显示器上可能不同
    page.add(geo_map(),pie_rosetype(china_data_list),bar_datazoom_slider(),line_base())
    page.render(path="./pie2.html")

