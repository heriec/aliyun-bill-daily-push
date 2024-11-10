
import datetime
from aliyun import AliyunClient
from feishu import FeishuClient
from feishuCard import FlybookRobotAlert


if __name__ == '__main__':
    ################# bill ##################
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)   
    billList  = AliyunClient().billList(yesterday.strftime('%Y-%m'))
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
    a = FlybookRobotAlert("https://open.feishu.cn/open-apis/bot/v2/hook/51b9e4d8-10d7-4772-b175-4b94d5f2d734")
    a.send_message(yesterday, result['acc'], result['traf'])
    
