import requests
import json
import csv
from fake_useragent import UserAgent
from _collections import defaultdict,OrderedDict
import datetime
import os

class COVID_19():

    def __init__(self):
        self.URL = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'


        ua = UserAgent()

        # DNT = Do not track Request Header
        # we need to add referer to show that we are inside the web
        self.headers = {'User-Agent': ua.chrome,'DNT': '1','Referer': 'https://news.qq.com/zt2020/page/feiyan.htm'}
        self.csv_path = 'F:/Python/疫情数据/'+ datetime.datetime.now().strftime('%F')+'疫情数据/'
        if os.path.exists(self.csv_path) is False:
            os.makedirs(self.csv_path)


    def get_page_data(self):
        """获取页面返回的json数据，并格式化数据"""

        page = requests.get(self.URL, headers=self.headers)
        page.encoding = 'UTF-8'

        # 将所有数据格式化为json数据
        formatted_data = json.loads(page.text)

        # 将所有疫情数据载入
        all_data = json.loads(formatted_data['data'])
        filename = self.csv_path + 'json_response.txt'
        with open(filename,'w',newline='') as temp:
            temp.write(json.dumps(all_data))
        temp.close()
        return all_data

    def get_global_data(self,items):
        """获取全球疫情数据"""

        # 数据格式化
        #全球数据结构（global_data）,OrderedDict为有序的字典
        dict_country = OrderedDict()

        # 全球疫情数据(json数据里面的list)
        global_data = items['areaTree']
        # 数据口径关闭
        # china_yesterday = items['chinaDayList'][-2]
        # print(china_yesterday)
        for country in global_data:
            country_data = []
            # 今日数据的获取
            country_data.append(country['name'])
            country_data.append(country['today']['confirm'])
            country_data.append(country['total']['suspect'])

            # 累计数据
            country_data.append(country['total']['confirm'])
            country_data.append(country['total']['heal'])
            country_data.append(country['total']['dead'])

            # if country['name'] == '中国':
            #     country_data.append(china_yesterday['confirm'])
            #     country_data.append(china_yesterday['suspect'])
            #     country_data.append(china_yesterday['heal'])
            #     country_data.append(china_yesterday['dead'])

               
            # print(country_data)
            dict_country[country_data[0]]=country_data

        filename = self.csv_path + '全球疫情数据.csv'
        first_row = ['国家',
                     '今日确诊病例',
                     '现有疑似病例',
                     '累计确诊病例',
                     '累计治愈病例',
                     '累计死亡病例',
                     '昨日累计确诊病例',
                     '昨日疑似病例',
                     '昨日治愈病例',
                     '昨日死亡病例'
                     ]
        self.write_csv(dict_country,first_row,filename)
        return dict_country

    def get_province_data(self,items):
        """获取各省疫情数据"""

        # 数据格式化
        # 各省数据结构（province_data）,OrderedDict为有序的字典
        dict_province = OrderedDict()

        # 各省疫情数据(json数据里面的list)
        province_data = items['areaTree'][0]['children']
        # province_yesterday = items['confirmAddRank']
        # print(china_yesterday)
        for province in province_data:
            province_data = []
            # 今日数据的获取
            province_data.append(province['name'])
            province_data.append(province['today']['confirm'])

            # 累计数据
            province_data.append(province['total']['confirm'])
            province_data.append(province['total']['heal'])
            province_data.append(province['total']['dead'])


            # 口径关闭
            # for yesterday_data in province_yesterday:
            #     if yesterday_data['name'] == province['name']:
            #         province_data.append(yesterday_data['before'])
            #         break


            dict_province[province_data[0]] = province_data

        filename = self.csv_path + '中国疫情数据（省级）.csv'
        first_row = ['地区',
                     '新增确诊病例',
                     '累计确诊病例',
                     '累计治愈病例',
                     '累计死亡病例'
                     ]
        self.write_csv(dict_province, first_row, filename)
        return dict_province

    def get_city_data(self, items):
        """获取各城市疫情数据"""

        # 数据格式化
        # 各城市数据结构（city_data）,OrderedDict为有序的字典
        dict_city = OrderedDict()


        # 各省疫情数据(json数据里面的list)
        province_data = items['areaTree'][0]['children']
        for province in province_data:
            for city in province['children']:
                # 今日数据的获取
                city_data = []
                city_data.append(province['name'])
                city_data.append(city['name'])
                city_data.append(city['today']['confirm'])
                # 累计数据的获取
                city_data.append(city['total']['confirm'])
                city_data.append(city['total']['heal'])
                city_data.append(city['total']['dead'])
                if city_data[1] == '地区待确认':
                    dict_city[city_data[0] + city_data[1]] = city_data
                else:
                    dict_city[city_data[1]] = city_data

        filename = self.csv_path + '中国疫情数据（市级）.csv'
        first_row = ['地区',
                     '城市',
                     '新增确诊病例',
                     '累计确诊病例',
                     '累计治愈病例',
                     '累计死亡病例'
                     ]
        self.write_csv(dict_city, first_row, filename)
        return dict_city

    def get_chinaHistory_data(self):
        """获取中国历史疫情数据"""

        page = requests.get('https://view.inews.qq.com/g2/getOnsInfo?name=disease_other', headers=self.headers)
        page.encoding = 'UTF-8'

        # 将所有数据格式化为json数据
        formatted_data = json.loads(page.text)

        # 将所有疫情数据载入
        all_data = json.loads(formatted_data['data'])
        filename = self.csv_path + 'json_response2.txt'
        with open(filename, 'a', newline='') as temp:
            temp.write(json.dumps(all_data))
        temp.close()




        chinaDailyHistory_data = all_data['chinaDayList']
        chinaDayAddList_data = all_data['chinaDayAddList']
        dict_history = OrderedDict()
        # print(len(province_yesterday))
        for history in chinaDailyHistory_data:
            history_data = []
            history_data.append("'"+history['date']+"'")
            history_data.append(history['confirm'])
            history_data.append(history['suspect'])
            history_data.append(history['heal'])
            history_data.append(history['dead'])
            history_data.append(history['nowConfirm'])
            history_data.append(history['nowSevere'])

            for add_data in chinaDayAddList_data:
                if add_data['date'] == history['date']:
                    history_data.append(add_data['confirm'])
                    history_data.append(add_data['suspect'])
                    break
            dict_history[history_data[0]] = history_data

        print(dict_history)

        filename = self.csv_path + '中国疫情历史数据.csv'
        first_row = ['日期',
                     '累计确诊',
                     '现有疑似',
                     '累计治愈',
                     '累计死亡',
                     '现有确诊',
                     '现有重症',
                     '新增确诊',
                     '新增疑似'
                     ]
        self.write_csv(dict_history, first_row, filename)
        return dict_history

    def write_csv(self,items,list,str):
        """数据整理到csv"""
        with open(str,'w',newline='') as temp:
            file = csv.writer(temp)
            first_row = list
            file.writerow(first_row)
            for name in items:
                file.writerow(items[name])
        temp.close()



if __name__ == '__main__':
    COVID19_data = COVID_19()
    page_data = COVID19_data.get_page_data()
    global_data = COVID19_data.get_global_data(page_data)
    province_data = COVID19_data.get_province_data(page_data)
    city_data = COVID19_data.get_city_data(page_data)
    history = COVID19_data.get_chinaHistory_data()
    # print(page_data)

# https://view.inews.qq.com/g2/getOnsInfo?name=disease_other&callback=jQuery341011927797283914199_1583812478231&_=1583812478232
#
# Referer: https://news.qq.com/zt2020/page/feiyan.htm