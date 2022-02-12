from tw.stock.collector import TWStockCollector
import time
import datetime


numdays = 1080

base = datetime.datetime.strptime('2021/01/31', '%Y/%m/%d')

date_list = [base - datetime.timedelta(days=x) for x in range(0, numdays, 30)]
value_rank = ['2330', '2454', '2317', '6505', '2412', '2881', '2882', '2303', '2308', '1303', '1301', '1314']
collector = TWStockCollector()
# for d in date_list:
#     for c in value_rank:
#         d_str = d.strftime('%Y%m%d')
#         collector.get_stock(d_str, c)
#         time.sleep(5)
print(TWStockCollector.transform())