
import datetime
import json
import time
from aliyun import AliyunClient
from feishu import FeishuClient


if __name__ == '__main__':
    billList  = AliyunClient().billList()
    # json.dump(billList, open('query_bill.json', 'w'), indent=4)
    # 过滤前一天的账单    
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)   

    yesterdayBillList = [item for item in billList if datetime.datetime.strptime(item["UsageStartTime"], f"%Y-%m-%d %H:%M:%S").date() == yesterday]
    feishuClient = FeishuClient()
    ids = feishuClient.findAll()
    feishuClient.deleteRecord(ids)
    feishuClient.addTableRecords(yesterdayBillList)
    # for bill in yesterdayBillList:
    #     feishuClient.addTableRecord(bill)
    
