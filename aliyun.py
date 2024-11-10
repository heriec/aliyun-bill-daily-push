import datetime
import os

from typing import List

from alibabacloud_bssopenapi20171214.client import Client as BssOpenApi20171214Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_bssopenapi20171214 import models as bss_open_api_20171214_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient

from alibabacloud_cdn20180510.client import Client as Cdn20180510Client
from alibabacloud_cdn20180510 import models as cdn_20180510_models


class AliyunClient:
    def __init__(self):
        pass

    def createBillClient(self) -> BssOpenApi20171214Client:
        """
        使用AK&SK初始化账号Client
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            access_key_id=os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID'],
            access_key_secret=os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET']
        )
        config.endpoint = f'business.aliyuncs.com'
        return BssOpenApi20171214Client(config)

    def billList(self, month) -> None:
        client = self.createBillClient()
        query_bill_request = bss_open_api_20171214_models.QueryBillRequest(
            billing_cycle=month,
            page_size=100
        )
        runtime = util_models.RuntimeOptions()
        try:
            response = client.query_bill_with_options(
                query_bill_request, runtime)
            body = UtilClient.to_map(response.body)
            return body['Data']['Items']['Item']
        except Exception as error:
            print(error.message)
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)

    def createCdnClient(self) -> Cdn20180510Client:
        """
        使用AK&SK初始化账号Client
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            access_key_id=os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID'],
            access_key_secret=os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET']
        )
        config.endpoint = f'cdn.aliyuncs.com'
        return Cdn20180510Client(config)

    def cdnUsage(self, day: datetime.date, domain: str, type: str) -> None:
        client = self.createCdnClient()
        describe_domain_usage_data_request = cdn_20180510_models.DescribeDomainUsageDataRequest(
            domain_name=domain,
            start_time=day.strftime('%Y-%m-%dT00:00:00Z'),
            end_time=day.strftime('%Y-%m-%dT23:59:59Z'),
            field=type
        )
        runtime = util_models.RuntimeOptions()
        try:
            response = client.describe_domain_usage_data_with_options(
                describe_domain_usage_data_request, runtime)
            return response.body.usage_data_per_interval.data_module
        except Exception as error:
            print(error.message)
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)


if __name__ == '__main__':
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    result = {}
    for type in ['acc', 'traf']:
        cdnUsage = AliyunClient().cdnUsage(yesterday, "easygif.cn", type)
        
        for item in cdnUsage:
            print(item)
        result[type] = sum([i.value for i in cdnUsage])
            
    print(result)