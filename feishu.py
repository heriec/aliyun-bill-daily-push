import datetime
import json
import os
import lark_oapi as lark
from lark_oapi.api.bitable.v1 import *


class FeishuClient:
    def __init__(self):
        self.appToken = os.environ['APP_TOKEN']
        self.tableId = os.environ['TABLE_ID']
        self.viewId = os.environ['VIEW_ID']
        self.appId = os.environ['FEISHU_APP_ID']
        self.AppSecret = os.environ['FEISHU_APP_SECRET']

        self.client = lark.Client.builder() \
            .app_id(self.appId) \
            .app_secret(self.AppSecret) \
            .log_level(lark.LogLevel.DEBUG) \
            .build()

    def findAll(self):
        recordIds = []
        pageToken = ''
        isEnd = False
        while not isEnd:
            request = SearchAppTableRecordRequest.builder() \
                .app_token(self.appToken) \
                .table_id(self.tableId) \
                .user_id_type("user_id") \
                .page_token(pageToken) \
                .page_size(20) \
                .request_body(SearchAppTableRecordRequestBody.builder()
                              .view_id(self.viewId)
                              .build()) \
                .build()
            response = self.client.bitable.v1.app_table_record.search(request)
            record = response.data
            for record in record.items:
                recordIds.append(record.record_id)
            if response.data.has_more == False:
                isEnd = True
            pageToken = response.data.page_token

        return recordIds

    def deleteRecord(self, recordIds):
        request = BatchDeleteAppTableRecordRequest.builder() \
            .app_token(self.appToken) \
            .table_id(self.tableId) \
            .request_body(BatchDeleteAppTableRecordRequestBody.builder()
                          .records(recordIds)
                          .build()) \
            .build()
        response = self.client.bitable.v1.app_table_record.delete(request)
        if not response.success():
            lark.logger.error(
                f"client.bitable.v1.app_table_record.delete failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
            return
        lark.logger.info(lark.JSON.marshal(response.data, indent=4))

    def addTableRecord(self, bill):
        fields = {
            "产品名称": bill['ProductName'],
            "代金券抵扣": bill['DeductedByCashCoupons'],
            "优惠金额": bill['InvoiceDiscount'],
            "原始金额": bill['PretaxGrossAmount'],
            "应付金额": bill['PretaxAmount'],
            "优惠券抵扣": bill['DeductedByCoupons'],
            "抹零优惠": bill['RoundDownDiscount'],
        }
        tableRecord = CreateAppTableRecordRequest.builder() \
            .app_token(self.appToken) \
            .table_id(self.tableId) \
            .request_body(AppTableRecord.builder()
                          .fields(fields)
                          .build()) \
            .build()

        response: CreateAppTableRecordResponse = self.client.bitable.v1.app_table_record.create(
            tableRecord)
        print('@', response.code, response.msg, response.data)
        # 处理失败返回
        if not response.success():
            lark.logger.error(
                f"client.bitable.v1.app_table_record.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
            return

    def addTableRecords(self, bills):
        list = []
        for bill in bills:
            fields = {
                "产品名称": bill['ProductName'],
                "代金券抵扣": bill['DeductedByCashCoupons'],
                "优惠金额": bill['InvoiceDiscount'],
                "原始金额": bill['PretaxGrossAmount'],
                "应付金额": bill['PretaxAmount'],
                "优惠券抵扣": bill['DeductedByCoupons'],
                "抹零优惠": bill['RoundDownDiscount'],
            }
            list.append(AppTableRecord.builder().fields(fields).build())

        request = BatchCreateAppTableRecordRequest.builder() \
            .app_token(self.appToken) \
            .table_id(self.tableId) \
            .user_id_type("user_id") \
            .request_body(BatchCreateAppTableRecordRequestBody.builder()
                          .records(list)
                          .build()).build()

        response = self.client.bitable.v1.app_table_record.batch_create(
            request)

        # 处理失败返回
        if not response.success():
            lark.logger.error(
                f"client.bitable.v1.app_table_record.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
            return

        # 处理业务结果
        lark.logger.info(lark.JSON.marshal(response.data, indent=4))


if __name__ == "__main__":
    client = FeishuClient()
    ids = client.findAll()
    client.deleteRecord(ids)
