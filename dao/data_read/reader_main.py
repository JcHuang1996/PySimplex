# -*- coding: utf-8 -*-
# @Time     : 2025/4/1
# @Author   : J. Huang
# @Email    : jiachenghuang0601@gmail.com


import logging
import pandas as pd

from util.names import InputType, RawDataName
from util.project_logger import init_logger

logger = logging.getLogger(__name__)


class DataReader(object):

    def __init__(self, read_method, local_file_type, local_file_path):
        self.read_method = read_method
        self.local_file_type = local_file_type
        self.local_file_path = local_file_path

        self.raw_data = {}

    def read(self):

        if self.read_method == 'local':
            self.read_local_input()

        elif self.read_method == 'remote':
            pass

        else:
            raise Exception("unsupported read method")

    def read_local_input(self):

        if self.local_file_type == InputType.CSV:
            standard_df = pd.read_csv(self.local_file_path)
        else:
            raise Exception("unsupported file type")

        self.raw_data[RawDataName.STD_FORM_DF] = standard_df


if __name__ == '__main__':
    init_logger()

    test_read_method = 'local'
    test_file_type = 'csv'
    test_file_path = '/Users/huangjiacheng/PySimplex/test/test_data/ex_1.csv'

    data_reader = DataReader(
        read_method=test_read_method,
        local_file_type=test_file_type,
        local_file_path=test_file_path
    )
    data_reader.read()
    logger.info('test finished')
