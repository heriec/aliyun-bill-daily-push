
import datetime
import os
from aliyun import AliyunClient
from feishu import FeishuClient
from feishuCard import FlybookRobotAlert


if __name__ == '__main__':
    ################# bill ##################
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)   
    billList  = AliyunClient().billList(yesterday.strftime('%Y-%m'))

    # 过滤掉没有UsageStartTime的数据
    # 其他付款的数据不在这里统计
    billList = filter(lambda x: x["UsageStartTime"] != '', billList)

    # json.dump(billList, open('query_bill.json', 'w'), indent=4)
    yesterdayBillList = [item for item in billList if datetime.datetime.strptime(item["UsageStartTime"], f"%Y-%m-%d %H:%M:%S").date() == yesterday]
    feishuClient = FeishuClient()
    ids = feishuClient.findAll()
    feishuClient.deleteRecord(ids)
    feishuClient.addTableRecords(yesterdayBillList)
    # for bill in yesterdayBillList:
    #     feishuClient.addTableRecord(bill)

    ################# cdn ##################
    result = {}
    for type in ['acc', 'traf']:
        cdnUsage = AliyunClient().cdnUsage(yesterday, "easygif.cn", type)
        result[type] = sum([item.value for item in cdnUsage])
            
    print(result)
    a = FlybookRobotAlert(os.environ['FEISHU_WEBHOOK'])
    a.send_message(yesterday, result['acc'], result['traf'])
    
