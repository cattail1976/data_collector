import pandas as pd
import requests, json
import datetime
import os
import glob


class TWStockCollector:
    def __init__(self):
        self.url = "www.twse.com.tw"
        self.prefix = "exchangeReport/STOCK_DAY"
        self.parameters = {"response":"json", "date":None , "stockNo":None}

    def _get_url(self, date, stock_no):
        self.parameters['date'] = date
        self.parameters['stockNo'] = stock_no
        query = ''
        for k in self.parameters:
            query += k+'='+self.parameters[k]+"&"
        print("https://{}/{}?{}".format(self.url, self.prefix, query))
        return "https://{}/{}?{}".format(self.url, self.prefix, query)

    def _get_fname(self, date, stock_no):
        return "{}_{}.csv".format(date, stock_no)

    def get_stock(self, date, stock_no):
        fname = self._get_fname(date, stock_no)
        if not os.path.isfile(fname):
            html = requests.get(self._get_url(date, stock_no))
            content = json.loads(html.text)
            print(content)
            if 'data' in content:
                stock_data = content['data']
                col_name = content['fields']
                print(content)
                df = pd.DataFrame(data=stock_data, columns=col_name)
                df['Symbol'] = stock_no
                df.to_csv (self._get_fname(date, stock_no), index=False)

    @staticmethod
    def to_ad_date(x):
        toks = x.split('/')
        toks[0] = str(int(toks[0]) + 1911)
        return '-'.join(toks)

    @staticmethod
    def parse_year(x):
        return x.split('-')[0]

    @staticmethod
    def parse_dow(x):
        return datetime.datetime.strptime(x, '%Y-%m-%d').weekday()

    @staticmethod
    def parse_woy(x):
        return datetime.datetime.strptime(x, '%Y-%m-%d').isocalendar()[1]

    @staticmethod
    def parse_month(x):
        return datetime.datetime.strptime(x, '%Y-%m-%d').month

    @staticmethod
    def parse_dom(x):
        return datetime.datetime.strptime(x, '%Y-%m-%d').strftime("%d")

    @staticmethod
    def get_df():
        all_files = glob.glob("./*.csv")
        li = []

        for filename in all_files:
            df = pd.read_csv(filename, index_col=None, header=0)
            li.append(df)

        df = pd.concat(li, axis=0, ignore_index=True)
        return df

    @staticmethod
    def transform():
        df = TWStockCollector.get_df()
        df['date'] = df['日期'].apply(lambda x: TWStockCollector.to_ad_date(x))
        df['year'] = df['date'].apply(lambda x: TWStockCollector.parse_year(x))
        df['day_of_week'] = df['date'].apply(lambda x: TWStockCollector.parse_dow(x))
        df['month'] = df['date'].apply(lambda x: TWStockCollector.parse_dow(x))
        df['week_of_the_year'] = df['date'].apply(lambda x: TWStockCollector.parse_woy(x))
        df['day_of_month'] = df['date'].apply(lambda x: TWStockCollector.parse_dom(x))
        df['dummy'] = 1
        return df




