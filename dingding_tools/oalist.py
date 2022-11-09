# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import sys

from typing import List

from alibabacloud_dingtalk.workflow_1_0.client import Client as dingtalkworkflow_1_0Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dingtalk.workflow_1_0 import models as dingtalkworkflow__1__0_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient


class Sample:
    def __init__(self):
        pass

    @staticmethod
    def create_client() -> dingtalkworkflow_1_0Client:
        """
        使用 Token 初始化账号Client
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config()
        config.protocol = 'https'
        config.region_id = 'central'
        return dingtalkworkflow_1_0Client(config)

    @staticmethod
    def main(
        args: List[str],
    ) -> None:
        client = Sample.create_client()
        list_process_instance_ids_headers = dingtalkworkflow__1__0_models.ListProcessInstanceIdsHeaders()
        list_process_instance_ids_headers.x_acs_dingtalk_access_token = '1c65658a32f132f681ef9db781ad9d9d'
        list_process_instance_ids_request = dingtalkworkflow__1__0_models.ListProcessInstanceIdsRequest(
            process_code='PROC-F74A0CE2-74E9-4E43-A8F0-D07C8BCE7F9D',
            start_time=1665044443000,
            end_time=1667722896000,
            next_token=0,
            max_results=10
            # user_ids=[
            #     '发起userid'
            # ]
        )
        try:
            print(
                client.list_process_instance_ids_with_options(list_process_instance_ids_request, list_process_instance_ids_headers,
                                                              util_models.RuntimeOptions()))
        except Exception as err:
            if not UtilClient.empty(err.code) and not UtilClient.empty(err.message):
                # err 中含有 code 和 message 属性，可帮助开发定位问题
                pass

    @staticmethod
    async def main_async(
        args: List[str],
    ) -> None:
        client = Sample.create_client()
        list_process_instance_ids_headers = dingtalkworkflow__1__0_models.ListProcessInstanceIdsHeaders()
        list_process_instance_ids_headers.x_acs_dingtalk_access_token = '1c65658a32f132f681ef9db781ad9d9d'
        list_process_instance_ids_request = dingtalkworkflow__1__0_models.ListProcessInstanceIdsRequest(
            process_code='PROC-F74A0CE2-74E9-4E43-A8F0-D07C8BCE7F9D',
            start_time=1496678400000,
            end_time=1496678400000,
            next_token=0,
            max_results=10
            # user_ids=[
            #     '发起userid'
            # ]
        )
        try:
            print(await client.list_process_instance_ids_with_options_async(list_process_instance_ids_request,
                                                                            list_process_instance_ids_headers,
                                                                            util_models.RuntimeOptions()))
        except Exception as err:
            if not UtilClient.empty(err.code) and not UtilClient.empty(err.message):
                # err 中含有 code 和 message 属性，可帮助开发定位问题
                pass


if __name__ == '__main__':
    Sample.main(sys.argv[1:])